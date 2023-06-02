import cas_vis
from dataclasses import dataclass

####### HIGH LEVEL API ######

###
# Basic Usage: Single CAS
###
# Option 1: CAS first
visualiser = cas_vis('path/to/cas1', 'path/to/typesystem1')
visualiser.highlight(...)

visualiser_2 = cas_vis('path/to/cas2', 'path/to/typesystem2')
visualiser_2.highlight(...)

# Option 2: Visualisation first
visualiser = cas_vis.highlight(**config)
visualiser.show('path/to/cas1', 'path/to/typesystem1')
visualiser.show('path/to/cas2', 'path/to/typesystem2')

# WINNER!!!🥳 Option 3: Equal terms
config = {
    'features': [...],
    'other_stuff': ...
}

my_cas = ... # CAS object from cassis
my_typesystem = ... # Typesystem object from cassis

vis1 = cas_vis.highlight('path/to/cas1', 'path/to/typesystem1', **config)
vis2 = cas_vis.highlight(my_cas, my_typesystem, **config)

my_stuff = [
    ('path/to/cas', 'path/to/typesystem'),
    (my_cas, my_typesystem),
    ('path/to/other/cas', my_typesystem)
]

for cas, ts in my_stuff:
    cas_vis.highlight(cas, ts, **config)

###
# Visualisation Types
###

cas_vis.table(my_cas, my_typesystem, ...)
cas_vis.highlight(my_cas, my_typesystem, ...)
cas_vis.tree(my_cas, my_typesystem, ...)

###
# Configuration
###

# Option 1: explicit configuration
cas_vis.highlight('path/to/cas1', 'path/to/typesystem1',
                  NAME_OF_WHATEVER_THESE_ARE=[
                      { 'type_name': 'POS', 'color_map': ... }, # Dictionary
                      VisualisationConfig('Frequency', cmap=...), # ConfigurationObject
                      'org.tudarmstadt.segmentation.Token' # Just Type Name
                  ])


VisualisationConfig(
    'something.something.POS/posValue',
    colour=ColourConfig(
        cmap='summer',
        vmap={
            'NN': '#ffffff',
            'ADJ': 'RGB(128, 64, 32)',
            'V': COLOUR.RED
        },
        type='nominal'
    ),
    tooltip=None,
    subscript=lambda anno: anno.name,
)

VisualisationConfig(
    'something.something.Frequency/value',
    colour=...
)

VisualisationConfig(
    'something.something.Difficulty/value',
    cmap='viridis',
    type='ordinal',
    valuemap={'F': 0, 'D': 1, 'C': 2}
)

#@dataclass
#class VisualisationConfig:


###
# Comparison
###

visualisations = [vis1, vis2, ...]
cas_vis.side_by_side(*visualisations)
vas_vis.grid(*visualisations)