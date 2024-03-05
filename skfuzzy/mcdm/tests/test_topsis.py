import nose
import numpy as np
import skfuzzy as fuzz


def setup():
    global ranker

    crit_lf = {
        'VH': (0.9, 1.0, 1.0),
        'H': (0.7, 0.9, 1.0),
        'MH': (0.5, 0.7, 0.9),
        'M': (0.3, 0.5, 0.7),
        'ML': (0.1, 0.3, 0.5),
        'L': (0, 0.1, 0.3),
        'VL': (0.0, 0.0, 0.1),
    }

    rat_lf = {
        'VG': (9, 10, 10),
        'G': (7, 9, 10),
        'MG': (5, 7, 9),
        'F': (3, 5, 7),
        'MP': (1, 3, 5),
        'P': (0, 1, 3),
        'VP': (0, 0, 1)
    }


    dm_1 = {
        'decision_matrix': [
            [rat_lf['MG'], rat_lf['G'], rat_lf['F'], rat_lf['VG'], rat_lf['F']],
            [rat_lf['G'], rat_lf['VG'], rat_lf['VG'], rat_lf['VG'], rat_lf['VG']],
            [rat_lf['VG'], rat_lf['MG'], rat_lf['G'], rat_lf['G'], rat_lf['G']],
        ],
        'criteria_weights': [
            crit_lf['H'], crit_lf['VH'], crit_lf['VH'], crit_lf['VH'], crit_lf['M']
        ]
    }

    dm_2 = {
        'decision_matrix': [
            [rat_lf['G'], rat_lf['MG'], rat_lf['G'], rat_lf['G'], rat_lf['F']],
            [rat_lf['G'], rat_lf['VG'], rat_lf['VG'], rat_lf['VG'], rat_lf['MG']],
            [rat_lf['G'], rat_lf['G'], rat_lf['MG'], rat_lf['VG'], rat_lf['G']],
        ],
        'criteria_weights': [
            crit_lf['VH'], crit_lf['VH'], crit_lf['H'], crit_lf['VH'], crit_lf['MH']
        ]
    }

    dm_3 = {
        'decision_matrix': [
            [rat_lf['MG'], rat_lf['F'], rat_lf['G'], rat_lf['VG'], rat_lf['F']],
            [rat_lf['MG'], rat_lf['VG'], rat_lf['G'], rat_lf['VG'], rat_lf['G']],
            [rat_lf['F'], rat_lf['VG'], rat_lf['VG'], rat_lf['MG'], rat_lf['MG']],
        ],
        'criteria_weights': [
            crit_lf['MH'], crit_lf['VH'], crit_lf['H'], crit_lf['VH'], crit_lf['MH']
        ]
    }

    criteria_benefit_indicator = [True, True, True, True, True]
    decision_matrix_list = [dm_1['decision_matrix'], dm_2['decision_matrix'], dm_3['decision_matrix']]
    criteria_weights_list = [dm_1['criteria_weights'], dm_2['criteria_weights'], dm_3['criteria_weights']]
    ranker = fuzz.mcdm.FuzzyTOPSIS(
        criteria_benefit_indicator=criteria_benefit_indicator,
        decision_matrix_list=decision_matrix_list,
        criteria_weights_list=criteria_weights_list
    )




@nose.with_setup(setup)
def test_fuzzy_topsis_centers():
    """
    Test fuzzy topsis with Chen input.

    """
    global ranker

    ret = ranker.evaluate()
    expected_rank_index = [1, 2, 0]

    np.testing.assert_array_equal(expected_rank_index, ret)

    # deviation from reported values in Chen's original paper  (0.62, 0.77, 0.71)
    # the rounding of numbers and the wrong reported value on Table 5 (aggregated attributes) for A1, C2
    # could be the culprit for this disdrepancy
    expected_ccs = [0.64, 0.77, 0.70]
    np.testing.assert_allclose(expected_ccs[0], ranker.closeness_coefficients[0], rtol=0.01)
    np.testing.assert_allclose(expected_ccs[1], ranker.closeness_coefficients[1], rtol=0.01)
    np.testing.assert_allclose(expected_ccs[2], ranker.closeness_coefficients[2], rtol=0.01)



if __name__ == '__main__':
    np.testing.run_module_suite()
