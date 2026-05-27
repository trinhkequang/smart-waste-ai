from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data=r"C:\Users\trinh\Downloads\waste-detection.v1i.yolov8\data.yaml",
    epochs=5,
    imgsz=320
)