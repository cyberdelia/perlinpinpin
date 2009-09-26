============
perlinpinpin
============

Convert french fuzzy date to a python date object.

Installation
============

Stable releases of perlinpinpin can be installed using
``easy_install`` or ``pip``.

Source
======

You can find the latest version of perlinpinpin at
http://github.com/cyberdelia/perlinpinpin

Example
=======

Example::

    >>> from perlinpinpin import perlinpinpin
    >>> perlinpinpin('il y a 3 jours')
    datetime.date(2009, 2, 28)
    >>> perlinpinpin('dans 3 jours')
    datetime.date(2009, 3, 6)

