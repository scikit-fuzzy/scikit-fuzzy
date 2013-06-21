"""
skfuzzy.intervals : Standard operations for intervals, provided as two-element
    1-D arrays or iterables.

Functions supported: addition, subtraction, division, multiplication, and
                     scaling. All interval function names have `*val` suffix.

Also contains algorithms for the DSW method arithmatic operations on fuzzy
sets, which depend upon heavy use of intervals.

"""
__all__ = ['addval',
           'divval',
           'dsw_add',
           'dsw_div',
           'dsw_mult',
           'dsw_sub',
           'multval',
           'scaleval',
           'subval']

from .intervalops import (addval, divval, dsw_add, dsw_div, dsw_mult, dsw_sub,
                          multval, scaleval, subval)
