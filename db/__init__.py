import sys
import uuid
import logging
import dataclasses
import typing as ty

import psycopg2
import psycopg2.extras

from . import execute, cursor

from .. import typs
from ..mt import may_throw

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

# pylint: disable-next=R0903
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

class DBLoggerHandler(logging.Handler):
    conn: typs.ConnTy
    user: str
    modulo: int
    sessao: uuid.UUID
    table: str
    _query: str
    _params: typs.MapTy[ty.Any]

    # pylint: disable-next=R0913
    def __init__(self, level: int
                     , conn: typs.ConnTy
                     , user: str
                     , modulo: int
                     , sessao: uuid.UUID
                     , *, table: str = 'persona.logs') -> None:
        super().__init__()

        self.conn = conn

        self.user = user
        self.modulo = modulo
        self.sessao = sessao
        self.table = table

        self._query = f"""
INSERT INTO {self.table}(level, usuario, modulo, sessao, mensagem)
VALUES(%(level)s, %(usuario)s, %(modulo)s, %(sessao)s, %(mensagem)s)
        """
        self._params = {
            'usuario': self.user,
            'modulo': self.modulo,
            'sessao': self.sessao,
        }
        pass

    def emit(self, record: logging.LogRecord) -> None:
        self._params['level'] = record.levelname
        self._params['mensagem'] = record.getMessage()

        err = execute.execute(self.conn, self._query, self._params)
        if err is not None:
            print(f"Falha ao tentar salvar log no banco." \
                    f" Erro: \'{repr(err)}\'." \
                    f" Query: \'{self._query}\'." \
                    f"Params: \'{self._params}\'.")
            pass
        pass
    pass


__all__ = [
    'DBInvalidStateError',
    'execute',
    'cursor',
    'ConnCreator',
    'DBLoggerHandler',
]
