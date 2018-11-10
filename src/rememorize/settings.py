from aqt import mw
from aqt.qt import *
from anki.hooks import addHook
from codecs import open
from anki.utils import json
import os


class Settings():
    conf = None

    def __init__(self):
        self.setConf()
        QTimer.singleShot(1000, self.setConfCallback)

    def get(self, key, default=None):
        return self.conf.get(key, default);

    def setConf(self, config=None):
        if not config and not self.conf:
            try:
                config=mw.addonManager.getConfig(__name__)
            except AttributeError:
                moduleDir, _ = os.path.split(__file__)
                path = os.path.join(moduleDir, 'config.json')
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        data=f.read()
                    config=json.loads(data)

        if config: self.conf=config

    def setConfCallback(self):
        try: #Must be loaded after profile loads, after addonmanger21 loads.
            mw.addonManager.setConfigUpdatedAction(__name__, self.setConf)
        except AttributeError: pass

