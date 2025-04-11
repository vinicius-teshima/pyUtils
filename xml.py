import typing as ty

from . import typs

class InvalidXMLStructureError(Exception):
    def __init__(self, msg: str):
        super().__init__(f"Estrutura de XML Inválida: {msg}.")
        pass
    pass

def to_dict(xml: str) -> typs.MayErrTy[ty.Dict[str, ty.Any]]:
    if '<' not in xml \
            or '>' not in xml \
            or '/' not in xml:
        return {}, Exception('Invalid XML')
    def _treat_key(key: str) -> str:
        if ' ' in key:
            key = key.split(' ')[0]
            pass
        #if ':' in key:
        #    key = key.split(':')[-1]
        #    pass
        return key
    class MultDict(ty.Dict[str, ty.Any]):
        def __setitem__(self, key: str, value: ty.Any) -> None:
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

    ret = MultDict()
    parent: ty.List[MultDict] = []
    inside: ty.List[str] = []

    cur: MultDict = ret
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
                return {}, InvalidXMLStructureError(
                    f"Estava esperando o fechamento da tag: {should_be}"
                    f", mas foi achado a tag: {found}"
                )
            cur = parent.pop()
            continue

        key: str
        value: str
        key, value = t.split('>')
        if key.endswith('/'):
            key = _treat_key(key)
            cur[key] = NotImplementedError('ValueLess XML Leaf')
            continue
        key = _treat_key(key)

        if value == '':
            _t = MultDict()
            cur[key] = _t

            parent.append(cur)
            inside.append(key)
            cur = _t
            continue

        cur[key] = value
        was_value = True

        pass

    if len(inside) != 0:
        return {}, InvalidXMLStructureError(
            f"Não foi achado o fechamento das tags: [{', '.join(inside)}]"
        )

    return ret, None
