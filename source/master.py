import socket
import json
import threading

def handle_agent(client_socket, addr):
    try:
        # Bước 1: Nhận thông số từ Agent (Ngày 1-2)
        data = client_socket.recv(1024).decode('utf-8')
        if not data: return
        resources = json.loads(data)
        agent_id = resources['agent_id']
        print(f"\n[KẾT NỐI] {agent_id} từ {addr}")

        # Bước 2: Giao việc (Ngày 3-4)
        # Master gửi một lệnh Python giả lập chạy trong 3 giây
        job_command = "python3 -c 'import time; time.sleep(3); print(\"Xong viec!\")'"
        client_socket.send(job_command.encode('utf-8'))
        print(f"[GIAO VIỆC] Đã gửi lệnh tới {agent_id}")

        # Bước 3: Nhận báo cáo (Ngày 5-6)
        report_data = client_socket.recv(1024).decode('utf-8')
        if report_data:
            report = json.loads(report_data)
            print(f"[BÁO CÁO] {agent_id} hoàn thành. Runtime thực tế: {report['runtime']:.4f}s")

    except Exception as e:
        print(f"[LỖI] Xảy ra vấn đề với {addr}: {e}")
    finally:
        client_socket.close()

def start_master():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8000))
    server.listen(5)
    print("=== MASTER NODE ĐANG CHẠY - ĐỢI AGENT ===")

    while True:
        client_socket, addr = server.accept()
        # ĐA LUỒNG: Tạo nhánh riêng cho mỗi Agent để Master rảnh tay đón Agent khác
        thread = threading.Thread(target=handle_agent, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_master()
    
# Khởi tạo khóa để tránh xung đột khi nhiều Agent cùng báo cáo
resource_lock = threading.Lock()
agent_registry = {}

def handle_agent(client_socket, addr):
    try:
        # Nhận khai báo tài nguyên
        data = client_socket.recv(1024).decode('utf-8')
        if not data: return
        resources = json.loads(data)
        agent_id = resources['agent_id']

        # Dùng LOCK khi ghi dữ liệu vào danh sách quản lý
        with resource_lock:
            agent_registry[agent_id] = resources
            print(f"[SAFE] Đã đăng ký {agent_id} vào hệ thống.")

        # Giao việc và đợi báo cáo (như đã làm ở ngày trước)
        job_command = "python3 -c 'import time; time.sleep(2)'"
        client_socket.send(job_command.encode('utf-8'))
        
        report_data = client_socket.recv(1024).decode('utf-8')
        
        # Dùng LOCK khi cập nhật lại tài nguyên sau khi xong việc
        with resource_lock:
            print(f"[UPDATE] {agent_id} đã xong việc, tài nguyên đã được giải phóng.")

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client_socket.close()