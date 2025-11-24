# ======================== #
# Imports                  #
# ======================== #
import Backends.Common.EventManager as EventManager
import Backends.Common.VideoInterface as VideoInterface
import Backends.Abstraction as Backends
from Common.Files.Settings import UpdateSettingsFromIni, FlushSettingsToIni
from Enums.Common.Backends import BACKENDS

def Run():
    UpdateSettingsFromIni()
    Backends.SetAIOBackend(BACKENDS.AIO.SDL3)
    VideoInterface.Init()

    EventManager.SetupCap()

    while EventManager.Running:
        EventManager.ProcessEvents()

        if not EventManager.Running: # do it early so we dont have to wait another frame
            break

        if EventManager.FrameTickOver():
            EventManager.UpdateTicks()

            VideoInterface.UpdateScreen()

    VideoInterface.Quit()
    FlushSettingsToIni()