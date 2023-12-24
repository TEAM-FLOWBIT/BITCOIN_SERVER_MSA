from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import sys
import os
import numpy as np


class FlowbitMachine:
    def __init__(self):
        """
        가장 먼저 호출되는 메서드
        config.ini에서 정보를 읽어옴
        """
        # self.model_path = "static/BITCOIN_MODEL_VER1.h5"

        # sys.path.append(os.path.abspath(__file__)[0:-15])
        self.scalerOne = MinMaxScaler(feature_range=(0, 1))
        self.scalerMul = MinMaxScaler(feature_range=(0, 1))
        # print(os.path.realpath(__file__))
        real_path = os.path.abspath(__file__)[0:-18]+"BITCOIN_MODEL_VER2.h5"
        print("리얼패스 시발",real_path)
        if os.path.isfile(real_path):
            print("File exists:", real_path)
        else:
            print("File does not exist:", real_path)
        self.model = load_model(real_path, compile=False)

    """def get_model(self, current_data):

        loaded_model = load_model(self.model_path, compile=False)
        predicted = loaded_model.predict(current_data)
        #ret = load_model.predict(current_data)

        return predicted"""

    def get_predict_value(self, current_data):
        """
        모델을 불러와서 학습을 진행하고 결과값을 return
        """
        # model = self.get_model(current_data)
        #print(current_data)
        predicted_value = self.model.predict(current_data)
        #print(predicted_value)
        predicted_value = self.scalerOne.inverse_transform(predicted_value)
        # predicted_value = model.predict(current_data)
        #print(predicted_value)
        #print(predicted_value)
        # print(np.array(predicted_value).reshape(-1, 1).shape)
        # predicted_value = self.scalerOne.inverse_transform(
        #     #predicted_value
        #     predicted_value
        # )
        #print(predicted_value)
        return predicted_value[0][0]

    def data_processing(self, raw_data):
        """
        학습을 위한 전처리 진행
        """

        final_data = [raw_data]
        final_close_data =  [entry[1] for entry in raw_data]
        #print(raw_data)
        #print(final_close_data)
        final_data = self.scalerMul.fit_transform(
            raw_data
        )
        #print(np.array(final_close_data).reshape(-1, 1).shape)
        final_close_data = self.scalerOne.fit_transform(
            #final_close_data
            np.array(final_close_data).reshape(-1, 1)
        )
        #print(final_close_data)
        
        final_data = [final_data.tolist()]
        #print(final_data)
        #print(final_data)
        #final_data = final_data.reshape(final_data.shape[0], final_data.shape[1], final_data.shape[2])
        #print(final_data.shape)

        return final_data