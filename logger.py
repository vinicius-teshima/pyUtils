import uuid
import logging
import typing as ty

from . import typs, db

# pylint: disable-next=R0902
class LoggerCreator:
    ident_level: int = 0
    name_padding: int = 0
    count: int = 0
    level: int
    file_path: ty.Optional[typs.PathTy]
    conn: ty.Optional[typs.ConnTy]
    user: ty.Optional[str]
    modulo: ty.Optional[int]
    sessao: ty.Optional[uuid.UUID]

    # pylint: disable-next=R0913
    def __init__(self, level: int, *
                     , file_path: ty.Optional[typs.PathTy] = None
                     , conn: ty.Optional[typs.ConnTy] = None
                     , user: ty.Optional[str] = None
                     , modulo: ty.Optional[int] = None
                     , sessao: ty.Optional[uuid.UUID] = None) -> None:
        self.level = level
        self.file_path = file_path
        self.conn = conn
        self.user = user
        self.modulo = modulo
        self.sessao = sessao

        if self.conn is not None:
            assert self.user is not None, \
                    'If conn is passed user needs to be passed too.'
            assert self.modulo is not None, \
                    'If conn is passed modulo needs to be passed too.'
            assert self.sessao is not None, \
                    'If conn is passed sessao needs to be passed too.'
            pass
        pass

    def __call__(self, name: str) -> logging.Logger:
        logger = logging.getLogger(name + str(self.count))
        self.count += 1
        logger.setLevel(self.level)

        ident = ''
        if self.ident_level > 0:
            ident = ''.join('    ' for _ in range(self.ident_level-1))
            ident += '|-- '
            pass

        fmtr = logging.Formatter(
            f"[%(asctime)s] [%(levelname)8s] [{name:>20}] {ident}%(message)s"
        )

        sh = logging.StreamHandler()
        sh.setFormatter(fmtr)
        logger.addHandler(sh)
        del sh

        if self.conn is not None:
            assert self.user is not None
            assert self.modulo is not None
            assert self.sessao is not None
            dblh = db.DBLoggerHandler(self.level, self.conn, self.user,
                                      self.modulo, self.sessao)
            logger.addHandler(dblh)
            pass

        if self.file_path is not None:
            fh = logging.FileHandler(self.file_path)
            fh.setFormatter(fmtr)
            logger.addHandler(fh)
            pass

        return logger

    def test_db_logger(self) -> ty.Optional[Exception]:
        err: ty.Optional[Exception] = None

        if self.conn is None:
            return None

        logger: logging.Logger
        logger = self('test_db_logger')

        msg: str = 'Teste de salvar logs no banco de dados.'
        logger.log(self.level, msg)

        _, err = db.execute.fetchone(
            self.conn,
            '''
SELECT id
  FROM persona.logs W
 WHERE level = %(level)s
   AND sessao = %(sessao)s
   AND usuario = %(user)s
   AND modulo = %(modulo)s
''',
            {
                'level' : logging.getLevelName(self.level),
                'sessao': self.sessao,
                'user'  : self.user,
                'modulo': self.modulo
            }
        )
        return err

    def new_child(self) -> 'LoggerCreator':
        ret: 'LoggerCreator' = LoggerCreator(
            self.level,
            file_path=self.file_path,
            conn=self.conn,
            user=self.user,
            modulo=self.modulo,
            sessao=self.sessao
        )
        ret.ident_level = self.ident_level + 1
        ret.count = self.count + 10
        return ret
    pass

class LoggerCreatorMock(LoggerCreator):
    def __init__(self, level: int) -> None:
        super().__init__(level)
        pass
    def __call__(self, name: str) -> logging.Logger:
        class L(logging.Logger):
            def debug(self, *_: ty.Any, **__: ty.Any) -> None:
                return None
            def info(self, *_: ty.Any, **__: ty.Any) -> None:
                return None
            def warning(self, *_: ty.Any, **__: ty.Any) -> None:
                return None
            def error(self, *_: ty.Any, **__: ty.Any) -> None:
                return None
            def fatal(self, *_: ty.Any, **__: ty.Any) -> None:
                return None
            def critical(self, *_: ty.Any, **__: ty.Any) -> None:
                return None
            pass
        return L(name)

    def test_db_logger(self) -> ty.Optional[Exception]:
        return None

    def new_child(self) -> 'LoggerCreatorMock':
        return LoggerCreatorMock(0)
    pass
