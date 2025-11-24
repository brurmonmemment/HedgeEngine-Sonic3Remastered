# ======================== #
# Imports                  #
# ======================== #
from enum import Enum, auto

# ======================== #
# NOTE                     #
# =========================================================== #
# The only currently working backend(s) as of now are SDL3.   #
# Everything else is merely dummy values for in case someone  #
# else wants to take a stab at implementing it.               #
# =========================================================== #

# ======================== #
# Categories               #
# ======================== #

class AIO(Enum):
    SDL3  = auto()
    SDL2  = auto()
    HEDGE = auto() # NOT HAPPENING LMFAOOOOOOOOO

class Video(Enum):
    SDL3   = auto()
    SDL2   = auto()
    OPENGL = auto()
    VULKAN = auto()
    GLFW   = auto()

class Audio(Enum):
    SDL3      = auto()
    SDL2      = auto()
    MINIAUDIO = auto()
    OPENAL    = auto()

class Input(Enum):
    SDL3      = auto()
    SDL2      = auto()
    GLFW      = auto()
    HEDGE_HID = auto()

class Events(Enum):
    SDL3 = auto()
    SDL2 = auto()

# ======================== #
# Main backends class      #
# ======================== #
class BACKENDS:
    AIO    = AIO
    VIDEO  = Video
    AUDIO  = Audio
    INPUT  = Input
    EVENTS = Events