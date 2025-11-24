# ======================== #
# Imports                  #
# ======================== #
from enum import Enum
from typing import Optional
from Structs.Common.Backend import (
    AIOMap,
    ScriptMap,
    FallbackBackend,
    CurrentBackends,
)
from Enums.Common.Backends import BACKENDS, AIO
from Utilities.Logging import Log

SS_TYPES = ["AIO", "Video", "Audio", "Input", "Events"]

_MP_CACHE = {}

# ======================== #
# Get helpers              #
# ======================== #
def GetCurrentBackend(Type, Fallback=None) -> Optional[BACKENDS]: return getattr(CurrentBackends, Type, Fallback) # so pycharm is hapi

def GetModulePathFromCurrentBackendType(Type):
    if Type in _MP_CACHE:
        return _MP_CACHE[Type]

    _CURRENT_SUBSYS = GetCurrentBackend(Type)
    if _CURRENT_SUBSYS is None:
        Log.Error("No backend found, cannot get module")
        return None

    BackendFolder = _CURRENT_SUBSYS.name # type: ignore
    Script = ScriptMap.get(Type, "ScriptName")

    ModulePath = f"Backends.{BackendFolder}.{Script}"
    _MP_CACHE[Type] = ModulePath
    return ModulePath

# ======================== #
# Setter helpers           #
# ======================== #
def SetAIOBackend(Backend: AIO): # AIO in Backends
    Log.Verbose("Current backend is " + str(CurrentBackends.AIO))
    Log.Verbose("Attempting to switch AIO backends...")
    CurrentBackends.AIO = Backend

    _MAP = AIOMap.get(Backend, AIOMap[FallbackBackend]).items()
    for Key, Value in _MAP:
        setattr(CurrentBackends, Key, Value)
        Log.Verbose(f"Set {str(Value)} to {str(Key)}")
    if not Backend in BACKENDS.AIO: # goes back around to line 4
        Log.Warn("AIO subsys does not exist! Will fall back to SDL3")

    Log.Important("Backend has been set to " + str(CurrentBackends.AIO))
    return True

def SetBackend(Type: str, Backend: Enum): # i love python
    if Type not in CurrentBackends:
        Log.Error("Backend type does not exist")
        return False

    setattr(CurrentBackends, Type, Backend)
    Log.Verbose(f"Set {Type} backend to {str(Backend)}")
    return True