from flask import Flask, render_template, Response, jsonify, send_from_directory
import cv2
from ultralytics import YOLO
import time
import requests
import json
import os
from collections import deque, Counter
from blockchain import Blockchain

app = Flask(__name__)

# ================= PATH =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BLOCKCHAIN_FILE = os.path.join(BASE_DIR, "blockchain_web_data.json")
BLOCK_IMAGE_FILE = os.path.join(BASE_DIR, "block_images.json")
CAPTURE_DIR = os.path.join(BASE_DIR, "static", "captures")

os.makedirs(CAPTURE_DIR, exist_ok=True)

# ================= TELEGRAM =================
BOT_TOKEN = "8394675541:AAEFioTztoQuM7wBoWfQSmA1unXJqBRj7TI"
CHAT_ID = "5253139760"


def send_telegram(text):
    if BOT_TOKEN == "YOUR_BOT_TOKEN":
        return False

    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        r = requests.post(
            url,
            data={"chat_id": CHAT_ID, "text": text},
            timeout=5
        )
        return r.ok
    except Exception as e:
        print("Telegram Error:", e)
        return False


def send_photo(path):
    if BOT_TOKEN == "YOUR_BOT_TOKEN":
        return False

    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

        with open(path, "rb") as f:
            r = requests.post(
                url,
                data={"chat_id": CHAT_ID},
                files={"photo": f},
                timeout=5
            )

        return r.ok
    except Exception as e:
        print("Photo Error:", e)
        return False


# ================= BLOCKCHAIN =================
blockchain = Blockchain(filename=BLOCKCHAIN_FILE)
blockchain.difficulty = 3

# ================= MODEL =================
model = YOLO(
    r"C:\Users\trinh\Downloads\waste_project\runs\detect\train8\weights\best.pt"
)

# ================= CAMERA =================
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# ================= FACE DETECTION =================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ================= STATE =================
history_vote = deque(maxlen=10)

locked_status = "WAITING"
locked_label = "None"
locked_confidence = 0
locked_until = 0

last_saved_time = 0

latest_info = {
    "status": "WAITING",
    "label": "None",
    "confidence": 0,
    "message": "Đưa rác vào vùng nhận diện",
    "action": "Đang chờ phân loại",
    "recycle_count": 0,
    "non_recycle_count": 0,
    "blockchain_status": "WAITING",
    "latest_block": "None",
    "latest_hash": "None",
    "telegram_status": "WAITING",
    "history": []
}

# ================= CLASS MAP =================
RECYCLE = [
    "can",
    "cardboard_bowl",
    "cardboard_box",
    "plastic_bag",
    "plastic_bottle",
    "plastic_bottle_cap",
    "plastic_box",
    "plastic_cultery",
    "plastic_cup",
    "plastic_cup_lid",
    "reuseable_paper",
    "scrap_paper",
    "scrap_plastic",
    "snack_bag"
]

NON_RECYCLE = [
    "battery",
    "chemical_plastic_bottle",
    "chemical_plastic_gallon",
    "chemical_spray_can",
    "light_bulb",
    "paint_bucket",
    "stick",
    "straw"
]


def map_waste(label):
    label = label.lower()

    if label in RECYCLE:
        return "Recyclable"

    if label in NON_RECYCLE:
        return "Non-Recyclable"

    return "Unknown"


def get_message(status):
    if status == "Recyclable":
        return "Rác có thể tái chế"

    if status == "Non-Recyclable":
        return "Rác không thể tái chế"

    return "Đưa rác vào vùng nhận diện"


def get_action(status):
    if status == "Recyclable":
        return "Đưa sang ngăn tái chế"

    if status == "Non-Recyclable":
        return "Đưa sang ngăn không tái chế"

    return "Đang chờ phân loại"


def is_box_on_face(box, faces, rx1, ry1):
    x1, y1, x2, y2 = box

    x1 += rx1
    x2 += rx1
    y1 += ry1
    y2 += ry1

    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2

    for (fx, fy, fw, fh) in faces:
        if fx < cx < fx + fw and fy < cy < fy + fh:
            return True

    return False


def stable_result(new_result, label, confidence):
    global locked_status
    global locked_label
    global locked_confidence
    global locked_until
    global history_vote

    now = time.time()

    if now < locked_until:
        return locked_status, locked_label, locked_confidence

    if new_result in ["Recyclable", "Non-Recyclable"]:
        history_vote.append({
            "result": new_result,
            "label": label,
            "confidence": confidence
        })

    if len(history_vote) < 5:
        return "WAITING", "None", 0

    results_only = [item["result"] for item in history_vote]
    count = Counter(results_only)

    result, times = count.most_common(1)[0]

    if times >= 4:
        same_items = [
            item for item in history_vote
            if item["result"] == result
        ]

        best_item = max(
            same_items,
            key=lambda x: x["confidence"]
        )

        locked_status = result
        locked_label = best_item["label"]
        locked_confidence = best_item["confidence"]
        locked_until = now + 4

        history_vote.clear()

        return locked_status, locked_label, locked_confidence

    return "WAITING", "None", 0


def save_block_image(block_index, image_filename):
    try:
        if os.path.exists(BLOCK_IMAGE_FILE):
            with open(BLOCK_IMAGE_FILE, "r", encoding="utf-8") as f:
                image_map = json.load(f)
        else:
            image_map = {}

        image_map[str(block_index)] = image_filename

        with open(BLOCK_IMAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(image_map, f, indent=4, ensure_ascii=False)

    except Exception as e:
        print("Save block image error:", e)


def save_result(frame, status, label, confidence):
    global latest_info
    global last_saved_time

    now = time.time()

    if status not in ["Recyclable", "Non-Recyclable"]:
        return

    # tránh ghi quá nhiều block liên tục
    if now - last_saved_time < 8:
        return

    last_saved_time = now

    current_time = time.strftime("%H:%M:%S")
    date_time = time.strftime("%Y-%m-%d %H:%M:%S")

    image_filename = f"capture_{int(time.time())}.jpg"
    image_path = os.path.join(CAPTURE_DIR, image_filename)

    cv2.imwrite(image_path, frame)

    try:
        blockchain.add_block(
            status,
            round(confidence, 2),
            "Camera 1"
        )

        valid = blockchain.is_chain_valid()
        latest_block = blockchain.get_latest_block()

        save_block_image(latest_block.index, image_filename)

        latest_info["blockchain_status"] = "VERIFIED" if valid else "TAMPERED"
        latest_info["latest_block"] = latest_block.index
        latest_info["latest_hash"] = latest_block.hash[:18] + "..."

        print("✅ Saved block:", latest_block.index)
        print("📁 Blockchain file:", BLOCKCHAIN_FILE)

    except Exception as e:
        print("Blockchain Error:", e)
        latest_info["blockchain_status"] = "ERROR"

    if status == "Recyclable":
        latest_info["recycle_count"] += 1
    else:
        latest_info["non_recycle_count"] += 1

    log_item = {
        "time": current_time,
        "datetime": date_time,
        "label": label,
        "status": status,
        "confidence": round(confidence, 2),
        "image": image_filename
    }

    latest_info["history"].insert(0, log_item)
    latest_info["history"] = latest_info["history"][:10]

    telegram_ok = send_telegram(
        f"♻️ SMART WASTE DETECTED\n"
        f"Object: {label}\n"
        f"Type: {status}\n"
        f"Confidence: {confidence:.2f}\n"
        f"Time: {date_time}\n"
        f"Blockchain: {latest_info['blockchain_status']}\n"
        f"Latest Block: {latest_info['latest_block']}"
    )

    photo_ok = send_photo(image_path)

    if telegram_ok or photo_ok:
        latest_info["telegram_status"] = "SENT"
    else:
        latest_info["telegram_status"] = "OFF"


def generate():
    global latest_info

    while True:
        success, frame = cap.read()

        if not success:
            break

        frame = cv2.resize(frame, (640, 480))

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(80, 80)
        )

        rx1, ry1 = 170, 145
        rx2, ry2 = 500, 430

        cv2.rectangle(
            frame,
            (rx1, ry1),
            (rx2, ry2),
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "PUT WASTE HERE",
            (205, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        roi = frame[ry1:ry2, rx1:rx2]

        detected_now = "Unknown"
        best_box = None
        best_conf = 0
        best_label = "None"

        results = model(
            roi,
            conf=0.35,
            imgsz=640,
            verbose=False,
            iou=0.45,
            max_det=3
        )

        for box in results[0].boxes:
            conf = float(box.conf[0])

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            area = (x2 - x1) * (y2 - y1)

            if area < 3000:
                continue

            if is_box_on_face((x1, y1, x2, y2), faces, rx1, ry1):
                continue

            if conf > best_conf:
                best_conf = conf
                best_box = box

        if best_box is not None:
            cls = int(best_box.cls[0])
            best_label = model.names[cls]
            detected_now = map_waste(best_label)

        status, show_label, show_conf = stable_result(
            detected_now,
            best_label,
            best_conf
        )

        if status == "Recyclable":
            status_color = (0, 255, 0)
        elif status == "Non-Recyclable":
            status_color = (0, 0, 255)
        else:
            status_color = (0, 255, 255)

        if best_box is not None and status != "WAITING":
            x1, y1, x2, y2 = map(int, best_box.xyxy[0])

            x1 += rx1
            x2 += rx1
            y1 += ry1
            y2 += ry1

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                status_color,
                3
            )

            cv2.putText(
                frame,
                status,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                status_color,
                3
            )

        cv2.putText(
            frame,
            status,
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            status_color,
            3
        )

        latest_info["status"] = status
        latest_info["label"] = show_label
        latest_info["confidence"] = round(show_conf, 2)
        latest_info["message"] = get_message(status)
        latest_info["action"] = get_action(status)

        if status in ["Recyclable", "Non-Recyclable"]:
            save_result(
                frame,
                status,
                show_label,
                show_conf
            )

        ret, buffer = cv2.imencode(".jpg", frame)

        if not ret:
            continue

        frame = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type:image/jpeg\r\n\r\n"
            + frame
            + b"\r\n"
        )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/video")
def video():
    return Response(
        generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/status")
def status():
    return jsonify(latest_info)


@app.route("/blockchain")
def blockchain_page():
    return render_template("blockchain.html")


@app.route("/api/blockchain")
def api_blockchain():
    if not os.path.exists(BLOCKCHAIN_FILE):
        return jsonify([])

    try:
        with open(BLOCKCHAIN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        image_map = {}

        if os.path.exists(BLOCK_IMAGE_FILE):
            with open(BLOCK_IMAGE_FILE, "r", encoding="utf-8") as f:
                image_map = json.load(f)

        for block in data:
            img = image_map.get(str(block.get("index")))

            if img:
                block["image_url"] = f"/captures/{img}"
            else:
                block["image_url"] = ""

        return jsonify(data[::-1])

    except Exception as e:
        print("Read blockchain error:", e)
        return jsonify([])


@app.route("/captures/<filename>")
def captures(filename):
    return send_from_directory(CAPTURE_DIR, filename)


if __name__ == "__main__":
    print("📁 BASE_DIR:", BASE_DIR)
    print("📁 BLOCKCHAIN_FILE:", BLOCKCHAIN_FILE)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        threaded=True
    )