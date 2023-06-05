import abc
import copy
import dataclasses
import functools
import typing

import cassis
import numpy as np
import pandas as pd
import streamlit as st

import src.util as util


@dataclasses.dataclass
class ColourConfig:
    cmap: str = 'Set1'
    vmap: dict = None
    data_type: str = 'nominal'

    # TODO: write proper implementation
    @classmethod
    def from_any(cls, config):
        return cls()


class VisualisationConfig:
    def __init__(self,
                 annotation: str,
                 colour: ColourConfig,
                 tooltip: str = None,
                 subscript: str = None
    ):
        self.annotation = annotation
        self.colour = colour
        self.tooltip = tooltip
        self.subscript = subscript
        type_path, feature_path = util.resolve_annotation(annotation)
        self.type_path = type_path
        self.feature_path = feature_path

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

class Visualiser(abc.ABC):
    def __init__(
            self,
            cas: cassis.Cas,
            visualisation_configs: typing.Iterable[VisualisationConfig] = None
    ):
        self.cas = cas
        self.visualisation_configs = visualisation_configs if visualisation_configs is not None else []

    def __call__(self, streamlit_context=None, *args, **kwargs):
        self.visualise(streamlit_context)

    @functools.cached_property
    def _entities(self):
        """Returns all entities to be visualised."""
        entities = []
        for cfg in self.visualisation_configs:
            entities.append(list(self.cas.select(cfg.type_path)))
        return entities

    @functools.cached_property
    def _entity_values(self):
        """Returns unique entity values to be used for visualisation."""
        entities = self._entities
        values = []
        for entity_list, cfg in zip(entities, self.visualisation_configs):
            vs = [entity.get(cfg.feature_path) for entity in entity_list]
            values.append(np.unique(vs).tolist())
        return values

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


class TableVisualiser(Visualiser):
    def render_visualisation(self):
        records = []
        for entity_list, cfg in zip(self._entities, self.visualisation_configs):
            for entity in entity_list:
                records.append({
                    'text': entity.get_covered_text(),
                    'feature': cfg.feature_path,
                    'value': entity.get(cfg.feature_path),
                    'begin': entity.begin,
                    'end': entity.end,
                })

        df = pd.DataFrame.from_records(records).sort_values(by=['begin', 'end'])
        return st.table(df)

