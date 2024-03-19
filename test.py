import sys
sys.path.append("C:\AGAPE\FLOW-BIT\projects\BITCOIN_SERVER_MSA")
import json
from AI.machine.model_controller import ModelController

flowbit = ModelController()

#print(flowbit.get_model_list())

for i in flowbit.get_model_list():
    print(i)
    #print(i, " : ", flowbit.get_model(i))

#print(flowbit.get_model())