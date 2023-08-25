## 项目简介

本项目用于每隔一定时间检测摄像头画面，若画面变化超过一定阈值，则进行目标检测。如果检测到有老鼠或未带安全帽的人员，将会发送POST请求到指定URL，并保存检测后的图片。未检测到目标的图片将不予保存。

### 环境配置

在运行本项目之前，请确保已经安装了`ultralytics`库，可通过以下命令进行安装：

```bash
pip install ultralytics
```

### 运行

使用以下命令来运行本项目：

```bash
python detect.py --cfg config.yaml
```

### 配置参数文件

请自行配置参数文件`config.yaml`，该文件将包含摄像头监测的相关设置和阈值，以及YOLO使用的权重路径等。

### 数据保存

所有检测后的图片将保存在`runs/detect`的最新文件夹下，文件名包含检测信息与日期时间。

### POST请求

若检测到老鼠，将会发送`{"type": "rat", "image": img_name}`。

若检测到未带安全帽的人员，将会发送`{"type": "person without helmet", "image": img_name}`。

若同时存在，将会发送`{"type": "person without helmet and rat", "image": img_name}`。

其中`img_name`为保存图片的文件名。