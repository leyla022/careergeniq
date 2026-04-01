import os
import zipfile
import shutil
from kaggle.api.kaggle_api_extended import KaggleApi

# Dataset details — update if the Kaggle dataset slug changes
DATASET = "swaptr/layoffs-2022"  # replace with the exact slug from your Kaggle URL
DOWNLOAD_PATH = "data"
FILE_NAME = "layoffs.csv"

def fetch_layoffs_data():
    print("Authenticating with Kaggle...")
    api = KaggleApi()
    api.authenticate()

    print(f"Downloading dataset: {DATASET}")
    api.dataset_download_files(DATASET, path=DOWNLOAD_PATH, unzip=False)

    # Find the downloaded zip file
    zip_path = os.path.join(DOWNLOAD_PATH, DATASET.split("/")[-1] + ".zip")

    print("Extracting CSV...")
    with zipfile.ZipFile(zip_path, "r") as z:
        # List files in zip to find the CSV
        csv_files = [f for f in z.namelist() if f.endswith(".csv")]
        if not csv_files:
            raise FileNotFoundError("No CSV found in the downloaded zip.")
        
        # Extract the first CSV found
        z.extract(csv_files[0], DOWNLOAD_PATH)

        # Rename to standard filename if needed
        extracted_path = os.path.join(DOWNLOAD_PATH, csv_files[0])
        target_path = os.path.join(DOWNLOAD_PATH, FILE_NAME)

        if extracted_path != target_path:
            shutil.move(extracted_path, target_path)

    # Clean up zip file
    os.remove(zip_path)
    print(f"Done. Fresh data saved to {DOWNLOAD_PATH}/{FILE_NAME}")

if __name__ == "__main__":
    fetch_layoffs_data()
