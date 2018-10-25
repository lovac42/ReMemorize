# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/ReMemorize
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.1.4


# CONFIGS ##################################

HOTKEY = 'Ctrl+M' #SM hotkey?

EF_HOTKEY = 'Ctrl+Shift+M'

REVLOG_RESCHEDULED = True #Changes shows up in revlog

FUZZ_DAYS = True

#BUG: Undo review brings up siblings as well.
FORGET_SIBLINGS = False
RESCHEDULE_SIBLINGS = False

#When a card is graded as incorrect.
AUTO_RESCHEDULE_SIBLINGS = True
SIBLING_BOUNDARY = 90
SIBLING_DAYS_MIN = 5    #Set equal days for no fuzz
SIBLING_DAYS_MAX = 9    #Set equal days for no fuzz

# END CONFIGS ##################################


from aqt import mw
from aqt.qt import *
from anki.hooks import wrap
from anki.sched import Scheduler
from aqt.utils import showWarning, showText, getText, tooltip
from anki.utils import intTime, ids2str
import random, time


#from: anki.sched.Scheduler, removed resetting ease factor, added logs
def customReschedCards(ids, imin, imax, imod=True):
    d = []
    t = mw.col.sched.today
    mod = intTime()
    for id in ids:
        card=mw.col.getCard(id)
        mw.col.markReview(card) #undo
        r = random.randint(imin, imax)
        ivl = max(1, r) if imod else card.ivl
        d.append(dict(id=id, due=r+t, ivl=ivl, mod=mod, usn=mw.col.usn()))
        try:
            log(card,ivl)
        except:
            time.sleep(0.01) # duplicate pk; retry in 10ms
            log(card,ivl)

    mw.col.sched.remFromDyn(ids)
    mw.col.db.executemany("""
update cards set type=2,queue=2,ivl=:ivl,due=:due,odue=0,
usn=:usn,mod=:mod where id=:id""", d)
    mw.col.log(ids)



#lastIvl = card.ivl
#ease=0, timeTaken=0
#custom log type: 4 = rescheduled
def log(card, ivl):
    if not REVLOG_RESCHEDULED: return
    logId = intTime(1000)
    mw.col.db.execute(
        "insert into revlog values (?,?,?,0,?,?,?,0,4)",
        logId, card.id, mw.col.usn(),
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

        mnew = QAction("reMemorize: Forget note", mw)
        mnew.triggered.connect(self.forgetCards)
        menu.addAction(mnew)

        cef = QAction("reMemorize: Change Card Factor", mw)
        cef.setShortcut(QKeySequence(EF_HOTKEY))
        cef.triggered.connect(self.changeEF)
        menu.addAction(cef)

        mdays = QAction("reMemorize: Reschedule", mw)
        mdays.setShortcut(QKeySequence(HOTKEY))
        mdays.triggered.connect(self.ask)
        menu.addAction(mdays)


    def getSiblings(self, nid): #includes all cards in note
        return [i for i in mw.col.db.list(
            "select id from cards where nid=?", nid)]

    def forgetCards(self):
        if mw.state != 'review': return
        card=mw.reviewer.card

        if FORGET_SIBLINGS:
            cids=self.getSiblings(card.nid)
        else:
            cids=[card.id]

        for id in cids:
            card=mw.col.getCard(id)
            mw.col.markReview(card) #undo
            try:
                log(card,0)
            except:
                time.sleep(0.01) # duplicate pk; retry in 10ms
                log(card,0)

        mw.col.sched.forgetCards(cids)
        mw.reset()
        tooltip(_("Card forgotten."), period=1000)


    def reschedCards(self, card, days, imod=True):
        #undo moved to customReschedCards()

        if imod and RESCHEDULE_SIBLINGS:
            cids=self.getSiblings(card.nid)
        else:
            cids=[card.id]

        if imod and FUZZ_DAYS:
            min, max = mw.col.sched._fuzzIvlRange(days)
            customReschedCards(cids, min, max)
        else:
            customReschedCards(cids, days, days, imod)

        mw.reviewer._answeredIds.append(card.id)
        mw.autosave()
        mw.reset()
        tooltip(_("Card rescheduled."), period=1000)


    def updateStats(self, card): #subtract count from new/rev queue
        if card.queue == 0:
            mw.col.sched._updateStats(card, 'new')
        else:
            mw.col.sched._updateStats(card, 'rev')
        #note: There's no lrnToday key


    def ask(self):
        if mw.state != 'review': return
        days, ok = getText("Reschedule Days: (0=forget, neg days=defer)", default='7')
        if not ok: return
        try:
            days = int(days)
        except ValueError: return

        c=mw.reviewer.card
        if days == 0: #mark as new
            self.forgetCards()
        elif days > 0: #change due and ivl
            self.updateStats(c)
            self.reschedCards(c, days)
        elif days < 0: #change due date only
            self.updateStats(c)
            self.reschedCards(c, abs(days), False)


    def changeEF(self):
        if mw.state != 'review': return
        c=mw.reviewer.card
        fct, ok = getText("Change Ease Factor:", default=str(c.factor))
        if not ok: return
        c.factor=max(1300,int(fct))
        c.flush()
        tooltip(_("Card's factor changed."), period=1000)



remem=ReMemorize()


#Reset sibling cards on forget
def answerCard(self, card, ease):
    if ease == 1 and AUTO_RESCHEDULE_SIBLINGS:
        cids=[i for i in mw.col.db.list(
            "select id from cards where nid=? and type=2 and queue=2 and id!=? and ivl > ?",
            card.nid, card.id, SIBLING_BOUNDARY)]
        if len(cids) > 0:
            customReschedCards(cids, SIBLING_DAYS_MIN, SIBLING_DAYS_MAX)

Scheduler.answerCard = wrap(Scheduler.answerCard, answerCard, 'after')
