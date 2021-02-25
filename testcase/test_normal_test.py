import sys

sys.path.append("..")
from po.browser_engine import BrowserEngine
from po.base_page import NormalPage
import pytest
import allure
import time

"""
操作对应:
    点击   page.element() page.click()
    输入   page.send_keys()
    打开网页  page.open_url()
    滚动   
    人工   time.sleep()

"""


@allure.feature("普通的测试")
class TestNormal:
    @classmethod
    def setup_class(cls):
        browse = BrowserEngine(cls)
        cls.driver = browse.get_driver()
        cls.page = NormalPage(cls.driver)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    @allure.story("测试通用功能1")
    @pytest.mark.dependency(name='test_noraml')
    @pytest.mark.parametrize("username, password", [('root', '12345678!a'), ()])
    def test_noraml(self, username, password):
        self.page.open_url('https://tsjc.patec.net/')
        ele_username = self.page.element('/html/body/div[1]/div/div[2]/div/form/div[1]/div/div[1]/input', name='用户名输入框')
        self.page.send_keys(ele_username, username, name='用户名输入框')

        ele_password = self.page.element('//*[@id="app"]/div/div[2]/div/form/div[2]/div/div/input', name='密码输入框')
        self.page.send_keys(ele_password, password, name='密码输入框')

        time.sleep(5)

        ele_submit = self.page.element('//*[@id="app"]/div/div[2]/div/form/div[4]/div/button', name='提交按钮')
        self.page.click_element(ele_submit, name='提交按钮')

    @allure.story("测试通用功能2")
    @pytest.mark.dependency(depends=["test_noraml"])
    def test_normal_2(self):
        self.page.element('//*[@id="app"]/div/div[1]/div[1]/div/ul/div[1]/a/li')


if __name__ == '__main__':
    pytest.main()
