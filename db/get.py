import typing as ty

from .. import typs, exceptions

from . import execute

def empresa_by_insc_esocial(conn: typs.ConnTy,
                            tp_insc: typs.esocial.TipoInscricao,
                            insc: str) -> typs.MayErrTy[typs.DictTy[ty.Any]]:
    err: ty.Optional[Exception]
    query: str = '''
SELECT *
FROM ns.empresas AS emp
    '''
    params: typs.DictTy[ty.Any] = {
        'insc': insc
    }

    if tp_insc is typs.esocial.TipoInscricao.PF:
        query += 'WHERE emp.tipoidentificacao = ' \
                + str(typs.erp.TipoInscricao.PF.value) + '\n'
        query += '  AND emp.cpf = %(insc)s\n'
    elif tp_insc is typs.esocial.TipoInscricao.PJ:
        query += 'WHERE emp.tipoidentificacao = ' \
                + str(typs.erp.TipoInscricao.PJ.value) + '\n'

        if len(insc) == 14:
            query += '  AND CONCAT(emp.raizcnpj, emp.ordemcnpj) = %(insc)s\n'
        elif len(insc) == 8:
            query += '  AND emp.raizcnpj = %(insc)s\n'
        else:
            return {}, exceptions.InvalidParameterError(
                f"CNPJ '{insc}' invalido"
            )
    else:
        _ = params.pop('insc')
        pass

    query += 'LIMIT 1;'

    res: ty.Dict[str, ty.Any]
    res, err = execute.fetchone(conn, query, params)

    if isinstance(err, exceptions.EmptyResultError):
        return {}, exceptions.NotFoundError(
            f"Empresa com inscrição '{insc}' não achada."
        )

    return res, err
