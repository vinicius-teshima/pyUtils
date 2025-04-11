import typing as ty

from .. import typs, may_throw

from . import cursor

def execute(conn: typs.ConnTy,
            query: str,
            params: typs.DictTy[ty.Any], *,
            do_commit: bool = True,
            do_rollback_on_error: bool = True
            ) -> ty.Optional[Exception]:
    with conn.cursor() as cur:
        _, err = may_throw(cur.execute, query, params)
        if err is not None:
            if do_rollback_on_error is True:
                conn.rollback()
                pass
            return err
        if do_commit is True:
            conn.commit()
            pass
        return None
    pass

def fetchall(conn: typs.ConnTy,
             query: str,
             params: typs.DictTy[ty.Any], *,
             do_commit: bool = True,
             do_rollback_on_error: bool = True
             ) -> typs.MayErrTy[typs.ListDictTy[ty.Any]]:
    with conn.cursor() as cur:
        _, err = may_throw(cur.execute, query, params)
        if err is not None:
            if do_rollback_on_error is True:
                conn.rollback()
                pass
            return [], err
        if do_commit is True:
            conn.commit()
            pass
        return cursor.fetchall(cur)
    pass

def fetchone(conn: typs.ConnTy,
             query: str,
             params: typs.DictTy[ty.Any], *,
             do_commit: bool = True,
             do_rollback_on_error: bool = True
             ) -> typs.MayErrTy[typs.DictTy[ty.Any]]:
    with conn.cursor() as cur:
        _, err = may_throw(cur.execute, query, params)
        if err is not None:
            if do_rollback_on_error is True:
                conn.rollback()
                pass
            return {}, err
        if do_commit is True:
            conn.commit()
            pass
        return cursor.fetchone(cur)
    pass
