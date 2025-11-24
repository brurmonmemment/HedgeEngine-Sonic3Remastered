# ======================== #
# Imports                  #
# ======================== #
from sdl3 import *
from typing import Optional
import math, time
from Structs.Game.Metadata import GameInfo
from Enums.Video.States import WINDOW_STATE
from Structs.Settings.Video import VideoSettings
import Backends.Common.EventManager as EventManager
from Utilities.Logging import Log

# ======================== #
# Objects                  #
# ======================== #
class Window:
    def __init__(self, Name, Width, Height, Flags):
        global WindowState
        self._WINDOW = SDL_CreateWindow(Name.encode(), # you can never be too safe
                                        Width, Height,
                                        Flags)

    @property
    def ptr(self):
        return self._WINDOW

class Renderer:
    def __init__(self, _WINDOW: Window, Backend):
        self._RENDERER = SDL_CreateRenderer(_WINDOW.ptr,
                                            Backend)

    @property
    def ptr(self):
        return self._RENDERER

# ======================== #
# State                    #
# ======================== #
CurWindow:   Optional[Window]   = None
CurRenderer: Optional[Renderer] = None
WindowState: WINDOW_STATE = WINDOW_STATE.PREPARING

# ======================== #
# Functions                #
# ======================== #
def Init():
    if InitSubsystems() and \
       MakeNewWindow() and \
       CreateRenderer(CurWindow):
        EventManager.Running = True
        return True
    return False

def InitSubsystems():
    if not SDL_Init(SDL_INIT_VIDEO | SDL_INIT_EVENTS):
        return False

    SDL_SetHint(SDL_HINT_RENDER_VSYNC, bytes(int(VideoSettings.VSync))) # type: ignore
    return True

def MakeNewWindow():
    global CurWindow
    if CurWindow is not None:
        return CurWindow

    Log.Info(f"Window scale is {VideoSettings.Scale}")
    Log.Verbose(f"Trying to create a window...")

    CurWindow = Window(GameInfo.Title,
                       VideoSettings.Calculate("Width"), VideoSettings.Calculate("Height"),
                       0)
    if CurWindow is None:
        Log.Error(f"Window couldn't be created ({SDL_GetError()})")
        return False
    Log.Success(f"Window created!")

    SDL_HideCursor()
    return CurWindow

def CreateRenderer(OnWindow: Window):
    global CurRenderer
    if CurRenderer is not None:
        return CurRenderer

    Log.Verbose(f"Trying to create a renderer...")

    CurRenderer = Renderer(OnWindow, None)
    if CurRenderer is None:
        Log.Error(f"Renderer couldn't be created ({SDL_GetError()})")
        return False
    Log.Success(f"Renderer created!")

    return CurRenderer

# ======================== #
# Renderer management      #
# ======================== #
def UpdateScreen():
    # TEMP UPDATE, will be replaced later once we are able to draw stuff
    timey    = time.time()
    RGBRed   = int((math.sin(timey) * 0.5 + 0.5) * 255)
    RGBGreen = int((math.sin(timey * 2) * 0.5 + 0.5) * 255)
    RGBBlue  = int((math.sin(timey * 4) * 0.5 + 0.5) * 255)
    SDL_SetRenderDrawColor(CurRenderer.ptr, RGBRed, RGBGreen, RGBBlue, 255) # type: ignore
    SDL_RenderClear(CurRenderer.ptr)
    SDL_RenderPresent(CurRenderer.ptr)

# ======================== #
# Quit                     #
# ======================== #
def Quit():
    global CurWindow, CurRenderer

    if CurRenderer:
        SDL_DestroyRenderer(CurRenderer.ptr)
        CurRenderer = None
    if CurWindow:
        SDL_DestroyWindow(CurWindow.ptr)
        CurWindow = None

    SDL_QuitSubSystem(SDL_INIT_VIDEO | SDL_INIT_EVENTS)
    SDL_Quit()