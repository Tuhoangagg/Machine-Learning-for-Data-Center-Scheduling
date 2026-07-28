# Hệ thống Đánh giá & Mô phỏng các Thuật toán Lập lịch CPU (CPU Scheduling Algorithms Benchmark)

Ứng dụng mô phỏng và đo đạc hiệu năng của các thuật toán lập lịch tiến trình (CPU Scheduling) trong Hệ điều hành. Dự án cung cấp công cụ phân tích trực quan, so sánh chi tiết các chỉ số vận hành ($Waiting\ Time$, $Turnaround\ Time$, $CPU\ Utilization$) giữa các thuật toán cổ điển và nâng cao.

Phát triển cho học phần **Hệ điều hành (Operating Systems)** / **Nghiên cứu Hệ thống**.

---

## 📸 Demo & Giao diện
<img width="829" height="543" alt="Demo khi chưa kích hoạt" src="https://github.com/user-attachments/assets/803d59f7-fc4e-499d-a69e-a8c846c6bf39" />

<img width="829" height="537" alt="Demo khi đã kích hoạt" src="https://github.com/user-attachments/assets/460c7025-a293-4281-9cda-9b3e63c23290" />
---

## 📌 Mục lục
- [Tính năng](#-tính-năng)
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

## 📐 Cơ sở Toán học của Support Vector Regression (SVR)
Vì thời gian thực thi của tác vụ tỷ lệ phi tuyến tính với kích thước dữ liệu đầu vào (độ phức tạp thuật toán $O(N \log N)$ hoặc $O(N^2)$), mô hình áp dụng thuật toán **SVR với hàm nhân Radial Basis Function (RBF Kernel)**.

Bài toán tối ưu hóa của SVR được phát biểu dưới dạng:

$$\min_{w, b, \xi, \xi^*} \frac{1}{2} \|w\|^2 + C \sum_{i=1}^{n} (\xi_i + \xi_i^*)$$

Thỏa mãn các điều kiện ràng buộc:

$$\begin{cases}
y_i - w^T \phi(x_i) - b \le \epsilon + \xi_i \\
w^T \phi(x_i) + b - y_i \le \epsilon + \xi_i^* \\
\xi_i, \xi_i^* \ge 0
\end{cases}$$

**Trong đó:**
* $C$: Tham số phạt chính quy hóa (Regularization parameter).
* $\epsilon$: Phạm vi vùng không phạt sai số (Epsilon-insensitive tube).
* $\phi(x)$: Hàm ánh xạ đặc trưng thông qua **RBF Kernel**:

$$K(x_i, x_j) = \exp\left(-\gamma \|x_i - x_j\|^2\right)$$

---

## 🛠️ Hiện thực hóa huấn luyện bằng Scikit-Learn

Mô hình được huấn luyện với quy trình chuẩn hóa dữ liệu và cấu hình siêu tham số tối ưu:

* **Phân chia dữ liệu:** $80\%$ dành cho huấn luyện (Train Set) và $20\%$ dành cho kiểm thử độc lập (Test Set) sử dụng `train_test_split()`.
* **Chuẩn hóa đặc trưng:** Áp dụng `StandardScaler` để chuyển đổi các đặc trưng về phân phối chuẩn $z = \frac{x - \mu}{\sigma}$ (kỳ vọng bằng $0$, phương sai bằng $1$).
* **Siêu tham số mô hình SVR (Kernel RBF):**
  * $C = 100$
  * $\gamma = 0.1$
  * $\epsilon = 0.1$
## 📐 Chỉ số Đánh giá
Để đánh giá năng lực dự đoán thời gian thực thi tác vụ của mô hình **Support Vector Regression (SVR)**, hệ thống sử dụng ba độ do thống kê tiêu chuẩn để lượng hóa sai số giữa giá trị dự báo ($\hat{y}_i$) và giá trị thực tế ($y_i$):

### 1. RMSE (Root Mean Squared Error) - Sai số bình phương trung bình căn
Dùng để phạt nặng các sai số lớn hoặc các điểm dữ liệu dị biệt (outliers). Giá trị $RMSE$ càng tiến dần về $0$ thể hiện mô hình có độ chính xác và độ ổn định cao.

$$RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}$$

### 2. MSE (Mean Squared Error) - Sai số bình phương trung bình
Là trung bình cộng của bình phương các khoảng cách sai lệch. Độ đo này loại bỏ hoàn toàn dấu của sai số bằng phép bình phương và phóng đại biên độ lỗi, làm nổi bật hiệu suất tổng thể của hàm mất mát.

$$MSE = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$$

### 3. MAE (Mean Absolute Error) - Sai số tuyệt đối trung bình
Phản ánh mức độ sai lệch trung bình theo đơn vị thực tế của thời gian thực thi tác vụ.

$$MAE = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|$$

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
