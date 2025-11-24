# ======================== #
# Imports                  #
# ======================== #
from Enums.Common.Logging import LOGLEVELS, SCRIPT_PATH
from datetime import datetime
import inspect

WriteToFile = False
Filename = "HE.log"

LogMode  = 0 # Determines logging mode, 0 is none, 1 is basic, and 2 is more verbose
LogLevel = 0 # Determines what kind of log is sent

SymbolMap = {
    LOGLEVELS.INFO:      "[i]",
    LOGLEVELS.SUCCESS:   "[✓]",
    LOGLEVELS.IMPORTANT: "[*]",
    LOGLEVELS.WARNING:   "[!]",
    LOGLEVELS.ERROR:     "[✕]",
    LOGLEVELS.VERBOSE:   "[⋯]"
}

ColorCodeMap = {
    LOGLEVELS.INFO:      94,
    LOGLEVELS.SUCCESS:   92,
    LOGLEVELS.IMPORTANT: 97,
    LOGLEVELS.WARNING:   93,
    LOGLEVELS.ERROR:     91,
    LOGLEVELS.VERBOSE:   90
}

"""
some print wrapper thingamajig
"""
class Log:
    @staticmethod
    def Print(Level: LOGLEVELS, Msg, Timestamp=True, FromFile=SCRIPT_PATH):
        if LogMode > 0:
            if FromFile == SCRIPT_PATH: # Get file origin then
                _STACK = inspect.stack()[2]
                FromFile = f"({_STACK.filename[_STACK.filename.lower().rfind('engine'):]})" # yowza

            ColorCode = f"\033[{ColorCodeMap[Level]}m"
            Time = f"[{datetime.now().strftime('%H:%M:%S')}]"
            print(
                f"{ColorCode}{SymbolMap[Level]} "
                f"{(str(FromFile) + ' ') if FromFile else ''}"
                f"{Time if Timestamp else ''} "
                f"{Msg}"
                "\033[0m", # holy reset
                flush=True
            )

    @staticmethod
    def Info(Msg, Timestamp=True, FromFile=SCRIPT_PATH): Log.Print(LOGLEVELS.INFO, Msg, Timestamp, FromFile)

    @staticmethod
    def Success(Msg, Timestamp=True, FromFile=SCRIPT_PATH): Log.Print(LOGLEVELS.SUCCESS, Msg, Timestamp, FromFile)

    @staticmethod
    def Important(Msg, Timestamp=True, FromFile=SCRIPT_PATH): Log.Print(LOGLEVELS.IMPORTANT, Msg, Timestamp, FromFile)

    @staticmethod
    def Warn(Msg, Timestamp=True, FromFile=SCRIPT_PATH): Log.Print(LOGLEVELS.WARNING, Msg, Timestamp, FromFile)

    @staticmethod
    def Error(Msg, Timestamp=True, FromFile=SCRIPT_PATH): Log.Print(LOGLEVELS.ERROR, Msg, Timestamp, FromFile)

    @staticmethod
    def Verbose(Msg, Timestamp=True, FromFile=SCRIPT_PATH):
        if LogMode > 1:
            Log.Print(LOGLEVELS.VERBOSE, Msg, Timestamp, FromFile)

# Uncomment these and test the logging for yourself!
# Log.Info("This is a test")
# Log.Warn("This is supposed to be a test")
# Log.Error("Brace for impact! Test failed!")
# Log.Success("Test tested!")
# Log.Important("This is a test")
# Log.Verbose("This is a test")