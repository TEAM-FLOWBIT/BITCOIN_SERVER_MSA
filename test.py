import json

with open('conf/config.json') as f:
    config = json.load(f)

model_data = config['modelData']

model_size = model_data["modelSize"]
coin_name = model_data["coinName"]
coin_currency = model_data["coinCurrency"]
model_version = model_data["modelVersion"]
file_name_extension = model_data["fileNameExtension"]

model_list = []

for index in range(model_size):
    model_list.append({
            coin_name[index]: 
            coin_currency[index] 
            + "_MODEL_" 
            + model_version[index] 
            + "." + file_name_extension[index]
        })

for i in model_list:
    print(i)