## RDP 项目简介

RDP是一个基于YOLOv8的，用于按一定频率检测所有摄像头画面（最多支持4个摄像头），检测目标为人，老鼠，火焰或者烟雾的项目。检测结果保存于MySQL数据库中。并提供一个API接口服务，支持调取和删除MySQL内数据。

### 一、环境配置

通过以下命令安装依赖包：

```bash
pip install -r requirements.txt
```

### 二、权重下载

在此下载权重：[百度网盘](https://pan.baidu.com/s/1EW2cfUOwv1JqGNpa-meyyg?pwd=jntm)

然后将其解压在项目目录下即可。

### 三、MySQL数据库表格式

```bash
CREATE TABLE rdp_result (
    id INT AUTO_INCREMENT PRIMARY KEY,
    camera INT,
    type VARCHAR(255),
    date_time TIMESTAMP(3),
    image_data LONGBLOB
);
```

### 四、配置文件

请自行配置参数文件：[`config.yaml`](./config.yaml)

### 五、MySQL详细配置说明与项目服务开机自启动

见[`other.md`](./other.md)

### 六.API接口文档

见[`API.md`](./API.md)

### 七.日志记录说明文档

见[`log.md`](./log.md)

### 八、（可选）手动运行

#### 1.使用以下命令来运行检测主程序：

```bash
python main.py
```

#### 2.使用以下命令在本机运行API接口：

```bash
python api.py
```

#### 3.使用以下命令以删除MySQL中已存在的所有记录：

```bash
python mysql_delete.py
```

#### 4.使用以下命令向接口发送POST请求（示例，或用于调试）：

```bash
python post.py
```

#### 5.使用以下命令进行模型测试：

```bash
python test.py  --path ./test_img
```
其中`--path`参数指出测试图片所在文件夹的路径。输出结果保存在`./test_img_predict`文件夹中。

### 九、（可选）其他

#### 1.数据集下载（YOLOv8格式）

[百度网盘](https://pan.baidu.com/s/1Buv2slwkvScuBe4nz7mCUA?pwd=jntm)
