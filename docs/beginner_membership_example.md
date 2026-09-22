# Beginner Example: Fuzzy Membership Functions

This example shows how to create a simple triangular fuzzy membership
function using scikit-fuzzy.

## Python Example

```python
import numpy as np
import skfuzzy as fuzz

x = np.arange(0, 11, 1)

membership = fuzz.trimf(x, [0, 5, 10])

for value, degree in zip(x, membership):
    print(f"Input: {value}, Membership: {degree:.2f}")


