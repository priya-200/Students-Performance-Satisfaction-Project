"""
This module contain all the code needed for reading the data from the source.
"""
import os
import sys

from src.exception import CustomeException
from src.logger import logging
from src.components.data_transformations import DataTransformation
from src.components.data_transformations import DataTransformationConfig

import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    """
    There maybe some inputs that we probabily need in some inputs example where the trainign model should be stored
    etc.. That kind of things will be got as a input from this.
    """
    train_data_path = os.path.join('artifacts','train.csv')
    test_data_path = os.path.join('artifacts','test.csv')
    raw_data_path = os.path.join('artifacts','data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        """
        If the data is stored in any of the databases such as mongo db as such,
        This code will be able to get the data from databases.
        """

        logging.info("Entered the data ingestion method or component")
        try:
            df = pd.read_csv('src\\notebook\\data\\stud.csv')
            logging.info("Read the dataset as dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index = False,header = True)

            logging.info("Train test split initiated")
            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index = False,header = True)
            test_set.to_csv(self.ingestion_config.test_data_path,index = False,header = True)

            logging.info("Train and test data are stored in the respective folders.")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
                #self.ingestion_config.raw_data_path
            )
        except Exception as e:
            raise CustomeException(e,sys)

if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformations = DataTransformation()
    data_transformations.initiate_data_transformation(train_data,test_data)
