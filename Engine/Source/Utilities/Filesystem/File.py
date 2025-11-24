# ======================== #
# Imports                  #
# ======================== #
import os
import shutil
from configparser import ConfigParser

# ======================== #
# General file management  #
# ======================== #
def Exists(Path): return os.path.exists(Path)

def Delete(Path):
    if Exists(Path):
        return os.remove(Path)
    else:
        return False

def Copy(Source, Dest):
    if not Exists(Dest):
        os.mkdir(Dest)
    if Exists(Source):
        return shutil.copy(Source, Dest)
    return False

def Move(Source, Dest):
    if not Exists(Dest):
        os.mkdir(Dest)
    if Exists(Source):
        return shutil.move(Source, Dest)
    return False

def Duplicate(Source, NewName=None, Extension=" (Copy)"):
    _DESTINATION = ""
    if not Exists(Source):
        return False
    _SOURCEFILE_DIR = os.path.dirname(Source)
    _BASE, _EXTENSION = os.path.splitext(os.path.basename(Source))
    if NewName:
        _DESTINATION = os.path.join(_SOURCEFILE_DIR, NewName)
        shutil.copy(Source, str(_DESTINATION))
    else:
        _BASE += Extension
        while Exists(os.path.join(_SOURCEFILE_DIR, _BASE + _EXTENSION)):
            _BASE += Extension
        _BASE_COPY = _BASE + _EXTENSION
        _DESTINATION = os.path.join(_SOURCEFILE_DIR, _BASE_COPY)
        shutil.copy(Source, str(_DESTINATION))
    return _DESTINATION

# ======================== #
# INI management           #
# ======================== #
_P = ConfigParser()
_P.optionxform = str
_CUR_PATH:    None | str  = None
_CUR_SECTION: None | dict = {}

def _PARSE_VALUE(Value, AUTOPARSE_TUPLES=True):
    if not isinstance(Value, str):
        return Value

    # could be a boolean?
    if Value.lower() == "true":
        return True
    elif Value.lower() == "false":
        return False

    # could be an integer?
    try:
        return int(Value)
    except ValueError:
        pass

    # could be a float?
    try:
        return float(Value)
    except ValueError:
        pass

    # could be a tuple?
    if Value.startswith("(") and Value.endswith(")"):
        _IN = Value[1:-1].strip()
        if not _IN:
            return tuple()
        _ITMS = [_ITM.strip() for _ITM in _IN.split(",")]
        if AUTOPARSE_TUPLES:
            _PI = []
            for _ITM in _ITMS:
                try:
                    _PI.append(_PARSE_VALUE(_ITM))
                except (TypeError, ValueError):
                    _PI.append(_ITM)
            return tuple(_PI)
        return tuple(_IN)

    # well it wasn't any of those so :(
    return Value

def _WRITE_INI_SAFE(Section, Data):
    """
    With ConfigParser, normally the data in the INI file gets overwritten completely.
    Comments are not preserved, so instead of using another library, I wrote an
    alternative. Not super amazing, but hey, it gets the job done.
    """
    with open(_CUR_PATH, "r+") as Ini:
        _LINES = Ini.readlines()
        __CUR_SECTION = None
        _RECONSTRUCT = []
        for _LINE in _LINES:
            _LINE_S = _LINE.strip()
            if _LINE_S.startswith("[") and _LINE_S.endswith("]"):
                __CUR_SECTION = _LINE_S[1:-1]

            if "=" in _LINE: # probably a key... hopefully
                _PRTS = _LINE.split("=", 1)
                _KEY  = _PRTS[0].strip()
                try:
                    if __CUR_SECTION == Section:
                        _VAL = Data[_KEY]
                        if _VAL is not None:
                            _LINE = f"{_KEY}={_VAL}\n"
                except KeyError:
                    pass # COPE!

            _RECONSTRUCT.append(_LINE)

        Ini.seek(0)
        Ini.write("".join(_RECONSTRUCT))
        Ini.truncate()

def UpdateCurrentPath(Path, IgnoreClearWarn = 1): # ignore = 0, clear = 1, warn = 2
    global _CUR_PATH
    if _CUR_PATH != Path:
        if _P.sections():
            if IgnoreClearWarn == 1:
                _P.clear()
            elif IgnoreClearWarn == 2:
                Log.Warn("ConfigParser already has leftover data, reading multiple files at a time may cause bugs")
            return True
        _CUR_PATH = Path
    return None

def ReadSection(Section):
    if not Exists(_CUR_PATH):
        return None
    UpdateCurrentPath(_CUR_PATH)
    _P.read(_CUR_PATH)
    if not _P.has_section(Section):
        return None
    return {_KEY: _PARSE_VALUE(_VALUE) for _KEY, _VALUE in _P.items(Section)}

def WriteSection(Section, Data):
    UpdateCurrentPath(_CUR_PATH)
    if not _P.has_section(Section):
        _P.add_section(Section)
    for _K, _VAL in Data.items():
        _P.set(Section, _K, str(_VAL)) # like i know it says it in the docs that it has to be a string, but why?
    _WRITE_INI_SAFE(Section, Data)
    return True

def ReadKey(Section, Key, Default=None):
    if not Exists(_CUR_PATH):
        return None
    global _CUR_SECTION
    if not _CUR_SECTION:
        _CUR_SECTION = ReadSection(Section)
        if not _CUR_SECTION:
            return Default
    return _PARSE_VALUE(_CUR_SECTION.get(Key, Default))

def WriteKey(Section, Key, Value):
    UpdateCurrentPath(_CUR_PATH)
    if not _P.has_section(Section):
        _P.add_section(Section)
    _P.set(Section, Key, str(Value))
    _WRITE_INI_SAFE(Section, {Key: Value})
    return True