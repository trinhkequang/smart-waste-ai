from ultralytics import YOLO

model = YOLO("runs/detect/train5/weights/best.pt")

results = model("dataset/train/images/istockphoto-927987734-612x612_jpg.rf.xmGLLWwHp1JlMP57GQCD.jpg", conf=0.1)

results[0].show()