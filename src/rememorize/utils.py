# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/ReMemorize
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.2.4


from aqt import mw
from aqt.utils import tooltip
from anki.utils import intTime, ids2str
import random, time
from .const import *


#From: anki.sched.Scheduler
#Mods: removed resetting ease factor, added logs
def customReschedCards(ids, imin, imax, logging=True):
    markForUndo=True
    if mw.state!='review':
        markForUndo=False
        mw.checkpoint(_("Rescheduled")) #undo state, inc siblings

    d = []
    t = mw.col.sched.today
    mod = intTime()
    for id in ids:
        card=mw.col.getCard(id)
        if markForUndo: #see bug/feature comment in readme.
            mw.col.markReview(card)

        #initialize new/new-lrn cards
        if card.type in (0,1):
            conf=mw.col.sched._lrnConf(card)
            mw.col.sched._rescheduleNew(card,conf,False)

        r = random.randint(imin, imax)
        ivl = max(1, r)
        d.append(dict(id=id, due=r+t, ivl=ivl, mod=mod, usn=mw.col.usn(), fact=card.factor))
        if logging:
            try:
                log(card,ivl)
            except:
                time.sleep(0.01) # duplicate pk; retry in 10ms
                log(card,ivl)

    mw.col.sched.remFromDyn(ids)
    mw.col.db.executemany("""
update cards set type=2,queue=2,ivl=:ivl,due=:due,odue=0,
usn=:usn,mod=:mod,factor=:fact where id=:id""", d)
    mw.col.log(ids)


#lastIvl = card.ivl
#ease=0, timeTaken=0
#custom log type: 4 = rescheduled
def log(card, ivl):
    delay=getDelay(card)
    logId = intTime(1000)
    mw.col.db.execute(
        "insert into revlog values (?,?,?,0,?,?,?,0,4)",
        logId, card.id, mw.col.usn(),
        ivl, -delay or card.ivl or 1, card.factor)

def getDelay(card):
    if card.queue not in (1,3): return 0
    conf=mw.col.sched._lrnConf(card)
    left=card.left%1000
    return mw.col.sched._delayForGrade(conf,left)
