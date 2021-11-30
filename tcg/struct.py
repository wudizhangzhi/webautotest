"""
1.储存参数，测试用例，操作
2.转化为json
3.数值判断
4.生成代码参数名、类名的interface
"""


class Field(dict):
    """字段"""


class BaseStruct(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)
    #
    # def __setattr__(self, key, value):
    #     print(f'__setattr__ {key} {value}')
    #     return super(BaseStruct, self).__setattr__(key, value)
    #
    # def __setitem__(self, key, value):
    #     print(f'__setitem__ {key} {value}')
    #     return super(BaseStruct, self).__setitem__(key, value)


class Variable(BaseStruct):
    """参数"""
    pass


class AllData(BaseStruct):
    """所有数据"""
    Sheets = []
    Variables = Variable()


class Sheet(BaseStruct):
    """表格"""
    TestCases = []


class TestCase(BaseStruct):
    """测试用例"""
    Ops = []


OpTypeEnums = (
    ()
)


class Op(BaseStruct):
    """操作
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
    """

    @property.setter
    def op_type(self, t):
        pass


class ApiOp(Op):
    """接口的操作"""
    pass
