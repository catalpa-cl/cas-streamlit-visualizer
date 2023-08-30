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

    with open('data/TypeSystem.xml', 'rb') as f:
        typesys = load_typesystem(f)

    with open('data/hagen.txt.xmi', 'rb') as f:
        cas = load_cas_from_xmi(f, typesystem=typesys)

    # --------------------------------------------------------------

    assignColors_and_multiselect(cas, pathPos, highlightVal)


# quick method to wrap the html part around a token (assign background color)
# can be modified like normal HTML
def addAnnotationVisHTML(text, color):
    if color is not 'noColor':
        return "<span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + \
            str(color) + "\">" + str(text) + "</span> "
    else:
        return text + ' '


# color matching and multiselect
def assignColors_and_multiselect(cas, typeFeaturePath):


    #testPathPos = "de.tudarmstadt.ukp.dkpro.core.api.lexmorph.type.pos.POS/coarseValue"
    
    typeFeaturePathList = []
    if isinstance(typeFeaturePath, str):
        typeFeaturePathList = [typeFeaturePath]
    else:
        typeFeaturePathList = typeFeaturePath


    allTypes = []
    unsortedAnnos = []
    fixbugwithdoublespellerrors = []
    for typeFeature in typeFeaturePathList:
        split = typeFeature.split('/')
        typePath = split[0]
        featPath = split[1]


        for item in cas.select(typePath):
        # get info from cas
        # spell-mis version
        #annoobject = AnnoObject(item.begin, item.end, item.name, item.get_covered_text())
            annoobject = AnnoObject(item.begin, item.end, getattr(item, featPath), item.get_covered_text())
            if item.begin not in fixbugwithdoublespellerrors:
                unsortedAnnos.append(annoobject)
                fixbugwithdoublespellerrors.append(item.begin)


        # get all possible Types
            if getattr(item, featPath) not in allTypes:
                allTypes.append(getattr(item, featPath))

    sortedAnnos = sorted(unsortedAnnos, key=lambda x: x.anno_begin, reverse=False)



    # currently configured to show all types at visualization time (TODO: make configurable)
    selectedTypes = st.multiselect("Select Type: ", allTypes, allTypes)

    color_scheme1 = ["skyblue", "orangered", "orange", "plum", "palegreen", "mediumseagreen", "lightseagreen",
                     "steelblue", "navajowhite", "mediumpurple", "rosybrown", "silver", "gray",
                     "paleturquoise", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue"]

    colorMapping = {}  # for the type-color display above the text

    # assign each type a unique color
    for my_type in allTypes:
        colorMapping[my_type] = color_scheme1[allTypes.index(my_type)]

    cas_text = cas.sofa_string
    #print(cas_text.find('\n'))
    #print(cas_text[140:160])
    new_text = cas_text.replace('\n', '  \n')
    #st.write(new_text)
    #print(new_text)
    #st.write('lululu  \nhshshshshshsh')


    output_string = ''
    current_offset = 0

    #create legend
    legend = ''
    #st.write(selectedTypes)
    for type in selectedTypes:
        legend = legend + addAnnotationVisHTML(type, colorMapping[type])
    # typ und feature
    # TODO parameter for type and feature
    # TODO fix whitespaces and punctuation
    # big TODO : make everything offset based!

#------------OFFSET--------------------------------------------------------------------------
    revSortAnnos = sorted(sortedAnnos, key=lambda x: x.anno_begin, reverse=True)
    #st.write(revSortAnnos)
    textToPrint = cas_text

    for anno in revSortAnnos:
        if anno.anno_type in selectedTypes:
            htmlend = "</span> "
            htmlstart = "<span style=\"border-radius: 25px; padding-left:8px; padding-right:8px; background-color: " + \
                        str(colorMapping[anno.anno_type]) + "\">"

            textToPrint = textToPrint[:anno.anno_end] + htmlend + textToPrint[anno.anno_end:]
            textToPrint = textToPrint[:anno.anno_begin] + htmlstart + textToPrint[anno.anno_begin:]


    #print(textToPrint)
    textToPrint = textToPrint.replace('\n', '  \n')
    #st.write(textToPrint, unsafe_allow_html=True)


    #------------OFFSET-END----------------------------------------------------------------------

    output_array = []
    output_array.append(legend)
    output_array.append(textToPrint)

    return output_array

    

def save_image(output_array, file_name):

    css = 'style.css'
    output_array[1] = output_array[1].replace('  \n', '<br><br>')

    html_string = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><br>' + output_array[0] + '<br><br><hr><br>' \
                  + output_array[1] + '</body></html>'
    html_file = open("test.html", "w")
    html_file.write(html_string)
    html_file.close()
    final_name = 'AD_marked/' + file_name + 'new.svg'
    #print(html_string)
    imgkit.from_file('test.html', final_name, css=css)

visualize_cas_span()
