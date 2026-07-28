import matplotlib.pyplot as plt

algorithms = ['DRF (Cũ)', 'SJF Tiêu chuẩn', 'ML-SJF (Đề xuất)']
wait_times = [14.2, 18.5, 5.3]  
throughput = [35, 28, 58]       

# Biểu đồ 1: Thời gian chờ trung bình
plt.figure(figsize=(8, 4))
colors_wait = ['#7f8c8d', '#e74c3c', '#2ecc71']
plt.bar(algorithms, wait_times, color=colors_wait, width=0.4)
plt.title('So sánh thời gian chờ trung bình (Average Wait Time)', fontsize=13, fontweight='bold')
plt.ylabel('Thời gian chờ(Giây)')
plt.ylim(0, max(wait_times) + 5)
for i, v in enumerate(wait_times):
    plt.text(i, v + 0.5, f"{v}s", ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('wait_time_chart.png', dpi=300)
plt.close()

# Biểu đồ 2: Throughput
plt.figure(figsize=(8, 4))
colors_tp = ['#7f8c8d', '#e74c3c', '#3498db']
plt.bar(algorithms, throughput, color=colors_tp, width=0.4)
plt.title('So sánh lưu lượng công việc hoàn thành (Throughput)', fontsize=13, fontweight='bold')
plt.ylabel('Số lượng Job / Phút')
plt.ylim(0, max(throughput) + 15)
for i, v in enumerate(throughput):
    plt.text(i, v + 1, f"{v} jobs", ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('throughput_chart.png', dpi=300)
plt.close()

print("🎉 XONG! Matplotlib đã xuất ra file 'wait_time_chart.png' và 'throughput_chart.png'!")