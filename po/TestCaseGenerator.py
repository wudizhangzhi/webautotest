import os
import json
from jinja2 import Template, BaseLoader, Environment, FileSystemLoader

"""
json格式

{
    "sheet1":{
        "模块1": [
            {
                "testcase_name": "用例名称",
                "dependency": "前置条件",
                "ops": [
                    {
                        "idx": 1,
                        "op_type": "点击",  # 操作类型
                        "target": "用户名输入框", # 对象
                        "value": "value1, value2",  # 数值
                        "xpath": "",  # 
                        "expect_type": "存在",  # 预期结果_判断类型
                        "expect_target": "输出框",  # 预期结果_对象
                        "expect_value": "value1, value2",  # 预期结果_数值
                        "expect_xpath": "",  # 预期结果_xpath
                        "desc": "",  # 描述
                    },
                ]
            }
            
        ],
    },
    "sheet2":{
        "模块3": [
        ]
    },
}
"""



def json_2_testcase(j):
    """
    @allure.story("测试通用功能1")
    @pytest.mark.dependency(name='test_noraml')
    @pytest.mark.parametrize("username, password", [('root', '12345678!a')])
    def test_noraml(self, username, password):
        self.page.open_url('https://tsjc.patec.net/')
        ele_username = self.page.element('/html/body/div[1]/div/div[2]/div/form/div[1]/div/div[1]/input', name='用户名输入框')
        self.page.send_keys(ele_username, username, name='用户名输入框')

        ele_password = self.page.element('//*[@id="app"]/div/div[2]/div/form/div[2]/div/div/input', name='密码输入框')
        self.page.send_keys(ele_password, password, name='密码输入框')

        time.sleep(5)

        ele_submit = self.page.element('//*[@id="app"]/div/div[2]/div/form/div[4]/div/button', name='提交按钮')
        self.page.click_element(ele_submit, name='提交按钮')

    1.判断是否有target没有xpath
    2.整合一个target的xpath字典
    3.生成输入数值的字典
    4.生成变量对象字典

    :param json:
    :return:
    """


def test():
    test_data = {
        "testcase_name": "用例名称",
        "dependency": "前置条件",
        "ops": [
            {
                "idx": 1,
                "op_type": "点击",  # 操作类型
                "target": "用户名输入框",  # 对象
                "value": "value1, value2",  # 数值
                "xpath": "/input",  #
                "expect_type": "存在",  # 预期结果_判断类型
                "expect_target": "输出框",  # 预期结果_对象
                "expect_value": "value1, value2",  # 预期结果_数值
                "expect_xpath": "",  # 预期结果_xpath
                "desc": "",  # 描述
            },
            {
                "idx": 2,
                "op_type": "点击",  # 操作类型
                "target": "fffff",  # 对象
                "xpath": "",  #
                "expect_type": "存在",  # 预期结果_判断类型
                "expect_target": "输出框",  # 预期结果_对象
                "expect_value": "value1, value2",  # 预期结果_数值
                "expect_xpath": "",  # 预期结果_xpath
                "desc": "",  # 描述
            },
        ]
    }
    variables_dict = {}
    # template = Template(open("F:/github/webauto/po/templates/test_function.templ", encoding='utf-8').read())
    template = Environment(loader=FileSystemLoader("F:/github/webauto/po/templates/")).from_string(open("F:/github/webauto/po/templates/test_function.templ", encoding='utf-8').read())
    result = template.render(test_data, variables_dict=variables_dict)
    print(result)


if __name__ == '__main__':
    test()
