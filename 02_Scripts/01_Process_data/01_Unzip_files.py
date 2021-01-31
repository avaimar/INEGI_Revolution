from config import get_dataset_config as config
import os
import glob
from zipfile import ZipFile

# Retrieve datasets
datasets_path = config.DATASETS_PATH

datasets_list = glob.glob(os.path.sep.join([datasets_path, "*.zip"]))

# Unzip datasets in directory
for dataset in datasets_list:
    # Read zipped directory
    zip_data = ZipFile(dataset, 'r')

    # Get directory name for extraction
    dataset_dir = dataset.split('.zip')[0]

    # TODO Add "if" in case there is only one folder
        # I have done nothing

    # Extract files
    zip_data.extractall(dataset_dir)
    zip_data.close()

    # Remove the zip file
    os.remove(dataset)
