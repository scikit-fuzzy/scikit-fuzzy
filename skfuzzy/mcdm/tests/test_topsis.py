import nose
import numpy as np
import skfuzzy as fuzz


def setupChenInput():
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


def setupOtherInputMultipleDMs():
    global ranker

    crit_lf = {
        'H': (0.7, 0.9, 1.0),
        'MH': (0.5, 0.7, 0.9),
        'M': (0.3, 0.5, 0.7),
        'ML': (0.1, 0.3, 0.5),
        'L': (0, 0.1, 0.3),
    }

    rat_lf = {
        'VG': (9, 10, 10),
        'G': (7, 9, 10),
        'F': (3, 5, 7),
        'P': (1, 3, 5),
        'VP': (1, 1, 3)
    }



    dm_1 = {
        'decision_matrix': [
            [rat_lf['VG'], rat_lf['F'], rat_lf['P']],
            [rat_lf['F'], rat_lf['P'], rat_lf['F']],
        ],
        'criteria_weights': [
            crit_lf['H'], crit_lf['M'], crit_lf['M']
        ]
    }

    dm_2 = {
        'decision_matrix': [
            [rat_lf['F'], rat_lf['G'], rat_lf['F']],
            [rat_lf['G'], rat_lf['P'], rat_lf['VG']],
        ],
        'criteria_weights': [
            crit_lf['M'], crit_lf['MH'], crit_lf['MH']
        ]
    }

    criteria_benefit_indicator = [True, False, True]
    decision_matrix_list = [dm_1['decision_matrix'], dm_2['decision_matrix']]
    criteria_weights_list = [dm_1['criteria_weights'], dm_2['criteria_weights']]
    ranker = fuzz.mcdm.FuzzyTOPSIS(
        criteria_benefit_indicator=criteria_benefit_indicator,
        decision_matrix_list=decision_matrix_list,
        criteria_weights_list=criteria_weights_list
    )


def setupOtherInputSingleDMs():
    global ranker

    crit_lf = {
        'H': (0.7, 0.9, 1.0),
        'MH': (0.5, 0.7, 0.9),
        'M': (0.3, 0.5, 0.7),
        'ML': (0.1, 0.3, 0.5),
        'L': (0.1, 0.1, 0.3),
    }

    rat_lf = {
        'G': (7, 9, 10),
        'MG': (5, 7, 9),
        'F': (3, 5, 7),
        'MP': (1, 3, 5),
        'P': (1, 1, 3),
    }

    dm_1 = {
        'decision_matrix': [
            [rat_lf['F'], rat_lf['F'], rat_lf['P']],
            [rat_lf['F'], rat_lf['F'], rat_lf['G']],
            [rat_lf['G'], rat_lf['P'], rat_lf['F']],
        ],
        'criteria_weights': [
            crit_lf['M'], crit_lf['L'], crit_lf['H']
        ]
    }


    criteria_benefit_indicator = [True, True, False]
    decision_matrix_list = [dm_1['decision_matrix']]
    criteria_weights_list = [dm_1['criteria_weights']]
    ranker = fuzz.mcdm.FuzzyTOPSIS(
        criteria_benefit_indicator=criteria_benefit_indicator,
        decision_matrix_list=decision_matrix_list,
        criteria_weights_list=criteria_weights_list
    )


@nose.with_setup(setupChenInput)
def test_fuzzy_topsis_ccs_with_chen_inputs():
    """
    Test fuzzy topsis with Chen input.

    """
    global ranker

    ret = ranker.evaluate()
    expected_rank_index = [1, 2, 0]

    np.testing.assert_array_equal(expected_rank_index, ret)

    # deviation from reported values in Chen's original paper  (0.62, 0.77, 0.71)
    # the rounding of numbers and the wrong reported value on Table 5 (aggregated attributes) for A1, C2
    # are most likelly the culprit for this disdrepancy
    expected_ccs = [0.64, 0.77, 0.70]
    np.testing.assert_allclose(expected_ccs[0], ranker.closeness_coefficients[0], rtol=0.01)
    np.testing.assert_allclose(expected_ccs[1], ranker.closeness_coefficients[1], rtol=0.01)
    np.testing.assert_allclose(expected_ccs[2], ranker.closeness_coefficients[2], rtol=0.01)


@nose.with_setup(setupOtherInputMultipleDMs)
def test_fuzzy_topsis_ccs_with_multiple_dms():
    """
    Test fuzzy topsis with other inputs using multiple dms.

    """
    global ranker

    ret = ranker.evaluate()
    expected_rank_index = [1, 0]

    np.testing.assert_array_equal(expected_rank_index, ret)

    expected_ccs = [0.352, 0.495]
    np.testing.assert_allclose(expected_ccs[0], ranker.closeness_coefficients[0], rtol=0.01)
    np.testing.assert_allclose(expected_ccs[1], ranker.closeness_coefficients[1], rtol=0.01)


@nose.with_setup(setupOtherInputSingleDMs)
def test_fuzzy_topsis_ccs_with_easy_single_dm():
    """
    Test fuzzy topsis with other inputs using logically sound
     and easy to interpret input, with a single DM.
    """
    global ranker

    ret = ranker.evaluate()
    expected_rank_index = [0, 2, 1]

    np.testing.assert_array_equal(expected_rank_index, ret)



    expected_ccs = [0.385, 0.195, 0.254]
    np.testing.assert_allclose(expected_ccs[0], ranker.closeness_coefficients[0], rtol=0.01)
    np.testing.assert_allclose(expected_ccs[1], ranker.closeness_coefficients[1], rtol=0.01)
    np.testing.assert_allclose(expected_ccs[2], ranker.closeness_coefficients[2], rtol=0.01)


if __name__ == '__main__':
    np.testing.run_module_suite()
