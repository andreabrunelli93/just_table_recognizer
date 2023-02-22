
import json
import os
import io
import random
from PIL import Image
import pandas as pd 

# import libraries
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.core.serialization import AzureJSONEncoder

# set `<your-endpoint>` and `<your-key>` variables with the values from the Azure portal
endpoint = "https://formrecognizerjustpoc.cognitiveservices.azure.com/"
key = "9f18515bc1524499aa0fc4b382073ce0"

def format_bounding_region(bounding_regions):
    if not bounding_regions:
        return "N/A"
    return ", ".join("Page #{}: {}".format(region.page_number, format_polygon(region.polygon)) for region in bounding_regions)

def format_polygon(polygon):
    if not polygon:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in polygon])

def convert_pil_image_to_byte_array(img):
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='JPEG', subsampling=0, quality=100)
    img_byte_array = img_byte_array.getvalue()
    return img_byte_array

def image_compression (img):
    image = Image.open(img)

    height, width = image.size
    
    if width > 2000:
        image = image.resize((height//4 ,width//4), Image.ANTIALIAS)
        height, width = image.size
        
    if width > 1000:
        image = image.resize((height//2 ,width//2), Image.ANTIALIAS)
        height, width = image.size

    return image

def analyze_general_documents(url):
    # sample document

    url = image_compression(url)

    document = convert_pil_image_to_byte_array(url)

    # create your `DocumentAnalysisClient` instance and `AzureKeyCredential` variable
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    
    poller = document_analysis_client.begin_analyze_document("justpod_v2", document=document)
    result = poller.result()

    return result

def dict_to_df(result_dict):

  row_list = []
  def_list = []
  header = ['cod', 'prodotto', 'capacita', 'Pz.', 'prezzo', 'importo']

  tabs = ['tab_1', 'tab_2']
  
  for tab in tabs:
    for elem_1 in result_dict['documents'][0]['fields'][tab]['value']:
      for col in header:
        row_list.append(elem_1['value'][col]['content'])
      
      def_list.append(row_list)
      row_list = [] 

  df = pd.DataFrame(def_list)
  df.columns = header

  return df