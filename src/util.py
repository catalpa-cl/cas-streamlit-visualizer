import cassis
from pathlib import Path
import typing

def identity(x):
    return x


def map_from_type(x, type_to_mapper: dict):
    T = type(x)
    mapping_fn = type_to_mapper.get(T)

    if mapping_fn is None:
        raise ValueError

    return mapping_fn(x)


def cas_from_string(cas: str, typesystem: typing.Union[cassis.TypeSystem, str]):
    ts_typemap = {
        str: cassis.load_typesystem,
        cassis.TypeSystem: identity
    }
    typesystem = map_from_type(typesystem, ts_typemap)

    for loading_fn in (cassis.load_cas_from_xmi, cassis.load_cas_from_json):
        try:
            return loading_fn(cas, typesystem)
        except IOError:
            continue

    raise ValueError('Provided "cas" does not correspond to a supported input.')