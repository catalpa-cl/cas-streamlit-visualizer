import typing
import dataclasses
import cassis
from pathlib import Path
import abc
import util
import copy


@dataclasses.dataclass
class ColourConfig:
    cmap: str = 'Set1'
    vmap: dict = None
    data_type: str = 'nominal'

    # TODO: write proper implementation
    @classmethod
    def from_any(cls, config):
        return cls()


@dataclasses.dataclass
class VisualisationConfig:
    annotation: str
    colour: ColourConfig
    tooltip: str = None
    subscript: str = None

    @classmethod
    def from_any(cls, config):
        type_dict = {
            cls: cls.from_config,
            str: cls.from_string,
            dict: cls.from_dict
        }
        return util.map_from_type(config, type_dict)

    @classmethod
    def from_config(cls, config):
        return copy.deepcopy(config)

    @classmethod
    def from_dict(cls, config: dict):
        return cls(
            config['annotation'],
            ColourConfig.from_any(config['colour']),
            config.get('tooltip'),
            config.get('subscript')
        )

    @classmethod
    def from_string(cls, annotation: str):
        return cls(
            annotation,
            ColourConfig()
        )


# TODO: Concrete versions to be implemented: TableVisualiser and HighlightedTextVisualiser
class Visualiser(abc.ABC):
    def __init__(
            self,
            cas: cassis.Cas,
            typesystem: cassis.TypeSystem,
            visualisation_configs: typing.Iterable[VisualisationConfig] = None
    ):
        self.cas = cas
        self.typesystem = typesystem
        self.visualisation_configs = visualisation_configs if visualisation_configs is not None else []

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


def highlight(cas: typing.Union[cassis.Cas, str, Path],
              typesystem: typing.Union[cassis.TypeSystem, str, Path],
              config: typing.Iterable[typing.Union[str, dict, VisualisationConfig]]):
    raise NotImplementedError


def table(cas: typing.Union[cassis.Cas, str, Path],
          typesystem: typing.Union[cassis.TypeSystem, str, Path],
          config: typing.Iterable[typing.Union[str, dict, VisualisationConfig]]):
    raise NotImplementedError


