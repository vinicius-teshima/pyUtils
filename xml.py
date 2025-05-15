import logging
import typing as ty

from . import typs, value
from .logger import LoggerCreator, LoggerCreatorMock


class InvalidXMLStructureError(Exception):
    def __init__(self, msg: str):
        super().__init__(f"Estrutura de XML Inválida: {msg}.")
        pass
    pass

class InvalidXPathError(Exception):
    def __init__(self, xpath: str, reason: ty.Optional[str] = None):
        if reason is None:
            super().__init__(f"XPath inválido: '{xpath}'.")
        else:
            super().__init__(f"XPath inválido: '{xpath}': {reason}.")
            pass
        pass
    pass

class XMLTagNotFoundError(InvalidXMLStructureError):
    def __init__(self, tag: str, xml: 'XMLDict'):
        path: str = xml.get_xpath()
        msg: str = f"Tag '{tag}' não encontrada dentro de {path}"
        super().__init__(msg)
        pass
    pass

class XMLDict(ty.Dict[str, ty.Any]):
    parent: ty.Optional['XMLDict'] = None
    tag: ty.Optional[str] = None

    def get_xpath(self) -> str:
        path: str

        if self.tag is None or self.parent is None:
            return ''

        path = '/' + self.parent.get_xpath()
        if path != '/':
            path += '/'
            pass

        path += self.tag

        return path

    def __setitem__(self, key: str, value: ty.Any) -> None:
        if isinstance(value, XMLDict) is True:
            value.parent = self
            value.tag = key
            pass

        if key not in self:
            dict.__setitem__(self, key, value)
            return

        tmp: ty.Any
        tmp = dict.__getitem__(self, key)
        if isinstance(tmp, list) is True:
            tmp.append(value)
            return

        dict.__setitem__(self, key, [tmp])
        pass
    pass

def get_xpath(xml: XMLDict, xpath: str, *,
              logger_creator: LoggerCreator = LoggerCreatorMock(0)
              ) -> typs.MayErrTy[ty.Union[XMLDict, ty.List[XMLDict], str]]:
    err: ty.Optional[Exception]
    tmp: ty.Any
    ret: XMLDict

    logger: logging.Logger
    logger = logger_creator('xml.get_xpath')

    if len(xpath) == 0 \
            or xpath[0] != '/' \
            or xpath[-1] == '/' \
            or ('[' in xpath and ']' not in xpath) \
            or (']' in xpath and '[' not in xpath):
        logger.error('XPath invalido: \'%s\'.', xpath)
        return XMLDict(), InvalidXPathError(xpath)

    ret = xml
    for tag in xpath.split('/')[1:]:
        if tag[0] == '[' or tag[0] == ']':
            logger.error('XPath invalido: \'%s\'.', xpath)
            return XMLDict(), InvalidXPathError(xpath)
        if tag == '*':
            if isinstance(ret, str) is True:
                logger.error('Tag \'%s\' não encontrada no caminho \'%s\'.',
                             tag, xpath)
                return XMLDict(), XMLTagNotFoundError(tag, ret)

            ind: int = xpath.index('*')
            if isinstance(ret, XMLDict) is True:
                for r in ret.keys():
                    tmp, err = get_xpath(
                        ret[r], xpath[ind+1:],
                        logger_creator=logger_creator.new_child()
                    )
                    if err is not None:
                        continue
                    return tmp, None
            else:
                for _r in ret:
                    tmp, err = get_xpath(
                        ty.cast(XMLDict, _r), xpath[ind+1:],
                        logger_creator=logger_creator.new_child()
                    )
                    if err is not None:
                        continue
                    return tmp, None
                pass

            logger.error('Tag \'%s\' não encontrada no caminho \'%s\'.',
                         tag, xpath)
            return XMLDict(), XMLTagNotFoundError(tag, ret)

        if '[' in tag:
            index: int
            index, err = value.to_int(tag[tag.index('[')+1 : tag.index(']')])
            if err is not None:
                logger.error('XPath invalido: \'%s\': \'%s\'.',
                             xpath, repr(err))
                return XMLDict(), InvalidXPathError(xpath, repr(err))

            ret = ret[tag[:tag.index('[')]]
            if isinstance(ret, list) is False:
                logger.error('Tag \'%s\' não encontrada no caminho \'%s\'.',
                             tag, xpath)
                return XMLDict(), XMLTagNotFoundError(tag, ret)

            ret = ret[index] # type: ignore
            continue

        if isinstance(ret, XMLDict) is False \
                or tag not in ret:
            logger.error('Tag \'%s\' não encontrada no caminho \'%s\'.',
                         tag, xpath)
            return XMLDict(), XMLTagNotFoundError(tag, ret)

        ret = ret[tag]
        pass
    return ret, None

def to_dict(xml: str) -> typs.MayErrTy[XMLDict]:
    if '<' not in xml \
            or '>' not in xml \
            or '/' not in xml:
        return XMLDict(), Exception('Invalid XML')
    def _treat_key(key: str) -> str:
        key = key.strip()
        if ' ' in key:
            key = key.split(' ')[0]
            pass
        #if ':' in key:
        #    key = key.split(':')[-1]
        #    pass
        return key

    ret = XMLDict()
    parent: ty.List[XMLDict] = []
    inside: ty.List[str] = []

    cur: XMLDict = ret
    was_value: bool = False
    for t in xml.split('<'):
        if t == '':
            continue
        if t[0] == '?':
            continue

        if t[0] == '/':
            if was_value is True:
                was_value = False
                continue
            should_be: str = inside.pop()
            found: str = _treat_key(t[1:t.index('>')])
            if found != should_be:
                return XMLDict(), InvalidXMLStructureError(
                    f"Estava esperando o fechamento da tag: {should_be}"
                    f", mas foi achado a tag: {found}"
                )
            cur = parent.pop()
            continue

        key: str
        value: str
        key, value = t.split('>')
        if key[-1] == '/':
            key = _treat_key(key)
            cur[key] = NotImplementedError('ValueLess XML Leaf')
            continue
        key = _treat_key(key)
        value = value.strip()

        if value == '':
            _t = XMLDict()
            cur[key] = _t

            parent.append(cur)
            inside.append(key)
            cur = _t
            continue

        cur[key] = value
        was_value = True

        pass

    if len(inside) != 0:
        return XMLDict(), InvalidXMLStructureError(
            f"Não foi achado o fechamento das tags: [{', '.join(inside)}]"
        )

    return ret, None
