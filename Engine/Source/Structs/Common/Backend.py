# ======================== #
# Imports                  #
# ======================== #
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from Enums.Common.Backends import BACKENDS

@dataclass
class CurrentBackends:
    AIO:    Optional[Enum] = None
    Video:  Optional[Enum] = None
    Audio:  Optional[Enum] = None
    Input:  Optional[Enum] = None
    Events: Optional[Enum] = None

AIOMap = {
    BACKENDS.AIO.SDL3: { # dedicated maps for if you wanted to do a little mixing and matching
        "Video":  BACKENDS.VIDEO.SDL3,
        "Audio":  BACKENDS.AUDIO.SDL3,
        "Input":  BACKENDS.INPUT.SDL3,
        "Events": BACKENDS.EVENTS.SDL3,
    }
}

ScriptMap = {
    "Video":  "VideoInterface",
    "Audio":  "AudioInterface",
    "Input":  "InputProcessor",
    "Events": "EventManager"
}

FallbackBackend = BACKENDS.AIO.SDL3