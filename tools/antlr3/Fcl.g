//-----------------------------------------------------------------------------
//
// FCL (IEC 1131) lexer & parser implementation
// using antlr (see http://www.antlr.org/)
//
//          Pablo Cingolani
//
// Notes: Adapted to ANTLR 3.1 (Sep 2008)
//-----------------------------------------------------------------------------
grammar Fcl;

options {
  // We're going to output an AST.
  output = AST;
  language=Python;
}
// Tokens (reserved words)
tokens {
    POINT;
    FCL;
    VALUE_REAL;
    VALUE_ID;
}
ABS :   ('a'|'A')('b'|'B')('s'|'S');
ACCU    :   ('a'|'A')('c'|'C')('c'|'C')('u'|'U');
ACT :   ('a'|'A')('c'|'C')('t'|'T');
AND :   ('a'|'A')('n'|'N')('d'|'D');
ASUM    :   ('a'|'A')('s'|'S')('u'|'U')('m'|'M');
BDIF    :   ('b'|'B')('d'|'D')('i'|'I')('f'|'F');
BSUM    :   ('b'|'B')('s'|'S')('u'|'U')('m'|'M');
COA :   ('c'|'C')('o'|'O')('a'|'A');
COSINE  :   ('c'|'C')('o'|'O')('s'|'S')('i'|'I')('n'|'N')('e'|'E');
COG :   ('c'|'C')('o'|'O')('g'|'G');
COGS    :   ('c'|'C')('o'|'O')('g'|'G')('s'|'S');
COGF    :   ('c'|'C')('o'|'O')('g'|'G')('f'|'F');
COS :   ('c'|'C')('o'|'O')('s'|'S');
DEFAULT :   ('d'|'D')('e'|'E')('f'|'F')('a'|'A')('u'|'U')('l'|'L')('t'|'T');
DEFUZZIFY   :   ('d'|'D')('e'|'E')('f'|'F')('u'|'U')('z'|'Z')('z'|'Z')('i'|'I')('f'|'F')('y'|'Y');
DMAX    :   ('d'|'D')('m'|'M')('a'|'A')('x'|'X');
DMIN    :   ('d'|'D')('m'|'M')('i'|'I')('n'|'N');
DSIGM   :   ('d'|'D')('s'|'S')('i'|'I')('g'|'G')('m'|'M');
EINSTEIN    :   ('e'|'E')('i'|'I')('n'|'N')('s'|'S')('t'|'T')('e'|'E')('i'|'I')('n'|'N');
END_DEFUZZIFY   :   ('e'|'E')('n'|'N')('d'|'D')'_'('d'|'D')('e'|'E')('f'|'F')('u'|'U')('z'|'Z')('z'|'Z')('i'|'I')('f'|'F')('y'|'Y');
END_FUNCTION_BLOCK  :   ('e'|'E')('n'|'N')('d'|'D')'_'('f'|'F')('u'|'U')('n'|'N')('c'|'C')('t'|'T')('i'|'I')('o'|'O')('n'|'N')'_'('b'|'B')('l'|'L')('o'|'O')('c'|'C')('k'|'K');
END_FUZZIFY :   ('e'|'E')('n'|'N')('d'|'D')'_'('f'|'F')('u'|'U')('z'|'Z')('z'|'Z')('i'|'I')('f'|'F')('y'|'Y');
END_RULEBLOCK   :   ('e'|'E')('n'|'N')('d'|'D')'_'('r'|'R')('u'|'U')('l'|'L')('e'|'E')('b'|'B')('l'|'L')('o'|'O')('c'|'C')('k'|'K');
END_VAR :   ('e'|'E')('n'|'N')('d'|'D')'_'('v'|'V')('a'|'A')('r'|'R');
EXP :   ('e'|'E')('x'|'X')('p'|'P');
HAMACHER    :   ('h'|'H')('a'|'A')('m'|'M')('a'|'A')('c'|'C')('h'|'H')('e'|'E')('r'|'R');
FUNCTION    :   ('f'|'F')('u'|'U')('n'|'N')('c'|'C')('t'|'T')('i'|'I')('o'|'O')('n'|'N');
GAUSS   :   ('g'|'G')('a'|'A')('u'|'U')('s'|'S')('s'|'S');
GAUSS2  :   ('g'|'G')('a'|'A')('u'|'U')('s'|'S')('s'|'S')'2';
GBELL   :   ('g'|'G')('b'|'B')('e'|'E')('l'|'L')('l'|'L');
FUNCTION_BLOCK  :   ('f'|'F')('u'|'U')('n'|'N')('c'|'C')('t'|'T')('i'|'I')('o'|'O')('n'|'N')'_'('b'|'B')('l'|'L')('o'|'O')('c'|'C')('k'|'K');
FUZZIFY :   ('f'|'F')('u'|'U')('z'|'Z')('z'|'Z')('i'|'I')('f'|'F')('y'|'Y');
IF  :   ('i'|'I')('f'|'F');
IS  :   ('i'|'I')('s'|'S');
LM  :   ('l'|'L')('m'|'M');
LN  :   ('l'|'L')('n'|'N');
LOG :   ('l'|'L')('o'|'O')('g'|'G');
MAX :   ('m'|'M')('a'|'A')('x'|'X');
METHOD  :   ('m'|'M')('e'|'E')('t'|'T')('h'|'H')('o'|'O')('d'|'D');
MIN :   ('m'|'M')('i'|'I')('n'|'N');
NIPMIN  :   ('n'|'N')('i'|'I')('p'|'P')('m'|'M')('i'|'I')('n'|'N');
NIPMAX  :   ('n'|'N')('i'|'I')('p'|'P')('m'|'M')('a'|'A')('x'|'X');
MM  :   ('m'|'M')('m'|'M');
NC  :   ('n'|'N')('c'|'C');
NOT :   ('n'|'N')('o'|'O')('t'|'T');
NSUM    :   ('n'|'N')('s'|'S')('u'|'U')('m'|'M');
OR  :   ('o'|'O')('r'|'R');
PROBOR  :   ('p'|'P')('r'|'R')('o'|'O')('b'|'B')('o'|'O')('r'|'R');
PROD    :   ('p'|'P')('r'|'R')('o'|'O')('d'|'D');
RANGE   :   ('r'|'R')('a'|'A')('n'|'N')('g'|'G')('e'|'E');
RM  :   ('r'|'R')('m'|'M');
RULE    :   ('r'|'R')('u'|'U')('l'|'L')('e'|'E');
RULEBLOCK   :   ('r'|'R')('u'|'U')('l'|'L')('e'|'E')('b'|'B')('l'|'L')('o'|'O')('c'|'C')('k'|'K');
SIGM    :   ('s'|'S')('i'|'I')('g'|'G')('m'|'M');
SIN :   ('s'|'S')('i'|'I')('n'|'N');
SINGLETONS  :   ('s'|'S')('i'|'I')('n'|'N')('g'|'G')('l'|'L')('e'|'E')('t'|'T')('o'|'O')('n'|'N')('s'|'S');
SUM :   ('s'|'S')('u'|'U')('m'|'M');
TAN :   ('t'|'T')('a'|'A')('n'|'N');
TERM    :   ('t'|'T')('e'|'E')('r'|'R')('m'|'M');
THEN    :   ('t'|'T')('h'|'H')('e'|'E')('n'|'N');
TRAPE   :   ('t'|'T')('r'|'R')('a'|'A')('p'|'P')('e'|'E');
TRIAN   :   ('t'|'T')('r'|'R')('i'|'I')('a'|'A')('n'|'N');
TYPE_REAL   :   ('r'|'R')('e'|'E')('a'|'A')('l'|'L');
VAR_INPUT   :   ('v'|'V')('a'|'A')('r'|'R')'_'('i'|'I')('n'|'N')('p'|'P')('u'|'U')('t'|'T');
VAR_OUTPUT  :   ('v'|'V')('a'|'A')('r'|'R')'_'('o'|'O')('u'|'U')('t'|'T')('p'|'P')('u'|'U')('t'|'T');
WITH    :   ('w'|'W')('i'|'I')('t'|'T')('h'|'H');
//-----------------------------------------------------------------------------
// Lexer
//-----------------------------------------------------------------------------
// Send runs of space and tab characters to the hidden channel.
WS: (' ' | '\t')+ { $channel = HIDDEN; };
// Treat runs of newline characters as a single NEWLINE token.
// On some platforms, newlines are represented by a \n character.
// On others they are represented by a \r and a \n character.
NEWLINE: ('\r'? '\n')+ { $channel=HIDDEN; };

// Common symbols
ASSIGN_OPERATOR : ':' '=';
COLON : ':';
COMMA : ',';
DOT :   '.';
DOTS :  '..';
HAT  : '^' ;
LEFT_CURLY : '{';
LEFT_PARENTHESIS: '(';
MINUS : '-' ;
PERCENT  : '%' ;
PLUS  : '+' ;
RIGHT_CURLY : '}';
RIGHT_PARENTHESIS: ')' ;
SEMICOLON  : ';' ;
SLASH  : '/' ;
STAR  : '*' ;
// A number is a set of digits
fragment NUMBER : (DIGIT)+;
// A DIGIT
fragment DIGIT : '0'..'9' ;
// A letter
fragment LETTER: LOWER | UPPER;
fragment LOWER: 'a'..'z';
fragment UPPER: 'A'..'Z';
// Letter or digit
fragment ALPHANUM   :   LETTER | DIGIT;
// Real number (float/double) without any sign
REAL  :   (PLUS|MINUS)? NUMBER ( '.' NUMBER )? (('e'|'E') (PLUS|MINUS)? NUMBER)? ;

// FCL style comments
COMMENT options { greedy = false; }
    : '(*' .* '*)' NEWLINE? { $channel=HIDDEN; };
// 'C' style comments
COMMENT_C options { greedy = false; }
    : '/*' .* '*/' NEWLINE? { $channel=HIDDEN; };

// 'C' style single line comments
COMMENT_SL : '//' ~('\r' | '\n')* NEWLINE   { $channel=HIDDEN; };
// An identifier.
ID  :   LETTER (ALPHANUM | '_')*;
//-----------------------------------------------------------------------------
// Parser
//-----------------------------------------------------------------------------
// FCL file may contain several funcion blocks
main :  f=fcl -> ^(FCL $f);
fcl :   (function_block)+;
// Function block
function_block : FUNCTION_BLOCK^ (ID)? (declaration)* END_FUNCTION_BLOCK!;
declaration : var_input | var_output | fuzzify_block | defuzzify_block | rule_block;
// Variables input and output
var_input : VAR_INPUT^ (var_def)* END_VAR!;
var_output : VAR_OUTPUT^ (var_def)+ END_VAR!;
var_def : ID^ COLON! data_type SEMICOLON! (range)? ;
// Fuzzify
fuzzify_block : FUZZIFY^ ID (linguistic_term)* END_FUZZIFY!;
linguistic_term: TERM^ ID ASSIGN_OPERATOR! membership_function SEMICOLON!;
membership_function : function | singleton | singletons | piece_wise_linear | gauss | gauss2 | trian | trape | sigm | gbell | cosine | dsigm ;
cosine: COSINE^ atom atom;
dsigm: DSIGM^ atom atom atom atom;
gauss: GAUSS^ atom atom;
gauss2: GAUSS2^ atom atom atom atom;
gbell: GBELL^ atom atom atom;
piece_wise_linear: (points)+;
sigm: SIGM^ atom atom;
singleton : atom;
singletons: SINGLETONS^ (points)+ ;
trape: TRAPE^ atom atom atom atom;
trian: TRIAN^ atom atom atom;
points : LEFT_PARENTHESIS x=atom COMMA y=atom RIGHT_PARENTHESIS -> ^(POINT $x $y);
atom :  real | id;
id  :   x=ID        ->  ^(VALUE_ID $x);
real :   x=REAL     ->  ^(VALUE_REAL $x);
// Functions (for singletons)
function: FUNCTION^ fun_pm;
fun_pm: fun_md ((PLUS^ | MINUS^ ) fun_md)*;                 // Function plus or minus
fun_md: fun_mp ((STAR^ | SLASH^) fun_mp)*;                  // Function multiply or divide
fun_mp : fun_atom ((HAT^ | PERCENT^) fun_atom)*;                    // Function modulus or power
fun_atom : atom | (EXP^|LN^|LOG^|SIN^|COS^|TAN^|ABS^)? LEFT_PARENTHESIS! fun_pm RIGHT_PARENTHESIS!; // Atom and parenthesis
// Defuzzify
defuzzify_block : DEFUZZIFY^ ID (defuzzify_item)* END_DEFUZZIFY!;
defuzzify_item : defuzzification_method | default_value | linguistic_term | range;
range : RANGE^ ASSIGN_OPERATOR! LEFT_PARENTHESIS! REAL DOTS! REAL RIGHT_PARENTHESIS! SEMICOLON!;
defuzzification_method : METHOD^ COLON! (COG|COGS|COGF|COA|LM|RM|MM) SEMICOLON!;
default_value : DEFAULT^ ASSIGN_OPERATOR! (REAL | NC) SEMICOLON!;
// Ruleblock
rule_block : RULEBLOCK^ ID (rule_item)* END_RULEBLOCK!;
rule_item : operator_definition | activation_method | accumulation_method | rule;
operator_definition : operator_definition_or | operator_definition_and;
operator_definition_or : OR^ COLON! (MAX|ASUM|BSUM|DMAX|NIPMAX|EINSTEIN) SEMICOLON!;
operator_definition_and : AND^ COLON! (MIN|PROD|BDIF|DMIN|NIPMIN|HAMACHER) SEMICOLON!;
activation_method : ACT^ COLON! (PROD|MIN) SEMICOLON!;
accumulation_method : ACCU^ COLON! (MAX|BSUM|NSUM|PROBOR|SUM) SEMICOLON!;
rule : RULE^ rule_name COLON! if_clause then_clause (with_x)? SEMICOLON! ;
rule_name : ID | REAL;
if_clause : IF^ condition;
then_clause : THEN^ conclusion;
condition : subcondition ((AND^|OR^) subcondition)*;
subcondition : (NOT^)? (subcondition_bare | subcondition_paren);
subcondition_bare : ID^ (IS! (NOT)? ID)? ;
subcondition_paren : LEFT_PARENTHESIS^ condition RIGHT_PARENTHESIS!;
conclusion : sub_conclusion (COMMA! sub_conclusion)*;
sub_conclusion : ID^ IS! ID;
with_x: WITH^ REAL;
// Data type
data_type : TYPE_REAL;
