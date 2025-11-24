# ======================== #
# Imports                  #
# ======================== #
from enum import Enum, auto

class LOGLEVELS(Enum):
    INFO      = auto()
    SUCCESS   = auto()
    IMPORTANT = auto()
    WARNING   = auto()
    ERROR     = auto()
    VERBOSE   = auto()

SCRIPT_PATH = auto()