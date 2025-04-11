from . import execute, cursor, get

class DBInvalidStateError(Exception):
    def __init__(self, msg: str):
        super().__init__(f"Banco em estado inválido: {msg}")
        pass
    pass

__all__ = [
    'DBInvalidStateError',
    'execute',
    'cursor',
    'get'
]
