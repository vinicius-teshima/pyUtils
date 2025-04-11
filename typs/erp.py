import enum

class TipoInscricao(enum.IntEnum):
    INVALID = -1
    PJ = 0
    PF = 1
    pass

class TipoPeriodoApuracao(enum.IntEnum):
    INVALID = -1
    MENSAL = 1
    ANUAL = 2
    pass
