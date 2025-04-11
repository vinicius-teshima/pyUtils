import typing as ty

from .. import may_throw, typs, exceptions

def fetchall(cur: typs.CurTy) -> typs.MayErrTy[typs.ListDictTy[ty.Any]]:
    rows, err = may_throw(cur.fetchall)
    if err is not None:
        return [], err

    if rows is None or len(rows) == 0:
        return [], exceptions.EmptyResultError('Nenhum Resultado da query.')

    assert cur.description is not None
    cols: ty.List[str] = [x.name for x in cur.description]
    return [dict(zip(cols, x)) for x in rows], None

def fetchone(cur: typs.CurTy) -> typs.MayErrTy[typs.DictTy[ty.Any]]:
    row, err = may_throw(cur.fetchone)
    if err is not None:
        return {}, err
    assert row is None \
           or isinstance(row, tuple)

    if row is None or len(row) == 0:
        return {}, exceptions.EmptyResultError('Nenhum Resultado da query.')

    assert cur.description is not None
    cols: ty.List[str] = [x.name for x in cur.description]
    return dict(zip(cols, row)), err
