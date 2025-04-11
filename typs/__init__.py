import typing as ty

try:
    import psycopg2 as psy
    ConnTy = psy.extensions.connection
    CurTy = psy.extensions.cursor
except:
    ConnTy = ty.Any
    CurTy = ty.Any
    pass

from . import esocial, erp

_T = ty.TypeVar('_T')

DictTy = ty.Dict[str, _T]
ListDictTy = ty.List[DictTy[_T]]
MayDictTy = ty.Optional[DictTy[_T]]
MayListTy = ty.Optional[ty.List[_T]]
MayListDictTy = ty.Optional[ListDictTy[_T]]
MayErrTy = ty.Tuple[_T, ty.Optional[Exception]]

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
]
