import socket
import json
import subprocess
import time

def start_agent():
    agent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Kết nối tới Master (127.0.0.1 nếu chạy cùng máy)
        agent_socket.connect(('127.0.0.1', 8000))
        
        # Khai báo bản thân (Ngày 1-2)
        my_info = {"agent_id": "Agent_Tú_Hoàng", "cpu": 4, "ram": 8}
        agent_socket.send(json.dumps(my_info).encode('utf-8'))

        # Nhận lệnh từ Master (Ngày 3-4)
        command = agent_socket.recv(1024).decode('utf-8')
        print(f"[NHẬN LỆNH]: {command}")
        
        # ĐO THỜI GIAN CHẠY (Ngày 5-6) - Đây là dữ liệu cực quan trọng cho ML
        start_t = time.time()
        result = subprocess.run(command, shell=True, capture_output=True)
        runtime = time.time() - start_t

        # Gửi báo cáo kết quả (Ngày 5-6)
        report = {
            "status": "Thành công" if result.returncode == 0 else "Thất bại",
            "runtime": runtime
        }
        agent_socket.send(json.dumps(report).encode('utf-8'))
        print(f"[HOÀN THÀNH] Runtime: {runtime:.4f}s. Đã báo cáo cho Master.")

    except Exception as e:
        print(f"Lỗi kết nối: {e}")
    finally:
        agent_socket.close()

if __name__ == "__main__":
    start_agent()