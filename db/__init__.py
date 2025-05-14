import dataclasses
import typing as ty

import psycopg2
import psycopg2.extras

from . import execute, cursor

from .. import typs, may_throw

class DBInvalidStateError(Exception):
    def __init__(self, msg: str):
        super().__init__(f"Banco em estado inválido: {msg}")
        pass
    pass


@dataclasses.dataclass(frozen=True)
class ConnInfo:
    database: str
    user: str
    password: str
    host: str
    port: str
    pass

class ConnCreator:
    conn_info: ConnInfo

    def __init__(self, conn_info: ConnInfo) -> None:
        self.conn_info = conn_info
        pass

    def __call__(self) -> typs.MayErrTy[typs.ConnTy]:
        err: ty.Optional[Exception]
        conn: typs.ConnTy
        conn, err = may_throw(
            psycopg2.connect,
              dbname=self.conn_info.database,
              user=self.conn_info.user,
              password=self.conn_info.password,
              host=self.conn_info.host,
              port=self.conn_info.port,
              cursor_factory=psycopg2.extras.RealDictCursor,
            _default=ty.cast(typs.ConnTy, object())
        )
        if err is not None:
            return conn, err

        psycopg2.extras.register_uuid(conn_or_curs=conn)
        return conn, err
    pass

__all__ = [
    'DBInvalidStateError',
    'execute',
    'cursor',
    'ConnCreator',
]
