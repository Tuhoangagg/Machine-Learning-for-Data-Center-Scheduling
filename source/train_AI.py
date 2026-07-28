import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error

print("=== NGÀY 2: ĐỌC DỮ LIỆU BẰNG PANDAS ===")
# 1. Sử dụng Pandas để đọc file dữ liệu
df = pd.read_csv('dataset.csv')

# 2. Tiền xử lý: Chuyển đổi biến chữ sang dạng số One-Hot Encoding bằng Pandas
df = pd.get_dummies(df, columns=['Job_Type'], dtype=float)

# Tách đặc trưng đầu vào X và nhãn mục tiêu y
X = df.drop(columns=['Actual_Runtime'])
y = df['Actual_Runtime']

# 3. Sử dụng Scikit-learn để chia tập dữ liệu thành 80% Train và 20% Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Chuẩn hóa đặc trưng (Feature Scaling) bằng StandardScaler của Scikit-learn
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Khởi tạo và khớp mô hình SVR với nhân RBF
model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
model.fit(X_train_scaled, y_train)

# 6. Dự đoán và Đánh giá sai số bằng Scikit-learn Metrics
y_pred = model.predict(X_test_scaled)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print("\n================ KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH AI ================")
print(f"Sai số tuyệt đối trung bình (MAE): {mae:.4f} giây")
print(f"Sai số bình phương trung bình (MSE): {mse:.4f} giây")
print(f"Căn sai số bình phương trung bình (RMSE): {rmse:.4f} giây")
print("==================================================================")