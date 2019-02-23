# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2019 Lovac42
# Support: https://github.com/lovac42/ReMemorize
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Version: 0.0.2

# ABOUT: Adds rate:1:0 search to browser allowing searching for rescheduled cards.
# Please note the license is agpl for this extension


# == User Config =========================================

MAX_SEARCH_DAYS = 365

# == End Config ==========================================
##########################################################


from aqt import mw
from anki.hooks import wrap
import anki


# FROM: anki.find.Finder (src 2.1.8)
# MOD: added 0 key
# MOD2: added option for max days
def wrap_findRated(self, args, _old):
    # days(:optional_ease)
    (val, args) = args
    r = val.split(":")
    try:
        days = int(r[0])
    except ValueError:
        return
    days = min(days, MAX_SEARCH_DAYS)
    # ease
    ease = ""
    if len(r) > 1:
        if r[1] not in ("1", "2", "3", "4", "0"):
            return
        ease = "and ease=%s" % r[1]
    cutoff = (self.col.sched.dayCutoff - 86400*days)*1000
    return ("c.id in (select cid from revlog where id>%d %s)" %
            (cutoff, ease))


anki.find.Finder._findRated = wrap(anki.find.Finder._findRated, wrap_findRated, 'around')
