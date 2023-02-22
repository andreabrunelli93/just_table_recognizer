import json
import os
import io
import random
from PIL import Image
import pandas as pd 

# import libraries
import os
import streamlit as st
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.core.serialization import AzureJSONEncoder

from functions import format_bounding_region, format_polygon, dict_to_df, analyze_general_documents

st.title('Just Table Recognizer')

url = "test_images\-1421603094_20191015_134815_3470632_resized_storto.jpg"
result = analyze_general_documents(url)

# convert the received model to a dictionary
analyze_result_dict = result.to_dict()
df = dict_to_df(analyze_result_dict)
df

st.write(df)