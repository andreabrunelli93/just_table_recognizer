import json
import os
import io
import random
from PIL import Image
import pandas as pd 

# import libraries
import streamlit as st

from functions import format_bounding_region, format_polygon, dict_to_df, analyze_general_documents
st.image("https://upload.wikimedia.org/wikipedia/commons/f/f0/Logo_Just.svg", width=150)
st.title('Just Table Recognizer')

image = st.file_uploader("Fotografa la tabella desiderata")

if image:
    url = "test_images\-1421603094_20191015_134815_3470632_resized_storto.jpg"
    result = analyze_general_documents(image)
    # convert the received model to a dictionary
    analyze_result_dict = result.to_dict()
    df = dict_to_df(analyze_result_dict)

    st.write(df)