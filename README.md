<div align="center">

# HỆ THỐNG PHÂN LOẠI RÁC TỰ ĐỘNG

## Ứng dụng AI, IoT và Blockchain trong quản lý rác thải thông minh

**Đồ án môn học: Thành phố thông minh và Nông nghiệp thông minh**

YOLOv8 · OpenCV · Flask · ESP32 · Blockchain · Telegram Bot

**Sinh viên thực hiện:** Trịnh Kế Quang<br>
**Khoa:** Công nghệ Thông tin<br>
**Trường:** Đại học Đại Nam

</div>

---

## Tổng quan đề tài

Quản lý rác thải không chỉ là bài toán vệ sinh môi trường, mà còn là một phần quan trọng trong quá trình xây dựng đô thị và khu sản xuất nông nghiệp bền vững. Khi rác không được phân loại từ nguồn, tài nguyên có thể tái chế bị lãng phí, chi phí xử lý tăng cao và nguy cơ ô nhiễm đất, nước, không khí ngày càng lớn.

Đề tài **Hệ thống phân loại rác tự động** được xây dựng như một mô hình thùng rác thông minh có khả năng nhận diện, phân loại và ghi nhận rác thải tự động. Hệ thống kết hợp trí tuệ nhân tạo, thị giác máy tính, thiết bị IoT và Blockchain để tạo nên một quy trình quản lý minh bạch, có thể giám sát và truy xuất.

Đề tài hướng tới hai bối cảnh ứng dụng:

- **Thành phố thông minh:** hỗ trợ phân loại rác tại trường học, khu dân cư, cơ quan và nơi công cộng.
- **Nông nghiệp thông minh:** làm nền tảng quản lý rác tại trang trại, khu sản xuất và chuỗi cung ứng nông nghiệp; góp phần phân tách vật liệu có thể tái chế khỏi chất thải cần xử lý riêng.

> Một thành phố thông minh không chỉ được đo bằng mức độ hiện đại của công nghệ, mà còn bằng khả năng sử dụng công nghệ để tạo ra môi trường sống xanh, minh bạch và bền vững hơn.

---

## Mục tiêu

- Tự động nhận diện và phân loại rác bằng mô hình YOLOv8.
- Điều khiển cơ cấu phân loại vật lý thông qua ESP32 và Servo.
- Giám sát trạng thái hệ thống trên Dashboard theo thời gian thực.
- Lưu lịch sử phân loại vào Blockchain để tăng tính toàn vẹn và khả năng truy xuất.
- Gửi cảnh báo và kết quả nhận diện qua Telegram.
- Xây dựng mô hình có thể mở rộng cho đô thị và khu sản xuất nông nghiệp thông minh.

---

## Giá trị của đề tài

### Đối với thành phố thông minh

Hệ thống hỗ trợ tự động hóa khâu phân loại rác tại nguồn, cung cấp dữ liệu phục vụ thống kê và giúp đơn vị quản lý theo dõi hoạt động của các điểm thu gom. Khi được triển khai ở quy mô lớn, dữ liệu có thể hỗ trợ tối ưu lịch thu gom, giảm chi phí vận chuyển và nâng cao hiệu quả tái chế.

### Đối với nông nghiệp thông minh

Các trang trại và khu sản xuất nông nghiệp phát sinh nhiều loại chất thải như bao bì, chai nhựa, vật tư đã qua sử dụng và chất thải cần xử lý riêng. Mô hình có thể được mở rộng để nhận diện các nhóm chất thải này, ghi lại nguồn phát sinh và hỗ trợ xây dựng quy trình sản xuất sạch hơn.

### Đối với môi trường và cộng đồng

- Khuyến khích thói quen phân loại rác tại nguồn.
- Hạn chế rác tái chế bị đưa vào khu xử lý chung.
- Tạo dữ liệu minh bạch phục vụ giám sát và nghiên cứu.
- Góp phần hướng tới kinh tế tuần hoàn và phát triển bền vững.

---

## Chức năng chính

### Nhận diện rác bằng AI

- Thu hình ảnh trực tiếp từ camera.
- Phát hiện vật thể bằng mô hình YOLOv8 đã huấn luyện.
- Phân loại kết quả thành `Recyclable` và `Non-Recyclable`.
- Sử dụng cơ chế bỏ phiếu nhiều khung hình để tăng độ ổn định.
- Hạn chế nhận diện sai khi khuôn mặt xuất hiện trong vùng camera.

### Phân loại tự động bằng IoT

- Flask gửi lệnh điều khiển đến ESP32 qua mạng nội bộ.
- ESP32 điều khiển Servo để chuyển rác sang đúng ngăn.
- Trạng thái kết nối IoT được cập nhật trên Dashboard.

### Dashboard giám sát thời gian thực

- Hiển thị luồng camera và kết quả nhận diện.
- Theo dõi nhãn vật thể, độ tin cậy và hành động phân loại.
- Thống kê số lượng rác tái chế và không tái chế.
- Hiển thị lịch sử các lần phân loại gần nhất.

### Lưu trữ và kiểm chứng bằng Blockchain

- Mỗi kết quả phân loại được ghi thành một Block.
- Các Block liên kết bằng `hash` và `previous_hash`.
- Sử dụng SHA-256 và cơ chế Proof of Work.
- Phát hiện dữ liệu bị chỉnh sửa hoặc chuỗi liên kết không hợp lệ.
- Cho phép xem lịch sử và hình ảnh liên quan trên trang Blockchain Monitor.

### Thông báo qua Telegram

- Gửi loại rác và độ tin cậy.
- Gửi thời gian phát hiện và trạng thái Blockchain.
- Gửi ảnh chụp tại thời điểm hệ thống ghi nhận kết quả.

---

## Kiến trúc hệ thống

```text
Camera
   |
   v
OpenCV + YOLOv8
   |
   v
Bộ xử lý và xác nhận kết quả
   |
   +------------------+-------------------+------------------+
   |                  |                   |                  |
   v                  v                   v                  v
Dashboard          ESP32 + Servo       Telegram          Blockchain
giám sát           phân loại vật lý     thông báo         lưu và kiểm chứng
```

### Quy trình hoạt động

1. Camera liên tục ghi nhận hình ảnh trong vùng nhận diện.
2. YOLOv8 phát hiện vật thể và trả về nhãn cùng độ tin cậy.
3. Hệ thống xác nhận kết quả qua nhiều khung hình liên tiếp.
4. Rác được xác định là tái chế hoặc không tái chế.
5. ESP32 nhận lệnh và điều khiển Servo phân loại rác.
6. Kết quả, thời gian và hình ảnh được lưu vào Blockchain.
7. Dashboard cập nhật dữ liệu và Telegram gửi thông báo.

---

## Công nghệ sử dụng

| Nhóm | Công nghệ | Vai trò |
|---|---|---|
| AI và Computer Vision | YOLOv8, OpenCV | Nhận diện và phân loại rác theo thời gian thực |
| Backend | Python, Flask | Xử lý nghiệp vụ, API và luồng camera |
| Frontend | HTML, CSS, JavaScript | Xây dựng Dashboard giám sát |
| IoT | ESP32, Servo SG90 | Điều khiển cơ cấu phân loại vật lý |
| Blockchain | SHA-256, Proof of Work, JSON | Lưu trữ và kiểm chứng lịch sử |
| Kết nối | HTTP, Telegram Bot API | Gửi lệnh IoT và thông báo từ xa |

---

## Giao diện hệ thống

### Dashboard giám sát

![Dashboard giám sát](dashboard.png)

### Blockchain Monitor

![Blockchain Monitor](blockchain.png)

### Thông báo Telegram

![Thông báo Telegram](telegram.png)

---

## Cấu trúc dự án

```text
smart-city-waste-management/
|
|-- app.py                       # Ứng dụng Flask và luồng xử lý chính
|-- blockchain.py                # Block, Blockchain và kiểm tra toàn vẹn
|-- detect_demo.py               # Chương trình nhận diện thử nghiệm
|-- train_yolo.py                # Huấn luyện mô hình YOLO
|-- blockchain_web_data.json     # Dữ liệu Blockchain cho Dashboard
|-- block_images.json            # Liên kết Block với ảnh nhận diện
|
|-- templates/
|   |-- index.html               # Dashboard chính
|   `-- blockchain.html          # Trang giám sát Blockchain
|
|-- static/
|   `-- captures/                # Ảnh được ghi nhận khi phân loại
|
|-- .env.example                 # Mẫu cấu hình Telegram
|-- requirements.txt             # Danh sách thư viện Python
`-- README.md
```

---

## Cài đặt và chạy dự án

### 1. Tải mã nguồn

```bash
git clone https://github.com/trinhkequang/smart-city-waste-management.git
cd smart-city-waste-management
```

### 2. Tạo môi trường Python

```bash
python -m venv .venv
```

Kích hoạt trên Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 4. Cấu hình hệ thống

- Cập nhật đường dẫn mô hình YOLO trong `app.py`.
- Cập nhật địa chỉ `ESP32_IP` để phù hợp với mạng đang sử dụng.
- Thiết lập Telegram bằng biến môi trường, không ghi token trực tiếp vào mã nguồn.

```powershell
$env:TELEGRAM_BOT_TOKEN="your_bot_token"
$env:TELEGRAM_CHAT_ID="your_chat_id"
```

### 5. Khởi chạy

```bash
python app.py
```

Truy cập:

- Dashboard: `http://127.0.0.1:5000`
- Blockchain Monitor: `http://127.0.0.1:5000/blockchain`

---

## Kết quả đạt được

- Nhận diện và phân loại nhiều nhóm rác theo thời gian thực.
- Tự động điều khiển mô hình thùng rác thông qua ESP32.
- Xây dựng Dashboard trực quan để theo dõi toàn bộ hệ thống.
- Lưu lịch sử phân loại và phát hiện thay đổi dữ liệu bằng Blockchain.
- Gửi kết quả và hình ảnh đến người quản lý qua Telegram.
- Hoàn thiện mô hình tích hợp AI, IoT, Web và Blockchain trong một quy trình thống nhất.

---

## Hạn chế hiện tại

- Mô hình phụ thuộc vào chất lượng và độ đa dạng của dữ liệu huấn luyện.
- Độ chính xác có thể bị ảnh hưởng bởi ánh sáng, góc camera và vật thể bị che khuất.
- Blockchain hiện được triển khai cục bộ, chưa phải mạng Blockchain phân tán.
- ESP32 và máy chủ cần kết nối cùng mạng để trao đổi lệnh.
- Hệ thống mới tập trung vào hai nhóm rác chính và cần mở rộng thêm cho chất thải nông nghiệp.

---

## Hướng phát triển

- Bổ sung nhận diện rác hữu cơ, rác nguy hại và chất thải nông nghiệp.
- Kết hợp cảm biến khối lượng, độ đầy và chất lượng không khí trong thùng rác.
- Xây dựng bản đồ số theo dõi các điểm thu gom trong đô thị hoặc trang trại.
- Ứng dụng dữ liệu để dự báo lượng rác và tối ưu tuyến thu gom.
- Kết nối Cloud Database và Dashboard quản lý nhiều thiết bị.
- Triển khai Blockchain phân tán hoặc Smart Contract để tăng khả năng xác thực.
- Nghiên cứu tái sử dụng rác hữu cơ cho ủ phân và mô hình kinh tế tuần hoàn.
- Phát triển ứng dụng di động để người quản lý nhận cảnh báo và theo dõi từ xa.

---

## Định hướng đóng góp cho phát triển bền vững

Đề tài thể hiện cách các công nghệ của thành phố thông minh và nông nghiệp thông minh có thể kết nối trong một bài toán gần gũi: quản lý rác thải. AI giúp hệ thống hiểu dữ liệu từ môi trường, IoT biến kết quả thành hành động vật lý, Blockchain bảo vệ tính minh bạch, còn Dashboard giúp con người giám sát và ra quyết định.

Với khả năng tiếp tục mở rộng, mô hình có thể trở thành nền tảng cho các điểm thu gom thông minh, trang trại xanh và hệ thống quản lý môi trường dựa trên dữ liệu.

---

## Tác giả

**Trịnh Kế Quang**<br>
Khoa Công nghệ Thông tin, Trường Đại học Đại Nam<br>
GitHub: [github.com/trinhkequang](https://github.com/trinhkequang)
