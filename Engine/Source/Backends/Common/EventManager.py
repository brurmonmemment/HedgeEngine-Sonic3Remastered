# ======================== #
# Imports                  #
# ======================== #
import importlib
import sys
from types import ModuleType as _M
from Backends.Abstraction import GetModulePathFromCurrentBackendType, GetCurrentBackend

# ======================== #
# Static analysis stubs    #
# ======================== #
Running = False
# noinspection PyUnusedLocal
def ProcessEvent(Event): pass
def ProcessEvents(): pass
FrequencyTarget = None
CurrentTicks    = None
PreviousTicks   = None
def SetupCap(): pass
def FrameTickOver(): pass
def UpdateTicks(): pass

# ======================== #
# Actual content @ runtime # exist because static sucks
# ======================== #
class anus(_M):
    _MODULE = None
    _SUBSYS = None

    def _GET_SUBSYS(self):
        _NEW_SUBSYS = GetCurrentBackend("Events")
        if _NEW_SUBSYS != self._SUBSYS: # probably haven't already cached the module so actually import it
            _MODULE_PATH = GetModulePathFromCurrentBackendType("Events")
            self._MODULE = importlib.import_module(_MODULE_PATH)
            self._SUBSYS = _NEW_SUBSYS
        return self._MODULE

    def __getattr__(self, name): return getattr(self._GET_SUBSYS(), name) # FUCK YOU PYCHARM
    def __setattr__(self, name, value):
        if name in ("_MODULE", "_SUBSYS"):
            super().__setattr__(name, value)
        else:
            setattr(self._GET_SUBSYS(), name, value)

sys.modules[__name__] = anus(__name__)