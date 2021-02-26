"""TCG.
自动化测试
Usage:
  cmdline.py <path> [-o FILE]
  cmdline.py (-h | --help)
  cmdline.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  -o DIR --output DIR 输出路径.
"""
import os
from docopt import docopt
from tcg.TestCaseGenerator import generate_code_from_excel

if __name__ == '__main__':

    arguments = docopt(__doc__, version='自动化测试 1.0')
    file_in = arguments.get('<path>')
    output = arguments.get('--output')
    if not output:
        output = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testcase', 'tmp')
    if not os.path.exists(file_in):
        print(f'找不到路径: {file_in}')
    else:
        generate_code_from_excel(file_in, output)
