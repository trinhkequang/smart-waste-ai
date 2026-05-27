# ♻️ Smart Waste AI

AI-powered smart waste classification system using YOLOv8, Flask, OpenCV, Blockchain and Telegram Bot.

---

# 📌 Introduction

Smart Waste AI is a real-time waste detection and classification system built with Deep Learning and Computer Vision technologies.

The system uses a webcam to detect waste objects and classify them into:

* Recyclable Waste
* Non-Recyclable Waste

Besides AI detection, the system also integrates:

* 🌐 Flask Web Dashboard
* ⛓️ Blockchain Data Storage
* 📲 Telegram Notification
* 📊 Detection History
* 🧠 YOLOv8 Deep Learning Model

---

# 🚀 Features

## ✅ Real-time Waste Detection

Detect waste objects directly from webcam using YOLOv8.

## ✅ Waste Classification

Classify waste into:

* Recyclable
* Non-Recyclable

## ✅ Smart Dashboard

Modern Flask web dashboard with:

* Live camera stream
* Detection information
* Statistics
* Detection history
* Blockchain status

## ✅ Telegram Notification

Automatically send:

* Captured image
* Waste type
* Confidence score
* Detection time

to Telegram Bot.

## ✅ Blockchain Integration

Store waste classification data into blockchain-style JSON blocks.

Each block contains:

* Timestamp
* Waste type
* Confidence
* Previous hash
* Current hash
* Nonce

## ✅ Blockchain Web Viewer

View all stored blocks from:

```bash
http://127.0.0.1:5000/blockchain
```

---

# 🧠 Technologies Used

* Python
* YOLOv8
* OpenCV
* Flask
* Deep Learning
* Computer Vision
* Telegram Bot API
* JSON Blockchain

---

# 📂 Project Structure

```bash
waste_project/
│
├── app.py
├── blockchain.py
├── blockchain_web_data.json
├── block_images.json
│
├── templates/
│   ├── index.html
│   └── blockchain.html
│
├── static/
│   └── captures/
│
├── runs/
│
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/trinhkequang/smart-waste-ai.git
```

---

## 2️⃣ Install Requirements

```bash
pip install flask ultralytics opencv-python requests numpy
```

---

## 3️⃣ Run Application

```bash
python app.py
```

---

# 🌐 Web Dashboard

Open browser:

```bash
http://127.0.0.1:5000
```

Blockchain page:

```bash
http://127.0.0.1:5000/blockchain
```

---

# 🤖 YOLOv8 Model

The system uses a custom YOLOv8 model trained on waste datasets.

Detected classes include:

* plastic_bottle
* cardboard
* can
* scrap_plastic
* paper
* battery
* chemical waste
* straw
* snack bag
* and more...

---

# 📸 System Workflow

```text
Camera
   ↓
OpenCV Frame Capture
   ↓
Face Detection Filter
   ↓
ROI Waste Detection
   ↓
YOLOv8 Inference
   ↓
Waste Classification
   ↓
Stable Prediction
   ↓
Flask Dashboard
   ↓
 ┌───────────────┬───────────────┐
 ↓               ↓               ↓
Telegram     Blockchain      History Log
```

---

# 🔐 Blockchain Structure

Example block:

```json
{
    "index": 14,
    "timestamp": 1778829791.89751,
    "real_time": "2026-05-15 14:23:11",
    "waste_type": "Recyclable",
    "confidence": 0.69,
    "status": "Camera 1",
    "previous_hash": "000071d46c9160271f21d28e02a05e2e728685ff75d40eb32fea10aca1875796",
    "nonce": 23916,
    "hash": "000013607aec632e1b5332ccc7f04d0ab89110d883e92541c3718ad5b36585ff"
}
```

---

# 📷 Screenshots

## Main Dashboard

* Real-time webcam
* Waste classification
* Statistics
* Detection history

## Blockchain Dashboard

* Stored blockchain blocks
* Detection images
* Hash verification

## Telegram Notification

* Captured waste image
* Detection result
* Confidence score

---

# 📈 Future Improvements

* IoT integration
* Servo-controlled smart trash bins
* Raspberry Pi deployment
* Cloud database
* Ethereum blockchain integration
* Multi-camera support

---

# 👨‍💻 Author

Trịnh Kế Quang

Email: [trinhkequang01032004@gmail.com](mailto:trinhkequang01032004@gmail.com)

GitHub:
https://github.com/trinhkequang

---

# 📜 License

This project is for educational and research purposes.
