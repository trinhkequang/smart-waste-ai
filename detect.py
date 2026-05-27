import cv2
import numpy as np
from tensorflow.keras.models import load_model

model = load_model("model.h5")

labels = ["organic", "paper", "plastic"]

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    img = cv2.resize(frame, (224,224))
    img = np.expand_dims(img, axis=0) / 255.0

    pred = model.predict(img)
    label = labels[np.argmax(pred)]

    cv2.putText(frame, label, (50,50),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0,255,0), 2)

    cv2.imshow("Waste Detection", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()