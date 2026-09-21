"""
================================================================
Fuzzy Logic Control: Medical Risk Assessment & Diagnosis System
================================================================

Fuzzy Logic Systems (FLS) provide a vital soft computing paradigm for medical
decision support and clinical risk assessment under uncertainty. Unlike rigid
binary thresholds, fuzzy membership functions capture continuous physiological
transitions:

.. math::

    \\mu_A(x): X \\rightarrow [0, 1]

This interactive tutorial demonstrates building an Automated Patient Risk
Assessment System using ``scikit-fuzzy``.

Clinical Problem Formulation
----------------------------
The controller estimates patient **Systemic Health Risk Level** ($R(t) \\in [0, 100]\\%$)
from two physiological vital signs:

1. **Body Temperature ($T(t)$)**: Core temperature in °C ($[35, 42]^\\circ\\text{C}$).
2. **Heart Rate ($HR(t)$)**: Cardiac pulse rate in beats per minute ($[40, 180]\\text{ bpm}$).

Fuzzy Membership Functions
--------------------------
We use Gaussian Membership Functions (``gaussmf``) for physiological modeling:

.. math::

    \\text{gaussmf}(x; \\sigma, c) = \\exp \\left( -\\frac{(x - c)^2}{2\\sigma^2} \\right)

and Triangular Membership Functions (``trimf``) for risk consequent output.
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import skfuzzy.control as ctrl

# 1. Define Universes of Discourse
temp_universe = np.linspace(35, 42, 141)
hr_universe = np.linspace(40, 180, 141)
risk_universe = np.linspace(0, 100, 101)

# 2. Define Antecedents and Consequents
temperature = ctrl.Antecedent(temp_universe, 'temperature')
heart_rate = ctrl.Antecedent(hr_universe, 'heart_rate')
risk = ctrl.Consequent(risk_universe, 'risk')

# 3. Define Linguistic Terms & Membership Functions
temperature['hypothermia'] = fuzz.gaussmf(temp_universe, 35.5, 0.8)
temperature['normal'] = fuzz.gaussmf(temp_universe, 37.0, 0.6)
temperature['fever'] = fuzz.gaussmf(temp_universe, 39.5, 1.0)

heart_rate['bradycardia'] = fuzz.gaussmf(hr_universe, 50, 10)
heart_rate['normal'] = fuzz.gaussmf(hr_universe, 75, 12)
heart_rate['tachycardia'] = fuzz.gaussmf(hr_universe, 140, 18)

risk['low'] = fuzz.trimf(risk_universe, [0, 0, 35])
risk['moderate'] = fuzz.trimf(risk_universe, [20, 50, 80])
risk['critical'] = fuzz.trimf(risk_universe, [65, 100, 100])


"""
Complete 9-Rule Medical Inference Matrix
----------------------------------------
We construct a full Mamdani fuzzy matrix ensuring complete state-space coverage:

- **Rule 1**: IF `hypothermia` AND `bradycardia` THEN `critical`
- **Rule 2**: IF `hypothermia` AND `normal` THEN `moderate`
- **Rule 3**: IF `hypothermia` AND `tachycardia` THEN `critical`
- **Rule 4**: IF `normal` AND `bradycardia` THEN `moderate`
- **Rule 5**: IF `normal` AND `normal` THEN `low`
- **Rule 6**: IF `normal` AND `tachycardia` THEN `moderate`
- **Rule 7**: IF `fever` AND `bradycardia` THEN `critical`
- **Rule 8**: IF `fever` AND `normal` THEN `moderate`
- **Rule 9**: IF `fever` AND `tachycardia` THEN `critical`
"""
rule1 = ctrl.Rule(temperature['hypothermia'] & heart_rate['bradycardia'], risk['critical'])
rule2 = ctrl.Rule(temperature['hypothermia'] & heart_rate['normal'], risk['moderate'])
rule3 = ctrl.Rule(temperature['hypothermia'] & heart_rate['tachycardia'], risk['critical'])
rule4 = ctrl.Rule(temperature['normal'] & heart_rate['bradycardia'], risk['moderate'])
rule5 = ctrl.Rule(temperature['normal'] & heart_rate['normal'], risk['low'])
rule6 = ctrl.Rule(temperature['normal'] & heart_rate['tachycardia'], risk['moderate'])
rule7 = ctrl.Rule(temperature['fever'] & heart_rate['bradycardia'], risk['critical'])
rule8 = ctrl.Rule(temperature['fever'] & heart_rate['normal'], risk['moderate'])
rule9 = ctrl.Rule(temperature['fever'] & heart_rate['tachycardia'], risk['critical'])

# Build Control System and Simulation
medical_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
medical_sim = ctrl.ControlSystemSimulation(medical_ctrl)

"""
Clinical Scenario Evaluation
----------------------------
Patient Vital Signs:
- Core Temperature = 39.8°C (High Fever)
- Heart Rate = 135 bpm (Elevated Tachycardia)
"""
medical_sim.input['temperature'] = 39.8
medical_sim.input['heart_rate'] = 135.0

medical_sim.compute()
print(f"Evaluated Patient Clinical Risk Level: {medical_sim.output['risk']:.2f}%")

"""
3D Clinical Risk Surface Rendering
----------------------------------
Visualizing non-linear patient risk progression across temperature and heart rate domains.
"""
t_grid, hr_grid = np.meshgrid(np.linspace(35, 42, 35), np.linspace(40, 180, 35))
r_grid = np.zeros_like(t_grid)

for i in range(35):
    for j in range(35):
        medical_sim.input['temperature'] = t_grid[i, j]
        medical_sim.input['heart_rate'] = hr_grid[i, j]
        medical_sim.compute()
        r_grid[i, j] = medical_sim.output['risk']

fig = plt.figure(figsize=(9, 7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(t_grid, hr_grid, r_grid, cmap='plasma', edgecolor='none', alpha=0.9)
ax.set_xlabel('Body Temperature (°C)')
ax.set_ylabel('Heart Rate (bpm)')
ax.set_zlabel('Clinical Risk Level (%)')
ax.set_title('Medical Fuzzy Risk Surface Map')
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
plt.tight_layout()

output_img_path = os.path.join(os.path.dirname(__file__), 'medical_risk_surface.png')
plt.savefig(output_img_path, dpi=150)
print(f"Risk surface visualization saved to {output_img_path}")
plt.close(fig)
