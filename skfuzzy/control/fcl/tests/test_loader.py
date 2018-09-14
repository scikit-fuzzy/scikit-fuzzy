# -*- coding: utf-8 -*-
from unittest import TestCase

from mock import Mock, MagicMock, patch
from skfuzzy.control.fcl.loader import FclTreeLoader


def mock_fcltree_with_children(children):
    fcl_tree = Mock(children=children)
    return fcl_tree


class TestFclTreeLoader(TestCase):

    @patch('skfuzzy.control.fcl.loader.FclTreeLoader.load_controlsystem_from_fcl_tree')
    @patch(
        'skfuzzy.control.fcl.loader.FclTreeLoader.get_parse_tree',
        return_value=mock_fcltree_with_children(children=["child1", "child2"])
    )
    def test_load(self, get_parse_tree, load_ctrl_from_tree):
        fcl_loader = FclTreeLoader("some_file")
        fcl_loader.load()
        get_parse_tree.assert_called_once()

        load_ctrl_from_tree.assert_any_call("child1")
        load_ctrl_from_tree.assert_any_call("child2")

    def test_get_loader_function_for_child_name_should_return_none_if_invalid_childname(self):
        fcl_loader = FclTreeLoader("some_file")

        self.assertIsNone(fcl_loader.get_loader_function_for_child_name("invalid_child_name"))

    def test_get_loader_function_for_child_name_for_lower_case_childname(self):
        fcl_loader = FclTreeLoader("some_file")
        child_name = "var_input"
        func = fcl_loader.get_loader_function_for_child_name(child_name)
        expected_func = fcl_loader.load_antecedents_from_fcl_tree
        self.assertEquals(expected_func, func)

    def test_get_loader_function_for_child_name_for_existing_childname(self):
        fcl_loader = FclTreeLoader("some_file")
        child_name = "VAR_INPUT"
        func = fcl_loader.get_loader_function_for_child_name(child_name)
        expected_func = fcl_loader.load_antecedents_from_fcl_tree
        self.assertEquals(expected_func, func)

    @patch(
        'skfuzzy.control.fcl.loader.FclTreeLoader.get_loader_function_for_child_name'
    )
    def test_load_controlsystem_from_fcl_tree(self, loader_function):
        fcl_loader = FclTreeLoader("some_file")
        child_0 = Mock(text="function block name")
        child_1 = Mock(text="child_block name 1")
        child_2 = Mock(text="child_block name 2")
        fcl_tree = mock_fcltree_with_children([child_0, child_1, child_2])
        control_system = fcl_loader.load_controlsystem_from_fcl_tree(fcl_tree)

        self.assertIn("function block name", fcl_loader.control_systems)
        self.assertEquals(control_system, fcl_loader.control_systems["function block name"])
        loader_function.assert_any_call("child_block name 1")
        loader_function.assert_any_call("child_block name 2")

    def test_load_antecedents_from_fcl_tree_with_no_universe_and_real_type(self):
        fcl_loader = FclTreeLoader("some_file")

        antecedent_type = Mock(text="REAL")
        antecedent_tree = Mock(text="antecedent name", children=[antecedent_type])
        fcl_tree = mock_fcltree_with_children(children=[antecedent_tree])
        fcl_loader.load_antecedents_from_fcl_tree(fcl_tree)

        self.assertIn('antecedent name', fcl_loader.antecedents)

        universe = fcl_loader.antecedents['antecedent name'].universe

        # assert is an array from None value
        self.assertEquals(len(universe.shape), 0)

    def test_load_antecedents_from_fcl_tree_with_universe_and_real_type(self):
        fcl_loader = FclTreeLoader("some_file")

        antecedent_range_min = Mock(text="1")
        antecedent_range_max = Mock(text="3")
        antecedent_range = Mock(text="RANGE", children=[antecedent_range_min, antecedent_range_max])
        antecedent_type = Mock(text="REAL")
        antecedent_tree = Mock(text="antecedent name", children=[antecedent_type, antecedent_range])
        fcl_tree = mock_fcltree_with_children(children=[antecedent_tree])
        fcl_loader.load_antecedents_from_fcl_tree(fcl_tree)

        self.assertIn('antecedent name', fcl_loader.antecedents)

        universe = fcl_loader.antecedents['antecedent name'].universe

        # assert is not a 'empty' universe
        self.assertGreater(len(universe.shape), 0)
        self.assertListEqual(list(universe), [1., 2.])
