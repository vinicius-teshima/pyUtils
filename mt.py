import typing as ty

from . import typs

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
