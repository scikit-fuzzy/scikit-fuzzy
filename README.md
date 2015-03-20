Readme
======

`scikit-fuzzy` is a fuzzy logic toolkit for SciPy.

The goals of scikit-fuzzy are:
* To provide the community with a robust toolkit of independently developed and implemented fuzzy logic algorithms
* To increase the attractiveness of scientific Python as a valid alternative to closed-source options.

Source
------

https://github.com/scikit-fuzzy/scikit-fuzzy

Online Discussion & Mailing List
--------------------------------

Please join the discussion in our public chat room on Gitter.im
[![Gitter](https://badges.gitter.im/Join Chat.svg)](https://gitter.im/scikit-fuzzy/scikit-fuzzy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

or view/post on the Google Groups mailing list
http://groups.google.com/group/scikit-fuzzy

Installation
------------

Scikit-Fuzzy depends on

  * NumPy >= 1.6
  * SciPy >= 0.9

and is now available on PyPi! The lastest stable release can be
obtained and installed simply by running

    $ pip install -U scikit-fuzzy

which will also work to upgrade existing installations to the latest release.


If you prefer to install from source or develop this package, you can fork and
clone this repository then install SciKit-Fuzzy by running

	$ python setup.py install

or locally by running

	$ python setup.py install --prefix=${HOME}

If you prefer, you can use SciKit-Fuzzy without installing by simply exporting
this path to your PYTHONPATH variable.

License
-------

Please read LICENSE.txt in this directory.

IEEE Rounding for Matlab users
------------------------------

It should be noted that Matlab rounds incorrectly. The IEEE standard (which is
how this package behaves) requires rounding to the nearest EVEN number if
exactly between, e.g. 1.5 --> 2; 2.5 --> 2; 3.5 --> 4; 4.5 --> 4, etc. This
minimizes systematic rounding error. Thus, if re-implementing algorithms from
Matlab code, slight inconsistencies in rounded results are expected. These are
not bugs, and will not be fixed.
