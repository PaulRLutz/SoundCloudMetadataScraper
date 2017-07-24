import unittest
from soundcloud import *

class SoundcloudTest(unittest.TestCase):

  def test_example_1(self):
    pass

  def test_random_user_playists(self):
    test_args = ["--user", "chancetherapper", "--playlists"]
    tracks = main(test_args=test_args)
    print(tracks)
    
  '''
  def test_upper(self):
    self.assertEqual('foo'.upper(), 'FOO')
    self.assertTrue('FOO'.isupper())
    self.assertFalse('Foo'.isupper())
    with self.assertRaises(TypeError):
      s.split(2)
  '''

if __name__ == '__main__':
  unittest.main()

