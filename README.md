Name
====

Perlinpinpin - Convert french fuzzy date to a python datetime object.

Synopsis
========

    >>> from perlinpinpin import perlinpinpin
    >>> perlinpinpin('il y a 3 jours')
    datetime.date(2009, 2, 28)
    >>> perlinpinpin('dans 3 jours')
    datetime.date(2009, 3, 6)

Description
===========

Perlinpinpin helps you convert french fuzzy date to a python datetime object, it's currently supporting these formats :

 * "il y a n semaines / jours / heures / minutes / secondes"
 * "dans n semaines / jours / heures / minutes / secondes"
 * "aujourd'hui"
 * "ce matin"
 * "cet après-midi"
 * "ce soir"
 * "maintenant"
 * "hier"
 * "après-demain"
 * "avant-hier"
 * "le 1er"
 * "le 3"
 * "le 3 Juin"
 * "le 4 Juillet 2009"
 * "dd/mm/yyyy" (European style)
 * "mm/dd/yyyy" (American style)
 * "yyyy-mm-dd"
 * "yyyymmdd"
 * "la semaine dernière"
 * "la semaine prochaine"
 * "mardi dernier"
 * "jeudi prochain"

It also allows you to find dates in free text like : 
 "Le match s'est déroulé le 2 décembre, malgré la pluie."

Authors
=======

Timothée Peignier <timothee.peignier@tryphon.org>

Perlinpinpin is based on the work of Roberto De Almeida <rob@pydap.org> on magicdate.

Copyright
=========

Perlinpinpin is : Copyright 2009-2011 Timothée Peignier <timothee.peignier@tryphon.org>