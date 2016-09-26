# -*- coding: utf-8 -*-
from __future__ import absolute_import
from functools import partial

import numpy as np

from skfuzzy.control.fcl.FclLexer import FclLexer
from skfuzzy.control.fcl.FclParser import FclParser

# from antlr3.recognizers import RecognitionException
from antlr3.streams import ANTLRFileStream
from antlr3.streams import CommonTokenStream
# from antlr3.tree import Tree
from ..controlsystem import ControlSystem
from ..antecedent_consequent import Antecedent, Consequent


class FclTreeLoader(object):
    """docstring for FclTreeLoader"""
    control_systems = {}
    rules = {}
    antecedents = {}
    consequents = {}
    mfs = {}

    treeLoadersMapping = {
        "VAR_INPUT": "load_antecedents_from_fcl_tree",
        # "VAR_OUTPUT": "load_consequents_from_fcl_tree",
        # "FUZZIFY": "load_memberships_from_fcl_tree",
        # "DEFUZZIFY": "load_defuzzify_from_fcl_tree",
        # "RULEBLOCK": "load_rules_from_fcl_tree",
    }

    def __init__(self, fcl_file_path):
        super(FclTreeLoader, self).__init__()
        self.fcl_file_path = fcl_file_path
        # self.fcl_file_path = 'tipper.fcl'

    def get_parse_tree(self):
        antlr_fstream = ANTLRFileStream(self.fcl_file_path)
        # st = ANTLRFileStream('tipper.fcl')
        lexer = FclLexer(antlr_fstream)
        ctokens = CommonTokenStream(lexer)
        parser = FclParser(ctokens)
        root = parser.main()
        return root.tree

    def load(self):
        parseTree = self.get_parse_tree()

        for child in parseTree.children:
            # a control system for each function block??
            # still trying to get more examples on FCLs with more then one functionBlock
            # and how they interact is described their interaction
            self.load_controlsystem_from_fcl_tree(child)

        return self.control_systems

    def get_loader_function_for_child_name(self, child_name):
        upper_child_name = child_name.upper()
        if upper_child_name not in self.treeLoadersMapping:
            return None

        loader_function_name = self.treeLoadersMapping[upper_child_name]
        return self.__getattribute__(loader_function_name)

    def load_controlsystem_from_fcl_tree(self, fcl_tree):
            control_system = ControlSystem()
            #first child, so it's the name of the function block
            name = fcl_tree.children[0].text
            self.control_systems[name] = control_system

            # now load the rest of the components
            other_children = fcl_tree.children[1:]
            for i, child in enumerate(other_children):
                child_name = child.text
                loader_function = self.get_loader_function_for_child_name(child_name)
                loader_function(child)
            return control_system

    def load_antecedents_from_fcl_tree(self, fcl_tree):
        # load each antecedent
        for child in fcl_tree.children:
            name = child.text

            universe = None
            has_range_defined = len(child.children) > 1
            if has_range_defined:
                range_tree = child.children[1]
                universe_min, universe_max = [float(value) for value in range_tree.children]

                universe = np.arange(universe_min, universe_max)

            antecedent = Antecedent(universe, name)
            self.antecedents[name] = antecedent
