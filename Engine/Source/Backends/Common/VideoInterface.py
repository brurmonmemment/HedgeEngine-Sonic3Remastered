# ======================== #
# Imports                  #
# ======================== #
import importlib
import sys
from types import ModuleType as _M
from sdl3 import SDL_Window
from Enums.Video.States import WINDOW_STATE
from Backends.Abstraction import GetModulePathFromCurrentBackendType, GetCurrentBackend

# ======================== #
# Static analysis stubs    #
# ======================== #
WindowInstance   = None
RendererInstance = None
WindowState: WINDOW_STATE | None = None

def Init(): return None
def InitSDLSubsystems(): return None
def CreateWindow(): return None
# noinspection PyUnusedLocal
def CreateRenderer(Window: SDL_Window): return None
def UpdateScreen(): return None
def Quit(): return None

# ======================== #
# Actual content @ runtime # exist because static sucks
# ======================== #
class anus(_M):
    _MODULE = None
    _SUBSYS = None

    def _GET_SUBSYS(self):
        _NEW_SUBSYS = GetCurrentBackend("Video")
        if _NEW_SUBSYS != self._SUBSYS: # probably haven't already cached the module so actually import it
            _MODULE_PATH = GetModulePathFromCurrentBackendType("Video")
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