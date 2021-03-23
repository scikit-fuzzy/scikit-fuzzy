#!/usr/bin/env python
"""Script to auto-generate our API docs."""

import apigen
import skfuzzy

if __name__ == '__main__':
    apigen.run(skfuzzy)
