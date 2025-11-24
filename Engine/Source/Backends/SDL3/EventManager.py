# ======================== #
# Imports                  #
# ======================== #
from sdl3 import *
from Enums.Video.States import WINDOW_STATE
from Structs.Settings.Video import VideoSettings
import Backends.Common.VideoInterface as VideoInterface
from Utilities.Logging import Log

# ======================== #
# Window events            #
# ======================== #
Running = False

def ProcessEvent(Event):
    global Running

    if Event.type == SDL_EVENT_WINDOW_FOCUS_GAINED:
        VideoInterface.WindowState = WINDOW_STATE.FOCUSED
    if Event.type == SDL_EVENT_WINDOW_FOCUS_LOST:
        VideoInterface.WindowState = WINDOW_STATE.UNFOCUSED
    elif Event.type == SDL_EVENT_WINDOW_MAXIMIZED:
        # noinspection PyTypeChecker
        SDL_SetWindowFullscreen(VideoInterface.WindowInstance, True)
        SDL_HideCursor()
        VideoSettings.Fullscreen.Enabled = True
        Log.Info("Maximize event detected! Changing to fullscreen...")
    elif Event.type == (SDL_EVENT_WINDOW_CLOSE_REQUESTED or SDL_EVENT_TERMINATING or SDL_EVENT_QUIT):
        Running = False
        Log.Important("Session end event detected! Closing...")

def ProcessEvents():
    global Running

    NewEvent = SDL_Event()
    while SDL_PollEvent(NewEvent):
        ProcessEvent(NewEvent)

# ======================== #
# FPS capping              #
# ======================== #
FrequencyTarget = None
CurrentTicks    = None
PreviousTicks   = None

def SetupCap():
    global FrequencyTarget, CurrentTicks, PreviousTicks

    FrequencyTarget = SDL_GetPerformanceFrequency() / VideoSettings.RefreshRate  # type: ignore
    CurrentTicks    = 0
    PreviousTicks   = 0

def FrameTickOver():
    global FrequencyTarget, CurrentTicks, PreviousTicks

    CurrentTicks = SDL_GetPerformanceCounter()
    return CurrentTicks >= PreviousTicks + FrequencyTarget # type: ignore

def UpdateTicks():
    global CurrentTicks, PreviousTicks
    PreviousTicks = CurrentTicks