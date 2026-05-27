from ultralytics import YOLO

model = YOLO(
    r"C:\Users\trinh\Downloads\waste_project\runs\detect\train7\weights\best.pt"
)

model.train(
    data=r"C:\Users\trinh\Downloads\waste-detection.v1i.yolov8\data.yaml",

    epochs=15,

    imgsz=320,

    batch=2,

    device="cpu"
)