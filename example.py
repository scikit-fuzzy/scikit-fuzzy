import numpy as np
import skfuzzy as fuzz

# New Antecedent/Consequent objects hold universe variables and membership functions
from skfuzzy.control.controlsystem import ControlSystemSimulation

quality = fuzz.Antecedent(np.arange(0, 11, 1), 'quality')
service = fuzz.Antecedent(np.arange(0, 11, 1), 'service')
tip = fuzz.Consequent(np.arange(0, 26, 1), 'tip')

# Auto-membership function population is possible with .automf(3, 5, or 7)
quality.automf(3)
service.automf(3)

# Custom membership functions can be built interactively with a familiar, Pythonic API
tip['poor'] = fuzz.trimf(tip.universe, [0, 0, 13])
tip['average'] = fuzz.trimf(tip.universe, [0, 13, 25])
tip['good'] = fuzz.trimf(tip.universe, [13, 25, 25])

# You can see how these look with .view()
quality['average'].view()
service.view()
tip.view()

# Rule objects connect one or more antecedent membership functions with
# one or more consequent membership functions, using 'or' or 'and' to combine the antecedents.
#   * rule1: "If food is poor OR services is poor, then tip will be poor
#   * rule2: "If service is average, then tip will be average
#   * rule3: "If service is good OR food is good, then tip will be good
rule1 = fuzz.Rule(quality['poor'] | service['poor'], tip['poor'])
rule2 = fuzz.Rule(service['average'], tip['average'])
rule3 = fuzz.Rule(service['good'] | quality['good'], tip['good'])

# Create a new ControlSystem with these rules added
# Note: it is possible to create an empty ControlSystem() and build it up interactively.
tipping_ctrl = fuzz.ControlSystem([rule1, rule2, rule3])

# View the whole system
tipping_ctrl.view()

tipping = ControlSystemSimulation(tipping_ctrl)

# Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
# Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
tipping.input['quality'] = 6.5
tipping.input['service'] = 9.8

# Crunch the numbers
tipping.compute()

# Output available as a dict, for arbitrary number of consequents
print tipping.output
tipping.print_state()
# Viewing the Consequent again after computation shows the calculated system
tip.view(sim=tipping)

###############
# More sophesticated system

# Inputs: qualtiy, service, decor
# Outpus: Tip
# Intermediary: ambiance
decor = fuzz.Antecedent(np.arange(0, 11, 1), 'decor')
decor.automf(3)

ambiance = fuzz.Intermediary(np.arange(0, 11, 1), 'ambiance')
ambiance.automf(3)

# If service is poor and decor is not good, ambiance is poor
rule4 = fuzz.Rule(service['poor'] & ~decor['good'], ambiance['poor'])
rule2.view()

# If ambiance is poor, tip is poor, but at a 75% weight
rule5 = fuzz.Rule(ambiance['poor'], tip['poor']%.75)

sys2 = fuzz.ControlSystem([rule1, rule4, rule5])
sys2_sim = ControlSystemSimulation(sys2)
sys2_sim.input['quality'] = 6.5
sys2_sim.input['service'] = 2.9
sys2_sim.input['decor'] = 3.5
sys2_sim.compute()

sys2.view()
sys2_sim.print_state()

a = 5
