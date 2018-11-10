# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/ReMemorize
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.2.0


from aqt import mw
from anki.hooks import wrap
from aqt.utils import getText
from .rememorize import *
from .utils import *
from .const import *
import anki.sched


remem=ReMemorize()


#Reset sibling cards on forget
def answerCard(self, card, ease):
    if ease == 1 and remem.conf.get("reschedule_siblings_on_again",False):
        if card.ivl>=21: return #avoid Lapse new ivl option

        conf=mw.col.decks.confForDid(card.did)
        if not card.odid or conf['resched']:
            cids=[i for i in mw.col.db.list(
                "select id from cards where nid=? and type=2 and queue=2 and id!=? and ivl > ?",
                card.nid, card.id, remem.conf.get("sibling_boundary",365))]
            L=len(cids)
            if L > 0:
                if not remem.conf.get("automatic_mode",False):
                    t,ok=getText("You have %d sibling(s) out of bound, reschedule them?"%L, default=str(cids))
                if ok or remem.conf.get("automatic_mode",False):
                    dMin=remem.conf.get("sibling_days_min",7)
                    dMax=remem.conf.get("sibling_days_max",20)
                    log=remem.conf.get("revlog_rescheduled",False)
                    customReschedCards(cids,dMin,dMax,log)


anki.sched.Scheduler.answerCard = wrap(anki.sched.Scheduler.answerCard, answerCard, 'after')
if ANKI21:
    import anki.schedv2
    anki.schedv2.Scheduler.answerCard = wrap(anki.schedv2.Scheduler.answerCard, answerCard, 'after')
