import mysql.connector
import os
import file_operations

if not os.path.exists("result_img"):
    os.makedirs("result_img")
else:
    file_operations.delete_all_files("result_img")

# 数据库连接参数
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '11111111',
    'database': 'test_rdp'
}

# 连接到数据库
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# 查询数据
query = "SELECT camera, type, date_time, image_data FROM rdp_result"
cursor.execute(query)


for (camera, type, date_time, image_data) in cursor:
    # 打印数据
    print(f"Camera: {camera}")
    print(f"Type: {type}")
    print(f"Date Time: {date_time}")
    print("------------------------")
    # 保存图片
    data_time_str = str(date_time)
    formatted_date_time = data_time_str.replace(":", "_")
    image_filename = os.path.join("result_img", f"camera{camera}_{formatted_date_time}_{type}.jpg")
    with open(image_filename, "wb") as img_file:
        img_file.write(image_data)

# 关闭游标和数据库连接
cursor.close()
conn.close()
