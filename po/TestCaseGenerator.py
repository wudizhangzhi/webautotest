import sys

sys.path.append("..")
import os
import json
from itertools import product
from collections import defaultdict
from jinja2 import Template, BaseLoader, Environment, FileSystemLoader

from po.GenerateVariableName import chinese2variable, to_test_func_name, to_test_class_name, to_test_file_name

TEMPLATE_FLODER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
TEMPLATE_TESTCASE = os.path.join(TEMPLATE_FLODER, 'testcase.templ')
TEMPLATE_FUNCATION = os.path.join(TEMPLATE_FLODER, 'test_function.templ')

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


def generate_code_from_template(template_path, *args, **kwargs):
    variables = dict(*args, **kwargs)
    template = Environment(loader=FileSystemLoader(TEMPLATE_FLODER)).from_string(
        open(template_path, encoding='utf-8').read())
    return template.render(variables)


def generate_function_code(test_case):
    """生成一个测试用例代码"""
    ops = test_case.get('ops', [])
    target_dict = defaultdict(dict)  # 用于储存target的xpath，变量名，数值，元素名
    param_dict = {}  # 输入参数的字典
    for op in ops:
        # 1.判断是否有target没有xpath
        # 2.整合一个target的xpath字典
        # 3.生成输入数值的字典（target转变量名）
        # 4.生成target元素对象字典(target转元素变量名)
        # 5.expect_target的字典
        # 6.期望值变量对象的字典
        target = op['target']
        if target not in target_dict:
            target_dict[target] = {}
        xpath = op.get('xpath')
        if xpath:
            target_dict[target]['xpath'] = xpath
        if not (target_dict[target].get('variable_name') and target_dict[target].get('element_name')):
            variable_name = chinese2variable(target)
            element_name = f"ele_{variable_name}"
            target_dict[target]['variable_name'] = variable_name
            target_dict[target]['element_name'] = element_name
        value = op.get('value')
        if value:
            param_dict[target_dict[target]['variable_name']] = value.split(',')

        # 预期
        expect_target = op.get('expect_target')
        if expect_target:
            if expect_target not in target_dict:
                target_dict[expect_target] = {}
            expect_xpath = op.get('expect_xpath')
            if expect_xpath:
                target_dict[expect_target]['xpath'] = expect_xpath
            if not (target_dict[expect_target].get('variable_name') and target_dict[expect_target].get(
                    'element_name')):
                variable_name = chinese2variable(expect_target)
                element_name = f"ele_{variable_name}"
                target_dict[expect_target]['variable_name'] = variable_name
                target_dict[expect_target]['element_name'] = element_name
    # TODO 如果有target的属性不全。报错
    # 生成test_case代码
    test_function_name = to_test_func_name(test_case['testcase_name'])
    # 整个输入参数
    params = ', '.join(list(param_dict.keys()))
    params_values = list(product(*param_dict.values()))
    function_code = generate_code_from_template(TEMPLATE_FUNCATION, test_case, target_dict=target_dict,
                                                test_function_name=test_function_name, params=params,
                                                params_values=params_values)
    return function_code


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

    :param json:
    :return:
    """
    for sheet, sheet_data in j.items():
        for module, test_case_list in sheet_data.items():
            func_code_list = []
            for test_case in test_case_list:
                func_code = generate_function_code(test_case)
                func_code_list.append(func_code)
                print(func_code)
                print('-'*50)
            test_class_name = to_test_class_name(module)
            result = generate_code_from_template(TEMPLATE_TESTCASE, functions=func_code_list,
                                                 test_class_name=test_class_name,
                                                 module_name=module)
            test_file_name = to_test_file_name(module)
            with open(test_file_name, 'w', encoding='utf8') as f:
                f.write(result)
            print(result)


def test():
    test_data = {
        "sheet1": {
            "模块1": [
                {
                    "testcase_name": "用例名称",
                    "dependency": "前置条件",
                    "ops": [
                        {
                            "idx": 1,
                            "op_type": "点击",  # 操作类型
                            "target": "用户名输入框",  # 对象
                            "value": "",  # 数值
                            "xpath": "/input",  #
                            "expect_type": "存在",  # 预期结果_判断类型
                            "expect_target": "输出框",  # 预期结果_对象
                            "expect_value": "value1, value2",  # 预期结果_数值
                            "expect_xpath": "",  # 预期结果_xpath
                            "desc": "",  # 描述
                        },
                        {
                            "idx": 2,
                            "op_type": "输入",  # 操作类型
                            "target": "用户名输入框",  # 对象
                            "value": "value1, value2",  # 数值
                            "xpath": "/input",  #
                            "expect_type": "存在",  # 预期结果_判断类型
                            "expect_target": "输出框",  # 预期结果_对象
                            "expect_value": "value1, value2",  # 预期结果_数值
                            "expect_xpath": "",  # 预期结果_xpath
                            "desc": "",  # 描述
                        },
                    ]
                },
                {
                    "testcase_name": "用例名称2",
                    "dependency": "前置条件2",
                    "ops": [
                        {
                            "idx": 1,
                            "op_type": "点击",  # 操作类型
                            "target": "用户名输入框",  # 对象
                            "value": "",  # 数值
                            "xpath": "/input",  #
                            "expect_type": "存在",  # 预期结果_判断类型
                            "expect_target": "输出框",  # 预期结果_对象
                            "expect_value": "value1, value2",  # 预期结果_数值
                            "expect_xpath": "",  # 预期结果_xpath
                            "desc": "",  # 描述
                        },
                        {
                            "idx": 2,
                            "op_type": "输入",  # 操作类型
                            "target": "用户名输入框",  # 对象
                            "value": "value1, value2",  # 数值
                            "xpath": "/input",  #
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
    }
    json_2_testcase(test_data)
    # variables_dict = {}
    # # template = Template(open("F:/github/webauto/po/templates/test_function.templ", encoding='utf-8').read())
    # template = Environment(loader=FileSystemLoader("F:/github/webauto/po/templates/")).from_string(
    #     open("F:/github/webauto/po/templates/test_function.templ", encoding='utf-8').read())
    # result = template.render(test_data, variables_dict=variables_dict)
    # print(result)


if __name__ == '__main__':
    test()
