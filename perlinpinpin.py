# -*- coding: utf-8 -*-
import os, re, datetime, calendar

__version__ = 0.3

class Perlinpinpin(object):
    def __init__(self):
        self.regexp = [
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
                    aujourd\'?hui                    # Today
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today()),
        
            # Now (special case, returns datetime.datetime
            (re.compile(
                r'''^
                    maintenant                      # Now
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.datetime.now()),
        
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
                    apres\-?\s?demain              # Afer-tomorrow
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today() + datetime.timedelta(days=2)),
            
            # Before-yesterday
            (re.compile(
                r'''^
                    avant\-?\s?hier              # Before-yesterday
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today() - datetime.timedelta(days=2)),
        
            # 4
            (re.compile(
                r'''^
                    (le                             # le
                    \s+)?                           # whitespace
                    (\w+\s+)?                       # vendredi
                    (?P<day>\d{1,2})                # 4
                    (?:ier|er|iere)?                # optional suffix
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today().replace(
                day=int(m.group('day')))),
        
            # 4 Janvier
            (re.compile(
                r'''^
                    (le                             # le
                    \s+)?                           # whitespace
                    (\w+\s+)?                       # vendredi
                    (?P<day>\d{1,2})                # 4
                    (?:ier|er|iere)?                # optional suffix
                    \s+                             # whitespace
                    (?P<month>\w+)                  # Janvier
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today().replace(
                day=int(m.group('day')),
                month=self._parseMonth(m.group('month')))),
        
            # 4 Janvier 2003
            (re.compile(
                r'''^
                    (le                             # le
                    \s+)?                           # whitespace
                    (\w+\s+)?                       # vendredi
                    (?P<day>\d{1,2})                # 4
                    (?:ier|er|iere)?                # optional suffix
                    \s+                             # whitespace
                    (?P<month>\w+)                  # Janvier
                    ,?                              # optional comma
                    \s+                             # whitespace
                    (?P<year>\d{4})                 # 2003
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date(
                year=int(m.group('year')),
                month=self._parseMonth(m.group('month')),
                day=int(m.group('day')))),
        
            # dd/mm/yyyy (European style, default in case of doubt)
            (re.compile(
                r'''^
                    (le                             # le
                    \s+)?                           # whitespace
                    (?P<day>0?[1-9]|[12]\d|30|31)   # d or dd
                    /                               #
                    (?P<month>0?[1-9]|10|11|12)     # m or mm
                    /                               #
                    (?P<year>\d{4})               # yyyy
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date(
                year=int(m.group('year')),
                month=int(m.group('month')),
                day=int(m.group('day')))),
            
            # mm/dd/yyyy (American style)
            (re.compile(
                r'''^
                    (?P<month>0?[1-9]|10|11|12)     # m or mm
                    /                               #
                    (?P<day>0?[1-9]|[12]\d|30|31)   # d or dd
                    /                               #
                    (?P<year>\d{4})               # yyyy
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date(
                year=int(m.group('year')),
                month=int(m.group('month')),
                day=int(m.group('day')))),
        
            # yyyy-mm-dd (ISO style)
            (re.compile(
                r'''^
                    (?P<year>\d{4})                 # yyyy
                    -                               #
                    (?P<month>0?[1-9]|10|11|12)     # m or mm
                    -                               #
                    (?P<day>0?[1-9]|[12]\d|30|31)   # d or dd
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date(
                year=int(m.group('year')),
                month=int(m.group('month')),
                day=int(m.group('day')))),
        
            # yyyymmdd
            (re.compile(
                r'''^
                    (?P<year>\d{4})                 # yyyy
                    (?P<month>0?[1-9]|10|11|12)     # m or mm
                    (?P<day>0?[1-9]|[12]\d|30|31)   # d or dd
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
                    (la                             # la
                    \s+)?                           # whitespace
                    semaine                         # week
                    \s+                             # whitespace
                    derniere                        # last
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today() - datetime.timedelta(days=7)),
            
            # Semaine prochaine
            (re.compile(
                r'''^
                    (la                             # la
                    \s+)?                           # whitespace
                    semaine                         # week
                    \s+                             # whitespace
                    prochaine                       # last
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: datetime.date.today() + datetime.timedelta(days=7)),
            
            # Mardi prochain
            (re.compile(
                r'''^
                    (?P<weekday>\w+)                # Mardi
                    \s+                             # whitespace
                    prochain                        # next
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: self._nextWeekday(self._parseWeekday(m.group('weekday')))),
        
            # Mardi dernier
            (re.compile(
                r'''^
                    (?P<weekday>\w+)                # Mardi
                    (\s+                            # whitespace
                    dernier)?                       # last
                    $                               # EOL
                ''',
                (re.VERBOSE | re.IGNORECASE)),
            lambda m: self._lastWeekday(self._parseWeekday(m.group('weekday')))),
       ]
    
    def parse(self, input, tz=None):
        input = self._normalize(input)
        if tz is not None: os.environ['TZ'] = tz
        for r, f in self.regexp:
            m = r.match(input.strip())
            if m:
                return f(m)
        raise ValueError
    
    def _normalize(self, input):
        import unicodedata
        return unicodedata.normalize('NFKD', unicode(input)).encode('ASCII', 'ignore')
    
    def _parseMonth(self, input):
        months = "Janvier Fevrier Mars Avril Mai Juin Juillet Aout Septembre Octobre Novembre Decembre".split(' ')
        for i, month in enumerate(months):
            p = re.compile(input, re.IGNORECASE)
            if p.match(month): return i+1
        else:
            raise ValueError
    
    def _parseWeekday(self, input):
        days = "Lundi Mardi Mercredi Jeudi Vendredi Samedi Dimanche".split(' ')
        for i, day in enumerate(days):
            p = re.compile(input, re.IGNORECASE)
            if p.match(day): return i
        else:
            raise ValueError
    
    def _nextWeekday(self, weekday):
        day = datetime.date.today() + datetime.timedelta(days=1)
        while calendar.weekday(*day.timetuple()[:3]) != weekday:
            day = day + datetime.timedelta(days=1)
        return day
    
    def _lastWeekday(self, weekday):
        day = datetime.date.today() - datetime.timedelta(days=1)
        while calendar.weekday(*day.timetuple()[:3]) != weekday:
            day = day - datetime.timedelta(days=1)
        return day
    

def perlinpinpin(input, tz=None):
    return Perlinpinpin().parse(input, tz)
