import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    RandomForestRegressor,
    GradientBoostingRegressor
)
from sklearn.linear_model import LinearRegression,Ridge,Lasso
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object,evaluate_model

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info('split training and test input')
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models={
                "LinearRegression":LinearRegression(),
                'Lasso':Lasso(),
                'Ridge':Ridge(),
                'KNeighbour regressor':KNeighborsRegressor(),
                'DecisionTreeRegressor':DecisionTreeRegressor(),
                'RandomForestRegressor':RandomForestRegressor(),
                'XGBRegressor':XGBRegressor(),
                'CatBoostRegressor':CatBoostRegressor(),
                'AdaboostRegressor':AdaBoostRegressor(),
                'Gradient Boosting':GradientBoostingRegressor()
            }

            model_report:dict= evaluate_model(X_train=X_train,X_test=X_test,y_train=y_train,y_test=y_test,models=models)


            #get the best model
            best_model_score=max(sorted(model_report.values()))

            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model=models[best_model_name]

            if best_model_score<0.6:
                raise CustomException('No best model found')
            logging.info('Best found model on training and test data')

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=best_model.predict(X_test)
            r2=r2_score(y_test,predicted)
            print(f'Best model is {best_model_name}')

            return r2
        
        except Exception as e:
            raise CustomException(e,sys)