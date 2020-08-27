from config import get_dataset_config as config
import json
import os
from dbfread import DBF
import pandas as pd
import numpy as np

# Get json dictionary input/output path
input_path = config.VARIABLE_DICTIONARIES_PATH
# output_path = config.VARIABLE_DICTIONARIES_PATH

# Load json dictionary with extracted variables
print("Loading extracted variable dictionary...")
with open(os.sep.join([input_path, 'dictionary_clean.json']), 'r') as file:
    dictionary = json.load(file)

# Loop over each element in the dictionary in order to clean variable data tables
for (database_name, database_content) in dictionary.items():
    print("Cleaning database {}...".format(database_name))

    # Loop over each data table in the database
    for (datatable_name, (datatable_desc, datatable_table)) in database_content.items():
        # TODO
        # Get dbf
        # table = DBF(os.sep.join([data_path, 'AYUNTAMI.DBF']))
        # Get df
        # table = pd.DataFrame(iter(table))
        pass


data_path = '..\\..\\01_Data\\01_Raw_Data\\CNGMDT\\2019\\2_Integrantes_ayuntami_cngmd2019_dbf\\Bases_Datos'
table = DBF(os.sep.join([data_path, 'COMISION.DBF']))
table = pd.DataFrame(iter(table))