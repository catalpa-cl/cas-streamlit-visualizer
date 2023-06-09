import numpy as np
import pandas as pd
import streamlit as st
from cassis import *
from operator import itemgetter

# st.set_page_config(layout="wide")
st.title("CAS Visualizer")



# -----------------------------------------------------------------------------------------
# parameters:
# needed:-------
# cas, typesystem, featurepath + value
# optional:-----
# colorscheme

# -----------------------------------------------------------------------------------------

class AnnoObject:
    def __init__(self, anno_begin, anno_end, anno_type, anno_text):
        self.anno_begin = anno_begin
        self.anno_end = anno_end
        self.anno_type = anno_type
        self.anno_text = anno_text

# -----------------------------------------------------------------------------------------


# span
def visualize_cas_span():
    # --------------------------------------------------------------
    # static stuff, not needed for every cas but for the example cas,
    # was formerly a parameter, but for this showcase its hardwired
    pathSen = "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Sentence"
    pathTok = "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token"
    pathPos = "de.tudarmstadt.ukp.dkpro.core.api.lexmorph.type.pos.POS"
    pathFreq = "org.lift.type.Frequency"
    highlightVal = "coarseValue" #

    with open('TypeSystem.xml', 'rb') as f:
        typesys = load_typesystem(f)

    with open('hagen.txt.xmi', 'rb') as f:
        cas = load_cas_from_xmi(f, typesystem=typesys)

    # --------------------------------------------------------------

    assignColors_and_multiselect(cas, pathPos, highlightVal)


# quick method to wrap the html part around a token (assign background color)
# can be modified like normal HTML
def addAnnotationVisHTML(text, color):
    return "<span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + \
           str(color) + "\">" + str(text) + "</span> "


# color matching and multiselect
def assignColors_and_multiselect(cas, featurePath, highlightValue):

    allTypes = []
    unsortedAnnos = []
    #featurePath = "de.tudarmstadt.ukp.dkpro.core.api.lexmorph.type.pos.POS"
    for item in cas.select(featurePath):
        # get info from cas
        annoobject = AnnoObject(item.begin, item.end, item.coarseValue, item.get_covered_text())
        unsortedAnnos.append(annoobject)

        # get all possible Types
        if item.coarseValue not in allTypes:
            allTypes.append(item.coarseValue)

    sortedAnnos = sorted(unsortedAnnos, key=lambda x: x.anno_begin, reverse=False)

    # currently configured to show all types at visualization time (TODO: make configurable)
    currentTypes = st.multiselect("Select Type: ", allTypes, allTypes)

    color_scheme1 = ["orangered", "orange", "plum", "palegreen", "mediumseagreen", "lightseagreen",
                     "steelblue", "skyblue", "navajowhite", "mediumpurple", "rosybrown", "silver", "gray",
                     "paleturquoise"]

    colorMapping = {}  # for the type-color display above the text

    # assign each type a unique color
    for my_type in allTypes:
        colorMapping[my_type] = color_scheme1[allTypes.index(my_type)]

    cas_text = cas.sofa_string
    output_string = ''
    current_offset = 0

    # typ und feature, zb pos u coarsevalue
    # TODO typepicking in multiselect
    # TODO parameter for type and feature

    for anno in sortedAnnos:

        output_string = output_string + cas_text[current_offset:anno.anno_begin]
        current_offset = current_offset + anno.anno_end
        output_string = output_string + addAnnotationVisHTML(anno.anno_text, colorMapping[anno.anno_type])

    # tail end des Textes hinzufügen
    if current_offset < len(cas_text):
        output_string = output_string + cas_text[:]  # slice

    # sounds dangerous, but it works ;)
    # and is commonly used in other streamlit components to mess around with texts
    # st.write(legend, unsafe_allow_html=True)
    st.write("---------------------")
    st.write(output_string, unsafe_allow_html=True)

# ---------------------------------------------------------------------------------------------------------------------
visualize_cas_span()
