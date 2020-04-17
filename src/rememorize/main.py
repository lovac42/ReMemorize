# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/ReMemorize
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import sys, aqt, random
import anki.sched
from aqt import mw
from anki.hooks import wrap, runHook
from aqt.utils import getText
from anki.utils import ids2str
from anki.lang import _

from .rememorize import *
from .utils import *
from .const import BROWSER_TAG
from .lib.com.lovac42.anki.version import ANKI21, CCBC


remem=ReMemorize()


#Reset sibling cards on forget
def answerCard(self, card, ease):
    if ease == 1 and remem.conf.get("reschedule_siblings_on_again",False):
        if card.ivl>=21: return #avoid Lapse new ivl option
        if card.id in mw.reviewer._answeredIds: return

        conf=mw.col.decks.confForDid(card.did)
        if not card.odid or conf['resched']:
            bound=card.ivl+remem.conf.get("sibling_boundary",365)
            cids=[i for i in mw.col.db.list(
                "select id from cards where nid=? and type=2 and queue=2 and id!=? and ivl > ?",
                card.nid, card.id, bound)]
            L=len(cids)
            if L > 0:
                am=ok=remem.conf.get("automatic_mode",False)
                if not am:
                    t,ok=getText("You have %d sibling(s) out of bound, reschedule them?"%L, default=str(cids))
                if am or ok:
                    dMin=remem.conf.get("sibling_days_min",7)
                    dMax=remem.conf.get("sibling_days_max",20)
                    log=remem.conf.get("revlog_rescheduled",True)
                    customReschedCards(cids,dMin,dMax,log)



# Replace scheduler.reschedCards called by browser
def reschedCards(self, ids, imin, imax, _old):
    browConf=remem.conf.get("browser",{})
    if not browConf.get("replace_brower_reschedule",False):
        return _old(self, ids, imin, imax)

    for i in range (2,5): #only wrap for browser calls
        try:
            f=sys._getframe(i)
        except ValueError: break

        if f.f_code.co_name==BROWSER_TAG:
            mw.requireReset()
            log=remem.conf.get("revlog_rescheduled",True)
            fuzz=remem.conf.get("fuzz_days",True) #for load balance
            runHook('ReMemorize.rescheduleAll',ids,imin,imax,log,fuzz)
            return
    return _old(self, ids, imin, imax) #called by other addons in reviewer.



# Replace scheduler.forgetCards called by browser
def forgetCards(self, ids, _old):
    browConf=remem.conf.get("browser",{})
    if not browConf.get("replace_brower_reschedule",False):
        return _old(self, ids)

    for i in range (2,5): #only wrap for browser calls
        try:
            f=sys._getframe(i)
        except ValueError: break

        if f.f_code.co_name==BROWSER_TAG:
            mw.requireReset()
            log=remem.conf.get("revlog_rescheduled",True)
            runHook('ReMemorize.forgetAll',ids,log)
            return
    return _old(self, ids) #called by bury card in reviewer



# Replaces reposition in browser so it changes the due date instead of changing the position of new cards.
def reposition(self, _old):
    browConf=remem.conf.get("browser",{})
    if not browConf.get("replace_brower_reposition",False):
        return _old(self)

    sel = self.selectedCards() #mixed selection
    if browConf.get("skip_new_card_types_on_reposition",False):
        newType = self.col.db.list(
            "select id from cards where type = 0 and id in " + ids2str(sel))
        if newType: #Change position of new cards
            return _old(self)

    d = QDialog(self)
    d.setWindowModality(Qt.WindowModal)
    frm = aqt.forms.reposition.Ui_Dialog()
    frm.setupUi(d)
    frm.start.setMinimum(0)

    frm.label.setText("""\
<b>ReMemorize</b>: set due date <br>\
(same as negative numbers during review) <br>""")
    frm.shift.setChecked(False)
    frm.shift.setText("""\
Increment n step(s) for each card?
(Start=1, Step=1) cA:1, cB:2, cC:3, cD:4
(Start=2, Step=2) cA:2, cB:4, cC:6, cD:8""")
    if not d.exec_(): return
    self.model.beginReset()
    self.mw.requireReset()

    start=frm.start.value()
    step=frm.step.value()
    shuffle=frm.randomize.isChecked()
    shift=frm.shift.isChecked()
    remem.changeDueSelected(sel,start,step,shuffle,shift)

    if ANKI21:
        self.search()
    else:
        self.onSearch(reset=False)
    self.model.endReset()



anki.sched.Scheduler.answerCard = wrap(anki.sched.Scheduler.answerCard, answerCard, 'after')
anki.sched.Scheduler.reschedCards = wrap(anki.sched.Scheduler.reschedCards, reschedCards, 'around')
anki.sched.Scheduler.forgetCards = wrap(anki.sched.Scheduler.forgetCards, forgetCards, 'around')

if ANKI21 or CCBC:
    import anki.schedv2
    anki.schedv2.Scheduler.answerCard = wrap(anki.schedv2.Scheduler.answerCard, answerCard, 'after')
    anki.schedv2.Scheduler.reschedCards = wrap(anki.schedv2.Scheduler.reschedCards, reschedCards, 'around')
    anki.schedv2.Scheduler.forgetCards = wrap(anki.schedv2.Scheduler.forgetCards, forgetCards, 'around')

if ANKI21:
    aqt.browser.Browser._reposition = wrap(aqt.browser.Browser._reposition, reposition, 'around')
else:
    aqt.browser.Browser.reposition = wrap(aqt.browser.Browser.reposition, reposition, 'around')
