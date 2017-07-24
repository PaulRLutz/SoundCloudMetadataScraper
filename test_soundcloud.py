import unittest
from soundcloud import *

class SoundcloudTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    self.driver = get_firefox_selenium_driver()

  def test_example_1(self):
    pass

  def test_chance_user_playists_urls(self):
    #test_args = ["--user", "chancetherapper", "--playlists"]
    #tracks = main(test_args=test_args)
    #print(tracks)
    chance_playlists_urls = get_user_playlists_urls(self.driver, "chancetherapper")
    self.assertTrue(chance_playlists_urls == ['https://soundcloud.com/chancetherapper/sets/new-1', 'https://soundcloud.com/chancetherapper/sets/coloring-book', 'https://soundcloud.com/chancetherapper/sets/sox', 'https://soundcloud.com/chancetherapper/sets/chance-the-rapper-acid-rap'])
   
  def test_chance_acid_rap_tracks(self):
    tracks = get_tracks_from_url(self.driver, "https://soundcloud.com/chancetherapper/sets/chance-the-rapper-acid-rap")
    self.assertTrue(tracks == [{'title': "Good Ass Intro (ft. BJ The Chicago Kid, Lili K., Kiara Lanier, Peter Cottontale, Will for the O'mys, & JP Floyd for Kids These Days)", 'artist': '"Chance The Rapper"', 'href': 'https://soundcloud.com/chancetherapper/good-ass-intro-ft-bj-the?in=chancetherapper/sets/chance-the-rapper-acid-rap', 'go': False, 'set_title': 'Chance The Rapper - Acid Rap', 'set_user': '"Chance The Rapper"', 'set_user_id': 'https://soundcloud.com/chancetherapper'}, {'title': 'Pusha Man (ft. Nate Fox & Lili K.)', 'artist': '"Chance The Rapper"', 'href': 'https://soundcloud.com/chancetherapper/pusha-man-ft-nate-fox-lili-k?in=chancetherapper/sets/chance-the-rapper-acid-rap', 'go': False, 'set_title': 'Chance The Rapper - Acid Rap', 'set_user': '"Chance The Rapper"', 'set_user_id': 'https://soundcloud.com/chancetherapper'}, {'title': 'Cocoa Butter Kisses (ft. Vic Mensa & Twista)', 'artist': '"Chance The Rapper"', 'href': 'https://soundcloud.com/chancetherapper/cocoa-butter-kisses-ft-vic?in=chancetherapper/sets/chance-the-rapper-acid-rap', 'go': False, 'set_title': 'Chance The Rapper - Acid Rap', 'set_user': '"Chance The Rapper"', 'set_user_id': 'https://soundcloud.com/chancetherapper'}, {'title': 'Juice', 'artist': '"Chance The Rapper"', 'href': 'https://soundcloud.com/chancetherapper/juice?in=chancetherapper/sets/chance-the-rapper-acid-rap', 'go': False, 'set_title': 'Chance The Rapper - Acid Rap', 'set_user': '"Chance The Rapper"', 'set_user_id': 'https://soundcloud.com/chancetherapper'}, {'title': 'Lost (ft. Noname Gypsy)', 'artist': '"Chance The Rapper"', 'href': 'https://soundcloud.com/chancetherapper/lost-ft-noname-gypsy?in=chancetherapper/sets/chance-the-rapper-acid-rap', 'go': False, 'set_title': 'Chance The Rapper - Acid Rap', 'set_user': '"Chance The Rapper"', 'set_user_id': 'https://soundcloud.com/chancetherapper'}, {'title': "Everybody's Something (ft. Saba & BJ The Chicago Kid) 1", 'artist': '"Chance The Rapper"', 'href': 'https://soundcloud.com/chancetherapper/everybodys-something-ft-saba?in=chancetherapper/sets/chance-the-rapper-acid-rap', 'go': False, 'set_title': 'Chance The Rapper - Acid Rap', 'set_user': '"Chance The Rapper"', 'set_user_id': 'https://soundcloud.com/chancetherapper'}, {'title': "Interlude (That's Love)", 'artist': '"Chance The Rapper"', 'href': 'https://soundcloud.com/chancetherapper/interlude-thats-love?in=chancetherapper/sets/chance-the-rapper-acid-rap', 'go': False, 'set_title': 'Chance The Rapper - Acid Rap', 'set_user': '"Chance The Rapper"', 'set_user_id': 'https://soundcloud.com/chancetherapper'}, {'title': 'Favorite Song (ft. Childish Gambino)', 'artist': '"Chance The Rapper"', 'href': 'https://soundcloud.com/chancetherapper/favorite-song-ft-childish?in=chancetherapper/sets/chance-the-rapper-acid-rap', 'go': False, 'set_title': 'Chance The Rapper - Acid Rap', 'set_user': '"Chance The Rapper"', 'set_user_id': 'https://soundcloud.com/chancetherapper'}, {'title': 'NaNa (ft. Action Bronson)', 'artist': '"Chance The Rapper"', 'href': 'https://soundcloud.com/chancetherapper/nana-ft-action-bronson?in=chancetherapper/sets/chance-the-rapper-acid-rap', 'go': False, 'set_title': 'Chance The Rapper - Acid Rap', 'set_user': '"Chance The Rapper"', 'set_user_id': 'https://soundcloud.com/chancetherapper'}, {'title': 'Smoke Again (ft. Ab-Soul)', 'artist': '"Chance The Rapper"', 'href': 'https://soundcloud.com/chancetherapper/smoke-again-ft-ab-soul?in=chancetherapper/sets/chance-the-rapper-acid-rap', 'go': False, 'set_title': 'Chance The Rapper - Acid Rap', 'set_user': '"Chance The Rapper"', 'set_user_id': 'https://soundcloud.com/chancetherapper'}, {'title': 'Acid Rain', 'artist': '"Chance The Rapper"', 'href': 'https://soundcloud.com/chancetherapper/acid-rain-1?in=chancetherapper/sets/chance-the-rapper-acid-rap', 'go': False, 'set_title': 'Chance The Rapper - Acid Rap', 'set_user': '"Chance The Rapper"', 'set_user_id': 'https://soundcloud.com/chancetherapper'}, {'title': 'Chain Smoker', 'artist': '"Chance The Rapper"', 'href': 'https://soundcloud.com/chancetherapper/chain-smoker?in=chancetherapper/sets/chance-the-rapper-acid-rap', 'go': False, 'set_title': 'Chance The Rapper - Acid Rap', 'set_user': '"Chance The Rapper"', 'set_user_id': 'https://soundcloud.com/chancetherapper'}, {'title': "Everything's Good (Good Ass Outro)", 'artist': '"Chance The Rapper"', 'href': 'https://soundcloud.com/chancetherapper/everythings-good-good-ass?in=chancetherapper/sets/chance-the-rapper-acid-rap', 'go': False, 'set_title': 'Chance The Rapper - Acid Rap', 'set_user': '"Chance The Rapper"', 'set_user_id': 'https://soundcloud.com/chancetherapper'}])

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

