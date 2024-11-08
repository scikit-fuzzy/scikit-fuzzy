"""
topsis.py : Fuzzy TOPSIS algorithm.
"""
import numpy as np


class FuzzyTOPSIS(object):
    """
    Class for running the Fuzzy TOPSIS ranking.
    Using [1] for the default aggregation methods of alternatives, criteria
     and normalisation.


    Parameters
    ----------

    Example of input:
    decision_maker_1_decision_matrix = [
        [(9, 10, 10), (9, 10, 10), (9, 10, 10)],
            # alt1: crit1, 2 and 3 as "very_good_rating"
        [(3, 5, 7), (3, 5, 7), (3, 5, 7)],
            # alt2: crit1, 2 and 3 as "medium_rating"
    ]
    decision_maker_1_weights = [
        (0.7, 0.9, 1.0), (0.3, 0.5, 0.7), (0.3, 0.5, 0.7)
    ]
    # weights for crit1, 2 and 3 as "high_weight", "medium_weight" the last two

    decision_maker_2_decision_matrix = [
        [(3, 5, 7), (3, 5, 7), (3, 5, 7)],
        # alt1: crit1, 2 and 3 as "medium_rating"
        [(7, 9, 10), (7, 9, 10), (7, 9, 10)],
        # alt2: crit1, 2 and 3 as "good_rating"
    ]
    decision_maker_2_weights = [
        (0.3, 0.5, 0.7), (0.5, 0.7, 0.9), (0.5, 0.7, 0.9)
    ]
    # weights for crit1, 2 and 3 as "medium_weight",
    # "medium_high_weight" the last two

    decision_matrix_list = [
        decision_maker_1_decision_matrix, decision_maker_2_decision_matrix
    ]
    weights_list = [decision_maker_1_weights, decision_maker_2_weights]
    criteria_benefit_indicator = [True, False, True]
    # indicates that criteria 1 and 3 are benefit, and criteria 2 is cost.

    Notes
    -----
    Algorithm implemented from  [1]_.

    References
    ----------
    .. [1] Chen, C.T., 2000. Extensions of the TOPSIS for group decision-making
        under fuzzy environment.
        Fuzzy sets and systems, 114(1), pp.1-9.

    """

    def __init__(
        self,
        criteria_benefit_indicator,
        decision_matrix_list=None,
        criteria_weights_list=None,
        agg_alt_fuzzy_method=None,
        agg_crit_fuzzy_method=None,
        norm_alt_fuzzy_method=None,
    ):
        if decision_matrix_list is None or criteria_weights_list is None:
            decision_matrix_list = []
            criteria_weights_list = []
            num_alternatives = None
            num_decision_makers = None
        else:
            num_alternatives = len(decision_matrix_list[0])
            num_decision_makers = len(decision_matrix_list)

        self.criteria_benefit_indicator = criteria_benefit_indicator
        self.num_alternatives = num_alternatives
        self.num_decision_makers = num_decision_makers
        self.num_criteria = len(self.criteria_benefit_indicator)

        self.decision_matrix_list = decision_matrix_list
        self.criteria_weights_list = criteria_weights_list

        self.validate_inputs(
            criteria_benefit_indicator,
            decision_matrix_list,
            criteria_weights_list,
        )

        if agg_alt_fuzzy_method is None:
            agg_alt_fuzzy_method = self._defaut_alt_agg_fuzzy_rating_method
        self.agg_alt_fuzzy_method = agg_alt_fuzzy_method

        if agg_crit_fuzzy_method is None:
            agg_crit_fuzzy_method = self._defaut_crit_agg_fuzzy_weight_method
        self.agg_crit_fuzzy_method = agg_crit_fuzzy_method

        if norm_alt_fuzzy_method is None:
            norm_alt_fuzzy_method = self._default_normalize_alternative_method
        self.norm_alt_fuzzy_method = norm_alt_fuzzy_method

        self.agg_decision_matrix = None
        self.agg_criteria_weights = None
        self.norm_decision_matrix = None
        self.weighted_norm_decision_matrix = None

        self.FPIS_value = None
        self.fpis_distances = None
        self.fpis_distances_per_criterion = None

        self.FNIS_value = None
        self.fnis_distances = None
        self.fnis_distances_per_criterion = None

        self.closeness_coefficients = None
        self.ranking_indexes = None

    def validate_inputs(
        self,
        criteria_benefit_indicator,
        decision_matrix_list,
        criteria_weights_list,
    ):
        assert (
            self.num_criteria > 0
        ), "Number of criteria should be more than zero."

        num_decision_makers = len(decision_matrix_list)
        if num_decision_makers > 0:
            assert_msg = (
                "Inconsistent number of decision makers",
                " in criteria weights list input",
            )
            assert num_decision_makers == len(
                criteria_weights_list
            ), assert_msg
            num_alternatives = len(decision_matrix_list[0])
            if self.num_alternatives is None:
                self.num_alternatives = num_alternatives

            for i_dm, dm in enumerate(decision_matrix_list):
                cw = criteria_weights_list[i_dm]
                self._validate_decision_maker(dm, cw)

    def _validate_decision_maker(self, decision_matrix, criteria_weights):
        num_alternatives = len(decision_matrix)
        num_criteria = len(decision_matrix[0])
        assert_msg = (
            "invalid number of alternatives in decision matrix: "
            f"{num_alternatives} != {self.num_alternatives}"
        )
        if self.num_alternatives is not None:
            assert num_alternatives == self.num_alternatives, assert_msg

        assert_msg = (
            f"invalid number of criteria in decision matrix: "
            f"{num_criteria} != {self.num_criteria}"
        )
        assert num_criteria == self.num_criteria, assert_msg

        num_criteria_w = len(criteria_weights)
        assert_msg = (
            f"invalid number of criteria in criteria weights: "
            f"{num_criteria_w} != {self.num_criteria}"
        )
        assert num_criteria_w == self.num_criteria, assert_msg

    def add_decision_maker(self, decision_matrix, criteria_weights):
        if self.num_alternatives is None:
            num_alternatives = len(decision_matrix)
            self.num_alternatives = num_alternatives
        self._validate_decision_maker(decision_matrix, criteria_weights)

        self.decision_matrix_list.append(decision_matrix)
        self.criteria_weights_list.append(criteria_weights)
        self.num_decision_makers = len(self.decision_matrix_list)

    def evaluate(self, validate_first=True):
        if validate_first:
            self.validate_inputs(
                self.criteria_benefit_indicator,
                self.decision_matrix_list,
                self.criteria_weights_list,
            )

        self._aggregated_ratings_and_weights()
        self._normalized_decision_matrix()
        self._weighted_normalized_decision_matrix()
        self._calculate_FPIS_FNIS()
        self._distance_from_FPIS_FNIS()
        self._calculate_closeness_coefficients()
        self._rank_alternatives()
        return self.ranking_indexes

    def _defaut_alt_agg_fuzzy_rating_method(self, alt_i, crit_j):
        """
        Same method for aggregating fuzzy ratings used in Chen [1].
        Returns the avg of each individual value in the triangular fuzzy number
        """
        avg_values = np.mean(
            [
                np.array(dm[alt_i][crit_j])
                for dm in self.decision_matrix_list
            ],
            axis=0
        )

        return avg_values.tolist()

    def _all_agg_ratings(self):
        """
        Function used to aggregate the fuzzy ratings for the
        alternatives for each decision maker
        """
        agg_decision_matrix = [
            [
                self.agg_alt_fuzzy_method(alt_i, crit_j)
                for crit_j in range(self.num_criteria)
            ]
            for alt_i in range(self.num_alternatives)
        ]

        return agg_decision_matrix

    def _defaut_crit_agg_fuzzy_weight_method(self, crit_j):
        """
        Same method for aggregating fuzzy criteria used in Chen [1].
        Returns the avg of each individual value in the triangular fuzzy number
        """
        avg_values = np.mean(
            [
                weights[crit_j]
                for weights in self.criteria_weights_list
            ],
            axis=0
        )

        return avg_values.tolist()

    def _all_agg_weights(self):
        """
        Function used to aggregate the fuzzy weights for the benefit and
        cost criteria respectively
        """
        return [
            self.agg_crit_fuzzy_method(crit_j)
            for crit_j in range(self.num_criteria)
        ]

    def _aggregated_ratings_and_weights(self):
        """
        Second step in fuzzy TOPSIS, where the aggregated fuzzy ratings and
        weights are calculated for the criteria and alternatives,
        respectivelly.
        """
        self.agg_decision_matrix = self._all_agg_ratings()
        self.agg_criteria_weights = self._all_agg_weights()

    def _get_min_left_or_max_right_for_criteria(self, crit_j):
        is_benefit_criterion = self.criteria_benefit_indicator[crit_j]
        value_index = -1 if is_benefit_criterion else 0

        # Initialize an array with either np.inf or 0
        # based on the benefit criterion
        init_value = np.inf if not is_benefit_criterion else 0

        comp_method = np.max if is_benefit_criterion else np.min

        values = np.array([init_value] + [
            alternative[crit_j][value_index]
            for alternative in self.agg_decision_matrix
        ])

        final_value = comp_method(values)
        return final_value

    def _default_normalize_alternative_method(
        self, alt_i, crit_j, minl_or_maxr_criteria
    ):
        alternative = self.agg_decision_matrix[alt_i]
        criterion = np.array(alternative[crit_j])

        is_benefit_criterion = self.criteria_benefit_indicator[crit_j]

        if is_benefit_criterion:
            norm_alt_crit_j = criterion / minl_or_maxr_criteria
        else:
            norm_alt_crit_j = minl_or_maxr_criteria / criterion[::-1]

        return tuple(norm_alt_crit_j)

    def _normalized_decision_matrix(self):
        """
        Third step in fuzzy TOPSIS, in which the normalized fuzzy decision
        matrix is calculated.
        """

        self.norm_decision_matrix = [
            [None for j in range(self.num_criteria)]
            for i in range(self.num_alternatives)
        ]
        for crit_j in range(self.num_criteria):
            minl_or_maxr_criteria = (
                self._get_min_left_or_max_right_for_criteria(crit_j)
            )

            for alt_i in range(self.num_alternatives):
                norm_alt_crit_j = self.norm_alt_fuzzy_method(
                    alt_i, crit_j, minl_or_maxr_criteria
                )
                self.norm_decision_matrix[alt_i][crit_j] = norm_alt_crit_j

    def _weighted_normalized_decision_matrix(self):
        """
        Fourth step in fuzzy TOPSIS, in which the weighted normalized fuzzy
        decision matrix is calculated.
        """
        self.weighted_norm_decision_matrix = []
        for alternative in self.norm_decision_matrix:

            alt_weighted_norm_criteria = np.array([
                np.array(criterion) * np.array(weight)

                for criterion, weight in zip(
                    alternative, self.agg_criteria_weights
                )
            ])

            self.weighted_norm_decision_matrix.append(
                alt_weighted_norm_criteria.tolist()
            )

    def _calculate_FPIS_FNIS(self):
        """
        Fifith step in fuzzy TOPSIS, in which the
        Fuzzy Positive Ideal Solution (FPIS) and
        Fuzzy Negative Ideal Solution (FNIS) are calculated.
        Chen’s method:
            FPIS: (1, 1, 1)... simplification where positive and
            negative ideal are an alternative with 1s and 0s respectivelly
            FNIS: (0, 0, 0)...
        """
        self.FPIS_value = np.ones((self.num_criteria, 3), dtype=int)
        self.FNIS_value = np.zeros((self.num_criteria, 3), dtype=int)

    def _fuzzy_number_distance_calculation(self, val1, val2):
        """
        Euclidean distance of two triangular fuzzy numbers
        proposed by Chen, C.T., 2000
        """
        difference = np.array(val1) - np.array(val2)
        squared_difference = difference ** 2
        mean_squared_difference = np.mean(squared_difference)
        euclidean_distance = np.sqrt(mean_squared_difference)
        return euclidean_distance

    def _calculate_distance_from_ideal_solutions(
        self, alt_i, crit_j, is_positive=True
    ):
        ideal_solution = self.FPIS_value if is_positive else self.FNIS_value
        ideal_criterion = ideal_solution[crit_j]
        criterion = self.weighted_norm_decision_matrix[alt_i][crit_j]
        dist = self._fuzzy_number_distance_calculation(
            criterion, ideal_criterion
        )
        return dist

    def _distance_from_FPIS_FNIS(self):
        """
        Sixth step in fuzzy TOPSIS, where the distances from
        each alternative to the
        Fuzzy Positive Ideal Solution (FPIS) and
        Fuzzy Negative Ideal Solution (FNIS) are calculated.
        """
        self.fpis_distances = []
        self.fpis_distances_per_criterion = []
        self.fnis_distances = []
        self.fnis_distances_per_criterion = []
        for alt_i, alternative in enumerate(
            self.weighted_norm_decision_matrix
        ):
            alt_fpis_distances = []
            alt_fnis_distances = []
            for crit_j, criterion in enumerate(alternative):
                fpis_dist = self._calculate_distance_from_ideal_solutions(
                    alt_i, crit_j, is_positive=True
                )
                fnis_dist = self._calculate_distance_from_ideal_solutions(
                    alt_i, crit_j, is_positive=False
                )

                alt_fpis_distances.append(fpis_dist)
                alt_fnis_distances.append(fnis_dist)

            self.fpis_distances_per_criterion.append(alt_fpis_distances)
            self.fpis_distances.append(sum(alt_fpis_distances))
            self.fnis_distances_per_criterion.append(alt_fnis_distances)
            self.fnis_distances.append(sum(alt_fnis_distances))

    def _calculate_closeness_coefficients(self):
        """
        Seventh step in fuzzy TOPSIS, where it is calculated the closeness
        coefficient for each alternative.
        """
        fnis_distances = np.array(self.fnis_distances)
        fpis_distances = np.array(self.fpis_distances)

        denominators = fnis_distances + fpis_distances
        closeness_coefficients = np.divide(
            fnis_distances, denominators
        )

        self.closeness_coefficients = closeness_coefficients.tolist()

    def get_alternatives_ranking_scores(self):
        return self.closeness_coefficients

    def _rank_alternatives(self):
        """
        Eight and last step in fuzzy TOPSIS, in which final alternative ranks
        are calculated as crips values.
        """

        self.ranking_indexes = sorted(
            range(self.num_alternatives),
            key=lambda k: self.closeness_coefficients[k],
            reverse=True,
        )
