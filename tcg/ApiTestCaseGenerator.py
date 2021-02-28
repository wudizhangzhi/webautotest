import sys

sys.path.append("..")
import os
import json
import pandas as pd
from numpy import nan
from itertools import product
from collections import defaultdict
from jinja2 import Template, BaseLoader, Environment, FileSystemLoader

from tcg.GenerateVariableName import chinese2variable, to_test_func_name, to_test_class_name, to_test_file_name, \
    to_test_folder_name

TEMPLATE_FLODER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
TEMPLATE_TESTCASE = os.path.join(TEMPLATE_FLODER, 'testcase.templ')
TEMPLATE_FUNCATION = os.path.join(TEMPLATE_FLODER, 'test_function.templ')

# __all__ = ['generate_code_from_excel',]

def read_from_excel(path):
    """
    读取excel，转化为json
    :param path:
    :return:
        json格式

        {
            "sheet1":{
                "模块1": [
                    {
                        "testcase_name": "用例名称",
                        "dependency": "前置条件",
                        "module_name": "模块1",
                        "order": 1,
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
    result = defaultdict(dict)
    xls = pd.ExcelFile(path)
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(path, sheet_name=sheet_name, header=1)
        df = df.replace(nan, '', regex=True)
        shape = df.shape
        test_case_name = None
        test_module_name = None
        dependency = None
        ops = []
        last_idx = shape[0] - 1
        test_case_module_dict = {}
        order = 0
        for idx, row in df.iterrows():
            """
            如果test_case_name变化或者是最后一行
            最后一行： op需要append
            中间 _test_case_name != null 且 test_case_name 跟上次不一样时候, 需要整合模块数据,并清空ops, 然后append 当前行的op
            """
            row_dict = row.to_dict()
            _test_case_name = row_dict['Unnamed: 0']
            _test_module_name = row_dict['Unnamed: 1']
            _dependency = row_dict['Unnamed: 2']
            op = {
                "idx": row_dict['序号'],
                "op_type": row_dict['操作'],
                "target": row_dict['对象'],
                "value": row_dict['数值'],
                "xpath": row_dict['selector'],
                "expect_type": row_dict['判断'],
                "expect_target": row_dict['对象.1'],
                "expect_value": row_dict['数值.1'],
                "expect_xpath": row_dict['selector.1'],
                "desc": row_dict['描述'],
            }
            if idx != 0 and _test_case_name and _test_case_name != test_case_name or idx == last_idx:
                # 如果不是第一行,之前的数据保存入字典
                # 如果是最后一行，需要把当前op加入
                if idx == last_idx:
                    ops.append(op)
                test_case_module_dict[test_case_name] = test_module_name

                result[sheet_name][test_module_name].append({
                    "testcase_name": test_case_name,
                    "module_name": test_module_name,
                    "order": order,
                    "dependency": f"{to_test_file_name(test_case_module_dict[dependency])}::{to_test_class_name(test_case_module_dict[dependency])}::{to_test_func_name(dependency)}" if dependency else None,  # 依赖名称
                    "ops": ops
                })
                # 清空ops
                ops = []
                order += 1

            if _test_module_name:
                test_module_name = _test_module_name
                result[sheet_name][test_module_name] = []
            if _dependency:
                dependency = _dependency
            if _test_case_name:
                test_case_name = _test_case_name

            ops.append(op)

    return result