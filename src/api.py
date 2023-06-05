import typing
from pathlib import Path

import cassis
import src.util as util

from src.visualisation import TableVisualiser, VisualisationConfig


def highlight(cas: typing.Union[cassis.Cas, str, Path],
              typesystem: typing.Union[cassis.TypeSystem, str, Path],
              config: typing.Iterable[typing.Union[str, dict, VisualisationConfig]],
              context=None):
    raise NotImplementedError


def table(cas: typing.Union[cassis.Cas, str, Path],
          typesystem: typing.Union[cassis.TypeSystem, str, Path],
          config: typing.Iterable[typing.Union[str, dict, VisualisationConfig]],
          context=None):
    # TODO: Resolve CAS, Typesystem and Config automatically
    cas = util.load_cas(cas, typesystem)
    visualiser = TableVisualiser(cas, config)
    return visualiser(context)

