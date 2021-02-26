
# GET STARTED
- 安装java，并配置环境路径
- 下载allure, 并加入环境路径
- 安装python依赖包


# USAGE
在命令行中切换到testcase目录，执行pytest --alluredir=F:\github\webauto\allure_results --clean-alluredir -vv
查看报告，执行allure serve F:\github\webauto\allure_results
生成html报告，执行allure generate E:\my_allure_results -o F:\github\webauto\allure_html

# TODO 
[ ] 支持使用输入的参数当作结果判断，例如 assert element.text.strip() == input_param
[ ] 支持判断结果是空或者不是空, 支持判断结果长度
[ ] 操作支持下拉选择