# -*- coding: utf-8 -*-
# Copyright 2018-2020 Lovac42
# Support: https://github.com/lovac42/ReMemorize
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


from .lib.com.lovac42.anki.version import POINT_VERSION, CCBC


if POINT_VERSION < 24 and not CCBC:
    from .rated0Search import *
else:
    print("""

*** *** *** *** *** *** *** *** *** ***
@Deprecated(since = "2.1.24")
The addon "ReMemorize Ex rated0Search" is no longer necessary for this version of anki. Please delete this addon as it's features have already been integrated with the current branch.
*** *** *** *** *** *** *** *** *** ***

""")
