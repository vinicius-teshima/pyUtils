import logging
import typing as ty

import psycopg2 as psy

from . import esocial, erp

_T = ty.TypeVar('_T')

ConnTy = psy.extensions.connection
CurTy = psy.extensions.cursor

DictTy = ty.Dict[str, _T]
ListDictTy = ty.List[DictTy[_T]]
MayDictTy = ty.Optional[DictTy[_T]]
MayListTy = ty.Optional[ty.List[_T]]
MayListDictTy = ty.Optional[ListDictTy[_T]]
MayErrTy = ty.Tuple[_T, ty.Optional[Exception]]

LoggerCreatorTy = ty.Callable[[str], logging.Logger]

__all__ = [
    'esocial',
    'erp',
    '_T',
    'ConnTy',
    'CurTy',
    'DictTy',
    'ListDictTy',
    'MayDictTy',
    'MayListTy',
    'MayListDictTy',
    'MayErrTy',
    'LoggerCreatorTy',
]
