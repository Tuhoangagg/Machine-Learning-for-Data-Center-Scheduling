import pandas as pd
import random

print("--- ĐANG KHỞI TẠO DỮ LIỆU BẰNG PANDAS ---")

data = []
for i in range(500):
    job_type = random.choice(['Flask_Sort', 'MapReduce_WordCount', 'ML_Train'])
    data_size = random.randint(100, 10000)
    
    # Tính toán thời gian chạy thực tế theo mô hình phi tuyến
    if job_type == 'Flask_Sort':
        actual_runtime = (data_size ** 2) * 0.0000005 + random.uniform(0.1, 0.5)
    elif job_type == 'MapReduce_WordCount':
        actual_runtime = data_size * 0.0005 + random.uniform(0.2, 0.8)
    else:
        actual_runtime = data_size * 0.001 + random.uniform(0.5, 1.5)

    data.append([job_type, data_size, actual_runtime])

# Tạo cấu trúc DataFrame bằng Pandas
df = pd.DataFrame(data, columns=['Job_Type', 'Data_Size', 'Actual_Runtime'])

# Xuất bảng dữ liệu ra file CSV
df.to_csv('dataset.csv', index=False)

print("🎉 THÀNH CÔNG: Đã tạo xong file dataset.csv")
print(df.head()) # In thử 5 dòng đầu tiên để kiểm tra