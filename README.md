### 概要信息
本接口自动化框架通过读取excel文件中维护的接口case，来调用接口，并通过接口返回的数据生成测试报告

### 需要安装的python扩展包
* requests  --用于请求接口
* jinja2    --渲染测试报告
* xlrd      --读取excel

### 文件和目录说明
![文件目录](https://github.com/yinzhixin/InterfaceAutomation/blob/master/images/dir.png)
* images和static目录：静态资源目录-包括测试报告中用到的js、css、image
* template：测试报告模板
* testreport：测试报告目录
* runcase.py：主程序文件
* util.py：工具类文件
* testcase.xlsx：测试用例文件

### 说明
* 直接运行runcase.py文件即可开始接口测试
* testcase.xlsx测试用例文件必须按照样例格式维护，post参数必须为json格式
* 测试报告中结果列表的表头数据在报告中目前是硬编码的，在template模板中可修改

### 图例如下
* 测试用例
![测试用例](https://github.com/yinzhixin/InterfaceAutomation/blob/master/images/case.png)
* 测试报告
![测试报告](https://github.com/yinzhixin/InterfaceAutomation/blob/master/images/report.png)
