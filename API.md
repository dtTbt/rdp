**基本信息**

- **Base URL：** `http://[api_ip]:[api_port]`

**约定**

- 图像类型（即`type`字段）是一个长度为5的字符串，由字符"0"或"1"组成，字符下标分别记为0,1,2,3,4。下标0处的字符代表是否检测到"佩戴头盔的人"，其中"0"代表未检测到，"1"代表检测到。下标1~4的字符分别代表"未戴头盔的人"，"老鼠"，"火焰"，"烟雾"。

- 图片数据（即`image_data`字段）为Base64编码的字符串。

**使用示例**

- 见[`post.py`](./post.py)

---

**查询最近N条记录**

- **URL：** `/query/recent-messages`
- **HTTP方法：** POST

**请求体参数：**

| 参数      | 类型   | 描述                   |
| --------- | ------ |----------------------|
| limit     | int    | 返回图片消息的数量，不指定则返回最近5条 |

**成功响应：**

- **状态码：** 200
- **响应体：**

```json
{
    "data": [
        {
            "id": 1,
            "camera": "1",
            "type": "01000",
            "date_time": "2023-08-20 15:30:45.123",
            "image_data": "base64_encoded_image_data"
        },
        ...
    ]
}
```

---

**查询指定日期时间之后所有记录**

- **URL：** `/query/by-datetime`
- **HTTP方法：** POST

**请求体参数：**

| 参数             | 类型   | 描述                                          |
| ---------------- | ------ | --------------------------------------------- |
| start_datetime   | string | 查询起始日期时间，格式为'YYYY-MM-DD HH:MM:SS' |

**成功响应：**

- **状态码：** 200
- **响应体：**

```json
{
    "data": [
        {
            "id": 1,
            "camera": "2",
            "type": "00101",
            "date_time": "2023-08-20 15:30:45.123",
            "image_data": "base64_encoded_image_data"
        },
        ...
    ]
}
```

---

**删除指定日期时间之前所有记录**

- **URL：** `/delete/by-datetime`
- **HTTP方法：** POST

**请求体参数：**

| 参数             | 类型   | 描述                                          |
| ---------------- | ------ | --------------------------------------------- |
| start_datetime   | string | 删除起始日期时间，格式为'YYYY-MM-DD HH:MM:SS' |

**成功响应：**

- **状态码：** 200
- **响应体：**

```json
{
    "message": "Records deleted successfully"
}
```

**注意**

- 使用`DELETE FROM`删除，不会重置自增ID。

---

**删除所有记录**

- **URL：** `/delete/all`
- **HTTP方法：** POST

**成功响应：**

- **状态码：** 200
- **响应体：**

```json
{
    "message": "All records deleted successfully"
}
```

**注意**

- 使用`TRUNCATE TABLE`删除，将重置自增ID，且不可回滚。

---

**错误响应：**

- **状态码：** 500
- **响应体：**

```json
{
    "api_error": "Error message"
}
```
