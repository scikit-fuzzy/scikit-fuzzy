# $ANTLR 3.1.3 Mar 18, 2009 10:09:25 Fcl.g 2016-09-21 22:32:47

import sys
from antlr3 import *
from antlr3.compat import set, frozenset

from antlr3.tree import *



# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
FUNCTION=34
SIGM=61
STAR=91
LN=43
LETTER=96
LM=42
LOG=44
EINSTEIN=26
COG=17
NOT=52
EOF=-1
COA=15
HAT=81
SIN=62
EXP=32
MM=50
COS=20
TAN=65
LEFT_PARENTHESIS=83
COMMENT=99
GAUSS2=36
NC=51
END_RULEBLOCK=30
VAR_OUTPUT=72
ACT=10
END_DEFUZZIFY=27
RULE=59
NUMBER=93
GBELL=37
SEMICOLON=89
DMIN=24
VALUE_REAL=6
ALPHANUM=97
TYPE_REAL=70
ABS=8
REAL=98
WS=74
NSUM=53
LEFT_CURLY=82
OR=54
LOWER=94
END_FUZZIFY=29
UPPER=95
TERM=66
COGF=19
PROBOR=55
RIGHT_CURLY=87
NIPMIN=48
POINT=4
RM=58
MAX=45
DOTS=80
COGS=18
ID=102
AND=11
SUM=64
VALUE_ID=7
DSIGM=25
IF=40
SLASH=90
THEN=67
RIGHT_PARENTHESIS=88
COMMA=78
IS=41
DMAX=23
TRAPE=68
BDIF=13
PROD=56
COSINE=16
PLUS=86
DIGIT=92
DOT=79
FUNCTION_BLOCK=38
WITH=73
END_VAR=31
ACCU=9
ASUM=12
PERCENT=85
SINGLETONS=63
NIPMAX=49
ASSIGN_OPERATOR=76
TRIAN=69
DEFAULT=21
HAMACHER=33
COMMENT_C=100
FCL=5
RANGE=57
MIN=47
MINUS=84
DEFUZZIFY=22
COLON=77
NEWLINE=75
COMMENT_SL=101
VAR_INPUT=71
BSUM=14
RULEBLOCK=60
FUZZIFY=39
END_FUNCTION_BLOCK=28
METHOD=46
GAUSS=35

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>",
    "POINT", "FCL", "VALUE_REAL", "VALUE_ID", "ABS", "ACCU", "ACT", "AND",
    "ASUM", "BDIF", "BSUM", "COA", "COSINE", "COG", "COGS", "COGF", "COS",
    "DEFAULT", "DEFUZZIFY", "DMAX", "DMIN", "DSIGM", "EINSTEIN", "END_DEFUZZIFY",
    "END_FUNCTION_BLOCK", "END_FUZZIFY", "END_RULEBLOCK", "END_VAR", "EXP",
    "HAMACHER", "FUNCTION", "GAUSS", "GAUSS2", "GBELL", "FUNCTION_BLOCK",
    "FUZZIFY", "IF", "IS", "LM", "LN", "LOG", "MAX", "METHOD", "MIN", "NIPMIN",
    "NIPMAX", "MM", "NC", "NOT", "NSUM", "OR", "PROBOR", "PROD", "RANGE",
    "RM", "RULE", "RULEBLOCK", "SIGM", "SIN", "SINGLETONS", "SUM", "TAN",
    "TERM", "THEN", "TRAPE", "TRIAN", "TYPE_REAL", "VAR_INPUT", "VAR_OUTPUT",
    "WITH", "WS", "NEWLINE", "ASSIGN_OPERATOR", "COLON", "COMMA", "DOT",
    "DOTS", "HAT", "LEFT_CURLY", "LEFT_PARENTHESIS", "MINUS", "PERCENT",
    "PLUS", "RIGHT_CURLY", "RIGHT_PARENTHESIS", "SEMICOLON", "SLASH", "STAR",
    "DIGIT", "NUMBER", "LOWER", "UPPER", "LETTER", "ALPHANUM", "REAL", "COMMENT",
    "COMMENT_C", "COMMENT_SL", "ID"
]




class FclParser(Parser):
    grammarFileName = "Fcl.g"
    antlr_version = version_str_to_tuple("3.1.3 Mar 18, 2009 10:09:25")
    antlr_version_str = "3.1.3 Mar 18, 2009 10:09:25"
    tokenNames = tokenNames

    def __init__(self, input, state=None, *args, **kwargs):
        if state is None:
            state = RecognizerSharedState()

        super(FclParser, self).__init__(input, state, *args, **kwargs)






        self._adaptor = None
        self.adaptor = CommonTreeAdaptor()




    def getTreeAdaptor(self):
        return self._adaptor

    def setTreeAdaptor(self, adaptor):
        self._adaptor = adaptor

    adaptor = property(getTreeAdaptor, setTreeAdaptor)


    class main_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.main_return, self).__init__()

            self.tree = None




    # $ANTLR start "main"
    # Fcl.g:145:1: main : f= fcl -> ^( FCL $f) ;
    def main(self, ):

        retval = self.main_return()
        retval.start = self.input.LT(1)

        root_0 = None

        f = None


        stream_fcl = RewriteRuleSubtreeStream(self._adaptor, "rule fcl")
        try:
            try:
                # Fcl.g:145:6: (f= fcl -> ^( FCL $f) )
                # Fcl.g:145:9: f= fcl
                pass
                self._state.following.append(self.FOLLOW_fcl_in_main2813)
                f = self.fcl()

                self._state.following.pop()
                stream_fcl.add(f.tree)

                # AST Rewrite
                # elements: f
                # token labels:
                # rule labels: f, retval
                # token list labels:
                # rule list labels:
                # wildcard labels:

                retval.tree = root_0

                if f is not None:
                    stream_f = RewriteRuleSubtreeStream(self._adaptor, "rule f", f.tree)
                else:
                    stream_f = RewriteRuleSubtreeStream(self._adaptor, "token f", None)


                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 145:15: -> ^( FCL $f)
                # Fcl.g:145:18: ^( FCL $f)
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(self._adaptor.createFromType(FCL, "FCL"), root_1)

                self._adaptor.addChild(root_1, stream_f.nextTree())

                self._adaptor.addChild(root_0, root_1)



                retval.tree = root_0



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "main"

    class fcl_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.fcl_return, self).__init__()

            self.tree = None




    # $ANTLR start "fcl"
    # Fcl.g:146:1: fcl : ( function_block )+ ;
    def fcl(self, ):

        retval = self.fcl_return()
        retval.start = self.input.LT(1)

        root_0 = None

        function_block1 = None



        try:
            try:
                # Fcl.g:146:5: ( ( function_block )+ )
                # Fcl.g:146:9: ( function_block )+
                pass
                root_0 = self._adaptor.nil()

                # Fcl.g:146:9: ( function_block )+
                cnt1 = 0
                while True: #loop1
                    alt1 = 2
                    LA1_0 = self.input.LA(1)

                    if (LA1_0 == FUNCTION_BLOCK) :
                        alt1 = 1


                    if alt1 == 1:
                        # Fcl.g:146:10: function_block
                        pass
                        self._state.following.append(self.FOLLOW_function_block_in_fcl2832)
                        function_block1 = self.function_block()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, function_block1.tree)


                    else:
                        if cnt1 >= 1:
                            break #loop1

                        eee = EarlyExitException(1, self.input)
                        raise eee

                    cnt1 += 1



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "fcl"

    class function_block_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.function_block_return, self).__init__()

            self.tree = None




    # $ANTLR start "function_block"
    # Fcl.g:148:1: function_block : FUNCTION_BLOCK ( ID )? ( declaration )* END_FUNCTION_BLOCK ;
    def function_block(self, ):

        retval = self.function_block_return()
        retval.start = self.input.LT(1)

        root_0 = None

        FUNCTION_BLOCK2 = None
        ID3 = None
        END_FUNCTION_BLOCK5 = None
        declaration4 = None


        FUNCTION_BLOCK2_tree = None
        ID3_tree = None
        END_FUNCTION_BLOCK5_tree = None

        try:
            try:
                # Fcl.g:148:16: ( FUNCTION_BLOCK ( ID )? ( declaration )* END_FUNCTION_BLOCK )
                # Fcl.g:148:18: FUNCTION_BLOCK ( ID )? ( declaration )* END_FUNCTION_BLOCK
                pass
                root_0 = self._adaptor.nil()

                FUNCTION_BLOCK2=self.match(self.input, FUNCTION_BLOCK, self.FOLLOW_FUNCTION_BLOCK_in_function_block2842)

                FUNCTION_BLOCK2_tree = self._adaptor.createWithPayload(FUNCTION_BLOCK2)
                root_0 = self._adaptor.becomeRoot(FUNCTION_BLOCK2_tree, root_0)

                # Fcl.g:148:34: ( ID )?
                alt2 = 2
                LA2_0 = self.input.LA(1)

                if (LA2_0 == ID) :
                    alt2 = 1
                if alt2 == 1:
                    # Fcl.g:148:35: ID
                    pass
                    ID3=self.match(self.input, ID, self.FOLLOW_ID_in_function_block2846)

                    ID3_tree = self._adaptor.createWithPayload(ID3)
                    self._adaptor.addChild(root_0, ID3_tree)




                # Fcl.g:148:40: ( declaration )*
                while True: #loop3
                    alt3 = 2
                    LA3_0 = self.input.LA(1)

                    if (LA3_0 == DEFUZZIFY or LA3_0 == FUZZIFY or LA3_0 == RULEBLOCK or (VAR_INPUT <= LA3_0 <= VAR_OUTPUT)) :
                        alt3 = 1


                    if alt3 == 1:
                        # Fcl.g:148:41: declaration
                        pass
                        self._state.following.append(self.FOLLOW_declaration_in_function_block2851)
                        declaration4 = self.declaration()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, declaration4.tree)


                    else:
                        break #loop3
                END_FUNCTION_BLOCK5=self.match(self.input, END_FUNCTION_BLOCK, self.FOLLOW_END_FUNCTION_BLOCK_in_function_block2855)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "function_block"

    class declaration_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.declaration_return, self).__init__()

            self.tree = None




    # $ANTLR start "declaration"
    # Fcl.g:149:1: declaration : ( var_input | var_output | fuzzify_block | defuzzify_block | rule_block );
    def declaration(self, ):

        retval = self.declaration_return()
        retval.start = self.input.LT(1)

        root_0 = None

        var_input6 = None

        var_output7 = None

        fuzzify_block8 = None

        defuzzify_block9 = None

        rule_block10 = None



        try:
            try:
                # Fcl.g:149:13: ( var_input | var_output | fuzzify_block | defuzzify_block | rule_block )
                alt4 = 5
                LA4 = self.input.LA(1)
                if LA4 == VAR_INPUT:
                    alt4 = 1
                elif LA4 == VAR_OUTPUT:
                    alt4 = 2
                elif LA4 == FUZZIFY:
                    alt4 = 3
                elif LA4 == DEFUZZIFY:
                    alt4 = 4
                elif LA4 == RULEBLOCK:
                    alt4 = 5
                else:
                    nvae = NoViableAltException("", 4, 0, self.input)

                    raise nvae

                if alt4 == 1:
                    # Fcl.g:149:15: var_input
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_var_input_in_declaration2863)
                    var_input6 = self.var_input()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, var_input6.tree)


                elif alt4 == 2:
                    # Fcl.g:149:27: var_output
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_var_output_in_declaration2867)
                    var_output7 = self.var_output()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, var_output7.tree)


                elif alt4 == 3:
                    # Fcl.g:149:40: fuzzify_block
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_fuzzify_block_in_declaration2871)
                    fuzzify_block8 = self.fuzzify_block()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, fuzzify_block8.tree)


                elif alt4 == 4:
                    # Fcl.g:149:56: defuzzify_block
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_defuzzify_block_in_declaration2875)
                    defuzzify_block9 = self.defuzzify_block()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, defuzzify_block9.tree)


                elif alt4 == 5:
                    # Fcl.g:149:74: rule_block
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_rule_block_in_declaration2879)
                    rule_block10 = self.rule_block()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, rule_block10.tree)


                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "declaration"

    class var_input_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.var_input_return, self).__init__()

            self.tree = None




    # $ANTLR start "var_input"
    # Fcl.g:151:1: var_input : VAR_INPUT ( var_def )* END_VAR ;
    def var_input(self, ):

        retval = self.var_input_return()
        retval.start = self.input.LT(1)

        root_0 = None

        VAR_INPUT11 = None
        END_VAR13 = None
        var_def12 = None


        VAR_INPUT11_tree = None
        END_VAR13_tree = None

        try:
            try:
                # Fcl.g:151:11: ( VAR_INPUT ( var_def )* END_VAR )
                # Fcl.g:151:13: VAR_INPUT ( var_def )* END_VAR
                pass
                root_0 = self._adaptor.nil()

                VAR_INPUT11=self.match(self.input, VAR_INPUT, self.FOLLOW_VAR_INPUT_in_var_input2887)

                VAR_INPUT11_tree = self._adaptor.createWithPayload(VAR_INPUT11)
                root_0 = self._adaptor.becomeRoot(VAR_INPUT11_tree, root_0)

                # Fcl.g:151:24: ( var_def )*
                while True: #loop5
                    alt5 = 2
                    LA5_0 = self.input.LA(1)

                    if (LA5_0 == ID) :
                        alt5 = 1


                    if alt5 == 1:
                        # Fcl.g:151:25: var_def
                        pass
                        self._state.following.append(self.FOLLOW_var_def_in_var_input2891)
                        var_def12 = self.var_def()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, var_def12.tree)


                    else:
                        break #loop5
                END_VAR13=self.match(self.input, END_VAR, self.FOLLOW_END_VAR_in_var_input2895)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "var_input"

    class var_output_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.var_output_return, self).__init__()

            self.tree = None




    # $ANTLR start "var_output"
    # Fcl.g:152:1: var_output : VAR_OUTPUT ( var_def )+ END_VAR ;
    def var_output(self, ):

        retval = self.var_output_return()
        retval.start = self.input.LT(1)

        root_0 = None

        VAR_OUTPUT14 = None
        END_VAR16 = None
        var_def15 = None


        VAR_OUTPUT14_tree = None
        END_VAR16_tree = None

        try:
            try:
                # Fcl.g:152:12: ( VAR_OUTPUT ( var_def )+ END_VAR )
                # Fcl.g:152:14: VAR_OUTPUT ( var_def )+ END_VAR
                pass
                root_0 = self._adaptor.nil()

                VAR_OUTPUT14=self.match(self.input, VAR_OUTPUT, self.FOLLOW_VAR_OUTPUT_in_var_output2903)

                VAR_OUTPUT14_tree = self._adaptor.createWithPayload(VAR_OUTPUT14)
                root_0 = self._adaptor.becomeRoot(VAR_OUTPUT14_tree, root_0)

                # Fcl.g:152:26: ( var_def )+
                cnt6 = 0
                while True: #loop6
                    alt6 = 2
                    LA6_0 = self.input.LA(1)

                    if (LA6_0 == ID) :
                        alt6 = 1


                    if alt6 == 1:
                        # Fcl.g:152:27: var_def
                        pass
                        self._state.following.append(self.FOLLOW_var_def_in_var_output2907)
                        var_def15 = self.var_def()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, var_def15.tree)


                    else:
                        if cnt6 >= 1:
                            break #loop6

                        eee = EarlyExitException(6, self.input)
                        raise eee

                    cnt6 += 1
                END_VAR16=self.match(self.input, END_VAR, self.FOLLOW_END_VAR_in_var_output2911)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "var_output"

    class var_def_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.var_def_return, self).__init__()

            self.tree = None




    # $ANTLR start "var_def"
    # Fcl.g:153:1: var_def : ID COLON data_type SEMICOLON ( range )? ;
    def var_def(self, ):

        retval = self.var_def_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID17 = None
        COLON18 = None
        SEMICOLON20 = None
        data_type19 = None

        range21 = None


        ID17_tree = None
        COLON18_tree = None
        SEMICOLON20_tree = None

        try:
            try:
                # Fcl.g:153:9: ( ID COLON data_type SEMICOLON ( range )? )
                # Fcl.g:153:11: ID COLON data_type SEMICOLON ( range )?
                pass
                root_0 = self._adaptor.nil()

                ID17=self.match(self.input, ID, self.FOLLOW_ID_in_var_def2919)

                ID17_tree = self._adaptor.createWithPayload(ID17)
                root_0 = self._adaptor.becomeRoot(ID17_tree, root_0)

                COLON18=self.match(self.input, COLON, self.FOLLOW_COLON_in_var_def2922)
                self._state.following.append(self.FOLLOW_data_type_in_var_def2925)
                data_type19 = self.data_type()

                self._state.following.pop()
                self._adaptor.addChild(root_0, data_type19.tree)
                SEMICOLON20=self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_var_def2927)
                # Fcl.g:153:43: ( range )?
                alt7 = 2
                LA7_0 = self.input.LA(1)

                if (LA7_0 == RANGE) :
                    alt7 = 1
                if alt7 == 1:
                    # Fcl.g:153:44: range
                    pass
                    self._state.following.append(self.FOLLOW_range_in_var_def2931)
                    range21 = self.range()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, range21.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "var_def"

    class fuzzify_block_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.fuzzify_block_return, self).__init__()

            self.tree = None




    # $ANTLR start "fuzzify_block"
    # Fcl.g:155:1: fuzzify_block : FUZZIFY ID ( linguistic_term )* END_FUZZIFY ;
    def fuzzify_block(self, ):

        retval = self.fuzzify_block_return()
        retval.start = self.input.LT(1)

        root_0 = None

        FUZZIFY22 = None
        ID23 = None
        END_FUZZIFY25 = None
        linguistic_term24 = None


        FUZZIFY22_tree = None
        ID23_tree = None
        END_FUZZIFY25_tree = None

        try:
            try:
                # Fcl.g:155:15: ( FUZZIFY ID ( linguistic_term )* END_FUZZIFY )
                # Fcl.g:155:17: FUZZIFY ID ( linguistic_term )* END_FUZZIFY
                pass
                root_0 = self._adaptor.nil()

                FUZZIFY22=self.match(self.input, FUZZIFY, self.FOLLOW_FUZZIFY_in_fuzzify_block2942)

                FUZZIFY22_tree = self._adaptor.createWithPayload(FUZZIFY22)
                root_0 = self._adaptor.becomeRoot(FUZZIFY22_tree, root_0)

                ID23=self.match(self.input, ID, self.FOLLOW_ID_in_fuzzify_block2945)

                ID23_tree = self._adaptor.createWithPayload(ID23)
                self._adaptor.addChild(root_0, ID23_tree)

                # Fcl.g:155:29: ( linguistic_term )*
                while True: #loop8
                    alt8 = 2
                    LA8_0 = self.input.LA(1)

                    if (LA8_0 == TERM) :
                        alt8 = 1


                    if alt8 == 1:
                        # Fcl.g:155:30: linguistic_term
                        pass
                        self._state.following.append(self.FOLLOW_linguistic_term_in_fuzzify_block2948)
                        linguistic_term24 = self.linguistic_term()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, linguistic_term24.tree)


                    else:
                        break #loop8
                END_FUZZIFY25=self.match(self.input, END_FUZZIFY, self.FOLLOW_END_FUZZIFY_in_fuzzify_block2952)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "fuzzify_block"

    class linguistic_term_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.linguistic_term_return, self).__init__()

            self.tree = None




    # $ANTLR start "linguistic_term"
    # Fcl.g:156:1: linguistic_term : TERM ID ASSIGN_OPERATOR membership_function SEMICOLON ;
    def linguistic_term(self, ):

        retval = self.linguistic_term_return()
        retval.start = self.input.LT(1)

        root_0 = None

        TERM26 = None
        ID27 = None
        ASSIGN_OPERATOR28 = None
        SEMICOLON30 = None
        membership_function29 = None


        TERM26_tree = None
        ID27_tree = None
        ASSIGN_OPERATOR28_tree = None
        SEMICOLON30_tree = None

        try:
            try:
                # Fcl.g:156:16: ( TERM ID ASSIGN_OPERATOR membership_function SEMICOLON )
                # Fcl.g:156:18: TERM ID ASSIGN_OPERATOR membership_function SEMICOLON
                pass
                root_0 = self._adaptor.nil()

                TERM26=self.match(self.input, TERM, self.FOLLOW_TERM_in_linguistic_term2959)

                TERM26_tree = self._adaptor.createWithPayload(TERM26)
                root_0 = self._adaptor.becomeRoot(TERM26_tree, root_0)

                ID27=self.match(self.input, ID, self.FOLLOW_ID_in_linguistic_term2962)

                ID27_tree = self._adaptor.createWithPayload(ID27)
                self._adaptor.addChild(root_0, ID27_tree)

                ASSIGN_OPERATOR28=self.match(self.input, ASSIGN_OPERATOR, self.FOLLOW_ASSIGN_OPERATOR_in_linguistic_term2964)
                self._state.following.append(self.FOLLOW_membership_function_in_linguistic_term2967)
                membership_function29 = self.membership_function()

                self._state.following.pop()
                self._adaptor.addChild(root_0, membership_function29.tree)
                SEMICOLON30=self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_linguistic_term2969)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "linguistic_term"

    class membership_function_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.membership_function_return, self).__init__()

            self.tree = None




    # $ANTLR start "membership_function"
    # Fcl.g:157:1: membership_function : ( function | singleton | singletons | piece_wise_linear | gauss | gauss2 | trian | trape | sigm | gbell | cosine | dsigm );
    def membership_function(self, ):

        retval = self.membership_function_return()
        retval.start = self.input.LT(1)

        root_0 = None

        function31 = None

        singleton32 = None

        singletons33 = None

        piece_wise_linear34 = None

        gauss35 = None

        gauss236 = None

        trian37 = None

        trape38 = None

        sigm39 = None

        gbell40 = None

        cosine41 = None

        dsigm42 = None



        try:
            try:
                # Fcl.g:157:21: ( function | singleton | singletons | piece_wise_linear | gauss | gauss2 | trian | trape | sigm | gbell | cosine | dsigm )
                alt9 = 12
                LA9 = self.input.LA(1)
                if LA9 == FUNCTION:
                    alt9 = 1
                elif LA9 == REAL or LA9 == ID:
                    alt9 = 2
                elif LA9 == SINGLETONS:
                    alt9 = 3
                elif LA9 == LEFT_PARENTHESIS:
                    alt9 = 4
                elif LA9 == GAUSS:
                    alt9 = 5
                elif LA9 == GAUSS2:
                    alt9 = 6
                elif LA9 == TRIAN:
                    alt9 = 7
                elif LA9 == TRAPE:
                    alt9 = 8
                elif LA9 == SIGM:
                    alt9 = 9
                elif LA9 == GBELL:
                    alt9 = 10
                elif LA9 == COSINE:
                    alt9 = 11
                elif LA9 == DSIGM:
                    alt9 = 12
                else:
                    nvae = NoViableAltException("", 9, 0, self.input)

                    raise nvae

                if alt9 == 1:
                    # Fcl.g:157:23: function
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_function_in_membership_function2977)
                    function31 = self.function()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, function31.tree)


                elif alt9 == 2:
                    # Fcl.g:157:34: singleton
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_singleton_in_membership_function2981)
                    singleton32 = self.singleton()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, singleton32.tree)


                elif alt9 == 3:
                    # Fcl.g:157:46: singletons
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_singletons_in_membership_function2985)
                    singletons33 = self.singletons()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, singletons33.tree)


                elif alt9 == 4:
                    # Fcl.g:157:59: piece_wise_linear
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_piece_wise_linear_in_membership_function2989)
                    piece_wise_linear34 = self.piece_wise_linear()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, piece_wise_linear34.tree)


                elif alt9 == 5:
                    # Fcl.g:157:79: gauss
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_gauss_in_membership_function2993)
                    gauss35 = self.gauss()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, gauss35.tree)


                elif alt9 == 6:
                    # Fcl.g:157:87: gauss2
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_gauss2_in_membership_function2997)
                    gauss236 = self.gauss2()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, gauss236.tree)


                elif alt9 == 7:
                    # Fcl.g:157:96: trian
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_trian_in_membership_function3001)
                    trian37 = self.trian()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, trian37.tree)


                elif alt9 == 8:
                    # Fcl.g:157:104: trape
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_trape_in_membership_function3005)
                    trape38 = self.trape()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, trape38.tree)


                elif alt9 == 9:
                    # Fcl.g:157:112: sigm
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_sigm_in_membership_function3009)
                    sigm39 = self.sigm()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, sigm39.tree)


                elif alt9 == 10:
                    # Fcl.g:157:119: gbell
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_gbell_in_membership_function3013)
                    gbell40 = self.gbell()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, gbell40.tree)


                elif alt9 == 11:
                    # Fcl.g:157:127: cosine
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_cosine_in_membership_function3017)
                    cosine41 = self.cosine()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, cosine41.tree)


                elif alt9 == 12:
                    # Fcl.g:157:136: dsigm
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_dsigm_in_membership_function3021)
                    dsigm42 = self.dsigm()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, dsigm42.tree)


                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "membership_function"

    class cosine_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.cosine_return, self).__init__()

            self.tree = None




    # $ANTLR start "cosine"
    # Fcl.g:158:1: cosine : COSINE atom atom ;
    def cosine(self, ):

        retval = self.cosine_return()
        retval.start = self.input.LT(1)

        root_0 = None

        COSINE43 = None
        atom44 = None

        atom45 = None


        COSINE43_tree = None

        try:
            try:
                # Fcl.g:158:7: ( COSINE atom atom )
                # Fcl.g:158:9: COSINE atom atom
                pass
                root_0 = self._adaptor.nil()

                COSINE43=self.match(self.input, COSINE, self.FOLLOW_COSINE_in_cosine3028)

                COSINE43_tree = self._adaptor.createWithPayload(COSINE43)
                root_0 = self._adaptor.becomeRoot(COSINE43_tree, root_0)

                self._state.following.append(self.FOLLOW_atom_in_cosine3031)
                atom44 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom44.tree)
                self._state.following.append(self.FOLLOW_atom_in_cosine3033)
                atom45 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom45.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "cosine"

    class dsigm_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.dsigm_return, self).__init__()

            self.tree = None




    # $ANTLR start "dsigm"
    # Fcl.g:159:1: dsigm : DSIGM atom atom atom atom ;
    def dsigm(self, ):

        retval = self.dsigm_return()
        retval.start = self.input.LT(1)

        root_0 = None

        DSIGM46 = None
        atom47 = None

        atom48 = None

        atom49 = None

        atom50 = None


        DSIGM46_tree = None

        try:
            try:
                # Fcl.g:159:6: ( DSIGM atom atom atom atom )
                # Fcl.g:159:8: DSIGM atom atom atom atom
                pass
                root_0 = self._adaptor.nil()

                DSIGM46=self.match(self.input, DSIGM, self.FOLLOW_DSIGM_in_dsigm3039)

                DSIGM46_tree = self._adaptor.createWithPayload(DSIGM46)
                root_0 = self._adaptor.becomeRoot(DSIGM46_tree, root_0)

                self._state.following.append(self.FOLLOW_atom_in_dsigm3042)
                atom47 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom47.tree)
                self._state.following.append(self.FOLLOW_atom_in_dsigm3044)
                atom48 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom48.tree)
                self._state.following.append(self.FOLLOW_atom_in_dsigm3046)
                atom49 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom49.tree)
                self._state.following.append(self.FOLLOW_atom_in_dsigm3048)
                atom50 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom50.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "dsigm"

    class gauss_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.gauss_return, self).__init__()

            self.tree = None




    # $ANTLR start "gauss"
    # Fcl.g:160:1: gauss : GAUSS atom atom ;
    def gauss(self, ):

        retval = self.gauss_return()
        retval.start = self.input.LT(1)

        root_0 = None

        GAUSS51 = None
        atom52 = None

        atom53 = None


        GAUSS51_tree = None

        try:
            try:
                # Fcl.g:160:6: ( GAUSS atom atom )
                # Fcl.g:160:8: GAUSS atom atom
                pass
                root_0 = self._adaptor.nil()

                GAUSS51=self.match(self.input, GAUSS, self.FOLLOW_GAUSS_in_gauss3054)

                GAUSS51_tree = self._adaptor.createWithPayload(GAUSS51)
                root_0 = self._adaptor.becomeRoot(GAUSS51_tree, root_0)

                self._state.following.append(self.FOLLOW_atom_in_gauss3057)
                atom52 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom52.tree)
                self._state.following.append(self.FOLLOW_atom_in_gauss3059)
                atom53 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom53.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "gauss"

    class gauss2_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.gauss2_return, self).__init__()

            self.tree = None




    # $ANTLR start "gauss2"
    # Fcl.g:161:1: gauss2 : GAUSS2 atom atom atom atom ;
    def gauss2(self, ):

        retval = self.gauss2_return()
        retval.start = self.input.LT(1)

        root_0 = None

        GAUSS254 = None
        atom55 = None

        atom56 = None

        atom57 = None

        atom58 = None


        GAUSS254_tree = None

        try:
            try:
                # Fcl.g:161:7: ( GAUSS2 atom atom atom atom )
                # Fcl.g:161:9: GAUSS2 atom atom atom atom
                pass
                root_0 = self._adaptor.nil()

                GAUSS254=self.match(self.input, GAUSS2, self.FOLLOW_GAUSS2_in_gauss23065)

                GAUSS254_tree = self._adaptor.createWithPayload(GAUSS254)
                root_0 = self._adaptor.becomeRoot(GAUSS254_tree, root_0)

                self._state.following.append(self.FOLLOW_atom_in_gauss23068)
                atom55 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom55.tree)
                self._state.following.append(self.FOLLOW_atom_in_gauss23070)
                atom56 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom56.tree)
                self._state.following.append(self.FOLLOW_atom_in_gauss23072)
                atom57 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom57.tree)
                self._state.following.append(self.FOLLOW_atom_in_gauss23074)
                atom58 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom58.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "gauss2"

    class gbell_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.gbell_return, self).__init__()

            self.tree = None




    # $ANTLR start "gbell"
    # Fcl.g:162:1: gbell : GBELL atom atom atom ;
    def gbell(self, ):

        retval = self.gbell_return()
        retval.start = self.input.LT(1)

        root_0 = None

        GBELL59 = None
        atom60 = None

        atom61 = None

        atom62 = None


        GBELL59_tree = None

        try:
            try:
                # Fcl.g:162:6: ( GBELL atom atom atom )
                # Fcl.g:162:8: GBELL atom atom atom
                pass
                root_0 = self._adaptor.nil()

                GBELL59=self.match(self.input, GBELL, self.FOLLOW_GBELL_in_gbell3080)

                GBELL59_tree = self._adaptor.createWithPayload(GBELL59)
                root_0 = self._adaptor.becomeRoot(GBELL59_tree, root_0)

                self._state.following.append(self.FOLLOW_atom_in_gbell3083)
                atom60 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom60.tree)
                self._state.following.append(self.FOLLOW_atom_in_gbell3085)
                atom61 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom61.tree)
                self._state.following.append(self.FOLLOW_atom_in_gbell3087)
                atom62 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom62.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "gbell"

    class piece_wise_linear_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.piece_wise_linear_return, self).__init__()

            self.tree = None




    # $ANTLR start "piece_wise_linear"
    # Fcl.g:163:1: piece_wise_linear : ( points )+ ;
    def piece_wise_linear(self, ):

        retval = self.piece_wise_linear_return()
        retval.start = self.input.LT(1)

        root_0 = None

        points63 = None



        try:
            try:
                # Fcl.g:163:18: ( ( points )+ )
                # Fcl.g:163:20: ( points )+
                pass
                root_0 = self._adaptor.nil()

                # Fcl.g:163:20: ( points )+
                cnt10 = 0
                while True: #loop10
                    alt10 = 2
                    LA10_0 = self.input.LA(1)

                    if (LA10_0 == LEFT_PARENTHESIS) :
                        alt10 = 1


                    if alt10 == 1:
                        # Fcl.g:163:21: points
                        pass
                        self._state.following.append(self.FOLLOW_points_in_piece_wise_linear3094)
                        points63 = self.points()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, points63.tree)


                    else:
                        if cnt10 >= 1:
                            break #loop10

                        eee = EarlyExitException(10, self.input)
                        raise eee

                    cnt10 += 1



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "piece_wise_linear"

    class sigm_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.sigm_return, self).__init__()

            self.tree = None




    # $ANTLR start "sigm"
    # Fcl.g:164:1: sigm : SIGM atom atom ;
    def sigm(self, ):

        retval = self.sigm_return()
        retval.start = self.input.LT(1)

        root_0 = None

        SIGM64 = None
        atom65 = None

        atom66 = None


        SIGM64_tree = None

        try:
            try:
                # Fcl.g:164:5: ( SIGM atom atom )
                # Fcl.g:164:7: SIGM atom atom
                pass
                root_0 = self._adaptor.nil()

                SIGM64=self.match(self.input, SIGM, self.FOLLOW_SIGM_in_sigm3102)

                SIGM64_tree = self._adaptor.createWithPayload(SIGM64)
                root_0 = self._adaptor.becomeRoot(SIGM64_tree, root_0)

                self._state.following.append(self.FOLLOW_atom_in_sigm3105)
                atom65 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom65.tree)
                self._state.following.append(self.FOLLOW_atom_in_sigm3107)
                atom66 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom66.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "sigm"

    class singleton_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.singleton_return, self).__init__()

            self.tree = None




    # $ANTLR start "singleton"
    # Fcl.g:165:1: singleton : atom ;
    def singleton(self, ):

        retval = self.singleton_return()
        retval.start = self.input.LT(1)

        root_0 = None

        atom67 = None



        try:
            try:
                # Fcl.g:165:11: ( atom )
                # Fcl.g:165:13: atom
                pass
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_atom_in_singleton3114)
                atom67 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom67.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "singleton"

    class singletons_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.singletons_return, self).__init__()

            self.tree = None




    # $ANTLR start "singletons"
    # Fcl.g:166:1: singletons : SINGLETONS ( points )+ ;
    def singletons(self, ):

        retval = self.singletons_return()
        retval.start = self.input.LT(1)

        root_0 = None

        SINGLETONS68 = None
        points69 = None


        SINGLETONS68_tree = None

        try:
            try:
                # Fcl.g:166:11: ( SINGLETONS ( points )+ )
                # Fcl.g:166:13: SINGLETONS ( points )+
                pass
                root_0 = self._adaptor.nil()

                SINGLETONS68=self.match(self.input, SINGLETONS, self.FOLLOW_SINGLETONS_in_singletons3120)

                SINGLETONS68_tree = self._adaptor.createWithPayload(SINGLETONS68)
                root_0 = self._adaptor.becomeRoot(SINGLETONS68_tree, root_0)

                # Fcl.g:166:25: ( points )+
                cnt11 = 0
                while True: #loop11
                    alt11 = 2
                    LA11_0 = self.input.LA(1)

                    if (LA11_0 == LEFT_PARENTHESIS) :
                        alt11 = 1


                    if alt11 == 1:
                        # Fcl.g:166:26: points
                        pass
                        self._state.following.append(self.FOLLOW_points_in_singletons3124)
                        points69 = self.points()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, points69.tree)


                    else:
                        if cnt11 >= 1:
                            break #loop11

                        eee = EarlyExitException(11, self.input)
                        raise eee

                    cnt11 += 1



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "singletons"

    class trape_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.trape_return, self).__init__()

            self.tree = None




    # $ANTLR start "trape"
    # Fcl.g:167:1: trape : TRAPE atom atom atom atom ;
    def trape(self, ):

        retval = self.trape_return()
        retval.start = self.input.LT(1)

        root_0 = None

        TRAPE70 = None
        atom71 = None

        atom72 = None

        atom73 = None

        atom74 = None


        TRAPE70_tree = None

        try:
            try:
                # Fcl.g:167:6: ( TRAPE atom atom atom atom )
                # Fcl.g:167:8: TRAPE atom atom atom atom
                pass
                root_0 = self._adaptor.nil()

                TRAPE70=self.match(self.input, TRAPE, self.FOLLOW_TRAPE_in_trape3133)

                TRAPE70_tree = self._adaptor.createWithPayload(TRAPE70)
                root_0 = self._adaptor.becomeRoot(TRAPE70_tree, root_0)

                self._state.following.append(self.FOLLOW_atom_in_trape3136)
                atom71 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom71.tree)
                self._state.following.append(self.FOLLOW_atom_in_trape3138)
                atom72 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom72.tree)
                self._state.following.append(self.FOLLOW_atom_in_trape3140)
                atom73 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom73.tree)
                self._state.following.append(self.FOLLOW_atom_in_trape3142)
                atom74 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom74.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "trape"

    class trian_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.trian_return, self).__init__()

            self.tree = None




    # $ANTLR start "trian"
    # Fcl.g:168:1: trian : TRIAN atom atom atom ;
    def trian(self, ):

        retval = self.trian_return()
        retval.start = self.input.LT(1)

        root_0 = None

        TRIAN75 = None
        atom76 = None

        atom77 = None

        atom78 = None


        TRIAN75_tree = None

        try:
            try:
                # Fcl.g:168:6: ( TRIAN atom atom atom )
                # Fcl.g:168:8: TRIAN atom atom atom
                pass
                root_0 = self._adaptor.nil()

                TRIAN75=self.match(self.input, TRIAN, self.FOLLOW_TRIAN_in_trian3148)

                TRIAN75_tree = self._adaptor.createWithPayload(TRIAN75)
                root_0 = self._adaptor.becomeRoot(TRIAN75_tree, root_0)

                self._state.following.append(self.FOLLOW_atom_in_trian3151)
                atom76 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom76.tree)
                self._state.following.append(self.FOLLOW_atom_in_trian3153)
                atom77 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom77.tree)
                self._state.following.append(self.FOLLOW_atom_in_trian3155)
                atom78 = self.atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, atom78.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "trian"

    class points_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.points_return, self).__init__()

            self.tree = None




    # $ANTLR start "points"
    # Fcl.g:169:1: points : LEFT_PARENTHESIS x= atom COMMA y= atom RIGHT_PARENTHESIS -> ^( POINT $x $y) ;
    def points(self, ):

        retval = self.points_return()
        retval.start = self.input.LT(1)

        root_0 = None

        LEFT_PARENTHESIS79 = None
        COMMA80 = None
        RIGHT_PARENTHESIS81 = None
        x = None

        y = None


        LEFT_PARENTHESIS79_tree = None
        COMMA80_tree = None
        RIGHT_PARENTHESIS81_tree = None
        stream_RIGHT_PARENTHESIS = RewriteRuleTokenStream(self._adaptor, "token RIGHT_PARENTHESIS")
        stream_COMMA = RewriteRuleTokenStream(self._adaptor, "token COMMA")
        stream_LEFT_PARENTHESIS = RewriteRuleTokenStream(self._adaptor, "token LEFT_PARENTHESIS")
        stream_atom = RewriteRuleSubtreeStream(self._adaptor, "rule atom")
        try:
            try:
                # Fcl.g:169:8: ( LEFT_PARENTHESIS x= atom COMMA y= atom RIGHT_PARENTHESIS -> ^( POINT $x $y) )
                # Fcl.g:169:10: LEFT_PARENTHESIS x= atom COMMA y= atom RIGHT_PARENTHESIS
                pass
                LEFT_PARENTHESIS79=self.match(self.input, LEFT_PARENTHESIS, self.FOLLOW_LEFT_PARENTHESIS_in_points3162)
                stream_LEFT_PARENTHESIS.add(LEFT_PARENTHESIS79)
                self._state.following.append(self.FOLLOW_atom_in_points3166)
                x = self.atom()

                self._state.following.pop()
                stream_atom.add(x.tree)
                COMMA80=self.match(self.input, COMMA, self.FOLLOW_COMMA_in_points3168)
                stream_COMMA.add(COMMA80)
                self._state.following.append(self.FOLLOW_atom_in_points3172)
                y = self.atom()

                self._state.following.pop()
                stream_atom.add(y.tree)
                RIGHT_PARENTHESIS81=self.match(self.input, RIGHT_PARENTHESIS, self.FOLLOW_RIGHT_PARENTHESIS_in_points3174)
                stream_RIGHT_PARENTHESIS.add(RIGHT_PARENTHESIS81)

                # AST Rewrite
                # elements: x, y
                # token labels:
                # rule labels: retval, y, x
                # token list labels:
                # rule list labels:
                # wildcard labels:

                retval.tree = root_0

                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                if y is not None:
                    stream_y = RewriteRuleSubtreeStream(self._adaptor, "rule y", y.tree)
                else:
                    stream_y = RewriteRuleSubtreeStream(self._adaptor, "token y", None)


                if x is not None:
                    stream_x = RewriteRuleSubtreeStream(self._adaptor, "rule x", x.tree)
                else:
                    stream_x = RewriteRuleSubtreeStream(self._adaptor, "token x", None)


                root_0 = self._adaptor.nil()
                # 169:65: -> ^( POINT $x $y)
                # Fcl.g:169:68: ^( POINT $x $y)
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(self._adaptor.createFromType(POINT, "POINT"), root_1)

                self._adaptor.addChild(root_1, stream_x.nextTree())
                self._adaptor.addChild(root_1, stream_y.nextTree())

                self._adaptor.addChild(root_0, root_1)



                retval.tree = root_0



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "points"

    class atom_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.atom_return, self).__init__()

            self.tree = None




    # $ANTLR start "atom"
    # Fcl.g:170:1: atom : ( real | id );
    def atom(self, ):

        retval = self.atom_return()
        retval.start = self.input.LT(1)

        root_0 = None

        real82 = None

        id83 = None



        try:
            try:
                # Fcl.g:170:6: ( real | id )
                alt12 = 2
                LA12_0 = self.input.LA(1)

                if (LA12_0 == REAL) :
                    alt12 = 1
                elif (LA12_0 == ID) :
                    alt12 = 2
                else:
                    nvae = NoViableAltException("", 12, 0, self.input)

                    raise nvae

                if alt12 == 1:
                    # Fcl.g:170:9: real
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_real_in_atom3194)
                    real82 = self.real()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, real82.tree)


                elif alt12 == 2:
                    # Fcl.g:170:16: id
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_id_in_atom3198)
                    id83 = self.id()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, id83.tree)


                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "atom"

    class id_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.id_return, self).__init__()

            self.tree = None




    # $ANTLR start "id"
    # Fcl.g:171:1: id : x= ID -> ^( VALUE_ID $x) ;
    def id(self, ):

        retval = self.id_return()
        retval.start = self.input.LT(1)

        root_0 = None

        x = None

        x_tree = None
        stream_ID = RewriteRuleTokenStream(self._adaptor, "token ID")

        try:
            try:
                # Fcl.g:171:5: (x= ID -> ^( VALUE_ID $x) )
                # Fcl.g:171:9: x= ID
                pass
                x=self.match(self.input, ID, self.FOLLOW_ID_in_id3210)
                stream_ID.add(x)

                # AST Rewrite
                # elements: x
                # token labels: x
                # rule labels: retval
                # token list labels:
                # rule list labels:
                # wildcard labels:

                retval.tree = root_0
                stream_x = RewriteRuleTokenStream(self._adaptor, "token x", x)

                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 171:21: -> ^( VALUE_ID $x)
                # Fcl.g:171:25: ^( VALUE_ID $x)
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(self._adaptor.createFromType(VALUE_ID, "VALUE_ID"), root_1)

                self._adaptor.addChild(root_1, stream_x.nextNode())

                self._adaptor.addChild(root_0, root_1)



                retval.tree = root_0



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "id"

    class real_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.real_return, self).__init__()

            self.tree = None




    # $ANTLR start "real"
    # Fcl.g:172:1: real : x= REAL -> ^( VALUE_REAL $x) ;
    def real(self, ):

        retval = self.real_return()
        retval.start = self.input.LT(1)

        root_0 = None

        x = None

        x_tree = None
        stream_REAL = RewriteRuleTokenStream(self._adaptor, "token REAL")

        try:
            try:
                # Fcl.g:172:6: (x= REAL -> ^( VALUE_REAL $x) )
                # Fcl.g:172:10: x= REAL
                pass
                x=self.match(self.input, REAL, self.FOLLOW_REAL_in_real3238)
                stream_REAL.add(x)

                # AST Rewrite
                # elements: x
                # token labels: x
                # rule labels: retval
                # token list labels:
                # rule list labels:
                # wildcard labels:

                retval.tree = root_0
                stream_x = RewriteRuleTokenStream(self._adaptor, "token x", x)

                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "rule retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self._adaptor, "token retval", None)


                root_0 = self._adaptor.nil()
                # 172:21: -> ^( VALUE_REAL $x)
                # Fcl.g:172:25: ^( VALUE_REAL $x)
                root_1 = self._adaptor.nil()
                root_1 = self._adaptor.becomeRoot(self._adaptor.createFromType(VALUE_REAL, "VALUE_REAL"), root_1)

                self._adaptor.addChild(root_1, stream_x.nextNode())

                self._adaptor.addChild(root_0, root_1)



                retval.tree = root_0



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "real"

    class function_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.function_return, self).__init__()

            self.tree = None




    # $ANTLR start "function"
    # Fcl.g:174:1: function : FUNCTION fun_pm ;
    def function(self, ):

        retval = self.function_return()
        retval.start = self.input.LT(1)

        root_0 = None

        FUNCTION84 = None
        fun_pm85 = None


        FUNCTION84_tree = None

        try:
            try:
                # Fcl.g:174:9: ( FUNCTION fun_pm )
                # Fcl.g:174:11: FUNCTION fun_pm
                pass
                root_0 = self._adaptor.nil()

                FUNCTION84=self.match(self.input, FUNCTION, self.FOLLOW_FUNCTION_in_function3259)

                FUNCTION84_tree = self._adaptor.createWithPayload(FUNCTION84)
                root_0 = self._adaptor.becomeRoot(FUNCTION84_tree, root_0)

                self._state.following.append(self.FOLLOW_fun_pm_in_function3262)
                fun_pm85 = self.fun_pm()

                self._state.following.pop()
                self._adaptor.addChild(root_0, fun_pm85.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "function"

    class fun_pm_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.fun_pm_return, self).__init__()

            self.tree = None




    # $ANTLR start "fun_pm"
    # Fcl.g:175:1: fun_pm : fun_md ( ( PLUS | MINUS ) fun_md )* ;
    def fun_pm(self, ):

        retval = self.fun_pm_return()
        retval.start = self.input.LT(1)

        root_0 = None

        PLUS87 = None
        MINUS88 = None
        fun_md86 = None

        fun_md89 = None


        PLUS87_tree = None
        MINUS88_tree = None

        try:
            try:
                # Fcl.g:175:7: ( fun_md ( ( PLUS | MINUS ) fun_md )* )
                # Fcl.g:175:9: fun_md ( ( PLUS | MINUS ) fun_md )*
                pass
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_fun_md_in_fun_pm3268)
                fun_md86 = self.fun_md()

                self._state.following.pop()
                self._adaptor.addChild(root_0, fun_md86.tree)
                # Fcl.g:175:16: ( ( PLUS | MINUS ) fun_md )*
                while True: #loop14
                    alt14 = 2
                    LA14_0 = self.input.LA(1)

                    if (LA14_0 == MINUS or LA14_0 == PLUS) :
                        alt14 = 1


                    if alt14 == 1:
                        # Fcl.g:175:17: ( PLUS | MINUS ) fun_md
                        pass
                        # Fcl.g:175:17: ( PLUS | MINUS )
                        alt13 = 2
                        LA13_0 = self.input.LA(1)

                        if (LA13_0 == PLUS) :
                            alt13 = 1
                        elif (LA13_0 == MINUS) :
                            alt13 = 2
                        else:
                            nvae = NoViableAltException("", 13, 0, self.input)

                            raise nvae

                        if alt13 == 1:
                            # Fcl.g:175:18: PLUS
                            pass
                            PLUS87=self.match(self.input, PLUS, self.FOLLOW_PLUS_in_fun_pm3272)

                            PLUS87_tree = self._adaptor.createWithPayload(PLUS87)
                            root_0 = self._adaptor.becomeRoot(PLUS87_tree, root_0)



                        elif alt13 == 2:
                            # Fcl.g:175:26: MINUS
                            pass
                            MINUS88=self.match(self.input, MINUS, self.FOLLOW_MINUS_in_fun_pm3277)

                            MINUS88_tree = self._adaptor.createWithPayload(MINUS88)
                            root_0 = self._adaptor.becomeRoot(MINUS88_tree, root_0)




                        self._state.following.append(self.FOLLOW_fun_md_in_fun_pm3282)
                        fun_md89 = self.fun_md()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, fun_md89.tree)


                    else:
                        break #loop14



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "fun_pm"

    class fun_md_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.fun_md_return, self).__init__()

            self.tree = None




    # $ANTLR start "fun_md"
    # Fcl.g:176:1: fun_md : fun_mp ( ( STAR | SLASH ) fun_mp )* ;
    def fun_md(self, ):

        retval = self.fun_md_return()
        retval.start = self.input.LT(1)

        root_0 = None

        STAR91 = None
        SLASH92 = None
        fun_mp90 = None

        fun_mp93 = None


        STAR91_tree = None
        SLASH92_tree = None

        try:
            try:
                # Fcl.g:176:7: ( fun_mp ( ( STAR | SLASH ) fun_mp )* )
                # Fcl.g:176:9: fun_mp ( ( STAR | SLASH ) fun_mp )*
                pass
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_fun_mp_in_fun_md3307)
                fun_mp90 = self.fun_mp()

                self._state.following.pop()
                self._adaptor.addChild(root_0, fun_mp90.tree)
                # Fcl.g:176:16: ( ( STAR | SLASH ) fun_mp )*
                while True: #loop16
                    alt16 = 2
                    LA16_0 = self.input.LA(1)

                    if ((SLASH <= LA16_0 <= STAR)) :
                        alt16 = 1


                    if alt16 == 1:
                        # Fcl.g:176:17: ( STAR | SLASH ) fun_mp
                        pass
                        # Fcl.g:176:17: ( STAR | SLASH )
                        alt15 = 2
                        LA15_0 = self.input.LA(1)

                        if (LA15_0 == STAR) :
                            alt15 = 1
                        elif (LA15_0 == SLASH) :
                            alt15 = 2
                        else:
                            nvae = NoViableAltException("", 15, 0, self.input)

                            raise nvae

                        if alt15 == 1:
                            # Fcl.g:176:18: STAR
                            pass
                            STAR91=self.match(self.input, STAR, self.FOLLOW_STAR_in_fun_md3311)

                            STAR91_tree = self._adaptor.createWithPayload(STAR91)
                            root_0 = self._adaptor.becomeRoot(STAR91_tree, root_0)



                        elif alt15 == 2:
                            # Fcl.g:176:26: SLASH
                            pass
                            SLASH92=self.match(self.input, SLASH, self.FOLLOW_SLASH_in_fun_md3316)

                            SLASH92_tree = self._adaptor.createWithPayload(SLASH92)
                            root_0 = self._adaptor.becomeRoot(SLASH92_tree, root_0)




                        self._state.following.append(self.FOLLOW_fun_mp_in_fun_md3320)
                        fun_mp93 = self.fun_mp()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, fun_mp93.tree)


                    else:
                        break #loop16



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "fun_md"

    class fun_mp_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.fun_mp_return, self).__init__()

            self.tree = None




    # $ANTLR start "fun_mp"
    # Fcl.g:177:1: fun_mp : fun_atom ( ( HAT | PERCENT ) fun_atom )* ;
    def fun_mp(self, ):

        retval = self.fun_mp_return()
        retval.start = self.input.LT(1)

        root_0 = None

        HAT95 = None
        PERCENT96 = None
        fun_atom94 = None

        fun_atom97 = None


        HAT95_tree = None
        PERCENT96_tree = None

        try:
            try:
                # Fcl.g:177:8: ( fun_atom ( ( HAT | PERCENT ) fun_atom )* )
                # Fcl.g:177:10: fun_atom ( ( HAT | PERCENT ) fun_atom )*
                pass
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_fun_atom_in_fun_mp3347)
                fun_atom94 = self.fun_atom()

                self._state.following.pop()
                self._adaptor.addChild(root_0, fun_atom94.tree)
                # Fcl.g:177:19: ( ( HAT | PERCENT ) fun_atom )*
                while True: #loop18
                    alt18 = 2
                    LA18_0 = self.input.LA(1)

                    if (LA18_0 == HAT or LA18_0 == PERCENT) :
                        alt18 = 1


                    if alt18 == 1:
                        # Fcl.g:177:20: ( HAT | PERCENT ) fun_atom
                        pass
                        # Fcl.g:177:20: ( HAT | PERCENT )
                        alt17 = 2
                        LA17_0 = self.input.LA(1)

                        if (LA17_0 == HAT) :
                            alt17 = 1
                        elif (LA17_0 == PERCENT) :
                            alt17 = 2
                        else:
                            nvae = NoViableAltException("", 17, 0, self.input)

                            raise nvae

                        if alt17 == 1:
                            # Fcl.g:177:21: HAT
                            pass
                            HAT95=self.match(self.input, HAT, self.FOLLOW_HAT_in_fun_mp3351)

                            HAT95_tree = self._adaptor.createWithPayload(HAT95)
                            root_0 = self._adaptor.becomeRoot(HAT95_tree, root_0)



                        elif alt17 == 2:
                            # Fcl.g:177:28: PERCENT
                            pass
                            PERCENT96=self.match(self.input, PERCENT, self.FOLLOW_PERCENT_in_fun_mp3356)

                            PERCENT96_tree = self._adaptor.createWithPayload(PERCENT96)
                            root_0 = self._adaptor.becomeRoot(PERCENT96_tree, root_0)




                        self._state.following.append(self.FOLLOW_fun_atom_in_fun_mp3360)
                        fun_atom97 = self.fun_atom()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, fun_atom97.tree)


                    else:
                        break #loop18



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "fun_mp"

    class fun_atom_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.fun_atom_return, self).__init__()

            self.tree = None




    # $ANTLR start "fun_atom"
    # Fcl.g:178:1: fun_atom : ( atom | ( EXP | LN | LOG | SIN | COS | TAN | ABS )? LEFT_PARENTHESIS fun_pm RIGHT_PARENTHESIS );
    def fun_atom(self, ):

        retval = self.fun_atom_return()
        retval.start = self.input.LT(1)

        root_0 = None

        EXP99 = None
        LN100 = None
        LOG101 = None
        SIN102 = None
        COS103 = None
        TAN104 = None
        ABS105 = None
        LEFT_PARENTHESIS106 = None
        RIGHT_PARENTHESIS108 = None
        atom98 = None

        fun_pm107 = None


        EXP99_tree = None
        LN100_tree = None
        LOG101_tree = None
        SIN102_tree = None
        COS103_tree = None
        TAN104_tree = None
        ABS105_tree = None
        LEFT_PARENTHESIS106_tree = None
        RIGHT_PARENTHESIS108_tree = None

        try:
            try:
                # Fcl.g:178:10: ( atom | ( EXP | LN | LOG | SIN | COS | TAN | ABS )? LEFT_PARENTHESIS fun_pm RIGHT_PARENTHESIS )
                alt20 = 2
                LA20_0 = self.input.LA(1)

                if (LA20_0 == REAL or LA20_0 == ID) :
                    alt20 = 1
                elif (LA20_0 == ABS or LA20_0 == COS or LA20_0 == EXP or (LN <= LA20_0 <= LOG) or LA20_0 == SIN or LA20_0 == TAN or LA20_0 == LEFT_PARENTHESIS) :
                    alt20 = 2
                else:
                    nvae = NoViableAltException("", 20, 0, self.input)

                    raise nvae

                if alt20 == 1:
                    # Fcl.g:178:12: atom
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_atom_in_fun_atom3389)
                    atom98 = self.atom()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, atom98.tree)


                elif alt20 == 2:
                    # Fcl.g:178:19: ( EXP | LN | LOG | SIN | COS | TAN | ABS )? LEFT_PARENTHESIS fun_pm RIGHT_PARENTHESIS
                    pass
                    root_0 = self._adaptor.nil()

                    # Fcl.g:178:19: ( EXP | LN | LOG | SIN | COS | TAN | ABS )?
                    alt19 = 8
                    LA19 = self.input.LA(1)
                    if LA19 == EXP:
                        alt19 = 1
                    elif LA19 == LN:
                        alt19 = 2
                    elif LA19 == LOG:
                        alt19 = 3
                    elif LA19 == SIN:
                        alt19 = 4
                    elif LA19 == COS:
                        alt19 = 5
                    elif LA19 == TAN:
                        alt19 = 6
                    elif LA19 == ABS:
                        alt19 = 7
                    if alt19 == 1:
                        # Fcl.g:178:20: EXP
                        pass
                        EXP99=self.match(self.input, EXP, self.FOLLOW_EXP_in_fun_atom3394)

                        EXP99_tree = self._adaptor.createWithPayload(EXP99)
                        root_0 = self._adaptor.becomeRoot(EXP99_tree, root_0)



                    elif alt19 == 2:
                        # Fcl.g:178:25: LN
                        pass
                        LN100=self.match(self.input, LN, self.FOLLOW_LN_in_fun_atom3397)

                        LN100_tree = self._adaptor.createWithPayload(LN100)
                        root_0 = self._adaptor.becomeRoot(LN100_tree, root_0)



                    elif alt19 == 3:
                        # Fcl.g:178:29: LOG
                        pass
                        LOG101=self.match(self.input, LOG, self.FOLLOW_LOG_in_fun_atom3400)

                        LOG101_tree = self._adaptor.createWithPayload(LOG101)
                        root_0 = self._adaptor.becomeRoot(LOG101_tree, root_0)



                    elif alt19 == 4:
                        # Fcl.g:178:34: SIN
                        pass
                        SIN102=self.match(self.input, SIN, self.FOLLOW_SIN_in_fun_atom3403)

                        SIN102_tree = self._adaptor.createWithPayload(SIN102)
                        root_0 = self._adaptor.becomeRoot(SIN102_tree, root_0)



                    elif alt19 == 5:
                        # Fcl.g:178:39: COS
                        pass
                        COS103=self.match(self.input, COS, self.FOLLOW_COS_in_fun_atom3406)

                        COS103_tree = self._adaptor.createWithPayload(COS103)
                        root_0 = self._adaptor.becomeRoot(COS103_tree, root_0)



                    elif alt19 == 6:
                        # Fcl.g:178:44: TAN
                        pass
                        TAN104=self.match(self.input, TAN, self.FOLLOW_TAN_in_fun_atom3409)

                        TAN104_tree = self._adaptor.createWithPayload(TAN104)
                        root_0 = self._adaptor.becomeRoot(TAN104_tree, root_0)



                    elif alt19 == 7:
                        # Fcl.g:178:49: ABS
                        pass
                        ABS105=self.match(self.input, ABS, self.FOLLOW_ABS_in_fun_atom3412)

                        ABS105_tree = self._adaptor.createWithPayload(ABS105)
                        root_0 = self._adaptor.becomeRoot(ABS105_tree, root_0)




                    LEFT_PARENTHESIS106=self.match(self.input, LEFT_PARENTHESIS, self.FOLLOW_LEFT_PARENTHESIS_in_fun_atom3417)
                    self._state.following.append(self.FOLLOW_fun_pm_in_fun_atom3420)
                    fun_pm107 = self.fun_pm()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, fun_pm107.tree)
                    RIGHT_PARENTHESIS108=self.match(self.input, RIGHT_PARENTHESIS, self.FOLLOW_RIGHT_PARENTHESIS_in_fun_atom3422)


                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "fun_atom"

    class defuzzify_block_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.defuzzify_block_return, self).__init__()

            self.tree = None




    # $ANTLR start "defuzzify_block"
    # Fcl.g:180:1: defuzzify_block : DEFUZZIFY ID ( defuzzify_item )* END_DEFUZZIFY ;
    def defuzzify_block(self, ):

        retval = self.defuzzify_block_return()
        retval.start = self.input.LT(1)

        root_0 = None

        DEFUZZIFY109 = None
        ID110 = None
        END_DEFUZZIFY112 = None
        defuzzify_item111 = None


        DEFUZZIFY109_tree = None
        ID110_tree = None
        END_DEFUZZIFY112_tree = None

        try:
            try:
                # Fcl.g:180:17: ( DEFUZZIFY ID ( defuzzify_item )* END_DEFUZZIFY )
                # Fcl.g:180:19: DEFUZZIFY ID ( defuzzify_item )* END_DEFUZZIFY
                pass
                root_0 = self._adaptor.nil()

                DEFUZZIFY109=self.match(self.input, DEFUZZIFY, self.FOLLOW_DEFUZZIFY_in_defuzzify_block3432)

                DEFUZZIFY109_tree = self._adaptor.createWithPayload(DEFUZZIFY109)
                root_0 = self._adaptor.becomeRoot(DEFUZZIFY109_tree, root_0)

                ID110=self.match(self.input, ID, self.FOLLOW_ID_in_defuzzify_block3435)

                ID110_tree = self._adaptor.createWithPayload(ID110)
                self._adaptor.addChild(root_0, ID110_tree)

                # Fcl.g:180:33: ( defuzzify_item )*
                while True: #loop21
                    alt21 = 2
                    LA21_0 = self.input.LA(1)

                    if (LA21_0 == DEFAULT or LA21_0 == METHOD or LA21_0 == RANGE or LA21_0 == TERM) :
                        alt21 = 1


                    if alt21 == 1:
                        # Fcl.g:180:34: defuzzify_item
                        pass
                        self._state.following.append(self.FOLLOW_defuzzify_item_in_defuzzify_block3438)
                        defuzzify_item111 = self.defuzzify_item()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, defuzzify_item111.tree)


                    else:
                        break #loop21
                END_DEFUZZIFY112=self.match(self.input, END_DEFUZZIFY, self.FOLLOW_END_DEFUZZIFY_in_defuzzify_block3442)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "defuzzify_block"

    class defuzzify_item_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.defuzzify_item_return, self).__init__()

            self.tree = None




    # $ANTLR start "defuzzify_item"
    # Fcl.g:181:1: defuzzify_item : ( defuzzification_method | default_value | linguistic_term | range );
    def defuzzify_item(self, ):

        retval = self.defuzzify_item_return()
        retval.start = self.input.LT(1)

        root_0 = None

        defuzzification_method113 = None

        default_value114 = None

        linguistic_term115 = None

        range116 = None



        try:
            try:
                # Fcl.g:181:16: ( defuzzification_method | default_value | linguistic_term | range )
                alt22 = 4
                LA22 = self.input.LA(1)
                if LA22 == METHOD:
                    alt22 = 1
                elif LA22 == DEFAULT:
                    alt22 = 2
                elif LA22 == TERM:
                    alt22 = 3
                elif LA22 == RANGE:
                    alt22 = 4
                else:
                    nvae = NoViableAltException("", 22, 0, self.input)

                    raise nvae

                if alt22 == 1:
                    # Fcl.g:181:18: defuzzification_method
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_defuzzification_method_in_defuzzify_item3450)
                    defuzzification_method113 = self.defuzzification_method()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, defuzzification_method113.tree)


                elif alt22 == 2:
                    # Fcl.g:181:43: default_value
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_default_value_in_defuzzify_item3454)
                    default_value114 = self.default_value()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, default_value114.tree)


                elif alt22 == 3:
                    # Fcl.g:181:59: linguistic_term
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_linguistic_term_in_defuzzify_item3458)
                    linguistic_term115 = self.linguistic_term()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, linguistic_term115.tree)


                elif alt22 == 4:
                    # Fcl.g:181:77: range
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_range_in_defuzzify_item3462)
                    range116 = self.range()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, range116.tree)


                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "defuzzify_item"

    class range_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.range_return, self).__init__()

            self.tree = None




    # $ANTLR start "range"
    # Fcl.g:182:1: range : RANGE ASSIGN_OPERATOR LEFT_PARENTHESIS REAL DOTS REAL RIGHT_PARENTHESIS SEMICOLON ;
    def range(self, ):

        retval = self.range_return()
        retval.start = self.input.LT(1)

        root_0 = None

        RANGE117 = None
        ASSIGN_OPERATOR118 = None
        LEFT_PARENTHESIS119 = None
        REAL120 = None
        DOTS121 = None
        REAL122 = None
        RIGHT_PARENTHESIS123 = None
        SEMICOLON124 = None

        RANGE117_tree = None
        ASSIGN_OPERATOR118_tree = None
        LEFT_PARENTHESIS119_tree = None
        REAL120_tree = None
        DOTS121_tree = None
        REAL122_tree = None
        RIGHT_PARENTHESIS123_tree = None
        SEMICOLON124_tree = None

        try:
            try:
                # Fcl.g:182:7: ( RANGE ASSIGN_OPERATOR LEFT_PARENTHESIS REAL DOTS REAL RIGHT_PARENTHESIS SEMICOLON )
                # Fcl.g:182:9: RANGE ASSIGN_OPERATOR LEFT_PARENTHESIS REAL DOTS REAL RIGHT_PARENTHESIS SEMICOLON
                pass
                root_0 = self._adaptor.nil()

                RANGE117=self.match(self.input, RANGE, self.FOLLOW_RANGE_in_range3469)

                RANGE117_tree = self._adaptor.createWithPayload(RANGE117)
                root_0 = self._adaptor.becomeRoot(RANGE117_tree, root_0)

                ASSIGN_OPERATOR118=self.match(self.input, ASSIGN_OPERATOR, self.FOLLOW_ASSIGN_OPERATOR_in_range3472)
                LEFT_PARENTHESIS119=self.match(self.input, LEFT_PARENTHESIS, self.FOLLOW_LEFT_PARENTHESIS_in_range3475)
                REAL120=self.match(self.input, REAL, self.FOLLOW_REAL_in_range3478)

                REAL120_tree = self._adaptor.createWithPayload(REAL120)
                self._adaptor.addChild(root_0, REAL120_tree)

                DOTS121=self.match(self.input, DOTS, self.FOLLOW_DOTS_in_range3480)
                REAL122=self.match(self.input, REAL, self.FOLLOW_REAL_in_range3483)

                REAL122_tree = self._adaptor.createWithPayload(REAL122)
                self._adaptor.addChild(root_0, REAL122_tree)

                RIGHT_PARENTHESIS123=self.match(self.input, RIGHT_PARENTHESIS, self.FOLLOW_RIGHT_PARENTHESIS_in_range3485)
                SEMICOLON124=self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_range3488)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "range"

    class defuzzification_method_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.defuzzification_method_return, self).__init__()

            self.tree = None




    # $ANTLR start "defuzzification_method"
    # Fcl.g:183:1: defuzzification_method : METHOD COLON ( COG | COGS | COGF | COA | LM | RM | MM ) SEMICOLON ;
    def defuzzification_method(self, ):

        retval = self.defuzzification_method_return()
        retval.start = self.input.LT(1)

        root_0 = None

        METHOD125 = None
        COLON126 = None
        set127 = None
        SEMICOLON128 = None

        METHOD125_tree = None
        COLON126_tree = None
        set127_tree = None
        SEMICOLON128_tree = None

        try:
            try:
                # Fcl.g:183:24: ( METHOD COLON ( COG | COGS | COGF | COA | LM | RM | MM ) SEMICOLON )
                # Fcl.g:183:26: METHOD COLON ( COG | COGS | COGF | COA | LM | RM | MM ) SEMICOLON
                pass
                root_0 = self._adaptor.nil()

                METHOD125=self.match(self.input, METHOD, self.FOLLOW_METHOD_in_defuzzification_method3496)

                METHOD125_tree = self._adaptor.createWithPayload(METHOD125)
                root_0 = self._adaptor.becomeRoot(METHOD125_tree, root_0)

                COLON126=self.match(self.input, COLON, self.FOLLOW_COLON_in_defuzzification_method3499)
                set127 = self.input.LT(1)
                if self.input.LA(1) == COA or (COG <= self.input.LA(1) <= COGF) or self.input.LA(1) == LM or self.input.LA(1) == MM or self.input.LA(1) == RM:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set127))
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse


                SEMICOLON128=self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_defuzzification_method3518)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "defuzzification_method"

    class default_value_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.default_value_return, self).__init__()

            self.tree = None




    # $ANTLR start "default_value"
    # Fcl.g:184:1: default_value : DEFAULT ASSIGN_OPERATOR ( REAL | NC ) SEMICOLON ;
    def default_value(self, ):

        retval = self.default_value_return()
        retval.start = self.input.LT(1)

        root_0 = None

        DEFAULT129 = None
        ASSIGN_OPERATOR130 = None
        set131 = None
        SEMICOLON132 = None

        DEFAULT129_tree = None
        ASSIGN_OPERATOR130_tree = None
        set131_tree = None
        SEMICOLON132_tree = None

        try:
            try:
                # Fcl.g:184:15: ( DEFAULT ASSIGN_OPERATOR ( REAL | NC ) SEMICOLON )
                # Fcl.g:184:17: DEFAULT ASSIGN_OPERATOR ( REAL | NC ) SEMICOLON
                pass
                root_0 = self._adaptor.nil()

                DEFAULT129=self.match(self.input, DEFAULT, self.FOLLOW_DEFAULT_in_default_value3526)

                DEFAULT129_tree = self._adaptor.createWithPayload(DEFAULT129)
                root_0 = self._adaptor.becomeRoot(DEFAULT129_tree, root_0)

                ASSIGN_OPERATOR130=self.match(self.input, ASSIGN_OPERATOR, self.FOLLOW_ASSIGN_OPERATOR_in_default_value3529)
                set131 = self.input.LT(1)
                if self.input.LA(1) == NC or self.input.LA(1) == REAL:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set131))
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse


                SEMICOLON132=self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_default_value3540)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "default_value"

    class rule_block_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.rule_block_return, self).__init__()

            self.tree = None




    # $ANTLR start "rule_block"
    # Fcl.g:186:1: rule_block : RULEBLOCK ID ( rule_item )* END_RULEBLOCK ;
    def rule_block(self, ):

        retval = self.rule_block_return()
        retval.start = self.input.LT(1)

        root_0 = None

        RULEBLOCK133 = None
        ID134 = None
        END_RULEBLOCK136 = None
        rule_item135 = None


        RULEBLOCK133_tree = None
        ID134_tree = None
        END_RULEBLOCK136_tree = None

        try:
            try:
                # Fcl.g:186:12: ( RULEBLOCK ID ( rule_item )* END_RULEBLOCK )
                # Fcl.g:186:14: RULEBLOCK ID ( rule_item )* END_RULEBLOCK
                pass
                root_0 = self._adaptor.nil()

                RULEBLOCK133=self.match(self.input, RULEBLOCK, self.FOLLOW_RULEBLOCK_in_rule_block3549)

                RULEBLOCK133_tree = self._adaptor.createWithPayload(RULEBLOCK133)
                root_0 = self._adaptor.becomeRoot(RULEBLOCK133_tree, root_0)

                ID134=self.match(self.input, ID, self.FOLLOW_ID_in_rule_block3552)

                ID134_tree = self._adaptor.createWithPayload(ID134)
                self._adaptor.addChild(root_0, ID134_tree)

                # Fcl.g:186:28: ( rule_item )*
                while True: #loop23
                    alt23 = 2
                    LA23_0 = self.input.LA(1)

                    if ((ACCU <= LA23_0 <= AND) or LA23_0 == OR or LA23_0 == RULE) :
                        alt23 = 1


                    if alt23 == 1:
                        # Fcl.g:186:29: rule_item
                        pass
                        self._state.following.append(self.FOLLOW_rule_item_in_rule_block3555)
                        rule_item135 = self.rule_item()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, rule_item135.tree)


                    else:
                        break #loop23
                END_RULEBLOCK136=self.match(self.input, END_RULEBLOCK, self.FOLLOW_END_RULEBLOCK_in_rule_block3559)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "rule_block"

    class rule_item_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.rule_item_return, self).__init__()

            self.tree = None




    # $ANTLR start "rule_item"
    # Fcl.g:187:1: rule_item : ( operator_definition | activation_method | accumulation_method | rule );
    def rule_item(self, ):

        retval = self.rule_item_return()
        retval.start = self.input.LT(1)

        root_0 = None

        operator_definition137 = None

        activation_method138 = None

        accumulation_method139 = None

        rule140 = None



        try:
            try:
                # Fcl.g:187:11: ( operator_definition | activation_method | accumulation_method | rule )
                alt24 = 4
                LA24 = self.input.LA(1)
                if LA24 == AND or LA24 == OR:
                    alt24 = 1
                elif LA24 == ACT:
                    alt24 = 2
                elif LA24 == ACCU:
                    alt24 = 3
                elif LA24 == RULE:
                    alt24 = 4
                else:
                    nvae = NoViableAltException("", 24, 0, self.input)

                    raise nvae

                if alt24 == 1:
                    # Fcl.g:187:13: operator_definition
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_operator_definition_in_rule_item3567)
                    operator_definition137 = self.operator_definition()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, operator_definition137.tree)


                elif alt24 == 2:
                    # Fcl.g:187:35: activation_method
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_activation_method_in_rule_item3571)
                    activation_method138 = self.activation_method()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, activation_method138.tree)


                elif alt24 == 3:
                    # Fcl.g:187:55: accumulation_method
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_accumulation_method_in_rule_item3575)
                    accumulation_method139 = self.accumulation_method()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, accumulation_method139.tree)


                elif alt24 == 4:
                    # Fcl.g:187:77: rule
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_rule_in_rule_item3579)
                    rule140 = self.rule()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, rule140.tree)


                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "rule_item"

    class operator_definition_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.operator_definition_return, self).__init__()

            self.tree = None




    # $ANTLR start "operator_definition"
    # Fcl.g:188:1: operator_definition : ( operator_definition_or | operator_definition_and );
    def operator_definition(self, ):

        retval = self.operator_definition_return()
        retval.start = self.input.LT(1)

        root_0 = None

        operator_definition_or141 = None

        operator_definition_and142 = None



        try:
            try:
                # Fcl.g:188:21: ( operator_definition_or | operator_definition_and )
                alt25 = 2
                LA25_0 = self.input.LA(1)

                if (LA25_0 == OR) :
                    alt25 = 1
                elif (LA25_0 == AND) :
                    alt25 = 2
                else:
                    nvae = NoViableAltException("", 25, 0, self.input)

                    raise nvae

                if alt25 == 1:
                    # Fcl.g:188:23: operator_definition_or
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_operator_definition_or_in_operator_definition3586)
                    operator_definition_or141 = self.operator_definition_or()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, operator_definition_or141.tree)


                elif alt25 == 2:
                    # Fcl.g:188:48: operator_definition_and
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_operator_definition_and_in_operator_definition3590)
                    operator_definition_and142 = self.operator_definition_and()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, operator_definition_and142.tree)


                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "operator_definition"

    class operator_definition_or_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.operator_definition_or_return, self).__init__()

            self.tree = None




    # $ANTLR start "operator_definition_or"
    # Fcl.g:189:1: operator_definition_or : OR COLON ( MAX | ASUM | BSUM | DMAX | NIPMAX | EINSTEIN ) SEMICOLON ;
    def operator_definition_or(self, ):

        retval = self.operator_definition_or_return()
        retval.start = self.input.LT(1)

        root_0 = None

        OR143 = None
        COLON144 = None
        set145 = None
        SEMICOLON146 = None

        OR143_tree = None
        COLON144_tree = None
        set145_tree = None
        SEMICOLON146_tree = None

        try:
            try:
                # Fcl.g:189:24: ( OR COLON ( MAX | ASUM | BSUM | DMAX | NIPMAX | EINSTEIN ) SEMICOLON )
                # Fcl.g:189:26: OR COLON ( MAX | ASUM | BSUM | DMAX | NIPMAX | EINSTEIN ) SEMICOLON
                pass
                root_0 = self._adaptor.nil()

                OR143=self.match(self.input, OR, self.FOLLOW_OR_in_operator_definition_or3597)

                OR143_tree = self._adaptor.createWithPayload(OR143)
                root_0 = self._adaptor.becomeRoot(OR143_tree, root_0)

                COLON144=self.match(self.input, COLON, self.FOLLOW_COLON_in_operator_definition_or3600)
                set145 = self.input.LT(1)
                if self.input.LA(1) == ASUM or self.input.LA(1) == BSUM or self.input.LA(1) == DMAX or self.input.LA(1) == EINSTEIN or self.input.LA(1) == MAX or self.input.LA(1) == NIPMAX:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set145))
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse


                SEMICOLON146=self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_operator_definition_or3617)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "operator_definition_or"

    class operator_definition_and_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.operator_definition_and_return, self).__init__()

            self.tree = None




    # $ANTLR start "operator_definition_and"
    # Fcl.g:190:1: operator_definition_and : AND COLON ( MIN | PROD | BDIF | DMIN | NIPMIN | HAMACHER ) SEMICOLON ;
    def operator_definition_and(self, ):

        retval = self.operator_definition_and_return()
        retval.start = self.input.LT(1)

        root_0 = None

        AND147 = None
        COLON148 = None
        set149 = None
        SEMICOLON150 = None

        AND147_tree = None
        COLON148_tree = None
        set149_tree = None
        SEMICOLON150_tree = None

        try:
            try:
                # Fcl.g:190:25: ( AND COLON ( MIN | PROD | BDIF | DMIN | NIPMIN | HAMACHER ) SEMICOLON )
                # Fcl.g:190:27: AND COLON ( MIN | PROD | BDIF | DMIN | NIPMIN | HAMACHER ) SEMICOLON
                pass
                root_0 = self._adaptor.nil()

                AND147=self.match(self.input, AND, self.FOLLOW_AND_in_operator_definition_and3625)

                AND147_tree = self._adaptor.createWithPayload(AND147)
                root_0 = self._adaptor.becomeRoot(AND147_tree, root_0)

                COLON148=self.match(self.input, COLON, self.FOLLOW_COLON_in_operator_definition_and3628)
                set149 = self.input.LT(1)
                if self.input.LA(1) == BDIF or self.input.LA(1) == DMIN or self.input.LA(1) == HAMACHER or (MIN <= self.input.LA(1) <= NIPMIN) or self.input.LA(1) == PROD:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set149))
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse


                SEMICOLON150=self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_operator_definition_and3645)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "operator_definition_and"

    class activation_method_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.activation_method_return, self).__init__()

            self.tree = None




    # $ANTLR start "activation_method"
    # Fcl.g:191:1: activation_method : ACT COLON ( PROD | MIN ) SEMICOLON ;
    def activation_method(self, ):

        retval = self.activation_method_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ACT151 = None
        COLON152 = None
        set153 = None
        SEMICOLON154 = None

        ACT151_tree = None
        COLON152_tree = None
        set153_tree = None
        SEMICOLON154_tree = None

        try:
            try:
                # Fcl.g:191:19: ( ACT COLON ( PROD | MIN ) SEMICOLON )
                # Fcl.g:191:21: ACT COLON ( PROD | MIN ) SEMICOLON
                pass
                root_0 = self._adaptor.nil()

                ACT151=self.match(self.input, ACT, self.FOLLOW_ACT_in_activation_method3653)

                ACT151_tree = self._adaptor.createWithPayload(ACT151)
                root_0 = self._adaptor.becomeRoot(ACT151_tree, root_0)

                COLON152=self.match(self.input, COLON, self.FOLLOW_COLON_in_activation_method3656)
                set153 = self.input.LT(1)
                if self.input.LA(1) == MIN or self.input.LA(1) == PROD:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set153))
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse


                SEMICOLON154=self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_activation_method3665)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "activation_method"

    class accumulation_method_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.accumulation_method_return, self).__init__()

            self.tree = None




    # $ANTLR start "accumulation_method"
    # Fcl.g:192:1: accumulation_method : ACCU COLON ( MAX | BSUM | NSUM | PROBOR | SUM ) SEMICOLON ;
    def accumulation_method(self, ):

        retval = self.accumulation_method_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ACCU155 = None
        COLON156 = None
        set157 = None
        SEMICOLON158 = None

        ACCU155_tree = None
        COLON156_tree = None
        set157_tree = None
        SEMICOLON158_tree = None

        try:
            try:
                # Fcl.g:192:21: ( ACCU COLON ( MAX | BSUM | NSUM | PROBOR | SUM ) SEMICOLON )
                # Fcl.g:192:23: ACCU COLON ( MAX | BSUM | NSUM | PROBOR | SUM ) SEMICOLON
                pass
                root_0 = self._adaptor.nil()

                ACCU155=self.match(self.input, ACCU, self.FOLLOW_ACCU_in_accumulation_method3673)

                ACCU155_tree = self._adaptor.createWithPayload(ACCU155)
                root_0 = self._adaptor.becomeRoot(ACCU155_tree, root_0)

                COLON156=self.match(self.input, COLON, self.FOLLOW_COLON_in_accumulation_method3676)
                set157 = self.input.LT(1)
                if self.input.LA(1) == BSUM or self.input.LA(1) == MAX or self.input.LA(1) == NSUM or self.input.LA(1) == PROBOR or self.input.LA(1) == SUM:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set157))
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse


                SEMICOLON158=self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_accumulation_method3691)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "accumulation_method"

    class rule_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.rule_return, self).__init__()

            self.tree = None




    # $ANTLR start "rule"
    # Fcl.g:193:1: rule : RULE rule_name COLON if_clause then_clause ( with_x )? SEMICOLON ;
    def rule(self, ):

        retval = self.rule_return()
        retval.start = self.input.LT(1)

        root_0 = None

        RULE159 = None
        COLON161 = None
        SEMICOLON165 = None
        rule_name160 = None

        if_clause162 = None

        then_clause163 = None

        with_x164 = None


        RULE159_tree = None
        COLON161_tree = None
        SEMICOLON165_tree = None

        try:
            try:
                # Fcl.g:193:6: ( RULE rule_name COLON if_clause then_clause ( with_x )? SEMICOLON )
                # Fcl.g:193:8: RULE rule_name COLON if_clause then_clause ( with_x )? SEMICOLON
                pass
                root_0 = self._adaptor.nil()

                RULE159=self.match(self.input, RULE, self.FOLLOW_RULE_in_rule3699)

                RULE159_tree = self._adaptor.createWithPayload(RULE159)
                root_0 = self._adaptor.becomeRoot(RULE159_tree, root_0)

                self._state.following.append(self.FOLLOW_rule_name_in_rule3702)
                rule_name160 = self.rule_name()

                self._state.following.pop()
                self._adaptor.addChild(root_0, rule_name160.tree)
                COLON161=self.match(self.input, COLON, self.FOLLOW_COLON_in_rule3704)
                self._state.following.append(self.FOLLOW_if_clause_in_rule3707)
                if_clause162 = self.if_clause()

                self._state.following.pop()
                self._adaptor.addChild(root_0, if_clause162.tree)
                self._state.following.append(self.FOLLOW_then_clause_in_rule3709)
                then_clause163 = self.then_clause()

                self._state.following.pop()
                self._adaptor.addChild(root_0, then_clause163.tree)
                # Fcl.g:193:53: ( with_x )?
                alt26 = 2
                LA26_0 = self.input.LA(1)

                if (LA26_0 == WITH) :
                    alt26 = 1
                if alt26 == 1:
                    # Fcl.g:193:54: with_x
                    pass
                    self._state.following.append(self.FOLLOW_with_x_in_rule3712)
                    with_x164 = self.with_x()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, with_x164.tree)



                SEMICOLON165=self.match(self.input, SEMICOLON, self.FOLLOW_SEMICOLON_in_rule3716)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "rule"

    class rule_name_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.rule_name_return, self).__init__()

            self.tree = None




    # $ANTLR start "rule_name"
    # Fcl.g:194:1: rule_name : ( ID | REAL );
    def rule_name(self, ):

        retval = self.rule_name_return()
        retval.start = self.input.LT(1)

        root_0 = None

        set166 = None

        set166_tree = None

        try:
            try:
                # Fcl.g:194:11: ( ID | REAL )
                # Fcl.g:
                pass
                root_0 = self._adaptor.nil()

                set166 = self.input.LT(1)
                if self.input.LA(1) == REAL or self.input.LA(1) == ID:
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set166))
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "rule_name"

    class if_clause_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.if_clause_return, self).__init__()

            self.tree = None




    # $ANTLR start "if_clause"
    # Fcl.g:195:1: if_clause : IF condition ;
    def if_clause(self, ):

        retval = self.if_clause_return()
        retval.start = self.input.LT(1)

        root_0 = None

        IF167 = None
        condition168 = None


        IF167_tree = None

        try:
            try:
                # Fcl.g:195:11: ( IF condition )
                # Fcl.g:195:13: IF condition
                pass
                root_0 = self._adaptor.nil()

                IF167=self.match(self.input, IF, self.FOLLOW_IF_in_if_clause3736)

                IF167_tree = self._adaptor.createWithPayload(IF167)
                root_0 = self._adaptor.becomeRoot(IF167_tree, root_0)

                self._state.following.append(self.FOLLOW_condition_in_if_clause3739)
                condition168 = self.condition()

                self._state.following.pop()
                self._adaptor.addChild(root_0, condition168.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "if_clause"

    class then_clause_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.then_clause_return, self).__init__()

            self.tree = None




    # $ANTLR start "then_clause"
    # Fcl.g:196:1: then_clause : THEN conclusion ;
    def then_clause(self, ):

        retval = self.then_clause_return()
        retval.start = self.input.LT(1)

        root_0 = None

        THEN169 = None
        conclusion170 = None


        THEN169_tree = None

        try:
            try:
                # Fcl.g:196:13: ( THEN conclusion )
                # Fcl.g:196:15: THEN conclusion
                pass
                root_0 = self._adaptor.nil()

                THEN169=self.match(self.input, THEN, self.FOLLOW_THEN_in_then_clause3746)

                THEN169_tree = self._adaptor.createWithPayload(THEN169)
                root_0 = self._adaptor.becomeRoot(THEN169_tree, root_0)

                self._state.following.append(self.FOLLOW_conclusion_in_then_clause3749)
                conclusion170 = self.conclusion()

                self._state.following.pop()
                self._adaptor.addChild(root_0, conclusion170.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "then_clause"

    class condition_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.condition_return, self).__init__()

            self.tree = None




    # $ANTLR start "condition"
    # Fcl.g:197:1: condition : subcondition ( ( AND | OR ) subcondition )* ;
    def condition(self, ):

        retval = self.condition_return()
        retval.start = self.input.LT(1)

        root_0 = None

        AND172 = None
        OR173 = None
        subcondition171 = None

        subcondition174 = None


        AND172_tree = None
        OR173_tree = None

        try:
            try:
                # Fcl.g:197:11: ( subcondition ( ( AND | OR ) subcondition )* )
                # Fcl.g:197:13: subcondition ( ( AND | OR ) subcondition )*
                pass
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_subcondition_in_condition3756)
                subcondition171 = self.subcondition()

                self._state.following.pop()
                self._adaptor.addChild(root_0, subcondition171.tree)
                # Fcl.g:197:26: ( ( AND | OR ) subcondition )*
                while True: #loop28
                    alt28 = 2
                    LA28_0 = self.input.LA(1)

                    if (LA28_0 == AND or LA28_0 == OR) :
                        alt28 = 1


                    if alt28 == 1:
                        # Fcl.g:197:27: ( AND | OR ) subcondition
                        pass
                        # Fcl.g:197:27: ( AND | OR )
                        alt27 = 2
                        LA27_0 = self.input.LA(1)

                        if (LA27_0 == AND) :
                            alt27 = 1
                        elif (LA27_0 == OR) :
                            alt27 = 2
                        else:
                            nvae = NoViableAltException("", 27, 0, self.input)

                            raise nvae

                        if alt27 == 1:
                            # Fcl.g:197:28: AND
                            pass
                            AND172=self.match(self.input, AND, self.FOLLOW_AND_in_condition3760)

                            AND172_tree = self._adaptor.createWithPayload(AND172)
                            root_0 = self._adaptor.becomeRoot(AND172_tree, root_0)



                        elif alt27 == 2:
                            # Fcl.g:197:33: OR
                            pass
                            OR173=self.match(self.input, OR, self.FOLLOW_OR_in_condition3763)

                            OR173_tree = self._adaptor.createWithPayload(OR173)
                            root_0 = self._adaptor.becomeRoot(OR173_tree, root_0)




                        self._state.following.append(self.FOLLOW_subcondition_in_condition3767)
                        subcondition174 = self.subcondition()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, subcondition174.tree)


                    else:
                        break #loop28



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "condition"

    class subcondition_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.subcondition_return, self).__init__()

            self.tree = None




    # $ANTLR start "subcondition"
    # Fcl.g:198:1: subcondition : ( NOT )? ( subcondition_bare | subcondition_paren ) ;
    def subcondition(self, ):

        retval = self.subcondition_return()
        retval.start = self.input.LT(1)

        root_0 = None

        NOT175 = None
        subcondition_bare176 = None

        subcondition_paren177 = None


        NOT175_tree = None

        try:
            try:
                # Fcl.g:198:14: ( ( NOT )? ( subcondition_bare | subcondition_paren ) )
                # Fcl.g:198:16: ( NOT )? ( subcondition_bare | subcondition_paren )
                pass
                root_0 = self._adaptor.nil()

                # Fcl.g:198:16: ( NOT )?
                alt29 = 2
                LA29_0 = self.input.LA(1)

                if (LA29_0 == NOT) :
                    alt29 = 1
                if alt29 == 1:
                    # Fcl.g:198:17: NOT
                    pass
                    NOT175=self.match(self.input, NOT, self.FOLLOW_NOT_in_subcondition3777)

                    NOT175_tree = self._adaptor.createWithPayload(NOT175)
                    root_0 = self._adaptor.becomeRoot(NOT175_tree, root_0)




                # Fcl.g:198:24: ( subcondition_bare | subcondition_paren )
                alt30 = 2
                LA30_0 = self.input.LA(1)

                if (LA30_0 == ID) :
                    alt30 = 1
                elif (LA30_0 == LEFT_PARENTHESIS) :
                    alt30 = 2
                else:
                    nvae = NoViableAltException("", 30, 0, self.input)

                    raise nvae

                if alt30 == 1:
                    # Fcl.g:198:25: subcondition_bare
                    pass
                    self._state.following.append(self.FOLLOW_subcondition_bare_in_subcondition3783)
                    subcondition_bare176 = self.subcondition_bare()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, subcondition_bare176.tree)


                elif alt30 == 2:
                    # Fcl.g:198:45: subcondition_paren
                    pass
                    self._state.following.append(self.FOLLOW_subcondition_paren_in_subcondition3787)
                    subcondition_paren177 = self.subcondition_paren()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, subcondition_paren177.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "subcondition"

    class subcondition_bare_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.subcondition_bare_return, self).__init__()

            self.tree = None




    # $ANTLR start "subcondition_bare"
    # Fcl.g:199:1: subcondition_bare : ID ( IS ( NOT )? ID )? ;
    def subcondition_bare(self, ):

        retval = self.subcondition_bare_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID178 = None
        IS179 = None
        NOT180 = None
        ID181 = None

        ID178_tree = None
        IS179_tree = None
        NOT180_tree = None
        ID181_tree = None

        try:
            try:
                # Fcl.g:199:19: ( ID ( IS ( NOT )? ID )? )
                # Fcl.g:199:21: ID ( IS ( NOT )? ID )?
                pass
                root_0 = self._adaptor.nil()

                ID178=self.match(self.input, ID, self.FOLLOW_ID_in_subcondition_bare3795)

                ID178_tree = self._adaptor.createWithPayload(ID178)
                root_0 = self._adaptor.becomeRoot(ID178_tree, root_0)

                # Fcl.g:199:25: ( IS ( NOT )? ID )?
                alt32 = 2
                LA32_0 = self.input.LA(1)

                if (LA32_0 == IS) :
                    alt32 = 1
                if alt32 == 1:
                    # Fcl.g:199:26: IS ( NOT )? ID
                    pass
                    IS179=self.match(self.input, IS, self.FOLLOW_IS_in_subcondition_bare3799)
                    # Fcl.g:199:30: ( NOT )?
                    alt31 = 2
                    LA31_0 = self.input.LA(1)

                    if (LA31_0 == NOT) :
                        alt31 = 1
                    if alt31 == 1:
                        # Fcl.g:199:31: NOT
                        pass
                        NOT180=self.match(self.input, NOT, self.FOLLOW_NOT_in_subcondition_bare3803)

                        NOT180_tree = self._adaptor.createWithPayload(NOT180)
                        self._adaptor.addChild(root_0, NOT180_tree)




                    ID181=self.match(self.input, ID, self.FOLLOW_ID_in_subcondition_bare3807)

                    ID181_tree = self._adaptor.createWithPayload(ID181)
                    self._adaptor.addChild(root_0, ID181_tree)







                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "subcondition_bare"

    class subcondition_paren_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.subcondition_paren_return, self).__init__()

            self.tree = None




    # $ANTLR start "subcondition_paren"
    # Fcl.g:200:1: subcondition_paren : LEFT_PARENTHESIS condition RIGHT_PARENTHESIS ;
    def subcondition_paren(self, ):

        retval = self.subcondition_paren_return()
        retval.start = self.input.LT(1)

        root_0 = None

        LEFT_PARENTHESIS182 = None
        RIGHT_PARENTHESIS184 = None
        condition183 = None


        LEFT_PARENTHESIS182_tree = None
        RIGHT_PARENTHESIS184_tree = None

        try:
            try:
                # Fcl.g:200:20: ( LEFT_PARENTHESIS condition RIGHT_PARENTHESIS )
                # Fcl.g:200:22: LEFT_PARENTHESIS condition RIGHT_PARENTHESIS
                pass
                root_0 = self._adaptor.nil()

                LEFT_PARENTHESIS182=self.match(self.input, LEFT_PARENTHESIS, self.FOLLOW_LEFT_PARENTHESIS_in_subcondition_paren3817)

                LEFT_PARENTHESIS182_tree = self._adaptor.createWithPayload(LEFT_PARENTHESIS182)
                root_0 = self._adaptor.becomeRoot(LEFT_PARENTHESIS182_tree, root_0)

                self._state.following.append(self.FOLLOW_condition_in_subcondition_paren3820)
                condition183 = self.condition()

                self._state.following.pop()
                self._adaptor.addChild(root_0, condition183.tree)
                RIGHT_PARENTHESIS184=self.match(self.input, RIGHT_PARENTHESIS, self.FOLLOW_RIGHT_PARENTHESIS_in_subcondition_paren3822)



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "subcondition_paren"

    class conclusion_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.conclusion_return, self).__init__()

            self.tree = None




    # $ANTLR start "conclusion"
    # Fcl.g:201:1: conclusion : sub_conclusion ( COMMA sub_conclusion )* ;
    def conclusion(self, ):

        retval = self.conclusion_return()
        retval.start = self.input.LT(1)

        root_0 = None

        COMMA186 = None
        sub_conclusion185 = None

        sub_conclusion187 = None


        COMMA186_tree = None

        try:
            try:
                # Fcl.g:201:12: ( sub_conclusion ( COMMA sub_conclusion )* )
                # Fcl.g:201:14: sub_conclusion ( COMMA sub_conclusion )*
                pass
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_sub_conclusion_in_conclusion3830)
                sub_conclusion185 = self.sub_conclusion()

                self._state.following.pop()
                self._adaptor.addChild(root_0, sub_conclusion185.tree)
                # Fcl.g:201:29: ( COMMA sub_conclusion )*
                while True: #loop33
                    alt33 = 2
                    LA33_0 = self.input.LA(1)

                    if (LA33_0 == COMMA) :
                        alt33 = 1


                    if alt33 == 1:
                        # Fcl.g:201:30: COMMA sub_conclusion
                        pass
                        COMMA186=self.match(self.input, COMMA, self.FOLLOW_COMMA_in_conclusion3833)
                        self._state.following.append(self.FOLLOW_sub_conclusion_in_conclusion3836)
                        sub_conclusion187 = self.sub_conclusion()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, sub_conclusion187.tree)


                    else:
                        break #loop33



                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "conclusion"

    class sub_conclusion_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.sub_conclusion_return, self).__init__()

            self.tree = None




    # $ANTLR start "sub_conclusion"
    # Fcl.g:202:1: sub_conclusion : ID IS ID ;
    def sub_conclusion(self, ):

        retval = self.sub_conclusion_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID188 = None
        IS189 = None
        ID190 = None

        ID188_tree = None
        IS189_tree = None
        ID190_tree = None

        try:
            try:
                # Fcl.g:202:16: ( ID IS ID )
                # Fcl.g:202:18: ID IS ID
                pass
                root_0 = self._adaptor.nil()

                ID188=self.match(self.input, ID, self.FOLLOW_ID_in_sub_conclusion3845)

                ID188_tree = self._adaptor.createWithPayload(ID188)
                root_0 = self._adaptor.becomeRoot(ID188_tree, root_0)

                IS189=self.match(self.input, IS, self.FOLLOW_IS_in_sub_conclusion3848)
                ID190=self.match(self.input, ID, self.FOLLOW_ID_in_sub_conclusion3851)

                ID190_tree = self._adaptor.createWithPayload(ID190)
                self._adaptor.addChild(root_0, ID190_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "sub_conclusion"

    class with_x_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.with_x_return, self).__init__()

            self.tree = None




    # $ANTLR start "with_x"
    # Fcl.g:203:1: with_x : WITH REAL ;
    def with_x(self, ):

        retval = self.with_x_return()
        retval.start = self.input.LT(1)

        root_0 = None

        WITH191 = None
        REAL192 = None

        WITH191_tree = None
        REAL192_tree = None

        try:
            try:
                # Fcl.g:203:7: ( WITH REAL )
                # Fcl.g:203:9: WITH REAL
                pass
                root_0 = self._adaptor.nil()

                WITH191=self.match(self.input, WITH, self.FOLLOW_WITH_in_with_x3857)

                WITH191_tree = self._adaptor.createWithPayload(WITH191)
                root_0 = self._adaptor.becomeRoot(WITH191_tree, root_0)

                REAL192=self.match(self.input, REAL, self.FOLLOW_REAL_in_with_x3860)

                REAL192_tree = self._adaptor.createWithPayload(REAL192)
                self._adaptor.addChild(root_0, REAL192_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "with_x"

    class data_type_return(ParserRuleReturnScope):
        def __init__(self):
            super(FclParser.data_type_return, self).__init__()

            self.tree = None




    # $ANTLR start "data_type"
    # Fcl.g:205:1: data_type : TYPE_REAL ;
    def data_type(self, ):

        retval = self.data_type_return()
        retval.start = self.input.LT(1)

        root_0 = None

        TYPE_REAL193 = None

        TYPE_REAL193_tree = None

        try:
            try:
                # Fcl.g:205:11: ( TYPE_REAL )
                # Fcl.g:205:13: TYPE_REAL
                pass
                root_0 = self._adaptor.nil()

                TYPE_REAL193=self.match(self.input, TYPE_REAL, self.FOLLOW_TYPE_REAL_in_data_type3868)

                TYPE_REAL193_tree = self._adaptor.createWithPayload(TYPE_REAL193)
                self._adaptor.addChild(root_0, TYPE_REAL193_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass
        return retval

    # $ANTLR end "data_type"


    # Delegated rules




    FOLLOW_fcl_in_main2813 = frozenset([1])
    FOLLOW_function_block_in_fcl2832 = frozenset([1, 38])
    FOLLOW_FUNCTION_BLOCK_in_function_block2842 = frozenset([22, 28, 39, 60, 71, 72, 102])
    FOLLOW_ID_in_function_block2846 = frozenset([22, 28, 39, 60, 71, 72])
    FOLLOW_declaration_in_function_block2851 = frozenset([22, 28, 39, 60, 71, 72])
    FOLLOW_END_FUNCTION_BLOCK_in_function_block2855 = frozenset([1])
    FOLLOW_var_input_in_declaration2863 = frozenset([1])
    FOLLOW_var_output_in_declaration2867 = frozenset([1])
    FOLLOW_fuzzify_block_in_declaration2871 = frozenset([1])
    FOLLOW_defuzzify_block_in_declaration2875 = frozenset([1])
    FOLLOW_rule_block_in_declaration2879 = frozenset([1])
    FOLLOW_VAR_INPUT_in_var_input2887 = frozenset([31, 102])
    FOLLOW_var_def_in_var_input2891 = frozenset([31, 102])
    FOLLOW_END_VAR_in_var_input2895 = frozenset([1])
    FOLLOW_VAR_OUTPUT_in_var_output2903 = frozenset([102])
    FOLLOW_var_def_in_var_output2907 = frozenset([31, 102])
    FOLLOW_END_VAR_in_var_output2911 = frozenset([1])
    FOLLOW_ID_in_var_def2919 = frozenset([77])
    FOLLOW_COLON_in_var_def2922 = frozenset([70])
    FOLLOW_data_type_in_var_def2925 = frozenset([89])
    FOLLOW_SEMICOLON_in_var_def2927 = frozenset([1, 57])
    FOLLOW_range_in_var_def2931 = frozenset([1])
    FOLLOW_FUZZIFY_in_fuzzify_block2942 = frozenset([102])
    FOLLOW_ID_in_fuzzify_block2945 = frozenset([29, 66])
    FOLLOW_linguistic_term_in_fuzzify_block2948 = frozenset([29, 66])
    FOLLOW_END_FUZZIFY_in_fuzzify_block2952 = frozenset([1])
    FOLLOW_TERM_in_linguistic_term2959 = frozenset([102])
    FOLLOW_ID_in_linguistic_term2962 = frozenset([76])
    FOLLOW_ASSIGN_OPERATOR_in_linguistic_term2964 = frozenset([16, 25, 34, 35, 36, 37, 61, 63, 68, 69, 83, 98, 102])
    FOLLOW_membership_function_in_linguistic_term2967 = frozenset([89])
    FOLLOW_SEMICOLON_in_linguistic_term2969 = frozenset([1])
    FOLLOW_function_in_membership_function2977 = frozenset([1])
    FOLLOW_singleton_in_membership_function2981 = frozenset([1])
    FOLLOW_singletons_in_membership_function2985 = frozenset([1])
    FOLLOW_piece_wise_linear_in_membership_function2989 = frozenset([1])
    FOLLOW_gauss_in_membership_function2993 = frozenset([1])
    FOLLOW_gauss2_in_membership_function2997 = frozenset([1])
    FOLLOW_trian_in_membership_function3001 = frozenset([1])
    FOLLOW_trape_in_membership_function3005 = frozenset([1])
    FOLLOW_sigm_in_membership_function3009 = frozenset([1])
    FOLLOW_gbell_in_membership_function3013 = frozenset([1])
    FOLLOW_cosine_in_membership_function3017 = frozenset([1])
    FOLLOW_dsigm_in_membership_function3021 = frozenset([1])
    FOLLOW_COSINE_in_cosine3028 = frozenset([98, 102])
    FOLLOW_atom_in_cosine3031 = frozenset([98, 102])
    FOLLOW_atom_in_cosine3033 = frozenset([1])
    FOLLOW_DSIGM_in_dsigm3039 = frozenset([98, 102])
    FOLLOW_atom_in_dsigm3042 = frozenset([98, 102])
    FOLLOW_atom_in_dsigm3044 = frozenset([98, 102])
    FOLLOW_atom_in_dsigm3046 = frozenset([98, 102])
    FOLLOW_atom_in_dsigm3048 = frozenset([1])
    FOLLOW_GAUSS_in_gauss3054 = frozenset([98, 102])
    FOLLOW_atom_in_gauss3057 = frozenset([98, 102])
    FOLLOW_atom_in_gauss3059 = frozenset([1])
    FOLLOW_GAUSS2_in_gauss23065 = frozenset([98, 102])
    FOLLOW_atom_in_gauss23068 = frozenset([98, 102])
    FOLLOW_atom_in_gauss23070 = frozenset([98, 102])
    FOLLOW_atom_in_gauss23072 = frozenset([98, 102])
    FOLLOW_atom_in_gauss23074 = frozenset([1])
    FOLLOW_GBELL_in_gbell3080 = frozenset([98, 102])
    FOLLOW_atom_in_gbell3083 = frozenset([98, 102])
    FOLLOW_atom_in_gbell3085 = frozenset([98, 102])
    FOLLOW_atom_in_gbell3087 = frozenset([1])
    FOLLOW_points_in_piece_wise_linear3094 = frozenset([1, 83])
    FOLLOW_SIGM_in_sigm3102 = frozenset([98, 102])
    FOLLOW_atom_in_sigm3105 = frozenset([98, 102])
    FOLLOW_atom_in_sigm3107 = frozenset([1])
    FOLLOW_atom_in_singleton3114 = frozenset([1])
    FOLLOW_SINGLETONS_in_singletons3120 = frozenset([83])
    FOLLOW_points_in_singletons3124 = frozenset([1, 83])
    FOLLOW_TRAPE_in_trape3133 = frozenset([98, 102])
    FOLLOW_atom_in_trape3136 = frozenset([98, 102])
    FOLLOW_atom_in_trape3138 = frozenset([98, 102])
    FOLLOW_atom_in_trape3140 = frozenset([98, 102])
    FOLLOW_atom_in_trape3142 = frozenset([1])
    FOLLOW_TRIAN_in_trian3148 = frozenset([98, 102])
    FOLLOW_atom_in_trian3151 = frozenset([98, 102])
    FOLLOW_atom_in_trian3153 = frozenset([98, 102])
    FOLLOW_atom_in_trian3155 = frozenset([1])
    FOLLOW_LEFT_PARENTHESIS_in_points3162 = frozenset([98, 102])
    FOLLOW_atom_in_points3166 = frozenset([78])
    FOLLOW_COMMA_in_points3168 = frozenset([98, 102])
    FOLLOW_atom_in_points3172 = frozenset([88])
    FOLLOW_RIGHT_PARENTHESIS_in_points3174 = frozenset([1])
    FOLLOW_real_in_atom3194 = frozenset([1])
    FOLLOW_id_in_atom3198 = frozenset([1])
    FOLLOW_ID_in_id3210 = frozenset([1])
    FOLLOW_REAL_in_real3238 = frozenset([1])
    FOLLOW_FUNCTION_in_function3259 = frozenset([8, 20, 32, 43, 44, 62, 65, 83, 98, 102])
    FOLLOW_fun_pm_in_function3262 = frozenset([1])
    FOLLOW_fun_md_in_fun_pm3268 = frozenset([1, 84, 86])
    FOLLOW_PLUS_in_fun_pm3272 = frozenset([8, 20, 32, 43, 44, 62, 65, 83, 98, 102])
    FOLLOW_MINUS_in_fun_pm3277 = frozenset([8, 20, 32, 43, 44, 62, 65, 83, 98, 102])
    FOLLOW_fun_md_in_fun_pm3282 = frozenset([1, 84, 86])
    FOLLOW_fun_mp_in_fun_md3307 = frozenset([1, 90, 91])
    FOLLOW_STAR_in_fun_md3311 = frozenset([8, 20, 32, 43, 44, 62, 65, 83, 98, 102])
    FOLLOW_SLASH_in_fun_md3316 = frozenset([8, 20, 32, 43, 44, 62, 65, 83, 98, 102])
    FOLLOW_fun_mp_in_fun_md3320 = frozenset([1, 90, 91])
    FOLLOW_fun_atom_in_fun_mp3347 = frozenset([1, 81, 85])
    FOLLOW_HAT_in_fun_mp3351 = frozenset([8, 20, 32, 43, 44, 62, 65, 83, 98, 102])
    FOLLOW_PERCENT_in_fun_mp3356 = frozenset([8, 20, 32, 43, 44, 62, 65, 83, 98, 102])
    FOLLOW_fun_atom_in_fun_mp3360 = frozenset([1, 81, 85])
    FOLLOW_atom_in_fun_atom3389 = frozenset([1])
    FOLLOW_EXP_in_fun_atom3394 = frozenset([83])
    FOLLOW_LN_in_fun_atom3397 = frozenset([83])
    FOLLOW_LOG_in_fun_atom3400 = frozenset([83])
    FOLLOW_SIN_in_fun_atom3403 = frozenset([83])
    FOLLOW_COS_in_fun_atom3406 = frozenset([83])
    FOLLOW_TAN_in_fun_atom3409 = frozenset([83])
    FOLLOW_ABS_in_fun_atom3412 = frozenset([83])
    FOLLOW_LEFT_PARENTHESIS_in_fun_atom3417 = frozenset([8, 20, 32, 43, 44, 62, 65, 83, 98, 102])
    FOLLOW_fun_pm_in_fun_atom3420 = frozenset([88])
    FOLLOW_RIGHT_PARENTHESIS_in_fun_atom3422 = frozenset([1])
    FOLLOW_DEFUZZIFY_in_defuzzify_block3432 = frozenset([102])
    FOLLOW_ID_in_defuzzify_block3435 = frozenset([21, 27, 46, 57, 66])
    FOLLOW_defuzzify_item_in_defuzzify_block3438 = frozenset([21, 27, 46, 57, 66])
    FOLLOW_END_DEFUZZIFY_in_defuzzify_block3442 = frozenset([1])
    FOLLOW_defuzzification_method_in_defuzzify_item3450 = frozenset([1])
    FOLLOW_default_value_in_defuzzify_item3454 = frozenset([1])
    FOLLOW_linguistic_term_in_defuzzify_item3458 = frozenset([1])
    FOLLOW_range_in_defuzzify_item3462 = frozenset([1])
    FOLLOW_RANGE_in_range3469 = frozenset([76])
    FOLLOW_ASSIGN_OPERATOR_in_range3472 = frozenset([83])
    FOLLOW_LEFT_PARENTHESIS_in_range3475 = frozenset([98])
    FOLLOW_REAL_in_range3478 = frozenset([80])
    FOLLOW_DOTS_in_range3480 = frozenset([98])
    FOLLOW_REAL_in_range3483 = frozenset([88])
    FOLLOW_RIGHT_PARENTHESIS_in_range3485 = frozenset([89])
    FOLLOW_SEMICOLON_in_range3488 = frozenset([1])
    FOLLOW_METHOD_in_defuzzification_method3496 = frozenset([77])
    FOLLOW_COLON_in_defuzzification_method3499 = frozenset([15, 17, 18, 19, 42, 50, 58])
    FOLLOW_set_in_defuzzification_method3502 = frozenset([89])
    FOLLOW_SEMICOLON_in_defuzzification_method3518 = frozenset([1])
    FOLLOW_DEFAULT_in_default_value3526 = frozenset([76])
    FOLLOW_ASSIGN_OPERATOR_in_default_value3529 = frozenset([51, 98])
    FOLLOW_set_in_default_value3532 = frozenset([89])
    FOLLOW_SEMICOLON_in_default_value3540 = frozenset([1])
    FOLLOW_RULEBLOCK_in_rule_block3549 = frozenset([102])
    FOLLOW_ID_in_rule_block3552 = frozenset([9, 10, 11, 30, 54, 59])
    FOLLOW_rule_item_in_rule_block3555 = frozenset([9, 10, 11, 30, 54, 59])
    FOLLOW_END_RULEBLOCK_in_rule_block3559 = frozenset([1])
    FOLLOW_operator_definition_in_rule_item3567 = frozenset([1])
    FOLLOW_activation_method_in_rule_item3571 = frozenset([1])
    FOLLOW_accumulation_method_in_rule_item3575 = frozenset([1])
    FOLLOW_rule_in_rule_item3579 = frozenset([1])
    FOLLOW_operator_definition_or_in_operator_definition3586 = frozenset([1])
    FOLLOW_operator_definition_and_in_operator_definition3590 = frozenset([1])
    FOLLOW_OR_in_operator_definition_or3597 = frozenset([77])
    FOLLOW_COLON_in_operator_definition_or3600 = frozenset([12, 14, 23, 26, 45, 49])
    FOLLOW_set_in_operator_definition_or3603 = frozenset([89])
    FOLLOW_SEMICOLON_in_operator_definition_or3617 = frozenset([1])
    FOLLOW_AND_in_operator_definition_and3625 = frozenset([77])
    FOLLOW_COLON_in_operator_definition_and3628 = frozenset([13, 24, 33, 47, 48, 56])
    FOLLOW_set_in_operator_definition_and3631 = frozenset([89])
    FOLLOW_SEMICOLON_in_operator_definition_and3645 = frozenset([1])
    FOLLOW_ACT_in_activation_method3653 = frozenset([77])
    FOLLOW_COLON_in_activation_method3656 = frozenset([47, 56])
    FOLLOW_set_in_activation_method3659 = frozenset([89])
    FOLLOW_SEMICOLON_in_activation_method3665 = frozenset([1])
    FOLLOW_ACCU_in_accumulation_method3673 = frozenset([77])
    FOLLOW_COLON_in_accumulation_method3676 = frozenset([14, 45, 53, 55, 64])
    FOLLOW_set_in_accumulation_method3679 = frozenset([89])
    FOLLOW_SEMICOLON_in_accumulation_method3691 = frozenset([1])
    FOLLOW_RULE_in_rule3699 = frozenset([98, 102])
    FOLLOW_rule_name_in_rule3702 = frozenset([77])
    FOLLOW_COLON_in_rule3704 = frozenset([40])
    FOLLOW_if_clause_in_rule3707 = frozenset([67])
    FOLLOW_then_clause_in_rule3709 = frozenset([73, 89])
    FOLLOW_with_x_in_rule3712 = frozenset([89])
    FOLLOW_SEMICOLON_in_rule3716 = frozenset([1])
    FOLLOW_set_in_rule_name0 = frozenset([1])
    FOLLOW_IF_in_if_clause3736 = frozenset([52, 83, 102])
    FOLLOW_condition_in_if_clause3739 = frozenset([1])
    FOLLOW_THEN_in_then_clause3746 = frozenset([102])
    FOLLOW_conclusion_in_then_clause3749 = frozenset([1])
    FOLLOW_subcondition_in_condition3756 = frozenset([1, 11, 54])
    FOLLOW_AND_in_condition3760 = frozenset([52, 83, 102])
    FOLLOW_OR_in_condition3763 = frozenset([52, 83, 102])
    FOLLOW_subcondition_in_condition3767 = frozenset([1, 11, 54])
    FOLLOW_NOT_in_subcondition3777 = frozenset([52, 83, 102])
    FOLLOW_subcondition_bare_in_subcondition3783 = frozenset([1])
    FOLLOW_subcondition_paren_in_subcondition3787 = frozenset([1])
    FOLLOW_ID_in_subcondition_bare3795 = frozenset([1, 41])
    FOLLOW_IS_in_subcondition_bare3799 = frozenset([52, 102])
    FOLLOW_NOT_in_subcondition_bare3803 = frozenset([102])
    FOLLOW_ID_in_subcondition_bare3807 = frozenset([1])
    FOLLOW_LEFT_PARENTHESIS_in_subcondition_paren3817 = frozenset([52, 83, 102])
    FOLLOW_condition_in_subcondition_paren3820 = frozenset([88])
    FOLLOW_RIGHT_PARENTHESIS_in_subcondition_paren3822 = frozenset([1])
    FOLLOW_sub_conclusion_in_conclusion3830 = frozenset([1, 78])
    FOLLOW_COMMA_in_conclusion3833 = frozenset([102])
    FOLLOW_sub_conclusion_in_conclusion3836 = frozenset([1, 78])
    FOLLOW_ID_in_sub_conclusion3845 = frozenset([41])
    FOLLOW_IS_in_sub_conclusion3848 = frozenset([102])
    FOLLOW_ID_in_sub_conclusion3851 = frozenset([1])
    FOLLOW_WITH_in_with_x3857 = frozenset([98])
    FOLLOW_REAL_in_with_x3860 = frozenset([1])
    FOLLOW_TYPE_REAL_in_data_type3868 = frozenset([1])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("FclLexer", FclParser)
    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)


if __name__ == '__main__':
    main(sys.argv)
