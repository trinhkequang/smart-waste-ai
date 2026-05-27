from ultralytics import YOLO
import cv2

# Load model
model = YOLO("runs/detect/train5/weights/best.pt")

# Mở camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Nhận diện
    results = model(frame)

    # Vẽ kết quả
    frame = results[0].plot()

    cv2.imshow("Waste Detection", frame)

    # ESC để thoát
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
results = model(frame, conf=0.01)
print(results)
print(results[0].boxes)