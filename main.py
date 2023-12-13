import argparse
import datetime
import os
import queue
import threading
import time
import mysql.connector
import cv2
import yaml
import file_operations
from ultralytics import YOLO
from file_operations import clear_large_file, get_folder_size_mb, get_disk_space
import logging


class VideoCapture:
    def __init__(self, url):
        self.cap = cv2.VideoCapture(url)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()


def read_config_file(config_file_path):
    with open(config_file_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def set_str(strs, index, strt):
    restr = strs[:index] + strt + strs[index+1:]
    return restr


def get_mysql_config(pth):
    config = read_config_file(pth)
    mysql_ip = config['mysql_ip']
    mysql_username = config['mysql_username']
    mysql_password = str(config['mysql_password'])
    mysql_database = config['mysql_database']
    mysql_table = config['mysql_table']
    return mysql_ip, mysql_username, mysql_password, mysql_database, mysql_table


if __name__ == '__main__':
    config = read_config_file("config.yaml")
    clear_large_file(config['log_path_main'], config['log_main_threshold'])
    logging.basicConfig(filename=config['log_path_main'], level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("================== new start ==================")

    save_pth_0 = "runs/detect"
    file_operations.delete_all_files(save_pth_0)

    camera_num = config['camera_num']
    camera_port = config['camera_port']
    cap = []
    for i in range(camera_num):
        index = i + 1
        camera_username = config[f'camera_username_{index}']
        camera_password = config[f'camera_password_{index}']
        camera_ip = config[f'camera_ip_{index}']
        camera_stream = config[f'camera_stream_{index}']
        rtsp_url = f"rtsp://{camera_username}:{camera_password}@{camera_ip}:{camera_port}{camera_stream}"
        cap.append(VideoCapture(rtsp_url))

    sleep_time = config['sleep_time']
    pth_pt = config["pth_pt"]

    mysql_ip , mysql_username, mysql_password, mysql_database, mysql_table = get_mysql_config("config.yaml")
    db_config = {
        'user': mysql_username,
        'password': mysql_password,
        'host': mysql_ip,
        'database': mysql_database,
    }
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    save_all = config['save_all']
    threshold_size_mb = config['delete_threshold']
    conf_threshold = config['conf_threshold']
    all_detect_info = True if config['all_detect_info'] == "True" else False
    mysql_data_path = os.path.join(config['mysql_path'], 'data', mysql_database)

    folder = None
    save_pth = os.path.join(save_pth_0, "predict")
    new_predict_folder_flg = 0

    model = None
    if config["pt_kd"] == "pt":
        model = YOLO(config["pth_pt"])
    else:
        model = YOLO(config["pth_onnx"])

    detect_success_num = 0
    detect_success_num_max = 2

    detect_smoke = False if config["ban_smoke"] == "True" else True
    logging.info(f"Ban save: {config['ban_save']}")
    logging.info(f"Save all: {save_all}")
    logging.info(f"Detect smoke: {detect_smoke}")

    disk_space_mb = get_disk_space()
    logging.info(f"Database threshold: {threshold_size_mb} MB")
    logging.info(f"Disk space now: {disk_space_mb} MB")
    if threshold_size_mb + 50 > disk_space_mb:
        logging.error(f"Insufficient Disk Space: The sum of database upper limit space and safety redundancy (50 MB) "
                      f"exceeds the remaining disk space. Please modify the 'delete_threshold' parameter "
                      f"in the configuration file or clean up disk space!")
        logging.info("RDP exit.")
        exit(1)

    print("Ready.")

    logging.info("Start detecting...")

    while True:
        time.sleep(sleep_time)
        clear_large_file(config['log_path_main'], config['log_main_threshold'])
        camera_index = 0
        if detect_success_num <= detect_success_num_max:
            if detect_success_num < detect_success_num_max:
                logging.info(f"Detecting circle {detect_success_num}.")
            else:
                logging.info(f"Detecting circle {detect_success_num}. "
                             f"The detection runs normally. There will be no more logs for detecting circle.")
            detect_success_num += 1
        for camera in cap:
            camera_index += 1
            frame = camera.read()
            now = datetime.datetime.now()
            date_time = now.strftime("%Y.%m.%d-%H.%M.%S.%f")[:-3]
            img_name = f'{date_time}.jpg'
            results = model(frame, save=True, conf=conf_threshold)
            obj_np = results[0].boxes.cls.cpu().numpy()
            kd = "00000"
            for obj in obj_np:
                if obj == 0:  # helmet
                    kd = set_str(kd, 0, '1')
                    if all_detect_info:
                        logging.info(f"Detected helmet: camera{camera_index}")
                if obj == 1:  # person
                    kd = set_str(kd, 1, '1')
                    if all_detect_info:
                        logging.info(f"Detected person: camera{camera_index}")
                if obj == 2:  # rat
                    kd = set_str(kd, 2, '1')
                    if all_detect_info:
                        logging.info(f"Detected rat: camera{camera_index}")
                if obj == 3:  # fire
                    kd = set_str(kd, 3, '1')
                    if all_detect_info:
                        logging.info(f"Detected fire: camera{camera_index}")
                if obj == 4 and detect_smoke:
                    kd = set_str(kd, 4, '1')
                    if all_detect_info:
                        logging.info(f"Detected smoke: camera{camera_index}")
            if all_detect_info and kd == "00000":
                logging.info(f"No object detected: camera{camera_index}")
            save_img = os.path.join(save_pth, "image0.jpg")
            with open(save_img, "rb") as image_file:
                binary_image = image_file.read()
                if save_all == 'True' or kd != "00000":
                    # delete data from mysql to reduce table size
                    table_size_mb = file_operations.get_folder_size_mb(mysql_data_path)
                    logging.info(f"Database size: {table_size_mb} MB")
                    if table_size_mb > threshold_size_mb:
                        delete_query = f"TRUNCATE TABLE {mysql_table}"
                        cursor.execute(delete_query)
                        conn.commit()
                        print(f"Deleted data from {mysql_table} to reduce table size.")
                        logging.info(f"The size of {mysql_table} is {table_size_mb} MB, which is larger than "
                                     f"the threshold {threshold_size_mb} MB. Deleted data from {mysql_table} to reduce "
                                     f"table size.")

                    if not config['ban_save'] == "True":
                        # insert data to mysql
                        sql = f"INSERT INTO {mysql_table} (`camera`, `type`, `date_time`, `image_data`) VALUES (%s, %s, %s, %s)"
                        data_to_insert = (camera_index, kd, date_time, binary_image)
                        cursor.execute(sql, data_to_insert)
                        conn.commit()
                        print(f"Saved to mysql: camera{camera_index}, {kd}, {date_time}")
                        logging.info(f"Saved to mysql: camera{camera_index}, {kd}, {date_time}")
            os.remove(save_img)
