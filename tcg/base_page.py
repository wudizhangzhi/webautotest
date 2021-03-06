from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

from tcg.browser_engine import BrowserEngine


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
    def element(self, loc, by=By.CSS_SELECTOR, name=None):
        ele = self.find_element(by, loc)
        return ele

    @allure.step('点击 {name}')
    def click_element(self, ele, name=None):
        ele.click()

    @allure.step('向元素: {name} 输入 {keys}')
    def send_keys(self, ele, keys, name=None):
        ele.send_keys(keys)

    @allure.step('{name} 选择 {value}')
    def select(self, ele, value, name=None):
        select = Select(ele)
        # select by visible text
        select.select_by_visible_text(value)
        # # select by value
        # select.select_by_value('1')

    @allure.step('{name} 选择 {value}')
    def select_by_visible_text(self, ele, value, name=None):
        matches = ele.find_elements_by_xpath(f"//*[contains(text(), '{value}')]")
        matches[-1].click()

    @allure.step('{name} 上传 {value}')
    def upload(self, ele, value, name=None):
        # script = f"""document.querySelector("{xpath}").value = '{value};'"""
        # self.driver.execute_script(script)
        ele_input = ele.find_element_by_xpath('//input[@type="file"]')
        ele_input.send_keys(value)

    @allure.step('人工操作, 等待{0}')
    def manual(self, value=10):
        time.sleep(value)

    @allure.step('验证标题是否正确')
    def verify(self, verify_char):
        title = self.driver.title
        assert verify_char == title


browse = BrowserEngine()
page = NormalPage(browse.get_driver())
