# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/ReMemorize
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.5


# CONFIGS ##################################

FUZZ_DAYS = True

SIBLING_RESCHEDULE = True
SIBLING_BOUNDARY = 90
SIBLING_DAYS_MIN = 5    #Set equal days for no fuzz
SIBLING_DAYS_MAX = 9    #Set equal days for no fuzz

HOTKEY = 'Ctrl+M' #SM hotkey?
EF_HOTKEY = 'Ctrl+Shift+M'

REVLOG_RESCHEDULED = True #Changes shows up in revlog

# END CONFIGS ##################################


from aqt import mw
from aqt.qt import *
from anki.hooks import wrap
from anki.sched import Scheduler
from aqt.utils import showWarning, showText, getText
from anki.utils import intTime, ids2str
import random, time


#from: anki.sched.Scheduler, removed resetting ease factor
def customReschedCards(ids, imin, imax):
    d = []
    t = mw.col.sched.today
    mod = intTime()
    logtime = int(time.time()*1000)
    for id in ids:
        r = random.randint(imin, imax)
        ivl = max(1, r)
        d.append(dict(id=id, due=r+t, ivl=ivl, mod=mod, usn=mw.col.usn()))
        card=mw.col.getCard(id)
        try:
            log(card,ivl,logtime)
        except:
            time.sleep(0.01) # duplicate pk; retry in 10ms
            log(card,ivl,logtime)

    mw.col.sched.remFromDyn(ids)
    mw.col.db.executemany("""
update cards set type=2,queue=2,ivl=:ivl,due=:due,odue=0,
usn=:usn,mod=:mod where id=:id""", d)
    mw.col.log(ids)


#custom log type: 4 = rescheduled
#lastIvl = card.ivl
def log(card, ivl, logtime):
    if not REVLOG_RESCHEDULED: return
    mw.col.db.execute(
        "insert into revlog values (?,?,?,0,?,?,?,0,4)",
        logtime, card.id, mw.col.usn(),
        ivl, card.ivl, card.factor )


class ReMemorize:
    def __init__(self):
        menu=None
        for a in mw.form.menubar.actions():
            if '&Study' == a.text():
                menu=a.menu()
                menu.addSeparator()
                break
        if not menu:
            menu=mw.form.menubar.addMenu('&Study')

        mnew = QAction("re-memorize: Forget note", mw)
        mnew.triggered.connect(self.forgetCards)
        menu.addAction(mnew)

        mdays = QAction("re-memorize: Reschedule "+HOTKEY, mw)
        mdays.triggered.connect(self.ask)
        menu.addAction(mdays)

        cef = QAction("re-memorize: Change Card Factor "+EF_HOTKEY, mw)
        cef.triggered.connect(self.changeEF)
        menu.addAction(cef)

        #Change due date
        shortcut = QShortcut(QKeySequence(HOTKEY), mw)
        shortcut.activated.connect(self.ask)
        shortcut = QShortcut(QKeySequence(EF_HOTKEY), mw)
        shortcut.activated.connect(self.changeEF)

    def getSiblings(self, nid):
        return [i for i in mw.col.db.list(
            "select id from cards where nid=?", nid)]

    def forgetCards(self):
        if mw.state != 'review': return
        cids=self.getSiblings(mw.reviewer.card.nid)
        mw.col.sched.forgetCards(cids)
        mw.reset()

    def reschedCards(self, card, days):
        mw.col.markReview(card)
        cids=self.getSiblings(card.nid)
        if FUZZ_DAYS:
            min, max = mw.col.sched._fuzzIvlRange(days)
            customReschedCards(cids, min, max)
        else:
            customReschedCards(cids, days, days)
        mw.reviewer._answeredIds.append(card.id)
        mw.autosave()
        mw.reset()

    def updateStats(self, card): #subtract count from new/rev queue
        if card.queue == 0:
            mw.col.sched._updateStats(card, 'new')
        else:
            mw.col.sched._updateStats(card, 'rev')


    def ask(self):
        if mw.state != 'review': return
        days, ok = getText("Reschedule Days:", default='7')
        if not ok: return
        try:
            days = int(days)
        except ValueError: return

        c=mw.reviewer.card
        if days == 0:
            self.forgetCards()
        elif days > 0:
            self.updateStats(c)
            self.reschedCards(c, days)


    def changeEF(self):
        if mw.state != 'review': return
        c=mw.reviewer.card
        fct, ok = getText("Change Ease Factor:", default=str(c.factor))
        if not ok: return
        c.factor=max(1300,int(fct))
        c.flush()


remem=ReMemorize()


#Reset sibling cards on forget
def answerCard(self, card, ease):
    if ease == 1 and SIBLING_RESCHEDULE:
        cids=[i for i in mw.col.db.list(
            "select id from cards where nid=? and type=2 and queue=2 and id!=? and ivl > ?",
            card.nid, card.id, SIBLING_BOUNDARY)]
        if len(cids) > 0:
            customReschedCards(cids, SIBLING_DAYS_MIN, SIBLING_DAYS_MAX)

Scheduler.answerCard = wrap(Scheduler.answerCard, answerCard, 'after')
