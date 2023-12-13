# 日志记录说明文档

## 日志记录

本API使用Python的logging模块进行日志记录,将日志写入到指定的日志文件中。

### 日志格式

每条日志按照以下格式记录:

```
时间 - 日志级别 - 日志内容
```

例如:

```
2023-02-28 15:32:11.123 - INFO - Received POST request to /query/recent-messages
```

### 日志级别

使用以下日志级别:

- INFO:记录正常的事件,如接收到请求、返回响应等
- ERROR:记录错误事件

### 日志内容

记录以下内容:

- 接收到请求时,记录请求方法和路径
- 返回响应时,记录响应内容(不包括图片二进制数据)  
- 发生错误时,记录错误详情
- 重要操作时,记录操作详情,如删除记录等

### 日志位置

检测主程序与API接口程序分别记录日志于两个文件:
- 检测主程序日志文件保存路径由`config.yaml` 中的 `log_path_main`参数指定。（此日志文件仅用于开发调试）
- API日志文件保存路径由`config.yaml` 中的 `log_path`参数指定。

### 示例

正常查询请求记录:

```
2023-02-28 15:32:11.123 - INFO - Received POST request to /query/recent-messages
2023-02-28 15:32:11.456 - INFO - Response sent: 
[
{
    "id": 1, 
    "camera": "1",
    ...
},
{
    "id": 2,
    "camera": "2",
    ...
},
...
]
```

删除记录请求记录:

``` 
2023-02-28 15:35:22.123 - INFO - Received POST request to /delete/by-datetime
2023-02-28 15:35:22.456 - INFO - Records deleted successfully
```

发生错误记录:

```
2023-02-28 15:40:11.123 - ERROR - Error: pymysql.err.OperationalError: (2003, "Can't connect to MySQL server on '192.168.0.1' ([Errno 111] Connection refused)")
```
