Examples of FCL files (with data)
=======================================

This directory contains some examples of FCL files, along with data
that can be used to test them.

These files were gathered from two sources:

 * [jFuzzyLogic](http://jfuzzylogic.sourceforge.net/)
   GNU Lesser General Public License (GPL) 3.0

 * [FuzzyLite](http://www.fuzzylite.com/)
   GNU General Public License (GPL) 3.0

The files in this folder are a _subset_ of those provided by these
tools.  I've removed any FCL files that used features not (yet)
supported by `scikit-fuzzy`.  For `FuzzyLite` I've only used the
mamdani-style examples - this is a small subset of those supplied with
the tool.  Also, I've tweaked some of the RANGEs for fuzzy variables
(or added them if not there), since this can have a dramatic effect on
the accuracy of the results.


Test Data
---------

Each of the FCL files in this folder is accompanied by an `.fld` file
which contains test data: basically a list of values for the input and
output variables.  In the case of FuzzyLite these were supplied with
the tool.  For jFuzzyLogic I ran the tool with some sample inputs;
since jFuzzyLogic also reports rule fire-strengths, I've included
these in the `.fld` file too as they helped with debugging.

The purpose of these files is to test the implementation: when we run
the same files through `scikit-fuzzy` we should get mostly the same
answers as the original tools.

The script [simulate.py](../simulate.py) can be used to run these -
note that running them _all_ make take a while.

Example run:

```
> python3 simulate.py Examples/jFuzzyLogic/tipper.fcl

======================================================================
= Examples/jFuzzyLogic/tipper.fcl on 08 Sep 2018 at 16:06
======================================================================
----------------------------------------------------------------------
Run 0: food=0.00 service=0.00 
Output variables:
  tip=5.00  CORRECT, ERROR=0.0%
Rule fire-strengths for test case 0:
  RULE No1.1 = 1.00 (CORRECT)
  RULE No1.2 = 0.00 (CORRECT)
  RULE No1.3 = 0.00 (CORRECT)
----------------------------------------------------------------------
.....
```



[James Power](http://www.cs.nuim.ie/~jpower/),
8 Sept 2018.