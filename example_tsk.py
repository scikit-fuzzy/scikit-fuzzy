import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as fcontrol
# New Antecedent/Consequent objects hold universe variables and membership functions

quality = fcontrol.Antecedent(np.array([0, 5, 10]), 'quality')
service = fcontrol.Antecedent(np.array([0, 5, 10]), 'service')
tip = fcontrol.Consequent(np.array([0, 100]), 'tip')

# Auto-membership function population is possible with .automf(3, 5, or 7)
quality.automf(3)
service.automf(3)

# Custom membership functions can be built interactively with a familiar, Pythonic API
tip['increasing'] = fuzz.Polynomial(domain=[-np.Inf,np.Inf],
                                    expression={'quality':[fuzz.Polynomial.term(5,2)],
                                                'service':[fuzz.Polynomial.term(5,2),fuzz.Polynomial.term(-10,1)]})
tip['stable'] = fuzz.Polynomial(domain=tip.universe, expression={'':50})
tip['decreasing'] = fuzz.Polynomial(domain=tip.universe,
                                    expression={'quality':[fuzz.Polynomial.term(-5,2)],
                                                'service':[fuzz.Polynomial.term(5,2)],
                                                '': 100})


rule1 = fcontrol.Rule(service['poor'] | quality['poor'], tip['increasing'])
rule2 = fcontrol.Rule(service['good'], tip['stable'])
rule3 = fcontrol.Rule((service['average'] | service['good']) & quality['average'], tip['decreasing'])

tipping_ctrl = fcontrol.ControlSystem([rule1, rule2, rule3])

tipping = fcontrol.ControlSystemSimulation(tipping_ctrl)

tipping.input['quality'] = 5
tipping.input['service'] = 7.5

# Crunch the numbers
tipping.compute()

# Output available as a dict, for arbitrary number of consequents
print tipping.output["tip"]

