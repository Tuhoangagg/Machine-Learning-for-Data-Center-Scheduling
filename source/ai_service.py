import pandas as pd
import numpy as np
import socket
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

print("--- [Python AI] Đang huấn luyện mô hình SVR thật từ dataset.csv ---")
df = pd.read_csv('dataset.csv')
df_processed = pd.get_dummies(df, columns=['Job_Type'], dtype=float)
X = df_processed.drop(columns=['Actual_Runtime'])
y = df['Actual_Runtime']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
model.fit(X_train_scaled, y_train)
print("--- [Python AI] Huấn luyện hoàn tất! Sẵn sàng phục vụ Java App... ---")

# Khởi tạo Socket Server lắng nghe Java kết nối
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9999))
server.listen(5)

while True:
    conn, addr = server.accept()
    data = conn.recv(1024).decode('utf-8').strip()
    if data:
        # Nhận chuỗi từ Java dạng: "JobType,DataSize" -> Ví dụ: "Flask_Sort,5000"
        parts = data.split(',')
        job_type = parts[0]
        data_size = float(parts[1])
        
        # Tạo vector One-Hot đúng cấu trúc Pandas đã huấn luyện
        is_flask = 1.0 if job_type == 'Flask_Sort' else 0.0
        is_mr = 1.0 if job_type == 'MapReduce_WordCount' else 0.0
        is_ml = 1.0 if job_type == 'ML_Train' else 0.0
        
        # Dự đoán bằng Scikit-Learn
        input_data = np.array([[data_size, is_flask, is_mr, is_ml]])
        input_scaled = scaler.transform(input_data)
        predicted_runtime = model.predict(input_scaled)[0]
        
        # Gửi trả kết quả dự đoán về cho Java
        conn.sendall(f"{predicted_runtime}\n".encode('utf-8'))
    conn.close()