import numpy as np
import pandas as pd
import streamlit as st
from cassis import *
from operator import itemgetter

# st.set_page_config(layout="wide")
st.title("CAS Visualizer")


# -----------------------------------------------------------------------------------------

class AnnoObject:
    def __init__(self, anno_begin, anno_end, anno_type, anno_text):
        self.anno_begin = anno_begin
        self.anno_end = anno_end
        self.anno_type = anno_type
        self.anno_text = anno_text


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

    sofaString = ""
    for word in tokenText:
        sofaString = sofaString + word + " "

    #st.write(possibleTypes)
    #st.write(allToken)
    return cas, possibleTypes, allToken


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
    currentTypes = st.multiselect("Select Type: ", types, types)

    color_scheme1 = ["orangered", "orange", "plum", "palegreen", "mediumseagreen", "lightseagreen",
                     "steelblue", "skyblue", "navajowhite", "mediumpurple", "rosybrown", "silver", "gray",
                     "paleturquoise"]

    colorMapping = {}  # for the type-color display above the text

    # assign each type a unique color
    for my_type in types:
        # st.write(types.index(my_type))
        # colorMapping.append([my_type, color_scheme1[types.index(my_type)]])
        # if my_type is not None:
        colorMapping[my_type] = color_scheme1[types.index(my_type)]
        # else:
        #   colorMapping['noType'] = color_scheme1[types.index(my_type)]

    # casss = cas.sofa_string
    #st.write(colorMapping)
    cas_text = cas.sofa_string
    output_string = ''
    current_offset = 0

    featurePath = "de.tudarmstadt.ukp.dkpro.core.api.lexmorph.type.pos.POS"

    # typ und feature, zb pos u coarsevalue
    # TODO typepicking in multiselect
    # TODO parameter for type and feature


    unsortedAnnos = []
    for item in cas.select(featurePath):
        annoobject = AnnoObject(item.begin, item.end, item.coarseValue, item.get_covered_text())
        unsortedAnnos.append(annoobject)

    sortedAnnos = sorted(unsortedAnnos, key=lambda x: x.anno_begin, reverse=False)

    for anno in sortedAnnos:

        output_string = output_string + cas_text[current_offset:anno.anno_begin]
        current_offset = current_offset + anno.anno_end
        output_string = output_string + addAnnotationVisHTML(anno.anno_text, colorMapping[anno.anno_type])

    #for item in cas.select(featurePath):
        # st.write(item)
        # anno, value = item
        #anno_type = str(item.coarseValue)
        #anno_begin = int(item.begin)
        #anno_end = int(item.end)
        #text_value = str(item.get_covered_text())
        # st.write(anno_begin)
        # st.write(anno_end)
        # st.write(anno_type)
        # st.write(text_value)


        #output_string = output_string + cas_text[current_offset:anno_begin]
        #current_offset = current_offset + anno_end
        # output_string = output_string + addAnnotationVisHTML(text_value, colorMapping[anno_type])

    # tail end des Textes hinzufügen
    if current_offset < len(cas_text):
        output_string = output_string + cas_text[:]  # slice

    # sounds dangerous, but it works ;)
    # and is commonly used in other streamlit components to mess around with texts
    # st.write(legend, unsafe_allow_html=True)
    st.write("---------------------")
    st.write(output_string, unsafe_allow_html=True)


visualize_cas_span()
