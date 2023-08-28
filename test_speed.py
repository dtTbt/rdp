import argparse
import datetime
import os
import queue
import threading
import time
import cv2
import yaml
from ultralytics import YOLO


def read_config_file(config_file_path):
    with open(config_file_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


if __name__ == '__main__':
    config = read_config_file("config.yaml")
    onnx_path = config["pth_pt"]
    model = YOLO(onnx_path)
    files_list = os.listdir("test_img")
    for file in files_list:
        file_path = os.path.join("test_img", file)
        model(file_path, save=True)