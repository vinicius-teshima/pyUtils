import decimal
import typing as ty

from . import typs

def to_int(obj: ty.Any) -> typs.MayErrTy[int]:
    try:
        return int(obj), None
    except Exception as err: # pylint: disable=W0718
        return 0, err
    pass

def to_decimal(val: ty.Any) -> typs.MayErrTy[decimal.Decimal]:
    if isinstance(val, str) is True:
        val = val.replace(',', '.')
        pass
    try:
        return decimal.Decimal(val), None
    except Exception as err: # pylint: disable=W0718
        return decimal.Decimal(0), err
    pass
