
# GET STARTED
- 安装java，并配置环境路径
- 下载allure, 并加入环境路径
- 安装python和依赖包


# USAGE
在命令行中切换到webautotest目录，执行
```shell
pytest --alluredir=.\allure_results --clean-alluredir -v
```
查看报告，执行
```shell
allure serve .\allure_results
```
生成html报告，执行
```shell
allure generate .\allure_results -o .\allure_html
```

# TODO
- [ ] 支持使用输入的参数当作结果判断，例如 assert element.text.strip() == input_param
- [ ] 支持判断结果是空或者不是空, 支持判断结果长度
- [x] ~~操作支持下拉选择(自定义前端框架的dropdown menu, 没有使用\<select\>)~~, 改用css-selector
- [ ] 执行顺序的优化
- [ ] 增加接口的自动化测试
