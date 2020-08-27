from config import get_dataset_config as config
import json
import os
import pandas as pd
import numpy as np

# Boolean: Do you wish to write tables as csv?
write_csv = True

# Get json dictionary input/output path
input_path = config.VARIABLE_DICTIONARIES_PATH
output_path = config.VARIABLE_DICTIONARIES_PATH

# Load json dictionary with extracted variables
print("Loading extracted variable dictionary...")
with open(os.sep.join([input_path, 'dictionary.json']), 'r') as file:
    dictionary = json.load(file)

# Loop over each element in the dictionary in order to clean variable data tables
for (database_name, database_content) in dictionary.items():
    print("Cleaning database {}...".format(database_name))

    # Loop over each data table in the database
    for (datatable_name, (datatable_desc, datatable_table)) in database_content.items():
        # Clean new lines in description
        dictionary[database_name][datatable_name][0] = datatable_desc.replace('\n', ' ')

        # Fix newline character
        table = pd.read_json(datatable_table)
        table = table.replace('\n', ' ', regex=True)
        table.columns = table.columns.str.replace('\n', '', regex=True)

        # Print table columns for user to identify any outliers
        print("Table columns: {}".format(table.columns))

        # Case 1. Num de Campo is empty. This means the row's
        # information stems from the previous row and rows should be combined.
        if 'Núm.de campo' in table.columns:
            table['Núm.de campo'] = table['Núm.de campo'].replace(r'^\s*$', np.nan, regex=True)
            if table['Núm.de campo'].isna().sum() > 0:
                print("Combining rows based on empty Núm.de campo column...")
                # We start by padding Num. de campo so that we can perform a group by.
                table[['Núm.de campo']] = table[['Núm.de campo']].fillna(method='pad')

                # Group by Num. de campo and concatenate rows
                columns_to_join = list(table.columns)
                columns_to_join.remove('Núm.de campo')
                table = table.groupby('Núm.de campo')[columns_to_join].agg(' '.join).reset_index()

        # Identify NAs for remaining columns
        table = table.replace(r'^\s*$', np.nan, regex=True)

        # Case 2. 'Origen', 'Descripcion' empty. This means the row is a new variable but
        # from the same family as the previous rows. Origin and description must be copied.
        if 'Origen' in table.columns or 'Descripcion' in table.columns:
            if table['Origen'].isna().sum() > 0 or table['Descripcion'].isna().sum() > 0:
                print("Padding NAs from 'Origen' and 'Descripcion' columns...")
                table[['Origen', 'Descripcion']] = table[['Origen', 'Descripcion']].fillna(method='pad')

        # Write as csv if selected
        if write_csv:
            file_path = os.sep.join([output_path, 'clean_variable_csv_tables',
                                     database_name.split(os.path.sep)[-1]])
            if not os.path.exists(file_path):
                os.mkdir(file_path)
            table.to_csv(os.sep.join([file_path, '{}.csv'.format(datatable_name)]), index=False)

        # Rewrite as json in order to serialize
        table = table.to_json()

        # Replace corrected table back in dictionary
        dictionary[database_name][datatable_name][1] = table

# Save json dictionary
print("Saving clean extracted variables to json dictionary...")
with open(os.sep.join([output_path, 'dictionary_clean.json']), 'w') as file:
    json.dump(dictionary, file, sort_keys=False)
