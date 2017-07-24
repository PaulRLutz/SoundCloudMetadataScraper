from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import os
from os.path import expanduser
import configparser
import argparse
from pyvirtualdisplay import Display
import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)

def get_user_playlists_urls(driver, user_id=None):
  if user_id is not None:
    driver.get(f"https://soundcloud.com/{user_id}")
  else:
    driver.get("https://soundcloud.com/")

  if user_id is None:
    driver.find_element_by_xpath('//a[@href="/you/collection"]').click()
    time.sleep(3)
  if user_id is None:
    driver.find_element_by_xpath('//a[@href="/you/sets"]').click()
  else:
    driver.find_element_by_xpath(f'//a[@href="/{user_id}/sets"]').click()
  time.sleep(3)

  set_names = []
  set_names_old = []
  while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3) # TODO Replace with wait
    set_names_old = list(set_names)
    set_names = [a.text for a in driver.find_elements_by_xpath('//a[contains(@href, "/sets/")]') if "tracks" not in a.text]
    if len(set_names) > len(set_names_old):
      log.debug("found new sets, keep scrolling")
      pass # found some new set names, so scroll and try again
    else:
      log.debug("no more sets found")
      break # no more set names were found after scrolling, so we're probably done

  return [a.get_attribute("href") for a in driver.find_elements_by_xpath('//a[contains(@href, "/sets/")]') if "tracks" not in a.text]

def get_tracks_from_url(driver, url):
  driver.get(url)

  try:
    set_title = driver.find_element_by_class_name("soundTitle__title").text
    log.debug(f"set title: {set_title}")
  except NoSuchElementException:
    set_title = None

  try:
    set_user_element = driver.find_element_by_class_name("soundTitle__username")
    set_user = set_user_element.text
    set_user_id = set_user_element.get_attribute("href")
    log.debug(f"set user: {set_user}")
    log.debug(f"set user id: {set_user_id}")
  except NoSuchElementException:
    set_user = None
    set_user_id = None

  track_elements = []
  old_track_elements = []

  while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4) # TODO Replace with wait
    old_track_elements = list(track_elements)
    track_elements = driver.find_elements_by_class_name("trackList__item")
    log.debug(f"num track elements: {len(track_elements)}, num old track elements: {len(old_track_elements)}")
    if len(track_elements) > len(old_track_elements):
      log.debug("found new track_elements, keep scrolling")
      pass # found some new track_elements, so scroll and try again
    else:
      log.debug("no more track_elements found")
      break # no more track_elements were found after scrolling, so we're probably done
  tracks = []
  for track_element in track_elements:
    try:
      track_title_element = track_element.find_element_by_class_name("trackItem__trackTitle")
      title = track_title_element.text
      href = track_title_element.get_attribute("href")
    except NoSuchElementException:
      title = None
      href = None
    try:
      artist = track_element.find_element_by_class_name("trackItem__username").text
    except NoSuchElementException:
      artist = set_user
    go = None
    try:
      track_element.find_element_by_class_name("sc-hidden")
      go = False
    except NoSuchElementException:
      go = True
    track = {
        "title" : title,
        "artist" : artist,
        "href" : href,
        "go" : go,
        "set_title" : set_title,
        "set_user" : set_user,
        "set_user_id" : set_user_id,
        }
    tracks.append(track)

  return tracks

def get_firefox_profile_path(profiles_folder_path="~/.mozilla/firefox", profile_name="Profile0"):
  """Gets the path to a firefox profile folder.
  Args:
    profiles_folder_path (str, optional, default='~/.mozilla/firefox'): Location of the profiles folders path.
    profile_name (str, optional, default='Profile0'): The name of the profile in the profiles.ini config file.
  Returns:
    str: The path of the profile folder. Returns None if both the user specified and default values are invalid.
  
  If the user specified profiles_folder_path or profile_name aren't found, the defaults are used instead. 


  """
  if not os.path.isdir(expanduser(profiles_folder_path)):
    log.warn(f"profiles path: {profiles_folder_path} doesn't exist, switching to default")
    profiles_folder_path = "~/.mozilla/firefox"
    if not os.path.isdir(expanduser(profiles_folder_path)):
      log.error("Default profiles path also doesn't exist.")
      return None

  profiles_folder_path = expanduser(profiles_folder_path) # turn ~ into home folder

  # check to see if profiles.ini exists
  if not os.path.isfile(profiles_folder_path + os.sep + "profiles.ini"):
    log.warn("Couldn't find profiles.ini in profiles path.")
    return None

  config = configparser.ConfigParser({})
  try:
    config.read(profiles_folder_path + os.sep + "profiles.ini")
  except: # TODO either be more specific in the error catching, or more expressive in the user warning
    log.warn("Error reading profiles.ini config file.")
    return None

  # default profile is Profile0, try that if user specified profile doesn't exist
  if profile_name not in config.sections():
    log.error(f"couldn't find profile name: '{profile_name}', trying Profile0")
    profile_name = "Profile0"

  if "Path" not in config[profile_name]:
    log.warn(f"Couldn't find 'Path' in profile {profile_name}.")
    return None
  else:
    return profiles_folder_path + os.sep + config[profile_name]["Path"]

def main(test_args=None):
  parser = argparse.ArgumentParser()

  parser.add_argument(
      "-r", "--url",
      default=None,
      help="The url of the songs to scrape. If specified, then the user argument is ignored."
  )
  parser.add_argument(
      "-f", "--file",
      default=None,
      help="Path to store the data. If not specified, defaults to soundcloud_data_<increment>.<extension>"
  )
  parser.add_argument(
      "-u", "--user",
      default=None,
      help="User to extract data from. Defaults to logged in user."
  )
  parser.add_argument(
      "-i", "--firefox_profile_name",
      default="Profile0",
      help="The name of the firefox profile to use, from the setting.ini in the firefox profile folder (probably ~/.mozilla/firefox). Default is 'Profile0'"
  )
  parser.add_argument(
      "-v", "--virtual",
      action="store_true",
      default=True,
      help="Perform the scraping in a virtual display if True."
  )
  parser.add_argument(
      "-p", "--playlists",
      action="store_true",
      default=False,
      help="Get the playlists from the specified user."
  )
  parser.add_argument(
      "-a", "--albums",
      action="store_true",
      default=False,
      help="Get the albums from the specified user."
  )
  parser.add_argument(
      "-s", "--songs",
      action="store_true",
      default=False,
      help="Get the songs from the specified user."
  )
  parser.add_argument(
      "-l", "--likes",
      action="store_true",
      default=False,
      help="Get the like songs from the logged in user. "
  )

  if test_args is not None:
    args = parser.parse_args(test_args)
  else:
    args = parser.parse_args()

  if args.virtual:
    virtual_display = get_virtual_display()
  else:
    virtual_display = None

  firefox_profile_path = get_firefox_profile_path(profile_name=args.firefox_profile_name)
  driver = get_firefox_selenium_driver(firefox_profile_path=firefox_profile_path)

  if args.user is None: # If no user is specified, then we are getting the logged in user's stuff, so log in if they're not.
    driver.get("https://soundcloud.com/")
    if (len(driver.find_elements_by_class_name("frontHero__loginButton")) > 0):
      input("Please login, then press enter.")

  tracks = []
  if args.url is not None:
    tracks = get_tracks_from_url(driver, args.url)
  else:
    if not args.playlists and not args.albums and not args.songs and not args.likes:
      log.error("Please specify which songs to download.")
      return
    if args.playlists:
      for url in get_user_playlists_urls(driver, args.user):
        tracks.extend(get_tracks_from_url(driver, url))
    if args.albums:
      for url in get_user_albums_urls(driver, args.user):
        tracks.extend(get_tracks_from_url(driver, url))
    if args.songs:
      if args.user is not None:
        user_tracks_url = f"https://soundcloud.com/{args.user}/tracks"
      else:
        user_tracks_url = f"https://soundcloud.com/you/tracks"
      tracks.extend(get_tracks_from_url(driver, user_tracks_url))
    if args.likes:
      if args.user is None:
        log.error("User needs to be logged in to get their liked tracks")
      else:
        tracks.extend(get_tracks_from_url(driver, get_user_likes_url(driver)))

  driver.quit()
  if virtual_display is not None:
    virtual_display.stop()

  write_tracks_to_file(tracks, args.file)
  return tracks

def get_virtual_display():
  display = Display(visible=0, size=(800, 600))
  display.start()
  return display

def get_firefox_selenium_driver(firefox_profile_path=None):
  if firefox_profile_path is not None:
    profile = webdriver.FirefoxProfile(firefox_profile_path)
    return webdriver.Firefox(profile)
  else:
    return webdriver.Firefox()

def write_tracks_to_file(tracks, destination_file):
  pass

if __name__ == "__main__":
  main()
