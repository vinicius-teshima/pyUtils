import typing as ty

import psycopg2
import psycopg2.extras

from . import execute, cursor

from .. import typs

class DBInvalidStateError(Exception):
    def __init__(self, msg: str):
        super().__init__(f"Banco em estado inválido: {msg}")
        pass
    pass

def conn_creator_closure(database: str, user: str,
                         password: str, host: str,
                         port: str) -> ty.Callable[[], typs.ConnTy]:
    def conn_creator() -> typs.ConnTy:
        conn = psycopg2.connect(dbname=database, user=user,
                                password=password, host=host,
                                port=port,
                                cursor_factory=psycopg2.extras.RealDictCursor)
        psycopg2.extras.register_uuid(conn_or_curs=conn)
        return conn
    return conn_creator

__all__ = [
    'DBInvalidStateError',
    'execute',
    'cursor',
    'conn_creator_closure',
]
