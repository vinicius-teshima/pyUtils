import io
import pathlib
import typing as ty

from . import typs
from .logger import LoggerCreator, LoggerCreatorMock
from .mt import may_throw

def read_all(path: ty.Union[pathlib.Path, str], *,
             logger_creator: LoggerCreator = LoggerCreatorMock(0),
             encoding: str = 'UTF-8') -> typs.MayErrTy[str]:
    logger = logger_creator('file.read_all')

    logger.info('Abrindo arquivo para leitura: \'%s\'.', path)
    file: ty.Optional[io.TextIOWrapper]
    file, err = may_throw(open, path, 'r', encoding=encoding)
    if file is None or err is not None:
        logger.error('Falha em abrir arquivo para leitura: \'%s\'.', repr(err))
        return '', err
    logger.info('Sucesso em abrir arquivo para leitura: \'%s\'.', path)

    logger.info('Lendo conteúdo do arquivo.')
    content, err = may_throw(file.read, _default='')
    if err is not None:
        logger.error('Falha em ler conteúdo do arquivo: \'%s\'.', repr(err))
        return '', err
    logger.info('Sucesso em ler conteúdo do arquivo.')
    logger.debug('    Tamanho do conteúdo: \'%s\'.', len(content))

    logger.info('Fechando arquivo.')
    _, err = may_throw(file.close)
    if err is not None:
        logger.error('Falha em fechar arquivo: \'%s\'.', repr(err))
        return '', err
    logger.info('Sucesso em fechar arquivo.')

    return content, None
