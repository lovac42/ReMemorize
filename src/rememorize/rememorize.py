# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/ReMemorize
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.2.2


from aqt import mw
from aqt.qt import *
from anki.hooks import addHook
from aqt.utils import getText
from .utils import *
from .const import *
from .settings import *


class ReMemorize:
    def __init__(self):
        addHook('profileLoaded', self.onProfileLoaded)

        #Allows other GUIs to tap into
        # e.g. runHook("ReMemorize.reschedule", card, 100)
        addHook('ReMemorize.forget', self.forgetCards)
        addHook('ReMemorize.reschedule', self.reschedCards)
        addHook('ReMemorize.changeDue', self.changeDue)


    def onProfileLoaded(self):
        self.conf=Settings()
        menu=None
        for a in mw.form.menubar.actions():
            if '&Study' == a.text():
                menu=a.menu()
                menu.addSeparator()
                break
        if not menu:
            menu=mw.form.menubar.addMenu('&Study')

        mnew = QAction("reMemorize: Forget note", mw)
        key=self.conf.get("fg_hotkey",None)
        if key: mnew.setShortcut(QKeySequence(key))
        mnew.triggered.connect(self._forgetCards)
        menu.addAction(mnew)

        cef = QAction("reMemorize: Change Card Factor", mw)
        key=self.conf.get("ef_hotkey",None)
        if key: cef.setShortcut(QKeySequence(key))
        cef.triggered.connect(self.changeEF)
        menu.addAction(cef)

        mdays = QAction("reMemorize: Reschedule", mw)
        key=self.conf.get("hotkey",None)
        if key: mdays.setShortcut(QKeySequence(key))
        mdays.triggered.connect(self.ask)
        menu.addAction(mdays)


    def getSiblings(self, nid): #includes all cards in note
        return [i for i in mw.col.db.list(
            "select id from cards where nid=?", nid)]


    def _forgetCards(self):
        if mw.state != 'review': return
        card=mw.reviewer.card
        self.forgetCards(card)

    def forgetCards(self, card):
        if self.conf.get("forget_siblings",False):
            cids=self.getSiblings(card.nid)
        else:
            cids=[card.id]

        for id in cids:
            card=mw.col.getCard(id)
            mw.col.markReview(card) #undo
            if self.conf.get("revlog_rescheduled",False):
                try:
                    log(card,0)
                except:
                    time.sleep(0.01) # duplicate pk; retry in 10ms
                    log(card,0)

        mw.col.sched.forgetCards(cids)
        mw.reset()
        tooltip(_("Card forgotten."), period=1000)


    def reschedCards(self, card, days):
        #undo() moved to customReschedCards()
        log=self.conf.get("revlog_rescheduled",True)

        if self.conf.get("reschedule_sibling",False):
            cids=self.getSiblings(card.nid)
        else:
            cids=[card.id]

        if self.conf.get("fuzz_days",True):
            min, max = mw.col.sched._fuzzIvlRange(days)
            customReschedCards(cids, min, max, log)
        else:
            customReschedCards(cids, days, days, log)

        mw.reviewer._answeredIds.append(card.id)
        mw.autosave()
        mw.reset()
        tooltip(_("Card rescheduled."), period=1000)


    def updateStats(self, card): #subtract count from new/rev queue
        if card.queue == 0:
            mw.col.sched._updateStats(card, 'new')
        else:
            mw.col.sched._updateStats(card, 'rev')
        #Note: There's no lrnToday key


    def ask(self):
        if mw.state != 'review': return
        dft=self.conf.get("default_days_on_ask",7)
        days, ok = getText("Reschedule Days: (0=forget, neg=keep IVL)", default=str(dft))
        if not ok: return
        try:
            days = int(days)
        except ValueError: return

        c=mw.reviewer.card
        if days == 0: #mark as new
            self.forgetCards(c)
        elif days > 0: #change due and ivl
            self.updateStats(c)
            self.reschedCards(c, days)
        elif days < 0: #change due date only
            self.changeDue(c, abs(days))

#TODO parse dates:  datetime.strptime("07/27/2012","%m/%d/%Y")


    def changeEF(self):
        if mw.state != 'review': return
        c=mw.reviewer.card
        fct, ok = getText("Change Ease Factor:", default=str(c.factor))
        if not ok: return
        c.factor=max(1300,int(fct))
        c.flushSched()
        tooltip(_("Card factor changed"), period=1000)


    def changeDue(self, card, days):
        "Push the due date forward, don't log or change ivl"
        mw.col.markReview(card) #undo
        if card.odid:
            card.did=card.odid
        card.left=card.odid=card.odue=0
        card.type=card.queue=2

        #initialize new cards, just in case.
        if card.factor==0: card.factor=2500
        if card.ivl==0: card.ivl=1

        card.due=mw.col.sched.today + days
        card.flushSched()
        mw.reset()
        tooltip(_("Card due date changed."), period=1000)


