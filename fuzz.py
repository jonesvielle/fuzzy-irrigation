import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# New Antecedent/Consequent objects hold universe variables and membership
# functions
humidity = ctrl.Antecedent(np.arange(0, 100, 1), 'humidity')
temperature = ctrl.Antecedent(np.arange(25, 45, 1), 'temperature')
soil_moisture = ctrl.Antecedent(np.arange(0, 100, 1), 'soil moisture')
pump_speed = ctrl.Consequent(np.arange(0, 255, 1), 'pump speed')

# Auto-membership function population is possible with .automf(3, 5, or 7)
humidity.automf(3)
temperature.automf(3)
soil_moisture.automf(3)

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
pump_speed['low'] = fuzz.trimf(pump_speed.universe, [0, 0, 50])
pump_speed['medium'] = fuzz.trimf(pump_speed.universe, [0, 50, 120])
pump_speed['high'] = fuzz.trimf(pump_speed.universe, [50, 120, 255])

# service.view()
# tip.view()
rule1 = ctrl.Rule(humidity['poor'] | temperature['good'] | soil_moisture['poor'], pump_speed['high'])
rule2 = ctrl.Rule(soil_moisture['average'] | temperature['good'] | humidity['poor'], pump_speed['medium'])
rule3 = ctrl.Rule(humidity['good'] | temperature['poor'] |  soil_moisture['good'], pump_speed['low'])

irrigation_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
irrigation = ctrl.ControlSystemSimulation(irrigation_ctrl)

# Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
# Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
irrigation.input['soil moisture'] = 80
irrigation.input['humidity'] = 85
irrigation.input['temperature'] = 31

# Crunch the numbers
irrigation.compute()

print(irrigation.output['pump speed'])
# tip.view(sim=tipping)