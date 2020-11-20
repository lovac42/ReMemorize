# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/ReMemorize
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from .lib.com.lovac42.anki.version import ANKI21
BROWSER_TAG = "_reschedule" if ANKI21 else "reschedule"

import os
ADDON_PATH = os.path.dirname(__file__)

ADDONNAME = "rememorize" #old reference, maybe used by other addons.
ADDON_NAME = "ReMemorize" #Used by safety first module

TARGET_STABLE_VERSION = 35

