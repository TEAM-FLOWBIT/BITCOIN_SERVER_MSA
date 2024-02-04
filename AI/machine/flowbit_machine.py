from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import sys
import os
import numpy as np
import json

class FlowbitMachine:
    def __init__(self):
        """
        가장 먼저 호출되는 메서드
        config.ini에서 정보를 읽어옴
        """
        with open('conf/config.json') as f:
            config = json.load(f)

        model_data = config['modelData']

        self.model_size = model_data["modelSize"]
        self.coin_name = model_data["coinName"]
        self.coin_currency = model_data["coinCurrency"]
        self.model_version = model_data["modelVersion"]
        self.file_name_extension = model_data["fileNameExtension"]

        model_list = {}

        for index in range(self.model_size):
            model_name = self.coin_currency[index] + "_MODEL_" + self.model_version[index]+ "." + self.file_name_extension[index]

            real_path = os.path.abspath(__file__)[0:-18]+"..\models\\" + model_name
            if os.path.isfile(real_path):
                model = load_model(real_path, compile=False)
            else:
                print("File does not exist:", real_path)
            
            model_list[self.coin_currency[index]] = model

        
        self.scalerOne = MinMaxScaler(feature_range=(0, 1))
        self.scalerMul = MinMaxScaler(feature_range=(0, 1))

        self.model_list = model_list

    def get_model(self, coin_currency="BTC"):
        return self.model_list.get(coin_currency)

    
    def get_model_list(self):
        return self.model_list

    def get_predict_value(self, current_data):
        """
        모델을 불러와서 학습을 진행하고 결과값을 return
        """
        predicted_value = self.model.predict(current_data)
        predicted_value = self.scalerOne.inverse_transform(predicted_value)

        return predicted_value[0][0]

    def data_processing(self, raw_data):
        """
        학습을 위한 전처리 진행
        """

        final_data = [raw_data]
        final_close_data =  [entry[1] for entry in raw_data]

        final_data = self.scalerMul.fit_transform(
            raw_data
        )
        final_close_data = self.scalerOne.fit_transform(
            np.array(final_close_data).reshape(-1, 1)
        )
        final_data = [final_data.tolist()]

        return final_data