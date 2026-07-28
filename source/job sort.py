# job_sort.py
import sys
import random
import time

def main():
    # Nhận tham số N từ dòng lệnh
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = 1000

    # Tạo mảng ngẫu nhiên
    data = [random.random() for _ in range(n)]
    
    # Thực hiện sắp xếp (Giả lập công việc nặng)
    data.sort() 
    print(f"Da sap xep {n} phan tu.")

if __name__ == "__main__":
    main()