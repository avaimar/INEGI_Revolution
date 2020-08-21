from typing import Dict, List, Any

from config import get_dataset_config as config
from utils.pdf_reader import PdfExtractVariables
import os
import glob
import json

# Retrieve datasets
datasets_path = config.DATASETS_PATH

datasets_list = os.scandir(datasets_path)
datasets_list = [data.path for data in datasets_list if data.is_dir()]

# Instantiate dictionary
dictionary: Dict[Any, Dict[Any, List[Any]]] = {}

# Get variables
for data in datasets_list:
    # Get pdf of variables
    variables_pdf = glob.glob(os.path.sep.join([data, 'Descripcion_Archivos', '*.pdf']))[0]

    # Extract pdf information
    variables_pdf = PdfExtractVariables(variables_pdf)

    # Get databases and descriptions
    databases_list, databases_descriptions = variables_pdf.get_databases_list()

    # Get dictionary
    database_dict = variables_pdf.get_databases(databases_list, databases_descriptions)

    # Append to overall dictionary
    dictionary[data] = database_dict

# Save dictionary as json file
output_path = config.VARIABLE_DICTIONARIES_PATH
json.dump(dictionary, os.sep.join([output_path, 'dictionary.json']), sort_keys=False)