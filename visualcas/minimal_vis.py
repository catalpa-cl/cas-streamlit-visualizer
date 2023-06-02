import numpy as np
import pandas as pd
import streamlit as st
from cassis import *
from operator import itemgetter

# st.set_page_config(layout="wide")
st.title("CAS Visualizer")

# -----------------------------------------------------------------------------------------



# -----------------------------------------------------------------------------------------
# load and read the cas + typesystem, create a list representation for further processing
def cas_read_preprocessing():

    # --------------------------------------------------------------
    # static stuff, not needed for every cas but for the example cas,
    # was formerly a parameter, but for this showcase its hardwired
    pathSen = "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Sentence"
    pathTok = "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token"
    pathPos = "de.tudarmstadt.ukp.dkpro.core.api.lexmorph.type.pos.POS"
    pathFreq = "org.lift.type.Frequency"

    with open('data/TypeSystem.xml', 'rb') as f:
        typesys = load_typesystem(f)

    with open('data/hagen.txt.xmi', 'rb') as f:
        cas = load_cas_from_xmi(f, typesystem=typesys)

    # --------------------------------------------------------------



    possibleTypes = ["noType"]
    tokenText = []
    tokenType = []
    tokenBegin = []
    toBeSorted = []
    allToken = []


    for sentence in cas.select(pathSen):  # sentence

        for t in cas.select_covered(pathTok, sentence):
            allToken.append([t.begin, t.get_covered_text(), "noType"])

        for token in cas.select_covered(pathPos, sentence):
            if token.coarseValue not in possibleTypes:
                possibleTypes.append(token.coarseValue)
            toBeSorted.append([token.begin, token.get_covered_text(), token.coarseValue])
            sortedArray = sorted(toBeSorted, key=itemgetter(0))

        for tokA in allToken:
            for tokB in sortedArray:
                if tokA[0] == tokB[0]:
                    tokA[2] = tokB[2]

    for sortedItem in allToken:
        tokenBegin.append(sortedItem[0])
        tokenText.append(sortedItem[1])
        tokenType.append(sortedItem[2])

    for word in tokenText:
        sofaString = sofaString + word + " "
    return possibleTypes, allToken

# -----------------------------------------------------------------------------------------
# span
def visualize_cas_span():
    typeArray, sortedArray, sofaString = cas_read_preprocessing()
    assignColors_and_multiselect(typeArray, sortedArray, sofaString)


# quick method to wrap the html part around a token (assign background color)
# can be modified like normal HTML
def addAnnotationVisHTML(text, color):
    return "<span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + \
           str(color) + "\">" + str(text) + "</span> "


# color matching and multiselect
def assignColors_and_multiselect(cas, types, tokens):
    
    # currently configured to show all types at visualization time (TODO: make configurable)
    currentType = st.multiselect("Select Type: ", types, types)

    color_scheme1 = ["orangered", "orange", "plum", "palegreen", "mediumseagreen", "lightseagreen",
                       "steelblue", "skyblue", "navajowhite", "mediumpurple", "rosybrown", "silver", "gray",
                       "paleturquoise"]

    colorMapping = {}  # for the type-color display above the text

    # assign each type a unique color
    for my_type in types:
        colorMapping.append([my_type, color_scheme1[my_type.index(types)]])

    cas_text = cas.sofa_string()   #??
    output_string = ''
    current_offset = 0
    for item in cas.select(featurePath):
        anno, value = item
        output_string = output_string + cas_text[current_offset, anno.begin]
        current_offset = current_offset + anno.end
        output_string = output_string + addAnnotationVisHTML(anno.coveredText, colorMapping(value))

    # tail end des Textes hinzufügen
    if current_offset < cas_text.len():
        output_string = output_string + cas_text[:] # slice


    # sounds dangerous, but it works ;)
    # and is commonly used in other streamlit components to mess around with texts
    st.write(legend, unsafe_allow_html=True)
    st.write("---------------------")
    st.write(output_string, unsafe_allow_html=True)

visualize_cas_span()
