# ======================== #
# Imports                  #
# ======================== #
import os, sys
from configparser import Error as ERR

MAGIC_WORDS = "HedgeEngine-Sonic3Remastered"
_ENGINE = "Engine"
_SOURCE = "Source"

# ======================== #
# Custom exception         #
# ======================== #
class wtfuh(ERR):
    def __init__(self, section):
        ERR.__init__(self, 'No section: %r' % (section,))
        self.section = section
        self.args = (section,)

# ======================== #
# Checks for the cwd       #
# ======================== #
# It's good enough lmao    #
# ======================== #
CWD = os.getcwd()

if os.path.basename(CWD) != MAGIC_WORDS:  # measure 1: cwd path contains the super secret magic words
    raise wtfuh("where are you LMAO")
if not os.path.isdir(os.path.join(CWD, _ENGINE)):  # measure 2: cwd has the engine folder
    raise wtfuh("nice try ankle-biter, but you've yet to face the wrath of my awesome tapping powers!!!!!")
if not os.path.isdir(os.path.join(CWD, _ENGINE, _SOURCE)):  # final measure: engine folder has the source folder
    # noinspection SpellCheckingInspection
    raise wtfuh(f"i just send yroue ip adres ({(lambda s: (s.connect(("8.8.8.8", 80)), s.getsockname()[0], s.close())[1])(__import__('socket').socket(__import__('socket').AF_INET, __import__('socket').SOCK_DGRAM))}) to my serber you failur!!@@!111") # Gag

sys.path.insert(0, os.path.join(CWD, _ENGINE, _SOURCE))

import HedgeEngine as HedgeEngine
HedgeEngine.Run()