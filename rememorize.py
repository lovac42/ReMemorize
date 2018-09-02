# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/ReMemorize
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.3


#config
RANDOM_DAYS_MAX = 7

SIBLING_BOUNDARY = 90

HOTKEY = 'Ctrl+M'


from aqt import mw
from aqt.qt import *
from anki.hooks import wrap
from anki.sched import Scheduler
from aqt.utils import showWarning, showText, getText


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

        mdays = QAction("re-memorize: Reschedule", mw)
        mdays.triggered.connect(self.ask)
        menu.addAction(mdays)

        shortcut = QShortcut(QKeySequence(HOTKEY), mw) #supermemo hotkey?
        shortcut.activated.connect(self.ask)

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
        mw.col.sched.reschedCards(cids, days, days+RANDOM_DAYS_MAX)
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


remem=ReMemorize()


#Reset sibling cards on forget
def answerCard(self, card, ease):
    if ease == 1:
        cids=[i for i in mw.col.db.list(
            "select id from cards where nid=? and type=2 and queue=2 and id!=? and ivl > ?",
            card.nid, card.id, SIBLING_BOUNDARY)]
        if len(cids) > 0:
            self.reschedCards(cids, 5, 9)

Scheduler.answerCard = wrap(Scheduler.answerCard, answerCard, 'after')
