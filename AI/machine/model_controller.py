from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import sys
sys.path.append("C:\AGAPE\FLOW-BIT\projects\BITCOIN_SERVER_MSA")
import os
import numpy as np
import json
from AI.machine.flowbit_machine import FlowbitMachine

class ModelController:
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

        self.model_list = {}

        for index in range(self.model_size):
            model_name = self.coin_currency[index] + "_MODEL_" + self.model_version[index]+ "." + self.file_name_extension[index]

            real_path = os.path.abspath(__file__)[0:-20]+"\..\models\\" + model_name
            #print(os.path.abspath(__file__)[0:-20])
            if os.path.isfile(real_path):
                print(real_path)
                model = FlowbitMachine(model_path=real_path)
            else:
                print("File does not exist:", real_path)
            
            self.model_list[model_name] = model


    def get_model(self, coin_currency="BTC"):
        return self.model_list.get(coin_currency)

    def get_model_list(self):
        return self.model_list