import sys
sys.path.append("C:\AGAPE\FLOW-BIT\projects\BITCOIN_SERVER_MSA")
import json
from AI.machine.model_controller import ModelController

flowbit = ModelController()

for i in flowbit.get_model_list():
    print(i, " : ", flowbit.get_model(i))

#print(flowbit.get_model())