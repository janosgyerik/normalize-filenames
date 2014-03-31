#!/usr/bin/env python

import unittest
from test.test_support import run_unittest
from movies import MovieFilenameNormalizer


class NormalizerTestCase(unittest.TestCase):
    def setUp(self):
        self.normalizer = MovieFilenameNormalizer()

    def test_well_formatted(self):
        self.assertTrue(self.normalizer.is_well_formatted('La Dolce Vita (1961).avi'))
        self.assertTrue(self.normalizer.is_well_formatted('La Dolce (1961).avi'))
        self.assertTrue(self.normalizer.is_well_formatted('Dolce (1961).avi'))
        self.assertTrue(self.normalizer.is_well_formatted('Dolce 2 (1961).avi'))
        self.assertTrue(self.normalizer.is_well_formatted('2012 (2012).avi'))
        self.assertTrue(self.normalizer.is_well_formatted('300 (2011).avi'))
        self.assertTrue(self.normalizer.is_well_formatted('12 Months (2011).avi'))

    def test_not_well_formatted(self):
        self.assertFalse(self.normalizer.is_well_formatted('La Dolce Vita[1961]DVDrip[Eng Subs]-Wurd.avi'))
        self.assertFalse(self.normalizer.is_well_formatted('La Dolce Vita[1961]DVDrip[Eng Subs].avi'))
        self.assertFalse(self.normalizer.is_well_formatted('La Dolce Vita[1961].avi'))
        self.assertFalse(self.normalizer.is_well_formatted('La Dolce Vita [1961].avi'))
        self.assertFalse(self.normalizer.is_well_formatted('La Dolce [1961].avi'))
        self.assertFalse(self.normalizer.is_well_formatted('La Dolce {1961}.avi'))
        self.assertFalse(self.normalizer.is_well_formatted('La Dolce <1961>.avi'))
        self.assertFalse(self.normalizer.is_well_formatted('La Dolce 1961.avi'))
        self.assertFalse(self.normalizer.is_well_formatted('2012.avi'))
        self.assertFalse(self.normalizer.is_well_formatted('300.avi'))
        self.assertFalse(self.normalizer.is_well_formatted('12 Months.avi'))
        self.assertFalse(self.normalizer.is_well_formatted('12 Months (2012)'))
        self.assertFalse(self.normalizer.is_well_formatted('12 Months (2012).'))
        self.assertFalse(self.normalizer.is_well_formatted('12 Months (2012).100'))
        self.assertFalse(self.normalizer.is_well_formatted('12 Months (2012).mk'))
        self.assertFalse(self.normalizer.is_well_formatted(' 12 Months (2012).mkv'))
        self.assertFalse(self.normalizer.is_well_formatted('12 Months  (2012).mkv'))

    def test_normalize(self):
        well_formatted = 'La Dolce (1961).avi'
        self.assertEqual(well_formatted, self.normalizer.normalize(well_formatted))
        self.assertEqual(well_formatted, self.normalizer.normalize('La Dolce[1961]DVDrip[Eng Subs].avi'))
        self.assertEqual(well_formatted, self.normalizer.normalize('La Dolce[1961].avi'))
        self.assertEqual(well_formatted, self.normalizer.normalize('La Dolce [1961].avi'))
        self.assertEqual(well_formatted, self.normalizer.normalize('La Dolce [1961].avi'))
        self.assertEqual(well_formatted, self.normalizer.normalize('La Dolce {1961}.avi'))
        self.assertEqual(well_formatted, self.normalizer.normalize('La Dolce <1961>.avi'))
        self.assertEqual(well_formatted, self.normalizer.normalize('La Dolce 1961.avi'))
        self.assertEqual(well_formatted, self.normalizer.normalize('La Dolce (1961) .avi'))
        self.assertEqual(well_formatted, self.normalizer.normalize(' La Dolce (1961).avi'))
        self.assertEqual(well_formatted, self.normalizer.normalize('La  Dolce (1961).avi'))
        self.assertEqual(well_formatted, self.normalizer.normalize('La Dolce (1961).avi'))
        self.assertEqual(well_formatted, self.normalizer.normalize('La Dolce ( 1961).avi'))

    def assert_basename(self, expected, filename):
        basename, _, _ = self.normalizer.split_to_parts(filename)
        self.assertEqual(expected, self.normalizer.normalize_basename(basename))

    def test_normalize_basename(self):
        self.assert_basename('La Dolce', 'La Dolce [1961].avi')
        self.assert_basename('La Dolce', 'la dolce [1961].avi')
        self.assert_basename('La Dolce', 'la DOLCE [1961].avi')
        self.assert_basename('La Dolce', ' La Dolce [1961].avi')
        self.assert_basename('La Dolce', 'La Dolce  [1961].avi')
        self.assert_basename('La Dolce', 'La  Dolce  [1961].avi')
        self.assert_basename('La Dolce', 'La Dolce[1961]DVDrip[Eng Subs].avi')
        self.assert_basename('La Dolce', 'La Dolce[1961].avi')
        self.assert_basename('La Dolce', 'La Dolce [1961].avi')
        self.assert_basename('La Dolce', 'La Dolce {1961}.avi')
        self.assert_basename('La Dolce', 'La Dolce <1961>.avi')
        self.assert_basename('La Dolce', 'La Dolce.avi')
        self.assert_basename('La Dolce', 'La Dolce 1961')
        self.assert_basename('La Dolce', 'la dolce')
        self.assert_basename('La Dolce', 'la.dolce')
        self.assert_basename('American Hustle', 'American.Hustle.2013.1080p.BluRay.x264.YIFY.mp4')

    def assert_year(self, expected, filename):
        _, year, _ = self.normalizer.split_to_parts(filename)
        self.assertEqual(expected, year)

    def test_normalize_year(self):
        self.assert_year('1961', 'La Dolce [1961].avi')
        self.assert_year('1961', 'la dolce [1961].avi')
        self.assert_year('1961', 'la DOLCE [1961].avi')
        self.assert_year('1961', ' La Dolce [1961].avi')
        self.assert_year('1961', 'La Dolce  [1961].avi')
        self.assert_year('1961', 'La Dolce[1961]DVDrip[Eng Subs].avi')
        self.assert_year('1961', 'La Dolce[1961].avi')
        self.assert_year('1961', 'La Dolce [1961].avi')
        self.assert_year('1961', 'La Dolce {1961}.avi')
        self.assert_year('1961', 'La Dolce <1961>.avi')
        self.assert_year(None, 'La Dolce.avi')
        self.assert_year('1961', 'La Dolce 1961')
        self.assert_year('2013', 'American.Hustle.2013.1080p.BluRay.x264.YIFY.mp4')

    def assert_ext(self, expected, filename):
        _, _, ext = self.normalizer.split_to_parts(filename)
        self.assertEqual(expected, self.normalizer.normalize_ext(ext))

    def test_normalize_ext(self):
        self.assert_ext('avi', 'La Dolce [1961].avi')
        self.assert_ext('avi', 'la dolce [1961].AVI')
        self.assert_ext('avi', ' La Dolce [1961].aVI')
        self.assert_ext(None, 'La Dolce')
        self.assert_ext('avi', 'la DOLCE [1961]. avi')
        self.assert_ext('avi', 'La Dolce  [1961].avi ')

    def test_valid_extension(self):
        self.assertFalse(self.normalizer.has_valid_extension('', 'avi', 'mkv'))
        self.assertFalse(self.normalizer.has_valid_extension('file.txt', 'avi', 'mkv'))
        self.assertFalse(self.normalizer.has_valid_extension('file.avi2', 'avi', 'mkv'))
        self.assertFalse(self.normalizer.has_valid_extension('file.2avi', 'avi', 'mkv'))
        self.assertFalse(self.normalizer.has_valid_extension('avi', 'avi', 'mkv'))
        self.assertTrue(self.normalizer.has_valid_extension('file. avi', 'avi', 'mkv'))
        self.assertTrue(self.normalizer.has_valid_extension('file.avi ', 'avi', 'mkv'))


def test_main():
    run_unittest(
            NormalizerTestCase,
            )

if __name__ == '__main__':
    test_main()
