"""
Fuzzy mathematics subpackage, containing essential mathematical operations for
fuzzy sets and universe variables.

"""
__all__ = ['cartadd',
           'cartprod',
           'classic_relation',
           'continuous_to_discrete',
           'contrast',
           'fuzzy_add',
           'fuzzy_sub',
           'fuzzy_mult',
           'fuzzy_div',
           'fuzzy_min',
           'fuzzy_or',
           'fuzzy_and',
           'fuzzy_not',
           'fuzzy_compare',
           'fuzzy_similarity',
           'inner_product',
           'interp_membership',
           'interp_universe',
           'interp10',
           'maxmin_composition',
           'maxprod_composition',
           'modus_ponens',
           'outer_product',
           'relation_min',
           'relation_product',
           'sigmoid',
           'partial_dmf']

from .fuzzy_ops import (cartadd, cartprod, classic_relation, contrast,
                        fuzzy_add, fuzzy_sub, fuzzy_mult, fuzzy_div,
                        fuzzy_min, fuzzy_compare, fuzzy_similarity,
                        inner_product, interp_membership, interp_universe, interp10,
                        maxmin_composition, maxprod_composition, modus_ponens,
                        outer_product, relation_min, relation_product,
                        sigmoid, partial_dmf)

from .fuzzy_logic import fuzzy_and, fuzzy_or, fuzzy_not

from ._continuous_to_discrete import continuous_to_discrete
