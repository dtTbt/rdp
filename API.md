**基本信息**

- **Base URL：** `http://[ip]:[port]`

---

**查询最近N条记录**

- **URL：** `/query/recent-messages`
- **HTTP方法：** POST

**请求体参数：**

| 参数      | 类型   | 描述                                       |
| --------- | ------ | ------------------------------------------ |
| limit     | int    | 返回图片消息的数量，默认为5                |

**成功响应：**

- **状态码：** 200
- **响应体：**

```json
{
    "data": [
        {
            "id": 1,
            "camera": "1",
            "type": "person without helmet",
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
            "type": "person without helmet",
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

---

**错误响应：**

- **状态码：** 500
- **响应体：**

```json
{
    "api_error": "Error message"
}
```

---

**注意事项：**

- 图片数据以Base64编码的字符串形式返回。