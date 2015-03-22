Scikit-Fuzzy logo generator
===========================

Running `skfuzzy_logo.py` in this directory will generate the package logo in
two versions - one high resolution suitable for print use, the other lower
resolution suitable for web use.

* `logo.png` : Low resolution, ideal for web
* `logo_full.png` : High resolution, ideal for print.


Scikit-Fuzzy icon generator
===========================

Running `skfuzzy_icon.py` in this directory will generate the package icon,
which only includes the main 'S' and 'F' motifs from the full logo. This is
generated in three versions, to allow thumbnails across a wide variety of
platforms.

* `icon_32px.png` : Low resolution, ideal for tab page icon
* `icon_64px.png` : Medium resolution, good for small thumbnails/medium icons
* `icon_128px.png` : High resolution, good for high PPI display thumbnails.


Dependencies
------------

In addition to the package dependencies for `scikit-fuzzy`, generation of these
graphics also require

* `scikit-image` >= 0.10
* `matplotlib` >= 1.2
