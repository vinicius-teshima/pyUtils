import enum

class TipoInscricao(enum.IntEnum):
    INVALID = -1
    PJ    = 1
    PF    = 2
    CAEPF = 3
    CNO   = 4
    CGC   = 5
    CEI   = 6
    pass
