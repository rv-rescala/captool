import unittest
from catswalk.scraping.webdriver import CWWebDriver
import time
from catswalk.scraping.types.type_webdriver import *
from selenium.webdriver.common.by import By


binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
executable_path = "/Users/rv/ws/tools/chromedriver"
proxy = None
headless = True
url = "https://video.unext.jp/book/title/BSD0000310877/BID0000856740"

request = CWWebDriver(binary_location=binary_location, executable_path=executable_path, execution_env=EXECUTION_ENV.LOCAL,  device = DEVICE.MOBILE_GALAXY_S5)
request.get(url=url)
request.move_to_element_by_class_name(class_name="Components__EpisodeListContainer-sc-4hyt7h-7 ejFlQx")
request.print_screen_by_window("/Users/rv/Desktop", "hoge.png")
#elem = request.driver.find_element_by_css_selector(".Components__EpisodeListContainer-sc-4hyt7h-7.ejFlQx")
#elem.location_once_scrolled_into_view
#request.print_fullscreen("/tmp", "test_print_screen")
time.sleep(100)
request.close()