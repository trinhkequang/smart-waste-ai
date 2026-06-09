import cv2
import numpy as np
import os
from ultralytics import YOLO
import time
import requests
from blockchain import Blockchain

# =========================================
# TELEGRAM
# =========================================
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")


def send_telegram(text):

    # Nếu chưa nhập token thì bỏ qua
    if not BOT_TOKEN or not CHAT_ID:
        return

    try:

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": text
            },
            timeout=5
        )

    except Exception as e:

        print("Telegram Error:", e)


def send_photo(path):

    # Nếu chưa nhập token thì bỏ qua
    if not BOT_TOKEN or not CHAT_ID:
        return

    try:

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

        with open(path, "rb") as f:

            files = {"photo": f}

            requests.post(
                url,
                data={"chat_id": CHAT_ID},
                files=files,
                timeout=5
            )

    except Exception as e:

        print("Photo Error:", e)


# =========================================
# BLOCKCHAIN
# =========================================
blockchain = Blockchain()

# =========================================
# LOAD MODEL
# =========================================
model = YOLO("yolov8n.pt")

# =========================================
# CAMERA
# =========================================
cap = cv2.VideoCapture(0)

if not cap.isOpened():

    print("❌ Cannot open camera")
    exit()

# =========================================
# DATA
# =========================================
counts = {
    "Plastic": 0,
    "Paper": 0,
    "Metal": 0
}

logs = []

last_logged = ""
last_send_time = 0

# =========================================
# WASTE MAP
# =========================================

PLASTIC = [
    "bottle",
    "cup",
    "wine glass",
    "remote",
    "mouse",
    "keyboard",
    "cell phone",
    "toothbrush"
]

PAPER = [
    "book",
    "tv",
    "laptop"
]

METAL = [
    "scissors"
]

# =========================================
# MAP WASTE
# =========================================
def map_waste(label):

    if label in PLASTIC:
        return "Plastic"

    elif label in PAPER:
        return "Paper"

    elif label in METAL:
        return "Metal"

    return None


# =========================================
# COLORS
# =========================================
def get_color(waste):

    if waste == "Plastic":
        return (0, 255, 0)

    elif waste == "Paper":
        return (0, 200, 255)

    elif waste == "Metal":
        return (255, 120, 0)

    return (180, 180, 180)


# =========================================
# GRADIENT
# =========================================
def gradient_bg(img):

    h, w = img.shape[:2]

    for i in range(h):

        c = int(15 + (i / h) * 70)

        cv2.line(
            img,
            (0, i),
            (w, i),
            (c, c, c),
            1
        )


# =========================================
# CARD
# =========================================
def draw_card(img, x1, y1, x2, y2):

    cv2.rectangle(
        img,
        (x1, y1),
        (x2, y2),
        (40, 40, 40),
        -1
    )

    cv2.rectangle(
        img,
        (x1, y1),
        (x2, y2),
        (90, 90, 90),
        2
    )


# =========================================
# BLOCKCHAIN VISUALIZATION
# =========================================
def draw_blockchain(panel, blockchain):

    start_x = 20
    y = 20

    max_blocks = 3

    blocks = blockchain.chain[-max_blocks:]

    for i, block in enumerate(blocks):

        x = start_x + (i * 95)

        # block
        cv2.rectangle(
            panel,
            (x, y),
            (x + 70, y + 50),
            (0, 255, 255),
            2
        )

        cv2.putText(
            panel,
            f"B{block.index}",
            (x + 18, y + 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            2
        )

        short_hash = block.hash[:6]

        cv2.putText(
            panel,
            short_hash,
            (x + 5, y + 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.35,
            (0, 255, 0),
            1
        )

        # arrow
        if i < len(blocks) - 1:

            cv2.arrowedLine(
                panel,
                (x + 70, y + 25),
                (x + 95, y + 25),
                (255, 255, 255),
                2
            )


# =========================================
# FPS
# =========================================
prev_time = time.time()

# =========================================
# MAIN LOOP
# =========================================
while True:

    try:

        ret, frame = cap.read()

        if not ret:
            print("❌ Camera frame error")
            break

        frame = cv2.resize(frame, (640, 480))

        annotated = frame.copy()

        # =========================================
        # FPS
        # =========================================
        curr_time = time.time()

        fps = int(1 / (curr_time - prev_time + 0.0001))

        prev_time = curr_time

        # =========================================
        # YOLO DETECT
        # =========================================
        results = model(
            frame,
            conf=0.25,
            verbose=False
        )

        current_type = "None"

        found = False

        # =========================================
        # HEADER
        # =========================================
        cv2.rectangle(
            annotated,
            (0, 0),
            (640, 50),
            (10, 10, 10),
            -1
        )

        cv2.putText(
            annotated,
            "SMART WASTE AI v4.0",
            (15, 32),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.putText(
            annotated,
            f"{fps} FPS",
            (540, 32),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        # =========================================
        # DETECT OBJECTS
        # =========================================
        for box in results[0].boxes:

            confidence = float(box.conf[0])

            if confidence < 0.30:
                continue

            cls = int(box.cls[0])

            label = model.names[cls]

            # ignore person
            if label == "person":
                continue

            waste = map_waste(label)

            if waste is None:
                continue

            found = True

            current_type = waste

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            color = get_color(waste)

            # =========================================
            # BOX
            # =========================================
            cv2.rectangle(
                annotated,
                (x1, y1),
                (x2, y2),
                color,
                3
            )

            # =========================================
            # LABEL BG
            # =========================================
            cv2.rectangle(
                annotated,
                (x1, y1 - 40),
                (x1 + 220, y1),
                color,
                -1
            )

            # =========================================
            # LABEL
            # =========================================
            cv2.putText(
                annotated,
                f"{waste} ({confidence:.2f})",
                (x1 + 10, y1 - 12),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2
            )

            # =========================================
            # SAVE BLOCKCHAIN
            # =========================================
            now = time.time()

            if (
                waste != last_logged
                and now - last_send_time > 5
            ):

                t = time.strftime("%H:%M:%S")

                log_text = f"{t} - {waste}"

                logs.append(log_text)

                counts[waste] += 1

                last_logged = waste

                last_send_time = now

                # =========================================
                # BLOCKCHAIN
                # =========================================
                blockchain.add_block(
                    waste,
                    round(confidence, 2),
                    "Camera 1"
                )

                valid = blockchain.is_chain_valid()

                print("Blockchain valid:", valid)

                # =========================================
                # SAVE IMAGE
                # =========================================
                img_name = "capture.jpg"

                cv2.imwrite(
                    img_name,
                    frame
                )

                # =========================================
                # TELEGRAM
                # =========================================
                send_telegram(
                    f"♻️ SMART WASTE DETECTED\n"
                    f"Type: {waste}\n"
                    f"Confidence: {confidence:.2f}\n"
                    f"Time: {t}"
                )

                send_photo(img_name)

        # =========================================
        # STATUS
        # =========================================
        if found:

            status = "AI DETECTED"

            col = (0, 255, 0)

        else:

            status = "WAITING"

            col = (0, 0, 255)

        cv2.putText(
            annotated,
            status,
            (15, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            col,
            3
        )

        # =========================================
        # AI SCAN EFFECT
        # =========================================
        scan_y = int((time.time() * 150) % 480)

        cv2.line(
            annotated,
            (0, scan_y),
            (640, scan_y),
            (0, 255, 255),
            2
        )

        # =========================================
        # SIDE PANEL
        # =========================================
        panel = np.zeros(
            (480, 320, 3),
            dtype="uint8"
        )

        gradient_bg(panel)

        # =========================================
        # BLOCKCHAIN VISUAL
        # =========================================
        draw_blockchain(
            panel,
            blockchain
        )

        # =========================================
        # TITLE
        # =========================================
        cv2.putText(
            panel,
            "AI DASHBOARD",
            (50, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2
        )

        # =========================================
        # CURRENT
        # =========================================
        draw_card(panel, 20, 120, 300, 200)

        cv2.putText(
            panel,
            "Current Waste",
            (30, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (180, 180, 180),
            1
        )

        cv2.putText(
            panel,
            current_type,
            (30, 185),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            get_color(current_type),
            2
        )

        # =========================================
        # STATS
        # =========================================
        draw_card(panel, 20, 220, 300, 340)

        cv2.putText(
            panel,
            "Statistics",
            (30, 250),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        y = 285

        for k, v in counts.items():

            cv2.putText(
                panel,
                f"{k}: {v}",
                (30, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                get_color(k),
                2
            )

            y += 30

        # =========================================
        # BLOCKCHAIN STATUS
        # =========================================
        valid = blockchain.is_chain_valid()

        if valid:

            txt = "Blockchain VERIFIED"
            color = (0, 255, 0)

        else:

            txt = "BLOCKCHAIN TAMPERED"
            color = (0, 0, 255)

        cv2.putText(
            panel,
            txt,
            (20, 390),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

        # =========================================
        # RECENT LOGS
        # =========================================
        draw_card(panel, 20, 405, 300, 470)

        y = 430

        for log in logs[-2:]:

            cv2.putText(
                panel,
                log,
                (30, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (220, 220, 220),
                1
            )

            y += 22

        # =========================================
        # COMBINE
        # =========================================
        combined = cv2.hconcat([
            annotated,
            panel
        ])

        cv2.imshow(
            "SMART WASTE AI",
            combined
        )

        # =========================================
        # EXIT
        # =========================================
        key = cv2.waitKey(1)

        if key & 0xFF == ord('q'):
            break

    except Exception as e:

        print("Runtime Error:", e)

# =========================================
# FINAL
# =========================================
blockchain.show_chain()

blockchain.is_chain_valid()

blockchain.export_report()

cap.release()

cv2.destroyAllWindows()
