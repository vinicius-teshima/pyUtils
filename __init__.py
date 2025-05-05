import logging
import typing as ty

from . import typs, value, date

def needler(first: ty.Callable[[], typs.MayErrTy[ty.Any]],
            *fns: ty.Callable[[ty.Any], typs.MayErrTy[ty.Any]],
            last: ty.Callable[[ty.Any], typs.MayErrTy[typs._T]],
            default: typs._T) -> typs.MayErrTy[typs._T]:
    err: ty.Optional[Exception]
    ret: ty.Any

    ret, err = first()
    if err is not None:
        return default, err

    for fn in fns:
        ret, err = fn(ret)
        if err is not None:
            return default, err
        pass

    ret, err = last(ret)
    if err is not None:
        return default, err

    return ret, None

@ty.overload
def may_throw(func: ty.Callable[..., typs._T],
              *args: ty.Any,
              _default: typs._T,
              _prev_err: ty.Optional[Exception] = None,
              **kwargs: ty.Any) -> ty.Tuple[typs._T, ty.Optional[Exception]]:
    ...

@ty.overload
def may_throw(func: ty.Callable[..., typs._T],
              *args: ty.Any,
              _default: None = None,
              _prev_err: ty.Optional[Exception] = None,
              **kwargs: ty.Any) -> ty.Tuple[ty.Optional[typs._T],
                                            ty.Optional[Exception]]:
    ...

def may_throw(func: ty.Callable[..., typs._T],
              *args: ty.Any,
              _default: ty.Optional[typs._T] = None,
              _prev_err: ty.Optional[Exception] = None,
              **kwargs: ty.Any) -> ty.Tuple[ty.Optional[typs._T],
                                            ty.Optional[Exception]]:
    if _prev_err is not None:
        return _default, _prev_err

    ret: ty.Tuple[ty.Optional[typs._T], ty.Optional[Exception]]
    try:
        ret = func(*args, **kwargs), None
    except Exception as err: # pylint: disable=W0718
        setattr(err, 'err_orig_func', getattr(func, '__name__', 'Unknown'))
        ret = _default, err
        pass
    return ret

class LoggerCreator:
    ident_level: int = 0
    name_padding: int = 0
    count: int = 0
    level: int

    def __init__(self, level: int) -> None:
        self.level = level
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

        return logger

    def new_child(self) -> 'LoggerCreator':
        ret: 'LoggerCreator' = LoggerCreator(self.level)
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

__all__ = [
    'needler',
    'may_throw',
    'LoggerCreator',
    'LoggerCreatorMock',
    'value',
    'date',
    'typs',
]
