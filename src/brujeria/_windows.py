from ctypes.wintypes import DWORD, WORD, BYTE, HANDLE, LPWSTR
from ctypes import windll, Structure, POINTER, byref

from pathlib import Path
from typing import List, get_type_hints
from uuid import UUID

import ctypes
import struct


def extern(cdll, name=None):
    """Use type hints to declare and create ctypes function pointers"""

    def wrapper(func):
        nonlocal name
        if not name:
            name = func.__name__
        fptr = cdll[name]
        types = get_type_hints(func)
        restype = types.pop("return", ctypes.c_int)
        # typing library special cases this and I personally find it weird
        if restype is type(None):  # noqa: E721
            restype = None
        fptr.restype = restype
        fptr.argtypes = list(types.values())
        return fptr

    return wrapper


class Pointer:
    def __class_getitem__(cls, typename):
        return POINTER(typename)


class _GUID(Structure):
    _fields_ = [("x", DWORD), ("y", WORD), ("z", WORD), ("w", BYTE * 8)]

    def __init__(self, uuid: UUID):
        super().__init__()
        self.x, self.y, self.z, *rest = uuid.fields
        self.w[:] = [*rest[:2], *tuple(struct.pack("!Q", rest[2]))[2:8]]


_REFKNOWNFOLDERID = Pointer[_GUID]
_PWSTR = Pointer[LPWSTR]


@extern(windll.ole32, "CoTaskMemFree")
def _CoTaskMemFree(_: ctypes.c_void_p) -> None:
    pass


@extern(windll.shell32, "SHGetKnownFolderPath")
def _GetFolderPath(
    rfid: _REFKNOWNFOLDERID, flags: DWORD, token: HANDLE, path: _PWSTR
) -> ctypes.HRESULT:
    pass


class FolderID:
    ROAMING_APP_DATA = UUID("{3EB685DB-65F9-4CF6-A03A-E3EF65729F3D}")
    LOCAL_APP_DATA = UUID("{F1B32785-6FBA-4FCF-9D55-7B8E7F157091}")
    PROGRAM_DATA = UUID("{62AB5D82-FDC1-4DC3-A9DD-070D1D495D97}")


def _get(uuid: UUID) -> Path:
    guid = _GUID(uuid)
    path = LPWSTR()
    if _GetFolderPath(byref(guid), 0, HANDLE(0), byref(path)) < 0:
        raise FileNotFoundError(f"Could not find guid with GUID {uuid}")
    try:
        return Path(path.value)
    finally:
        _CoTaskMemFree(path)


def config_dirs() -> List[Path]:
    return [_get(FolderID.PROGRAM_DATA)]


def data_dirs() -> List[Path]:
    return [_get(FolderID.PROGRAM_DATA)]


def config_home() -> Path:
    return _get(FolderID.ROAMING_APP_DATA)


def cache_home() -> Path:
    return _get(FolderID.LOCAL_APP_DATA)


def data_home() -> Path:
    return _get(FolderID.LOCAL_APP_DATA)