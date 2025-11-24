# ======================== #
# Imports                  #
# ======================== #
import os
from Structs.Settings.Video import VideoSettings
import Utilities.Logging as AAAAAAAA
from Utilities.Logging import Log # not doing AAAAA.log
from Utilities.Filesystem.File import ReadSection, WriteSection, WriteKey, UpdateCurrentPath

SettingsFile = "Settings.ini"
FullPath = os.path.join(os.getcwd(), SettingsFile)

def UpdateSettingsFromIni():
    Update.Game()
    Update.Video()

def FlushSettingsToIni():
    Flush.Video()

class Update:
    @staticmethod
    def Game():
        UpdateCurrentPath(FullPath)
        Game = ReadSection("Game")
        if not Game:
            return False

        for Key, Value in Game.items(): # goddamn it we have to specify unlike with video
            if Key == "LogMode":
                AAAAAAAA.LogMode = Value
        Log.Info("Updated game settings from .ini configuration file")
        return True

    @staticmethod
    def Video():
        UpdateCurrentPath(FullPath)
        Video = ReadSection("Video")
        if not Video:
            return False
        for Key, Value in Video.items():
            setattr(VideoSettings, Key, Value)
        Fullscreen = ReadSection("Video.Fullscreen")
        if not Fullscreen:
            return False
        for Key, Value in Fullscreen.items():
            setattr(VideoSettings.Fullscreen, Key, Value)
        Log.Info("Updated video settings from .ini configuration file")
        return True

class Flush:
    @staticmethod
    def Video(): # same thing but in reverse essentially
        UpdateCurrentPath(FullPath)
        WriteSection( "Video", {
            "Width": VideoSettings.Width,
            "Height": VideoSettings.Height,
            "Bordered": VideoSettings.Bordered,
            "VSync": VideoSettings.VSync,
            "Shaders": VideoSettings.Shaders,
            "RefreshRate": VideoSettings.RefreshRate
        })
        WriteSection( "Video.Fullscreen", {
            "Enabled": VideoSettings.Fullscreen.Enabled,
            "Exclusive": VideoSettings.Fullscreen.Exclusive
        })

        # optional vals
        if VideoSettings.Scale:
            WriteKey("Video", "Scale", VideoSettings.Scale)

        if VideoSettings.Fullscreen.Width:
            WriteKey("Video.Fullscreen", "Width", VideoSettings.Fullscreen.Width)
        if VideoSettings.Fullscreen.Height:
            WriteKey("Video.Fullscreen", "Height", VideoSettings.Fullscreen.Height)

        Log.Info("Flushed current video settings values to .ini configuration file")