# Hệ thống Đánh giá & Mô phỏng các Thuật toán Lập lịch CPU (CPU Scheduling Algorithms Benchmark)

Ứng dụng mô phỏng và đo đạc hiệu năng của các thuật toán lập lịch tiến trình (CPU Scheduling) trong Hệ điều hành. Dự án cung cấp công cụ phân tích trực quan, so sánh chi tiết các chỉ số vận hành ($Waiting\ Time$, $Turnaround\ Time$, $CPU\ Utilization$) giữa các thuật toán cổ điển và nâng cao.

Phát triển cho học phần **Hệ điều hành (Operating Systems)** / **Nghiên cứu Hệ thống**.

---

## 📸 Demo & Giao diện
<img width="829" height="543" alt="Demo khi chưa kích hoạt" src="https://github.com/user-attachments/assets/803d59f7-fc4e-499d-a69e-a8c846c6bf39" />

<img width="829" height="537" alt="Demo khi đã kích hoạt" src="https://github.com/user-attachments/assets/460c7025-a293-4281-9cda-9b3e63c23290" />
---

## 📌 Mục lục
- [Tính năng](#-tính-năng)<img width="2400" height="1200" alt="wait_time_chart" src="https://github.com/user-attachments/assets/277e7ed9-e603-4a28-afed-2cb5e3d53418" />
- [Thuật toán & So sánh Lý thuyết](#-thuật-toán--so-sánh-lý-thuyết)
- [Mô hình Toán học & Chỉ số Đánh giá](#-mô-hình-toán-học--chỉ-số-đánh-giá)
- [Cấu trúc Thư mục](#-cấu-trúc-thư-mục)
- [Cài đặt & Cách chạy](#-cài-đặt--cách-chạy)
- [Kết quả Thực nghiệm & Benchmark](#-kết-quả-thực-nghiệm--benchmark)
- [Tác giả & Đóng góp](#-tác-giả--đóng-góp)
- [License](#-license)

---

## 🌟 Tính năng

- **Mô phỏng đa thuật toán:** Độc lập hoặc so sánh song song nhiều thuật toán lập lịch CPU.
- **Hỗ trợ Preemptive & Non-preemptive:** Cho phép tùy chỉnh cơ chế độc quyền hoặc tranh chấp CPU.
- **Tự động tính toán chỉ số:** Tự động xuất biểu đồ Gantt (Gantt Chart) và bảng thống kê thời gian.
- **Tùy biến Dataset:** Cho phép nhập danh sách tiến trình ($Process\ ID$, $Arrival\ Time$, $Burst\ Time$, $Priority$) thủ công hoặc sinh ngẫu nhiên theo phân phối.
- **Xuất báo cáo trực quan:** Xuất đồ thị so sánh hiệu năng dưới dạng hình ảnh (`.png`) và dữ liệu thô (`.csv`).

---

## 🧠 Thuật toán & So sánh Lý thuyết

Hệ thống đã cài đặt và đánh giá 5 thuật toán lập lịch cốt lõi:

| Thuật toán | Loại (Type) | Ưu điểm | Nhược điểm / Hạn chế |
| :--- | :--- | :--- | :--- |
| **FCFS** (First-Come, First-Served) | Non-Preemptive | Đơn giản, công bằng về thời gian đến | Bị hiệu ứng Convoy Effect (tiến trình ngắn chờ tiến trình dài) |
| **SJF** (Shortest Job First) | Non-Preemptive | Tối ưu hóa thời gian chờ trung bình ($\bar{W}$) | Có thể gây đói tài nguyên (Starvation) cho tiến trình dài |
| **SRTF** (Shortest Remaining Time First) | Preemptive | Đạt thời gian phản hồi cực nhanh cho tác vụ ngắn | Chi phí chuyển bối cảnh (Context Switch Overhead) cao |
| **Round Robin (RR)** | Preemptive | Công bằng, phù hợp hệ thống chia sẻ thời gian | Phụ thuộc hoàn toàn vào Kích thước Lát cắt Thời gian ($Time\ Quantum$) |
| **Priority Scheduling** | Preemptive / Non-Preemptive | Ưu tiên các tác vụ quan trọng của hệ thống | Dễ gây Starvation (Cần giải pháp Aging để khắc phục) |

---

## 📐 Mô hình Toán học & Chỉ số Đánh giá

Hệ thống đánh giá hiệu năng dựa trên 4 chỉ số chuẩn mực trong Hệ điều hành:

1. **Thời gian hoàn tất ($Completion\ Time - CT$):** Thời điểm tiến trình kết thúc thực thi.
2. **Thời gian lưu lại ($Turnaround\ Time - TAT$):**
   $$TAT = CT - Arrival\ Time$$
3. **Thời gian chờ ($Waiting\ Time - WT$):**
   $$WT = TAT - Burst\ Time$$
4. **Hiệu suất sử dụng CPU ($CPU\ Utilization$):**
   $$CPU\ Utilization = \left( \frac{\sum Burst\ Time}{Total\ Simulation\ Time} \right) \times 100\%$$

---

## 📁 Cấu trúc Thư mục

```text
Machine-Learning-for-Data-Center-Scheduling/
├── src/                 # Source code chính của chương trình
│   ├── algorithms/      # Cài đặt các thuật toán (FCFS, SJF, RR, SRTF, Priority)
│   ├── models/          # Định nghĩa cấu trúc Process, CPU State
│   └── utils/           # Helper tính toán chỉ số và xuất đồ thị
│
├── docs/                # Báo cáo nghiên cứu chi tiết (PDF) & Slide
│   └── OS_CPU_Scheduling_Report.pdf
│
├── assets/              # Chứa ảnh chụp biểu đồ kết quả (dùng cho README)
│   └── cpu_scheduling_demo.png
│
├── logs/ / datasets/    # Dữ liệu thử nghiệm đầu vào và kết quả CSV
├── README.md            # Tài liệu hướng dẫn dự án
└── .gitignore           # File cấu hình bỏ qua file rác khi Git push<img width="2400" height="1200" alt="wait_time_chart" src="https://github.com/user-attachments/assets/3e2a0e95-81e1-4409-9990-123089bac850" />
<img width="2400" height="1200" alt="throughput_chart" src="https://github.com/user-attachments/assets/1616c57f-2793-4594-a433-18f36481f882" />
<img width="384" height="102" alt="Job lúc sau" src="https://github.com/user-attachments/assets/b33423b2-cf5e-4307-933a-c5d40ddc7a4b" />
<img width="386" height="102" alt="Job ban đầu" src="https://github.com/user-attachments/assets/6ac14af6-19eb-4918-9fa7-76a085b699a7" />
<img width="829" height="537" alt="Demo khi đã kích hoạt" src="https://github.com/user-attachments/assets/ba0e83d9-7e41-4057-ab64-cba5af31ce20" />
<img width="829" height="543" alt="Demo khi chưa kích hoạt" src="https://github.com/user-attachments/assets/258a2a7b-b1dc-4322-8973-22ab4820daa9" />
<img width="829" height="543" alt="Demo khi chưa kích hoạt" src="https://github.com/user-attachments/assets/748332bd-8389-4dc2-bb96-cb6af46a8124" />
