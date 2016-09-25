# -*- coding: utf-8 -*-
from unittest import TestCase

from mock import Mock, MagicMock, patch, call
from skfuzzy.control.fcl.loader import FclTreeLoader


class TestFclTreeLoader(TestCase):

    @patch('skfuzzy.control.fcl.loader.FclTreeLoader.load_controlsystem_from_fcl_tree')
    @patch(
        'skfuzzy.control.fcl.loader.FclTreeLoader.get_parse_tree',
        return_value=Mock(children=["child1", "child2"])
    )
    def test_load(self, get_parse_tree, load_ctrl_from_tree):
        fcl_loader = FclTreeLoader("some_file")
        fcl_loader.load()
        get_parse_tree.assert_called_once()

        calls = [call("child1"), call("child2")]
        load_ctrl_from_tree.aseert_has_calls(calls)

    # def test_load_controlsystem_from_fcl_tree(self):
    #     fcl_loader = FclTreeLoader("some_file")
    #     fcl_tree = None
    #     fcl_loader.load_controlsystem_from_fcl_tree(fcl_tree)

    def test_get_loader_function_for_child_name(self):
        fcl_loader = FclTreeLoader("some_file")
