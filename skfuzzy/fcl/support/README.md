An FCL parser with a scikit-fuzzy back-end
=======================================

This is a parser for the Fuzzy Control Language
[FCL](https://en.wikipedia.org/wiki/Fuzzy_Control_Language)
along with a back-end for
[scikit-fuzzy](https://github.com/scikit-fuzzy/scikit-fuzzy),
a fuzzy logic toolkit for SciPy.

The basic use-case is to parse a FCL file and then use the fuzzy rules
in your `scikit-fuzzy` code.  For example:

```python
from fcl_parser import FCLParser

p = FCLParser()    # Create the parser
p.read_fcl_file('tipper.fcl')  # Parse a file

# ... and so on, as usual for skfuzzy:
cs = ctrl.ControlSystem(p.rules)

```

After reading a file the parser object has attributes to supply the
`rules` (as above) or the `antecedents`, the `consequents`, or all the
`fuzzy_variables` All these are represented via lists of their
corresponding `scikit-fuzzy` objects.


Other Entry Points
------------------

The parser can be used to accept program fragments, so you can
interleave its use with regular `scikit-fuzzy` code.

For example, in the following `scikit-fuzzy` code we set up the
tipping example in the usual way by specifying the variables and
defining some membership functions for the inputs:

```python
# First we set up the variables in the usual way:
food = ctrl.Antecedent(np.linspace(0, 10, 11), 'quality')
service = ctrl.Antecedent(np.linspace(0, 10, 11), 'service')
tip = ctrl.Consequent(np.linspace(0, 25, 26), 'tip')

# Auto-generate the membership functions for the inputs:
food.automf(3)
service.automf(3)
```

We can define the output variable using FCL code, in this case getting
the parser to parse a membership function `mf` definition:

```python
# Define a FCL parser-object:
p = FCLParser()
# Use FCL to define membership functions for the output:
tip['bad'] = p.mf('Triangle 0 0 13', tip.universe)
tip['middling'] = p.mf('Triangle 0 13 25', tip.universe)
tip['lots'] = p.mf('Triangle 13 25 25', tip.universe)

```
                        
Last, we can define the rules in FCL, and get a `scikit-fuzzy` rule
object for each of them if we like:

```python
# We need to tell the parser about the variables before we parse any rules:
p.add_vars([food, service, tip])

# Now use FCL to define three rules:
rule1 = p.rule('IF quality is poor OR service is poor THEN tip is bad')
rule2 = p.rule('IF service is average THEN tip is middling')
rule3 = p.rule('IF service is good OR quality is good THEN tip is lots')

# To get the control system, just add the rules (from the parser):
tipping = ctrl.ControlSystem(p.rules)
```

There are some more examples of mixed FCL/skfuzzy use in the file
[tests/test_fcl_parser.py](./tests/test_fcl_parser.py)


Dependencies
------------

The scanner is written using
[PLY](http://www.dabeaz.com/ply/ply.html) (Python Lex-Yacc),
so you need to install PLY before the code here will work.

     $ pip install ply

You don't need to import this anywhere, my scanner code just needs it.
The parser is hand-written so we don't actually use the
parser-generation features of PLY.


What's implemented
------------------

Much of FCL is implemented, concentrating on
the subset of FCL that can be translated easily into
`scikit-fuzzy`.  That includes most parts of a standard
(Mamdani-style) fuzzy system.

At the moment the main options are for:
  * defuzzification methods: cog, coa, lm, rm, mom
  * membership functions: quite a collection; have a look in
  [fcl_symbols.py](./fcl_symbols.py) for a list.
  * and/or methods (norms and co-norms): again, quite a few,
  including (norms) min, prod, bdif, drp, eprod, hprod, nilmin
  and their co-norm duals.

I was doing this with an eye on the XML standard, hence the rather
large selection of membership functions and norms.


I've also implemented the *hedge functions* listed in the IEEE standard,
so you can write things like:

```python
rule1 = p.rule('IF quality is slightly poor OR service is very poor THEN tip is extremely bad')
```

What happens here is that when the rule is processed, the hedge
functions are applied to the corresponding membership function, and a
new membership function is generated and added to the variable.  For
example, a membership function called `_slightly_poor` would be added
to the variable `quality` above.


What's not implemented
------------------

Most notably _not_ implemented (yet) are options for:

* activation method (this is hard-wired to `MIN`).

  At the moment `scikit-fuzzy` doesn't have an option to change this;
  its CrispValueCalculator always uses np.minimum.

* accumulation method (well, not exactly).

  This is a small incompatibility: FCL sees the accumulation as a
  property of the rule-base, whereas `scikit-fuzzy` sees it as a
  property of the output variables.  I could fix the parser to
  propagate the setting from the rules to the variables used in those
  rules, but this might cause unexpected behaviour if the variables
  are used in more than one rule base.

  You can set an 'ACCU' option as part of an (output) variable
  definition, and this will be propagated through to `scikit-fuzzy`.


* default values for variables.

  In FCL these values are used in defuzzification when all the
  memberships have been cut to zero area.  As far as I can see this
  case will raise an exception in `scikit-fuzzy`.
  

The parser accepts these, I just haven't figured out how to get them
into the `scikit-fuzzy` code, so they are ignored for the moment.

Compliance
----------

First of all, I'm working from the draft of the FCL standard (IEC
TC65/WG 7/TF8), plus any examples I could find, so I may have missed a
few things.
Second, the parser does not enforce strict conformance to the FCL standard,
and is somewhat liberal in the kind of FCL code it will accept.
This is intended as a feature, not a bug.

In particular:
  * Case is not relevant for keywords
  (so `rule` and `RULE` are the same)
  but note that case _is_ relevant for identifiers (e.g. variable names).
  * The semi-colon at the end of lines can be left out in most cases.
  * The parser doesn't impose a strict ordering on the contents of 
  variable definitions, so you can mix `TERM`, `RANGE`, `METHOD`
  etc. in your preferred order.

I only made one real change to the FCL language
to better support `scikit-fuzzy`:
  * When defining a variable range (universe) you can specify
  the granularity using an optional `WITH` setting, thus:
  ```
  RANGE := (0 .. 2.1) WITH 0.01
  ```
  This maps directly to a NumPy `arange(1, 2.1, 0.01)` expression.

This is due to the way `scikit-fuzzy` calculates its membership
functions: these get worked out to point-lists when they are defined,
so I need to know the granularity to get this right.

This working-out is also the reason we can't really generate FCL from
a `scikit-fuzzy` program, since the information on the original
definition of the membership functions is not retained once the
point-sets have been calculated.




Reading the code
----------------

The main functionality is in [fcl_parser.py](./fcl_parser.py)
which contains the
hand-written top-down parser.  This is essentially a context-free
grammar, with a Python method for each non-terminal.

This can be called from the command-line if you just want to parse a file;
for example:

```
$ python fcl_parser.py tests/tipper.fcl
```

The scanner code is in [fcl_scanner.py](./fcl_scanner.py).
This uses a few tricks related
to PLY, but us essentially a list of regular expressions plus some
extra code to check tokens etc.

The symbol table is in [fcl_symbols.py](./fcl_symbols.py)
and contains a list of the
variables and rules, added in as they are processed.  The mappings
between option names (membership functions, defuzzification method
etc.) is also kept here.

The other files are simple auxiliary definitions: some extra
membership functions (that are not in `scikit-fuzzy`) are defined in
[extramf.py](./extramf.py)
and the t-norms and their duals are defined in
[norms.py](./norms.py).
The set of hedge functions as defined in the IEEE standard is implemented in
[hedges.py](./hedges.py).



[James Power](http://www.cs.nuim.ie/~jpower/),
27 August 2018.