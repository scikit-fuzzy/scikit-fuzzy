"""
============================================================
Fuzzy Logic Control: Smart HVAC & Temperature Control System
============================================================

Fuzzy Logic Systems (FLS) provide a robust framework for soft computing and
automated control in complex, non-linear environments. Unlike traditional crisp
binary logic (0 or 1), fuzzy logic handles partial truth values ranging between
0 and 1 via membership functions:

.. math::

    \\mu_A(x): X \\rightarrow [0, 1]

This example demonstrates building a Smart HVAC (Heating, Ventilation, and Air
Conditioning) Fuzzy Logic Controller using ``scikit-fuzzy``.

Problem Overview
----------------
The goal of the controller is to regulate indoor climate by computing the
optimal **Fan / HVAC Power Output** ($u(t) \\in [0, 100]\\%$) based on:

1. **Temperature Error ($e(t)$)**: Difference between target setpoint and ambient temperature (in °C, $[-10, 10]$).
2. **Temperature Error Change Rate ($\\Delta e(t)$)**: Rate of change of error over time (in °C/min, $[-5, 5]$).

Fuzzy Membership Functions
--------------------------
We use Triangular Membership Functions (``trimf``) defined as:

.. math::

    \\text{trimf}(x; a, b, c) = \\max \\left(0, \\min \\left( \\frac{x-a}{b-a}, \\frac{c-x}{c-b} \\right) \\right)

"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import skfuzzy.control as ctrl

# 1. Define Universes of Discourse
error_universe = np.linspace(-10, 10, 201)
delta_universe = np.linspace(-5, 5, 101)
power_universe = np.linspace(0, 100, 101)

# 2. Define Antecedents and Consequents
error = ctrl.Antecedent(error_universe, 'error')
delta = ctrl.Antecedent(delta_universe, 'delta')
power = ctrl.Consequent(power_universe, 'power')

# 3. Define Linguistic Variables and Terms
error['too_cold'] = fuzz.trimf(error_universe, [-10, -10, 0])
error['comfortable'] = fuzz.trimf(error_universe, [-3, 0, 3])
error['too_hot'] = fuzz.trimf(error_universe, [0, 10, 10])

delta['cooling_fast'] = fuzz.trimf(delta_universe, [-5, -5, 0])
delta['steady'] = fuzz.trimf(delta_universe, [-1.5, 0, 1.5])
delta['heating_fast'] = fuzz.trimf(delta_universe, [0, 5, 5])

power['off'] = fuzz.trimf(power_universe, [0, 0, 25])
power['medium'] = fuzz.trimf(power_universe, [15, 50, 85])
power['maximum'] = fuzz.trimf(power_universe, [60, 100, 100])

"""
Rule Base Construction
----------------------
We formulate a complete 9-rule fuzzy inference matrix covering all input combinations:

- **Rule 1**: IF `too_cold` AND `cooling_fast` THEN `maximum`
- **Rule 2**: IF `too_cold` AND `steady` THEN `medium`
- **Rule 3**: IF `too_cold` AND `heating_fast` THEN `off`
- **Rule 4**: IF `comfortable` AND `cooling_fast` THEN `medium`
- **Rule 5**: IF `comfortable` AND `steady` THEN `off`
- **Rule 6**: IF `comfortable` AND `heating_fast` THEN `off`
- **Rule 7**: IF `too_hot` AND `cooling_fast` THEN `off`
- **Rule 8**: IF `too_hot` AND `steady` THEN `medium`
- **Rule 9**: IF `too_hot` AND `heating_fast` THEN `maximum`
"""
rule1 = ctrl.Rule(error['too_cold'] & delta['cooling_fast'], power['maximum'])
rule2 = ctrl.Rule(error['too_cold'] & delta['steady'], power['medium'])
rule3 = ctrl.Rule(error['too_cold'] & delta['heating_fast'], power['off'])
rule4 = ctrl.Rule(error['comfortable'] & delta['cooling_fast'], power['medium'])
rule5 = ctrl.Rule(error['comfortable'] & delta['steady'], power['off'])
rule6 = ctrl.Rule(error['comfortable'] & delta['heating_fast'], power['off'])
rule7 = ctrl.Rule(error['too_hot'] & delta['cooling_fast'], power['off'])
rule8 = ctrl.Rule(error['too_hot'] & delta['steady'], power['medium'])
rule9 = ctrl.Rule(error['too_hot'] & delta['heating_fast'], power['maximum'])

# Build Control System and Simulation Environment
hvac_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
hvac_sim = ctrl.ControlSystemSimulation(hvac_ctrl)


"""
Simulation & Crisp Input Evaluation
-----------------------------------
Evaluate system response for a scenario:
Ambient temperature error = -6.0°C (Room is significantly colder than target setpoint).
Error derivative delta = -2.0°C/min (Room temperature is continuing to drop).
"""
hvac_sim.input['error'] = -6.0
hvac_sim.input['delta'] = -2.0

hvac_sim.compute()
print(f"Evaluated HVAC Power Output: {hvac_sim.output['power']:.2f}%")

"""
Control Surface Visualization (3D Response Map)
----------------------------------------------
Rendering the non-linear fuzzy control surface over the full operating space.
"""
x_grid, y_grid = np.meshgrid(np.linspace(-10, 10, 41), np.linspace(-5, 5, 41))
z_grid = np.zeros_like(x_grid)

for i in range(41):
    for j in range(41):
        hvac_sim.input['error'] = x_grid[i, j]
        hvac_sim.input['delta'] = y_grid[i, j]
        hvac_sim.compute()
        z_grid[i, j] = hvac_sim.output['power']

fig = plt.figure(figsize=(9, 7))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(x_grid, y_grid, z_grid, cmap='viridis', edgecolor='none', alpha=0.9)
ax.set_xlabel('Temperature Error (°C)')
ax.set_ylabel('Error Change Rate (°C/min)')
ax.set_zlabel('HVAC Power Output (%)')
ax.set_title('Smart HVAC Fuzzy Control Surface')
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
plt.tight_layout()
output_img_path = os.path.join(os.path.dirname(__file__), 'hvac_control_surface.png')
plt.savefig(output_img_path, dpi=150)
print(f"Control surface visualization saved to {output_img_path}")
plt.close(fig)

