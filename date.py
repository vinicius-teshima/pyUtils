import calendar
import typing as ty
import datetime as dt

def last_day_of_month(date: dt.date) -> int:
    return calendar.monthrange(date.year, date.month)[1]

def inc(date: dt.date, *,
        years: ty.Optional[int] = None,
        months: ty.Optional[int] = None,
        days: ty.Optional[int] = None) -> dt.date:
    def iny(d: dt.date, y: int) -> dt.date:
        return d.replace(year=d.year+y)

    def inm(d: dt.date, m: int) -> dt.date:
        t: int = d.month + m
        if t > 12:
            return iny(d.replace(month=1), 1)
        return d.replace(month=t)

    def ind(d: dt.date, ds: int) -> dt.date:
        l: int = last_day_of_month(d)
        t: int = d.day + ds
        if t > l:
            return inm(d.replace(day=t-l), 1)
        return d.replace(day=t)

    if days is not None:
        date = ind(date, days)
    if months is not None:
        date = inm(date, months)
    if years is not None:
        date = iny(date, years)

    return date
