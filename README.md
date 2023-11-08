# tqsdk_data_record

使用天勤量化tqsdk的tick、bar行情存储

## 数据库

使用TDengine时序数据库进行存储，建议使用docker安装，详见TDengine的官方文档。

## tqsdk

使用tqsdk订阅持仓量＞50000的合约，并存储tick和1min bar行情。

## 使用

trader文件setting.py中配置database.user和password，同时填写天勤账号和密码。

## 运行

执行 python server.py
使用 apscheduler 库进行任务调度。
