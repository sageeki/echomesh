from __future__ import absolute_import, division, print_function, unicode_literals

from cechomesh import Color

from echomesh.util.TestCase import TestCase

class ColorTest(TestCase):
  def test_empty_color(self):
    self.assertEqual(str(Color()), 'none')

  def test_black(self):
    self.assertEqual(str(Color('black')), 'black')

  def test_red(self):
    self.assertEqual(str(Color('red')), 'red')

  def test_red2(self):
    self.assertEqual(str(Color([1.0, 0, 0])), 'red')

  def test_equal(self):
    self.assertEqual(Color('red'), Color('red'))

  def test_unnamed(self):
    self.assertEqual(str(Color([0.7, 0.1, 0.2])),
                     '[red=0.700, green=0.100, blue=0.200]')

  def test_unknown(self):
    self.assertRaises(ValueError, Color, 'glug')

  def test_sort2(self):
    self.assertTrue(Color('blue') > Color('green'))

  def test_sort6(self):
    self.assertTrue(Color('blue') > Color('red'))

  def test_sort9(self):
    self.assertTrue(Color('green') > Color('red'))