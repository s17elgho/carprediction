import sys 
sys.path.insert(0, r"C:\Users\Salma El Ghourbal\Documents\projects\carprediction\src")
import os
from src.logger import logging
from src.exceptions import CustomException
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation
# from src.components.data_transformation import DataTransformationConfig
from src.components.model_trainer import ModelTrainer, ModelTrainerConfig

@dataclass
class DataIngestionConfig:
    train_data_path : str = os.path.join('artifacts','train.csv')
    test_data_path : str = os.path.join('artifacts', 'test.csv')
    raw_data_path : str = os.path.join('artifacts', 'data.csv')

class DataIngestion : 
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    def initiate_data_ingestion(self):
        logging.info('Entering the data ingestion component')
        try : 
            df = pd.read_csv("notebook\data\car_data.csv") 

            logging.info("Read the dataset with pandas")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index = False, header = True)

            logging.info("Initiate train test split")

            train,test = train_test_split(df,test_size = 0.2,random_state=42)

            train.to_csv(self.ingestion_config.train_data_path, index = False, header = True)

            test.to_csv(self.ingestion_config.test_data_path, index = False, header = True)

            logging.info("Ingestion of data completed")
            
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path

            )
        except Exception as e:
            raise CustomException(e,sys)
    
if __name__=="__main__":
    data_ing_obj = DataIngestion()
    train_path, test_path = data_ing_obj.initiate_data_ingestion()
    data_transform_obj = DataTransformation()
    train_arr, test_arr,_ = data_transform_obj.initiate_data_transformation(train_path, test_path )
    model_tr_obj = ModelTrainer()
    print(model_tr_obj.initiate_model_trainer(train_arr, test_arr))