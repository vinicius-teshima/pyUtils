import uuid
import logging
import typing as ty

from . import typs, db

class LoggerCreator:
    ident_level: int = 0
    name_padding: int = 0
    count: int = 0
    level: int
    conn: ty.Optional[typs.ConnTy]
    user: ty.Optional[str]
    modulo: ty.Optional[int]
    sessao: ty.Optional[uuid.UUID]

    def __init__(self, level: int
                     , conn: ty.Optional[typs.ConnTy] = None
                     , user: ty.Optional[str] = None
                     , modulo: ty.Optional[int] = None
                     , sessao: ty.Optional[uuid.UUID] = None) -> None:
        self.level = level
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

        sh = logging.StreamHandler()
        fmtr = logging.Formatter(
            f"[%(asctime)s] [%(levelname)8s] " \
                    f" [{name:>20}] {ident}%(message)s"
        )
        sh.setFormatter(fmtr)
        logger.addHandler(sh)
        del sh, fmtr

        if self.conn is not None:
            assert self.user is not None
            assert self.modulo is not None
            assert self.sessao is not None
            dblh = db.DBLoggerHandler(self.level, self.conn, self.user,
                                      self.modulo, self.sessao)
            logger.addHandler(dblh)
            pass

        return logger

    def new_child(self) -> 'LoggerCreator':
        ret: 'LoggerCreator' = LoggerCreator(self.level, self.conn, self.user,
                                             self.modulo, self.sessao)
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

    def new_child(self) -> 'LoggerCreatorMock':
        return LoggerCreatorMock(0)
    pass
