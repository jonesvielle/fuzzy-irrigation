import serial
import ast
import time
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

port = input("Enter PORT:::::")
usbport ='COM4'
ser = serial.Serial(usbport, 9600, timeout=1)
RawData=ser.readline()
time.sleep(3)
while True:
    RawData=ser.readline()
    data = RawData.decode('UTF-8')
    print("####################################")
    print("#-----"+"data = "+data+"------#")
    data = ast.literal_eval(data)
    # print(data)
    # New Antecedent/Consequent objects hold universe variables and membership
    # functions
    humidity = ctrl.Antecedent(np.arange(0, 100, 1), 'humidity')
    temperature = ctrl.Antecedent(np.arange(25, 40, 1), 'temperature')
    soil_moisture = ctrl.Antecedent(np.arange(0, 100, 1), 'soil moisture')
    pump_speed = ctrl.Consequent(np.arange(0, 255, 10), 'pump speed')

    # Auto-membership function population is possible with .automf(3, 5, or 7)
    humidity.automf(3)
    temperature.automf(3)
    soil_moisture.automf(3)

    pump_speed.automf(3)
    # Custom membership functions can be built interactively with a familiar,
    # Pythonic API
    # pump_speed['off'] = fuzz.trimf(pump_speed.universe, [0, 0, 0])
    # pump_speed['low'] = fuzz.trimf(pump_speed.universe, [0, 0, 70])
    # pump_speed['medium'] = fuzz.trimf(pump_speed.universe, [70, 140, 200])
    # pump_speed['high'] = fuzz.trimf(pump_speed.universe, [140, 200, 255])

    # service.view()
    # tip.view()
    rule1 = ctrl.Rule(humidity['good'] | temperature['poor'] | soil_moisture['poor'], pump_speed['good'])
    rule2 = ctrl.Rule(soil_moisture['average'] | temperature['average'] | humidity['average'], pump_speed['average'])
    rule3 = ctrl.Rule(humidity['good'] | temperature['poor'] |  soil_moisture['good'], pump_speed['poor'])
    # rule4 = ctrl.Rule(humidity['good'] | temperature['poor'] |  soil_moisture['good'], pump_speed['off'])
    

    irrigation_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    irrigation = ctrl.ControlSystemSimulation(irrigation_ctrl)

    # Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
    # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
    irrigation.input['soil moisture'] = data['soil moisture']
    irrigation.input['humidity'] = data['humidity']
    irrigation.input['temperature'] = data['temperature']

    # Crunch the numbers
    irrigation.compute()
    print("##------"+str(irrigation.output['pump speed'])+"------##")
  
    ser.write(bytes(str(irrigation.output['pump speed']), 'utf-8'))
    print("####################################")
    time.sleep(3)