from config import get_dataset_config as config
import os
import glob
from zipfile import ZipFile
import re
import shutil

# Retrieve datasets
datasets_path = config.DATASETS_PATH

datasets_list = glob.glob(os.path.sep.join([datasets_path, "*.zip"]))

# Unzip datasets in directory
for dataset in datasets_list:
    # Read zipped directory
    zip_data = ZipFile(dataset, 'r')

    # Get directory name for extraction
    dataset_dir = dataset.split('.zip')[0]

    # Extract files
    zip_data.extractall(dataset_dir)
    zip_data.close()

    # If there is only one folder, move everything one folder up
    if len(os.listdir(dataset_dir)) == 1:
        # Read folders
        paths = []
        for (root, folder, files) in os.walk(dataset_dir):
            paths.append(root)
        # Move files
        for path in paths:
            # Create new folder
            new_path = path.replace('/' + os.path.basename(dataset_dir), '')
            os.makedirs(new_path, exist_ok=True)
            # Move files
            for files in glob.glob(path + "/*.*"):
                if len(files) > 0:
                    for file in [files]:
                        shutil.move(file,
                                    file.replace('/' + os.path.basename(dataset_dir), ''))
        # Drop previous tree
        shutil.rmtree(dataset_dir)

    # Remove the zip file
    os.remove(dataset)
