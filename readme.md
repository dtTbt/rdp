## 项目简介

本项目基于YOLOv8。用于每隔一定时间检测所有摄像头画面（最多支持4个摄像头），检测目标为老鼠，未带安全帽的人员，火焰或者烟雾。检测结果保存于mysql数据库中。并提供一个API接口服务，支持调取和删除mysql内数据。

### 环境配置

在运行本项目之前，请确保已经安装了`ultralytics`库，可通过以下命令进行安装：

```bash
pip install ultralytics
```

### mysql数据库表格式

```bash
CREATE TABLE rdp_result (
    id INT AUTO_INCREMENT PRIMARY KEY,
    camera INT,
    type VARCHAR(255),
    date_time TIMESTAMP(3),
    image_data LONGBLOB
);
```

### 运行

#### 1.使用以下命令来运行检测主程序：

```bash
python main.py
```

#### 2.使用以下命令在本机运行一个API接口：

```bash
python api.py
```

接口具体功能见 [`API.md`](./API.md)。

#### 3.使用以下命令以删除mysql中已存在的所有记录：

```bash
python mysql_delete.py
```

#### 3.使用以下命令向接口发送POST请求（用于调试）：

```bash
python post.py
```

### 配置参数文件

请自行配置参数文件`config.yaml`。