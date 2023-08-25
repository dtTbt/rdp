import requests
from main import read_config_file
import base64
import os
import file_operations

folder = "post_img"  # 保存图片的文件夹

if not os.path.exists(folder):
    os.makedirs(folder)
else:
    file_operations.delete_all_files(folder)

config = read_config_file("config.yaml")
api_ip , api_port = config['api_ip'], config['api_port']
# 定义要发送的JSON数据
data_to_send = {
    "start_datetime": "2023-08-21 22:09:09",
    "limit": 3  # 在这里设置您想要的查询限制
}
#url = "http://{}:{}/delete/by-datetime".format(api_ip, api_port)
url = "http://{}:{}/query/recent-messages".format(api_ip, api_port)
#headers = {'Content-Type': 'application/json'}
response = requests.post(url, json=data_to_send)
if response.status_code == 200:
    data = response.json()
    # 解码Base64编码的LONGBLOB字段
    for row in data['data']:
        row['image_data'] = base64.b64decode(row['image_data'])
    # 对每一条数据进行处理
    for row in data['data']:
        ID = row['id']
        camera = row['camera']
        type = row['type']
        date_time = row['date_time']
        image_data = row['image_data']
        # 打印数据
        print(f"ID: {ID}")
        print(f"Camera: {camera}")
        print(f"Type: {type}")
        print(f"Date Time: {date_time}")
        print("------------------------")
        # 保存图片
        data_time_str = str(date_time)
        formatted_date_time = data_time_str.replace(":", "_")
        image_filename = os.path.join(folder, f"camera{camera}_{formatted_date_time}_{type}.jpg")
        with open(image_filename, "wb") as img_file:
            img_file.write(image_data)
else:
    print("Error:", response.json())
