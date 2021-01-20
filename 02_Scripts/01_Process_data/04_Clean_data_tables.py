from config import get_dataset_config as config
import json
import os
import shapefile
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
        # Get table path
        path = os.sep.join([database_name, datatable_name, '.dbf'])

        # Get table
        sf = shapefile.Reader(path)
        table = pd.DataFrame(sf.records())
        # TODO clean

        pass
