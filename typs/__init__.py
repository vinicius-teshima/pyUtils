import logging
import pathlib
import typing as ty

import psycopg2 as psy

from . import esocial, erp

_T = ty.TypeVar('_T')

ConnTy = psy.extensions.connection
CurTy = psy.extensions.cursor

DictTy = ty.Dict[str, _T]
MapTy = ty.MutableMapping[str, _T]
ImuMapTy = ty.Mapping[str, _T]
ListDictTy = ty.List[DictTy[_T]]
MayDictTy = ty.Optional[DictTy[_T]]
MayListTy = ty.Optional[ty.List[_T]]
MayListDictTy = ty.Optional[ListDictTy[_T]]
MayErrTy = ty.Tuple[_T, ty.Optional[Exception]]

LoggerCreatorTy = ty.Callable[[str], logging.Logger]

PathTy = ty.Union[str, pathlib.Path]

class CNPJ(str):
    @staticmethod
    def is_valid(s: str) -> bool:
        if len(s) != 14:
            return False
        return True

    def raiz(self) -> str:
        return self[:8]
    def ordem(self) -> str:
        return self[8:]
    pass

class CPF(str):
    @staticmethod
    def is_valid(s: str) -> bool:
        if len(s) != 11:
            return False
        return True
    pass

__all__ = [
    'esocial',
    'erp',
    '_T',
    'ConnTy',
    'CurTy',
    'DictTy',
    'MapTy',
    'ImuMapTy',
    'ListDictTy',
    'MayDictTy',
    'MayListTy',
    'MayListDictTy',
    'MayErrTy',
    'LoggerCreatorTy',
]
