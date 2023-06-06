import os
import sys
import zipfile
from src.logger import logging
from src.exception import ProdException
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
import requests


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
           raise ProdException(e, sys)
        

    def download_data(self):
        try:
            zip_download_dir = self.data_ingestion_config.data_ingestion_dir
            os.makedirs(zip_download_dir, exist_ok=True)
            data_file_name = "file.zip"
            zip_file_path = os.path.join(zip_download_dir, data_file_name)
            URL = "https://drive.google.com/u/0/uc?&export=download"
            id = "1MEgDYJwO_PVVfAbyfjaRHXt7qoiBBHYt"

            logging.info(f"Downloading data from {URL} into file {zip_file_path}")
            session = requests.Session()
            response = session.get(URL, params = { 'id' : id }, stream = True)
            params = { 'id' : id, 'confirm' : 1 }
            response = session.get(URL, params = params, stream = True)
            CHUNK_SIZE = 32768
            with open(zip_file_path, "wb") as f:
                for chunk in response.iter_content(CHUNK_SIZE):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
            logging.info(f"Downloaded data from {URL} into file {zip_file_path}")
            return zip_file_path
        
        except Exception as e:
            raise ProdException(e, sys)
            
    def extract_zip_file(self,zip_file_path: str)-> str:
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        try:
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(feature_store_path, exist_ok=True)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(feature_store_path)
            logging.info(f"Extracting zip file: {zip_file_path} into dir: {feature_store_path}")

            return feature_store_path

        except Exception as e:
            raise ProdException(e, sys)
    

    
    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")
        try: 
            zip_file_path = self.download_data()
            feature_store_path = self.extract_zip_file(zip_file_path)

            data_ingestion_artifact = DataIngestionArtifact(
                data_zip_file_path = zip_file_path,
                feature_store_path = feature_store_path
            )

            logging.info("Exited initiate_data_ingestion method of Data_Ingestion class")
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise ProdException(e, sys)