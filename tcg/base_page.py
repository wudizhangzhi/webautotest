from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from selenium.webdriver.common.by import By
import time


class BasePage:
    def __init__(self, selenium_driver):
        self.driver = selenium_driver

    def find_element(self, *loc):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
            return self.driver.find_element(*loc)
        except:
            raise Exception("%s 页面未能找到 %s 元素" % (self, loc))


class NormalPage(BasePage):
    @allure.step('打开链接: {1}')
    def open_url(self, url):
        self.driver.get(url)

    @allure.step('找到{name}元素: {loc}')
    def element(self, loc, by=By.XPATH, name=None):
        ele = self.find_element(by, loc)
        return ele

    @allure.step('点击 {name}')
    def click_element(self, ele, name=None):
        ele.click()

    @allure.step('向元素: {name} 输入 {keys}')
    def send_keys(self, ele, keys, name=None):
        ele.send_keys(keys)

    @allure.step('验证标题是否正确')
    def verify(self, verify_char):
        title = self.driver.title
        print(title)
        assert verify_char == title
