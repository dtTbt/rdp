import argparse
import os
import cv2
import yaml
from ultralytics import YOLO


def read_config_file(config_file_path):
    with open(config_file_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, help='the folder path of test images')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    config = read_config_file("config.yaml")
    args = parse_args()

    model = None
    if config["pt_kd"] == "pt":
        model = YOLO(config["pth_pt"])
    else:
        model = YOLO(config["pth_onnx"])

    print("Ready.")

    save_pth_0 = "runs/detect"
    os.system("rm -rf {}".format(save_pth_0))
    img_path_tmp = os.path.join(save_pth_0, 'predict', "image0.jpg")

    assert args.path is not None, "The folder path of test images is not specified."
    assert os.path.exists(args.path), "The folder path of test images does not exist."
    test_folder_path = args.path
    save_folder_path = test_folder_path + "_predict"
    if os.path.exists(save_folder_path):
        os.system("rm -rf {}".format(save_folder_path))
    os.mkdir(save_folder_path)
    img_list = os.listdir(test_folder_path)
    for img_name in img_list:
        img_path = os.path.join(test_folder_path, img_name)
        img = cv2.imread(img_path)
        results = model(img, save=True, conf=0.5)
        save_name = os.path.join(save_folder_path, img_name)
        os.system("mv {} {}".format(img_path_tmp, save_name))