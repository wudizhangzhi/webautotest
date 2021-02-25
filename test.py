from tcg import generate_code_from_excel

if __name__ == '__main__':
    import os

    file_in = os.path.join(os.path.dirname(os.path.abspath(__file__)), '测试.xlsx')
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testcase', 'tmp')
    generate_code_from_excel(file_in, out)
