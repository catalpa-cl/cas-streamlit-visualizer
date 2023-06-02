import typing
import dataclasses
import cassis
from pathlib import Path
import abc


@dataclasses.dataclass
class ColourConfig:
    cmap: str
    vmap: dict
    data_type: str


@dataclasses.dataclass
class VisualisationConfig:
    annotation: str
    colour: ColourConfig
    tooltip: str
    subscript: str


# TODO: Concrete versions to be implemented: TableVisualiser and HighlightedTextVisualiser
class Visualiser(abc.ABC):
    def __init__(
            self,
            cas: typing.Union[cassis.Cas, str, Path],
            typesystem: typing.Union[cassis.Cas, str, Path],
            visualisation_configs: typing.Iterable[typing.Union[str, dict, VisualisationConfig]] = None
    ):
        self.cas = cas
        self.typesystem = typesystem
        self.visualisation_configs = visualisation_configs

    def __call__(self, streamlit_context=None, *args, **kwargs):
        self.visualise(streamlit_context)

    def visualise(self, streamlit_context=None):
        """Generates the visualisation based on the provided configuration in the provided context.

        :arg streamlit_context: A streamlit context to render the visualisation in.
            Must implement the context provider protocol.
            If not provided, the global streamlit context should be used.
        """
        if streamlit_context is None: # render wherever the function is called in the global context.
            self.render_visualisation()
        else:
            with streamlit_context: # render within the given container
                self.render_visualisation()

    @abc.abstractmethod
    def render_visualisation(self):
        """Generates the visualisation based on the provided configuration."""
        raise NotImplementedError


def highlight(cas: typing.Union[cassis.Cas, str],
              typesystem: typing.Union[cassis.TypeSystem, str],
              config: typing.Iterable):
    raise NotImplementedError

def table(cas: cassis.Cas,
          typesystem: cassis.TypeSystem,
          config: typing.Iterable[VisualisationConfig]):
    raise NotImplementedError


