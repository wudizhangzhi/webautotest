import os
from selenium import webdriver


class BrowserEngine(object):
    chrome_driver_path = os.path.join(os.path.dirname(os.path.basename(__file__)), 'driver', 'chromedriver.exe')

    def __init__(self, selenium_driver=None):
        self.driver = selenium_driver

    def get_driver(self):
        selenium_driver = webdriver.Chrome(self.chrome_driver_path)
        selenium_driver.maximize_window()
        selenium_driver.implicitly_wait(10)
        return selenium_driver
