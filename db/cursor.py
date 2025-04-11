import typing as ty

from .. import may_throw, typs, exceptions

def fetchall(cur: typs.CurTy) -> typs.MayErrTy[typs.ListDictTy[ty.Any]]:
    res, err = may_throw(cur.fetchall)
    if err is not None:
        return [], err

    if res is None or len(res) == 0:
        return [], exceptions.EmptyResultError('Nenhum Resultado da query.')

    return ty.cast(typs.ListDictTy[ty.Any], res), None

def fetchone(cur: typs.CurTy) -> typs.MayErrTy[typs.DictTy[ty.Any]]:
    res, err = may_throw(cur.fetchone)
    if err is not None:
        return {}, err
    assert res is None \
           or isinstance(res, dict)

    if res is None or len(res) == 0:
        return {}, exceptions.EmptyResultError('Nenhum Resultado da query.')

    return res, err
