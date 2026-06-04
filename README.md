# ♻️ HỆ THỐNG PHÂN LOẠI RÁC THÔNG MINH TÍCH HỢP BLOCKCHAIN

## Giới thiệu

Hệ thống phân loại rác thông minh là giải pháp ứng dụng Trí tuệ nhân tạo (AI), Thị giác máy tính (Computer Vision), Blockchain và IoT nhằm hỗ trợ quản lý chất thải trong mô hình Thành phố thông minh.

Hệ thống sử dụng mô hình YOLOv8 để nhận diện và phân loại rác theo thời gian thực thông qua camera. Kết quả nhận diện được hiển thị trên Web Dashboard, gửi thông báo qua Telegram và lưu trữ trên Blockchain nhằm đảm bảo tính minh bạch, bảo mật và khả năng truy xuất dữ liệu.

---

## Chức năng chính

### Nhận diện rác thời gian thực

* Nhận dữ liệu từ camera.
* Phát hiện đối tượng bằng YOLOv8.
* Phân loại thành:

  * ♻️ Recyclable (Tái chế)
  * 🚫 Non-Recyclable (Không tái chế)

### Dashboard giám sát

* Hiển thị camera trực tiếp.
* Hiển thị kết quả nhận diện.
* Thống kê số lượng rác.
* Lưu lịch sử phân loại.

### Blockchain Monitoring

* Lưu dữ liệu nhận diện dưới dạng Block.
* Kiểm tra tính toàn vẹn dữ liệu.
* Phát hiện chỉnh sửa trái phép (Tampered Detection).

### Telegram Notification

Tự động gửi:

* Ảnh nhận diện.
* Loại rác.
* Độ tin cậy (Confidence).
* Thời gian nhận diện.

### IoT Smart Sorting

* ESP32 nhận lệnh từ hệ thống.
* Servo SG90 tự động phân loại:

  * Rác tái chế → Bên phải.
  * Rác không tái chế → Bên trái.

---

## Công nghệ sử dụng

### Trí tuệ nhân tạo

* YOLOv8
* Deep Learning
* Computer Vision
* OpenCV

### Phát triển hệ thống

* Python
* Flask
* HTML/CSS
* JavaScript

### Blockchain

* Blockchain Python
* SHA256 Hash
* Proof of Work
* JSON Blockchain Storage

### IoT

* ESP32
* Servo SG90

### Kết nối

* Telegram Bot API

---

## Kiến trúc hệ thống

Camera

↓

OpenCV

↓

YOLOv8

↓

Phân loại rác

↓

Flask Dashboard

↓

├── Telegram Bot

├── Blockchain

└── ESP32 + Servo SG90

---

## Cấu trúc dự án

```text
smart-waste-ai/
│
├── app.py
├── detect.py
├── blockchain.py
├── blockchain_data.json
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
├── poster/
│   ├── Poster_Blockchain.pdf
│   └── Poster_Blockchain.png
│
└── README.md
```

## Cài đặt

### Clone Repository

```bash
git clone https://github.com/trinhkequang/smart-waste-ai.git
```

### Cài đặt thư viện

```bash
pip install flask ultralytics opencv-python requests numpy
```

### Chạy chương trình

```bash
python app.py
```

---

## Truy cập hệ thống

Dashboard:

```bash
http://127.0.0.1:5000
```

Blockchain Monitor:

```bash
http://127.0.0.1:5000/blockchain
```

---

## Kết quả đạt được

✅ Nhận diện rác thời gian thực

✅ Phân loại tái chế / không tái chế

✅ Dashboard trực quan

✅ Lưu trữ Blockchain

✅ Gửi Telegram tự động

✅ Tích hợp ESP32 và Servo SG90

✅ Hỗ trợ mô hình Thành phố thông minh

---

## Hướng phát triển

* Triển khai trên Ethereum Blockchain.
* Kết nối Cloud để lưu trữ dữ liệu.
* Tích hợp Smart Bin thực tế.
* Hỗ trợ nhiều camera đồng thời.
* Mở rộng bộ dữ liệu huấn luyện.
* Triển khai tại khu dân cư và trường học.

---

## Poster Đề Tài

Poster môn Công nghệ Blockchain được lưu tại:

```text
poster/Poster_Blockchain.pdf
```

hoặc

```text
poster/Poster_Blockchain.png
```

---

## Tác giả

**Trịnh Kế Quang**

Khoa Công Nghệ Thông Tin

Trường Đại Học Đại Nam

GitHub: https://github.com/trinhkequang

---

## Giấy phép

Dự án được xây dựng phục vụ mục đích học tập, nghiên cứu và báo cáo học phần.
