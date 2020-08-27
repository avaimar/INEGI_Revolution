from typing import Dict, List, Any
from config import get_dataset_config as config
from utils.pdf_reader import PdfExtractVariables
import os
import glob
import json

# Retrieve datasets
print("Retrieving datasets...")
datasets_path = config.DATASETS_PATH

datasets_list = os.scandir(datasets_path)
datasets_list = [data.path for data in datasets_list if data.is_dir()]

# Instantiate dictionary
dictionary: Dict[Any, Dict[Any, List[Any]]] = {}

# Get variables
print("Extracting variables from datatables...")
for data in datasets_list:
    print("Pdf: {}".format(data))
    # Get pdf of variables
    variables_pdf = glob.glob(os.path.sep.join([data, 'Descripcion_Archivos', '*.pdf']))[0]

    # Extract pdf information
    variables_pdf = PdfExtractVariables(variables_pdf)

    # Get databases and descriptions
    databases_list, databases_descriptions = variables_pdf.get_databases_list()

    # Get dictionary
    database_dict = variables_pdf.get_databases(databases_list, databases_descriptions)

    # Convert tables obtained in dictionary from df to json in order to serialize
    for (data_name, (data_desc, data_table)) in database_dict.items():
        table = data_table.copy()
        table.reset_index(inplace=True, drop=True)
        table = table.rename(columns=table.iloc[0]).drop(table.index[0])
        table.reset_index(inplace=True, drop=True)
        database_dict[data_name][1] = table.to_json()

    # Append to overall dictionary
    dictionary[data] = database_dict

# Save dictionary as json file
print("Loading extracted variables to json dictionary...")
output_path = config.VARIABLE_DICTIONARIES_PATH
with open(os.sep.join([output_path, 'dictionary.json']), 'w') as file:
    json.dump(dictionary, file, sort_keys=False)
