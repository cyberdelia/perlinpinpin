# -*- coding: utf-8 -*-
import unittest, datetime
import perlinpinpin

class TestPerlinpinpin(unittest.TestCase):
    def _make_date(self):
        class MockDate(datetime.date):
            @classmethod
            def today(cls):
                return datetime.date(2009, 3, 6)
        return MockDate
    
    def setUp(self):
        self.old_date = datetime.date
        datetime.date = self._make_date()
        self.perlinpinpin = perlinpinpin.perlinpinpin
    
    def tearDown(self):
        datetime.date = self.old_date
    
    def test_exception(self):
        self.assertRaises(ValueError, self.perlinpinpin, u"4 Jnaier")
        self.assertRaises(ValueError, self.perlinpinpin, u"Luni prochain")
        self.assertRaises(ValueError, self.perlinpinpin, u"supercalifragilisticexpialidocious")
    
    def test_today(self):
        self.assertEqual(self.perlinpinpin(u"aujourd'hui"), datetime.date(2009, 3, 6))
    
    def test_yesterday(self):
        self.assertEqual(self.perlinpinpin(u"hier"), datetime.date(2009, 3, 5))
    
    def test_before_yesterday(self):
        self.assertEqual(self.perlinpinpin(u"avant-hier"), datetime.date(2009, 3, 4))
        self.assertEqual(self.perlinpinpin(u"avant hier"), datetime.date(2009, 3, 4))
    
    def test_tomorrow(self):
        self.assertEqual(self.perlinpinpin(u"demain"), datetime.date(2009, 3, 7))
        
    def test_after_tomorrow(self):
        self.assertEqual(self.perlinpinpin(u"après-demain"), datetime.date(2009, 3, 8))
        self.assertEqual(self.perlinpinpin(u"après demain"), datetime.date(2009, 3, 8))
    
    def test_last_tuesday(self):
        self.assertEqual(self.perlinpinpin(u"mardi dernier"), datetime.date(2009, 3, 3))
    
    def test_next_tuesday(self):
        self.assertEqual(self.perlinpinpin(u"mardi prochain"), datetime.date(2009, 3, 10))
    
    def test_last_week(self):
        self.assertEqual(self.perlinpinpin(u"la semaine dernière"), datetime.date(2009, 2, 27))
        self.assertEqual(self.perlinpinpin(u"semaine dernière"), datetime.date(2009, 2, 27))
    
    def test_next_week(self):
        self.assertEqual(self.perlinpinpin(u"la semaine prochaine"), datetime.date(2009, 3, 13))
        self.assertEqual(self.perlinpinpin(u"semaine prochaine"), datetime.date(2009, 3, 13))
    
    def test_day(self):
        self.assertEqual(self.perlinpinpin(u"4"), datetime.date(2009, 3, 4))
        self.assertEqual(self.perlinpinpin(u"le 4"), datetime.date(2009, 3, 4))
    
    def test_day_and_month(self):
        self.assertEqual(self.perlinpinpin(u"4 Avril"), datetime.date(2009, 4, 4))
        self.assertEqual(self.perlinpinpin(u"le 4 Avril"), datetime.date(2009, 3, 4))
        self.assertEqual(self.perlinpinpin(u"4 Fevrier"), datetime.date(2009, 2, 4))
        self.assertEqual(self.perlinpinpin(u"4 Février"), datetime.date(2009, 2, 4))
        
    def test_day_and_month(self):
        self.assertEqual(self.perlinpinpin(u"4 Avril 2008"), datetime.date(2008, 4, 4))
        self.assertEqual(self.perlinpinpin(u"le 4 Avril 2008"), datetime.date(2008, 4, 4))
    
    def test_european_style(self):
        self.assertEqual(self.perlinpinpin(u"02/03/2009"), datetime.date(2009, 3, 2))
        self.assertEqual(self.perlinpinpin(u"2/3/2009"), datetime.date(2009, 3, 2))
    
    def test_american_style(self):
        self.assertEqual(self.perlinpinpin(u"01/24/2009"), datetime.date(2009, 1, 24))
        self.assertEqual(self.perlinpinpin(u"1/24/2009"), datetime.date(2009, 1, 24))
    
    def test_iso_style(self):
        self.assertEqual(self.perlinpinpin(u"2009-01-09"), datetime.date(2009, 1, 9))
        self.assertEqual(self.perlinpinpin(u"2009-1-9"), datetime.date(2009, 1, 9))
    
    def test_time_ago(self):
        self.assertEqual(self.perlinpinpin(u"il y a 2 jours"), datetime.date(2009, 3, 4))
        self.assertEqual(self.perlinpinpin(u"il y a 1 semaine"), datetime.date(2009, 2, 27))
        self.assertEqual(self.perlinpinpin(u"il y a 2 semaines"), datetime.date(2009, 2, 20))
        self.assertEqual(self.perlinpinpin(u"il y a 1 semaine et 3 jours"), datetime.date(2009, 2, 24))
    

if __name__ == '__main__':
    unittest.main()
