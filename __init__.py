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

def logger_creator_closure(level: int) -> ty.Callable[[str], logging.Logger]:
    def logger_creator(name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(level)

        sh = logging.StreamHandler()
        fmtr = logging.Formatter(
            f"[%(asctime)s] [%(levelname)s] [{name}] %(message)s"
        )
        sh.setFormatter(fmtr)
        logger.addHandler(sh)
        del sh, fmtr

        return logger
    return logger_creator

__all__ = [
    'needler',
    'may_throw',
    'logger_creator_closure',
    'value',
    'date',
    'typs',
]
