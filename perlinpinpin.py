# -*- coding: utf-8 -*-
import calendar
import datetime
import os
import re
import time

__version__ = "0.9.1"


class Perlinpinpin(object):
    days = "Lundi Mardi Mercredi Jeudi Vendredi Samedi Dimanche".split(' ')
    months = "Janvier Fevrier Mars Avril Mai Juin Juillet Aout Septembre Octobre Novembre Decembre".split(' ')

    def __init__(self):
        relative = r"(?:aujourd[']?hui|hier|maintenant|matin|soir|apres[\s-]?midi|demain|apres[\s-]?demain|avant[\s-]?hier)"
        relative_spec = r"(?:suivant[es]?|précédent[es]?|prochain[es]?|dernier[es]?)"

        relative_delta = r"(?:dans|il\sy\sa)"
        delta = r"(?:%s\s+(?:\d+\s+(?:(?:semaine|jour|heure|minute|seconde)[s]?)+[^\d]*)+)" % relative_delta

        weekday = r"(?:le|%s)" % '|'.join(Perlinpinpin.days)
        month = r"(?:%s)" % '|'.join(Perlinpinpin.months)

        relative_weekday = r"(?:%s\s*%s)" % (weekday, relative_spec)
        relative_week = r"(?:semaine\s*%s)" % relative_spec

        # 1 - 31
        cardinal_monthday = r"(?:[1-9]|[0-2][0-9]|3[01])"
        monthday = r"(?:%s\s*(ier|er|iere)?)" % cardinal_monthday

        day_month = r"(?:(%s)?\s*%s\s*%s)" % (
            weekday, monthday, month
        )
        month_day = r"(?:%s\s*%s)" % (month, monthday)
        day_month_year = r"(?:(?:%s|%s)[-\s]*\d{4})" % (
            day_month, month_day
        )
        day = r"(?:(le|%s)+\s*%s)" % (weekday, monthday)

        yyyymmdd = r"(?:\d{4}[-/]?\d{1,2}[-/]?\d{1,2})"
        ddmmyy = r"(?:\d{1,2}[-/]?\d{1,2}[-/]?\d{2})"
        ddmmyyyy = r"(?:\d{1,2}[-/]?\d{1,2}[-/]?\d{4})"

        self.detect = re.compile(r"""
            \b(
              %(relative)s
            | %(relative_weekday)s  # Vendredi dernier
            | %(relative_week)s     # Semaine suivante
            | %(delta)s             # Dans 1 semaine
            | %(day_month_year)s    # 12 Décembre, 1985
            | %(day_month)s         # 12 Septembre
            | %(day)s               # le 12
            | %(month_day)s         # Novembre 13
            | %(yyyymmdd)s          # 1986/11/13
            | %(ddmmyyyy)s          # 11-13-1986
            | %(ddmmyy)s            # 11-13-86
            )\b
        """ % {
            'relative': relative,
            'relative_weekday': relative_weekday,
            'relative_week': relative_week,
            'delta': delta,
            'weekday': weekday,
            'day': day,
            'day_month_year': day_month_year,
            'day_month': day_month,
            'month_day': month_day,
            'yyyymmdd': yyyymmdd,
            'ddmmyy': ddmmyy,
            'ddmmyyyy': ddmmyyyy,
        }, (re.VERBOSE | re.IGNORECASE))

        self.convert = [
            # Il y a x
            (re.compile(
                r'''^
                    il\sy\sa\s
                    ((?P<weeks>\d+) \s semaine(s?)?)?
                    [^\d]*
                    ((?P<days>\d+) \s jour(s?)?)?
                    [^\d]*
                    ((?P<hours>\d+) \s heure(s?)?)?
                    [^\d]*
                    ((?P<minutes>\d+) \s minute(s?)?)?
                    [^\d]*
                    ((?P<seconds>\d+) \s seconde(s?)?)?
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today() - datetime.timedelta(
                    days=int(m.group('days') or 0),
                    seconds=int(m.group('seconds') or 0),
                    minutes=int(m.group('minutes') or 0),
                    hours=int(m.group('hours') or 0),
                    weeks=int(m.group('weeks') or 0))),
            # Dans x
            (re.compile(
                r'''^
                    dans\s
                    ((?P<weeks>\d+) \s semaine(s?)?)?
                    [^\d]*
                    ((?P<days>\d+) \s jour(s?)?)?
                    [^\d]*
                    ((?P<hours>\d+) \s heure(s?)?)?
                    [^\d]*
                    ((?P<minutes>\d+) \s minute(s?)?)?
                    [^\d]*
                    ((?P<seconds>\d+) \s seconde(s?)?)?
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today() + datetime.timedelta(
                    days=int(m.group('days') or 0),
                    seconds=int(m.group('seconds') or 0),
                    minutes=int(m.group('minutes') or 0),
                    hours=int(m.group('hours') or 0),
                    weeks=int(m.group('weeks') or 0))),
            # Today
            (re.compile(
                r'''^
                    aujourd[']?hui                  # Today
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today()),
            # Now
            (re.compile(
                r'''^
                    maintenant                      # Now
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today()),
            # Tomorrow
            (re.compile(
                r'''^
                    demain                          # Tomorrow
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today() + datetime.timedelta(days=1)),
            # Yesterday
            (re.compile(
                r'''^
                    hier                            # Yesterday
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today() - datetime.timedelta(days=1)),
            # After-tomorrow
            (re.compile(
                r'''^
                    apres[\s-]?demain               # After-tomorrow
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today() + datetime.timedelta(days=2)),
            # Before-yesterday
            (re.compile(
                r'''^
                    avant[\s-]?hier                 # Before-yesterday
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today() - datetime.timedelta(days=2)),
            # This morning
            (re.compile(
                r'''^
                    matin                           # morning
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today()),
            # This afternoon
            (re.compile(
                r'''^
                    apres[\s-]?midi                 # afternoon
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today()),
            # This evening
            (re.compile(
                r'''^
                    soir                            # evening
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today()),
            # 4
            (re.compile(
                r'''^
                    (le\s*)?                        # le
                    (%s\s*)?                        # vendredi
                    (?P<day>[1-9]|[0-2][0-9]|3[01]) # 4
                    (?:\s*(ier|er|iere)?)           # optional suffix
                    $                               # EOL
                ''' % weekday,
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today().replace(
                day=int(m.group('day')))),
            # 4 Janvier
            (re.compile(
                r'''^
                    (%s\s*)?                        # vendredi
                    (?P<day>[1-9]|[0-2][0-9]|3[01]) # 4
                    (?:\s*(ier|er|iere)?)           # optional suffix
                    \s+                             # whitespace
                    (?P<month>%s+)                  # Janvier
                    $                               # EOL
                ''' % (weekday, '|'.join(Perlinpinpin.months)),
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today().replace(
                day=int(m.group('day')),
                month=self._month(m.group('month')))),
            # 4 Janvier 2003
            (re.compile(
                r'''^
                    (%s\s*)?                        # vendredi
                    (?P<day>[1-9]|[0-2][0-9]|3[01]) # 4
                    (?:\s*(ier|er|iere)?)           # optional suffix
                    \s+                             # whitespace
                    (?P<month>%s+)                  # Janvier
                    ,?                              # optional comma
                    \s+                             # whitespace
                    (?P<year>\d{4})                 # 2003
                    $                               # EOL
                ''' % (weekday, '|'.join(Perlinpinpin.months)),
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date(
                year=int(m.group('year')),
                month=self._month(m.group('month')),
                day=int(m.group('day')))),
            # dd/mm/yyyy (European style, default in case of doubt)
            (re.compile(
                r'''^
                    (?P<day>[1-9]|[0-2][0-9]|3[01]) # d or dd
                    [-/]?                           #
                    (?P<month>[1-9]|0[0-9]|1[0-2])  # m or mm
                    [-/]?                           #
                    (?P<year>\d{4})                 # yyyy
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date(*time.strptime(
                "%s %s %s" % (m.group('year'), m.group('month'), m.group('day')), "%Y %m %d")[:3]
            )),
            # dd/mm/yy (European short style)
            (re.compile(
                r'''^
                    (?P<day>[1-9]|[0-2][0-9]|3[01]) # d or dd
                    [-/]?                           #
                    (?P<month>[1-9]|0[0-9]|1[0-2])  # m or mm
                    [-/]?                           #
                    (?P<year>\d{2})                 # yy
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date(*time.strptime(
                "%s %s %s" % (m.group('year'), m.group('month'), m.group('day')), "%y %m %d")[:3]
            )),
            # mm/dd/yyyy (American style)
            (re.compile(
                r'''^
                    (?P<month>[1-9]|0[0-9]|1[0-2])  # m or mm
                    [-/]?                           #
                    (?P<day>[1-9]|[0-2][0-9]|3[01]) # d or dd
                    [-/]?                           #
                    (?P<year>\d{4})                 # yyyy
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date(*time.strptime(
                "%s %s %s" % (m.group('year'), m.group('month'), m.group('day')), "%Y %m %d")[:3]
            )),
            # mm/dd/yy (American short style)
            (re.compile(
                r'''^
                    (?P<month>[1-9]|0[0-9]|1[0-2])  # m or mm
                    [-/]?                           #
                    (?P<day>[1-9]|[0-2][0-9]|3[01]) # d or dd
                    [-/]?                           #
                    (?P<year>\d{2})                 # yy
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date(*time.strptime(
                "%s %s %s" % (m.group('year'), m.group('month'), m.group('day')), "%y %m %d")[:3]
            )),
            # yyyy-mm-dd (ISO style)
            (re.compile(
                r'''^
                    (?P<year>\d{4})                 # yyyy
                    [-/]?                           #
                    (?P<month>[1-9]|0[0-9]|1[0-2])  # m or mm
                    [-/]?                           #
                    (?P<day>[1-9]|[0-2][0-9]|3[01]) # d or dd
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date(
                year=int(m.group('year')),
                month=int(m.group('month')),
                day=int(m.group('day')))),
            # Semaine dernière
            (re.compile(
                r'''^
                    semaine                         # week
                    \s+                             # whitespace
                    (derniere|precedente)?          # last
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today() - datetime.timedelta(days=7)),
            # Semaine prochaine
            (re.compile(
                r'''^
                    semaine                         # week
                    \s+                             # whitespace
                    (prochaine|suivante)?           # last
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today() + datetime.timedelta(days=7)),
            # Mardi prochain
            (re.compile(
                r'''^
                    (?P<weekday>\w+)                # Mardi
                    \s+                             # whitespace
                    (prochain|suivant)?             # next
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: self._next_weekday(self._weekday(m.group('weekday')))),
            # Mardi dernier
            (re.compile(
                r'''^
                    (?P<weekday>\w+)                # Mardi
                    \s+                             # whitespace
                    (dernier|precedent)?            # last
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: self._last_weekday(self._weekday(m.group('weekday')))),
       ]

    def extract(self, text, timezone=None):
        """Extract dates from fuzzy text with respect to the given timezone"""
        text = self._normalize(text)
        if timezone:
            os.environ['TZ'] = timezone
        matches = []
        for match in self.detect.finditer(text.strip()):
            if match:
                date = self.parse(match.group())
                if date:
                    matches.append(date)
        return matches

    def parse(self, date, timezone=None):
        """Parse fuzzy date with respect to the given timezone"""
        date = self._normalize(date)
        if timezone:
            os.environ['TZ'] = timezone
        for regexp, func in self.convert:
            match = regexp.match(date.strip())
            if match:
                return func(match)
        return None

    def _normalize(self, text):
        """Remove accents from text"""
        import unicodedata
        return unicodedata.normalize('NFKD', unicode(text)).encode('ASCII', 'ignore')

    def _month(self, text):
        """Get the month as a decimal number"""
        for i, month in enumerate(Perlinpinpin.months):
            regexp = re.compile(text, re.IGNORECASE)
            if regexp.match(month):
                return i + 1
        else:
            raise ValueError

    def _weekday(self, text):
        """Get weekday as a decimal number"""
        for i, day in enumerate(Perlinpinpin.days):
            regexp = re.compile(text, re.IGNORECASE)
            if regexp.match(day):
                return i
        else:
            raise ValueError

    def _next_weekday(self, weekday):
        """Get next weekday as a date"""
        day = datetime.date.today() + datetime.timedelta(days=1)
        while calendar.weekday(*day.timetuple()[:3]) != weekday:
            day = day + datetime.timedelta(days=1)
        return day

    def _last_weekday(self, weekday):
        """Get previous weekday as a date"""
        day = datetime.date.today() - datetime.timedelta(days=1)
        while calendar.weekday(*day.timetuple()[:3]) != weekday:
            day = day - datetime.timedelta(days=1)
        return day


def perlinpinpin(text, timezone=None):
    dates = Perlinpinpin().extract(text, timezone)
    if dates:
        return dates[0]
    raise ValueError


def parse(text, timezone=None):
    return Perlinpinpin().parse(text, timezone)


def extract(text, timezone=None):
    return Perlinpinpin().extract(text, timezone)
