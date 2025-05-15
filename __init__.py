import uuid
import logging
import typing as ty

from . import typs, value, date, db
from .logger import LoggerCreator, LoggerCreatorMock
from .mt import may_throw

def needler(first: ty.Callable[[], typs.MayErrTy[ty.Any]],
            *fns: ty.Callable[[ty.Any], typs.MayErrTy[ty.Any]],
            last: ty.Callable[[ty.Any], typs.MayErrTy[typs._T]],
            default: typs._T) -> typs.MayErrTy[typs._T]:
    err: ty.Optional[Exception]
    ret: ty.Any

    ret, err = first()
    if err is not None:
        return default, err

    for fn in fns:
        ret, err = fn(ret)
        if err is not None:
            return default, err
        pass

    ret, err = last(ret)
    if err is not None:
        return default, err

    return ret, None


__all__ = [
    'needler',
    'may_throw',
    'LoggerCreator',
    'LoggerCreatorMock',
    'value',
    'date',
    'typs',
    'db',
]
