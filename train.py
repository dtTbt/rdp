from ultralytics import YOLO
from dbg import *

# Load a model
model = YOLO('pt/yolov8x.pt')  # load a pretrained model (recommended for training)

# Train the model
pth=r"./datasets/data.yaml"
model.train(data=pth, epochs=60, imgsz=640,batch=14)
shutdown_if_linux_not_windows(60)