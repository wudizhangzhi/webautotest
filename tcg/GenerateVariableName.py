from pypinyin import pinyin, lazy_pinyin, Style


def chinese2variable(chi, first_upper=False):
    "中文->拼音->下划线或者驼峰"
    pinyin_list = lazy_pinyin(chi)
    if first_upper:
        return ''.join(map(lambda x: x.capitalize(), pinyin_list))
    else:
        return '_'.join(pinyin_list)


def to_test_func_name(s):
    return f"test_{chinese2variable(s)}"


def to_test_class_name(s):
    return f"Test{chinese2variable(s, first_upper=True)}"


def to_test_file_name(s):
    return f"test_{chinese2variable(s)}.py"


def to_test_folder_name(s):
    # return to_test_func_name(s)
    return s
