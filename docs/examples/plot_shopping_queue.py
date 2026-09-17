import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Inputs and output
queue = ctrl.Antecedent(np.arange(0, 31, 1), 'queue')
items = ctrl.Antecedent(np.arange(0, 31, 1), 'items')
cashiers = ctrl.Antecedent(np.arange(1, 7, 1), 'cashiers')
wait = ctrl.Consequent(np.arange(0, 41, 1), 'wait')

# Membership functions
queue['short'] = fuzz.trimf(queue.universe, [0, 0, 10])
queue['medium'] = fuzz.trimf(queue.universe, [5, 15, 25])
queue['long'] = fuzz.trimf(queue.universe, [20, 30, 30])

items['few'] = fuzz.trimf(items.universe, [0, 0, 10])
items['medium'] = fuzz.trimf(items.universe, [5, 15, 25])
items['many'] = fuzz.trimf(items.universe, [20, 30, 30])

cashiers['few'] = fuzz.trimf(cashiers.universe, [1, 1, 3])
cashiers['many'] = fuzz.trimf(cashiers.universe, [3, 6, 6])

wait['short'] = fuzz.trimf(wait.universe, [0, 0, 15])
wait['medium'] = fuzz.trimf(wait.universe, [10, 20, 30])
wait['long'] = fuzz.trimf(wait.universe, [25, 40, 40])

# Rules
r1 = ctrl.Rule(queue['short'] & items['few'], wait['short'])
r2 = ctrl.Rule(queue['medium'] & items['medium'] & cashiers['few'], wait['long'])
r3 = ctrl.Rule(queue['medium'] & items['medium'], wait['medium'])
r4 = ctrl.Rule(queue['long'] & items['many'], wait['long'])
r5 = ctrl.Rule(queue['long'] & cashiers['many'], wait['medium'])

# Control system
system = ctrl.ControlSystem([r1, r2, r3, r4, r5])
sim = ctrl.ControlSystemSimulation(system)

# Example
sim.input['queue'] = 15
sim.input['items'] = 8
sim.input['cashiers'] = 2
sim.compute()

print(f"Expected waiting time: {sim.output['wait']:.2f} minutes")

# Show result
wait.view(sim=sim)
plt.show()