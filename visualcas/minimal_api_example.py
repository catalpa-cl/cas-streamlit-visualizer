from cassis import load_typesystem, load_cas_from_xmi
import streamlit as st
import pathlib
import sys

p = pathlib.Path(__file__).absolute()/ '..' /'src'
sys.path.extend(str(p))

import src as cas_vis

cas = 'data/hagen.txt.xmi'
ts = 'data/TypeSystem.xml'

cfg = cas_vis.visualisation.VisualisationConfig.from_string('de.tudarmstadt.ukp.dkpro.core.api.lexmorph.type.pos.POS/PosValue')

st.write('## Rendering in a container')
container = st.container()
cas_vis.table(cas, ts, [cfg], container)

st.write('## Rendering on the spot')
cas_vis.table(cas, ts, [cfg])