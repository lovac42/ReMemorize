# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2019 Lovac42
# Support: https://github.com/lovac42/ReMemorize
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from aqt.qt import *
from anki.hooks import addHook
from aqt.utils import getText, showInfo
from .utils import *
from .const import *
from .config import *

ADDON_NAME='rememorize'


class ReMemorize:
    loaded=False

    def __init__(self):
        self.conf=Config(ADDON_NAME)
        addHook(ADDON_NAME+".configLoaded", self.onConfigLoaded)

        #Allows other GUIs to tap into
        # e.g. runHook("ReMemorize.reschedule", card, 100)
        addHook('ReMemorize.forget', self.forgetCards) #w/ siblings & conf settings
        addHook('ReMemorize.forgetAll', self.forgetSelected) #util wrapper
        addHook('ReMemorize.reschedule', self.reschedCards) #w/ siblings & conf settings
        addHook('ReMemorize.rescheduleAll', self.reschedSelected) #util wrapper
        addHook('ReMemorize.changeDue', self.changeDue)
        addHook('ReMemorize.changeDueAll', self.changeDueSelected)


    def onConfigLoaded(self):
        if not self.loaded:
            self.setupMenu()
            self.loaded=True


    def setupMenu(self):
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


    def _forgetCards(self): #triggered from study menu
        if mw.state != 'review': return
        card=mw.reviewer.card
        self.forgetCards(card)
        self._finished(card,"Card forgotten.")

    def forgetCards(self, card):
        if self.conf.get("forget_siblings",False):
            cids=self.getSiblings(card.nid)
        else:
            cids=[card.id]
        logging=self.conf.get("revlog_rescheduled",False)
        customForgetCards(cids,logging)

    def forgetSelected(self, cids, logging=True):
        "wrapper, access to util function"
        mw.progress.start()
        customForgetCards(cids,logging)
        mw.autosave()
        mw.progress.finish()


    def reschedSelected(self, cids, imin, imax, logging=True, lbal=False):
        "wrapper, access to util function"
        mw.progress.start()
        customReschedCards(cids,imin,imax,logging,lbal)
        mw.autosave()
        mw.progress.finish()

    def reschedCards(self, card, days):
        log=self.conf.get("revlog_rescheduled",True)
        fuzz=self.conf.get("fuzz_days",True)
        if self.conf.get("reschedule_sibling",False):
            cids=self.getSiblings(card.nid)
        else:
            cids=[card.id]
        customReschedCards(cids,days,days,log,fuzz)


    def updateStats(self, card): #subtract count from new/rev queue
        if card.queue == 0:
            mw.col.sched._updateStats(card, 'new')
        elif card.queue == 2:
            mw.col.sched._updateStats(card, 'rev')

        #Note: There's no lrnToday key in V2
        #mw.reset will reset the lrn count, making this unnecessary
        # elif card.type == 1 and mw.col.sched.name!="std2":
            # mw.col.sched._updateStats(card, 'lrn')


    def parseDate(self, days):
        try:
            return getDays(days)
        except ValueError: #non date format
            return days
        except TypeError: #passed date
            showInfo("Already passed due date")
            return None


    def ask(self, c, checkBury=True):
        if mw.state != 'review': return
        dft=self.conf.get("default_days_on_ask",7)
        days, ok = getText("""
Reschedule Days: (0=forget, neg=keep IVL) Or 1/15/2020
""", default=str(dft))
        if not ok: return

        c=neg=None
        if days[0]=='p': #previous card, p prefix, changes due date after grading
            c=mw.reviewer.lastCard()
            if not c:
                showInfo('Previous card not found.')
                return
            days=days[1:]

        if days[0]=='-': #negative num, change due, keep interval
            neg=True
            days=days[1:]

        try:
            days = int(self.parseDate(days))
            if neg: days = - days
        except TypeError: return
        except ValueError: return

        if not c: #current card
            c=mw.reviewer.card
            if days and self.conf.get("bury_siblings",False):
                mw.col.sched._burySiblings(c)

        tipTxt=self.evalDays(c,days)
        self._finished(c,tipTxt)


    def evalDays(self, c, days):
        if days == 0: #mark as new
            self.forgetCards(c)
            return "Card forgotten."

        elif days > 0: #change due and ivl
            self.updateStats(c)
            self.reschedCards(c, days)
            return "Card rescheduled."

        elif days < 0: #change due date only
            self.changeDue(c, abs(days))
            return "Card due date changed."


    def _finished(self, card, msg):
        #for warrior mode last_card preview
        mw.reviewer._answeredIds.append(card.id)
        mw.autosave()
        mw.reset()
        tooltip(_(msg), period=1000)


    def changeEF(self):
        if mw.state != 'review': return
        c=mw.reviewer.card
        fct, ok = getText("Change Ease Factor:", default=str(c.factor))
        if not ok: return

        if fct[0]=='p': #previous card
            c=mw.reviewer.lastCard()
            if not c:
                showInfo('Previous card not found.')
                return
            fct=fct[1:]

        c.factor=max(1300,int(fct))
        c.flushSched()
        tooltip(_("Card factor changed"), period=1000)


    def changeDueSelected(self, cids, start=1, step=0, shuffle=False, shift=False):
        mw.checkpoint(_("Rescheduled"))
        mw.progress.start()
        for cid in cids:
            card=mw.col.getCard(cid)
            if shuffle:
                due=random.randint(start,start+step)
                self.changeDue(card,due)
            else:
                self.changeDue(card,start)
            if shift: start+=step
        mw.autosave()
        mw.progress.finish()


    def changeDue(self, card, days):
        "Push the due date forward, don't log or change ivl except for new cards"
        if mw.state=='review':
            mw.col.markReview(card) #undo

        if card.type in (0,1):
            initNewCard(card)
            #Log new types only since the IVL changed.
            if self.conf.get("revlog_rescheduled",False):
                trylog(card,card.ivl) #records fuzzed/LB ivl

        card.due=mw.col.sched.today + days
        if card.odid:
            card.did=card.odid
        card.left=card.odid=card.odue=0
        card.type=card.queue=2
        card.flushSched()

