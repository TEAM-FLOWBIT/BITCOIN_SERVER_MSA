import json
from AI.machine.flowbit_machine import FlowbitMachine

flowbit = FlowbitMachine()

for i in flowbit.get_model_list():
    print(i, " : ", flowbit.get_model(i))

print(flowbit.get_model())