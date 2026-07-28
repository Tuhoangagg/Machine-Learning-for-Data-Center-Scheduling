import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;
import java.net.*;
import java.util.*;
import java.util.List;

class Job {
    String id;
    String type;
    double dataSize;
    double predictedRuntime;

    public Job(String id, String type, double dataSize) {
        this.id = id;
        this.type = type;
        this.dataSize = dataSize;
    }
}

public class DatacenterDemo extends JFrame {
    private JTable inputTable;
    private JTable outputTable;
    private DefaultTableModel inputModel;
    private DefaultTableModel outputModel;
    private JButton btnSchedule;
    private List<Job> jobQueue;

    public DatacenterDemo() {
        // Cấu hình cửa sổ ứng dụng
        setTitle("MÔ PHỎNG ĐIỀU PHỐI DATACENTER - ML-SJF");
        setSize(850, 550);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout(10, 10));

        // Khởi tạo dữ liệu mẫu
        initData();

        // --- TIÊU ĐỀ APP ---
        JLabel lblTitle = new JLabel("HỆ THỐNG ĐIỀU PHỐI TÁC VỤ THÔNG MINH ML-SJF (JAVA GUI)", JLabel.CENTER);
        lblTitle.setFont(new Font("Tahoma", Font.BOLD, 16));
        lblTitle.setForeground(new Color(41, 128, 185));
        lblTitle.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        add(lblTitle, BorderLayout.NORTH);

        // --- KHU VỰC TRUNG TÂM (CHỨA 2 BẢNG DỮ LIỆU) ---
        JPanel panelCenter = new JPanel(new GridLayout(1, 2, 15, 0));
        panelCenter.setBorder(BorderFactory.createEmptyBorder(0, 10, 0, 10));

        // Bảng 1: Hàng đợi tác vụ ban đầu
        JPanel panelInput = new JPanel(new BorderLayout());
        panelInput.setBorder(BorderFactory.createTitledBorder("1. Hàng đợi tác vụ thô đầu vào"));
        inputModel = new DefaultTableModel(new Object[]{"Mã Job", "Loại Tác Vụ", "Kích Thước (KB)"}, 0);
        inputTable = new JTable(inputModel);
        panelInput.add(new JScrollPane(inputTable), BorderLayout.CENTER);
        
        // Đổ dữ liệu thô vào bảng 1
        for (Job j : jobQueue) {
            inputModel.addRow(new Object[]{j.id, j.type, String.format("%,.0f", j.dataSize)});
        }

        // Bảng 2: Kết quả lập lịch tối ưu
        JPanel panelOutput = new JPanel(new BorderLayout());
        panelOutput.setBorder(BorderFactory.createTitledBorder("2. Thứ tự thực thi tối ưu (ML-SJF Schedule)"));
        outputModel = new DefaultTableModel(new Object[]{"Thứ tự", "Mã Job", "Loại Tác Vụ", "AI Dự Đoán (Giây)"}, 0);
        outputTable = new JTable(outputModel);
        panelOutput.add(new JScrollPane(outputTable), BorderLayout.CENTER);

        panelCenter.add(panelInput);
        panelCenter.add(panelOutput);
        add(panelCenter, BorderLayout.CENTER);

        // --- KHU VỰC NÚT BẤM ĐIỀU KHIỂN ---
        JPanel panelBottom = new JPanel();
        btnSchedule = new JButton("KÍCH HOẠT AI & LẬP LỊCH HỆ THỐNG");
        btnSchedule.setFont(new Font("Tahoma", Font.BOLD, 13));
        btnSchedule.setBackground(new Color(46, 204, 113));
        btnSchedule.setForeground(Color.WHITE);
        btnSchedule.setPreferredSize(new Dimension(300, 40));
        panelBottom.add(btnSchedule);
        add(panelBottom, BorderLayout.SOUTH);

        // Sự kiện khi bấm nút kích hoạt
        btnSchedule.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                processScheduling();
            }
        });
    }

    private void initData() {
        jobQueue = new ArrayList<>();
        jobQueue.add(new Job("JOB-01", "MapReduce_WordCount", 8500)); 
        jobQueue.add(new Job("JOB-02", "Flask_Sort", 4500));
        jobQueue.add(new Job("JOB-03", "ML_Train", 1200));
        jobQueue.add(new Job("JOB-04", "Flask_Sort", 9500));
        jobQueue.add(new Job("JOB-05", "ML_Train", 3500));
    }

    // Hàm kết nối cổng Socket đến Python AI Service
    private double askPythonAI(String jobType, double dataSize) {
        try (Socket socket = new Socket("127.0.0.1", 9999);
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {
            out.println(jobType + "," + dataSize);
            return Double.parseDouble(in.readLine());
        } catch (Exception e) {
            return dataSize * 0.001; // Thuật toán dự phòng nếu không bật Python
        }
    }

    // Luồng xử lý gọi AI và sắp xếp thuật toán ML-SJF
    private void processScheduling() {
        outputModel.setRowCount(0); // Xóa bảng cũ nếu có

        // Bước 1: Gọi Python dự đoán qua Socket
        for (Job j : jobQueue) {
            j.predictedRuntime = askPythonAI(j.type, j.dataSize);
        }

        // Bước 2: Sắp xếp theo thuật toán ML-SJF
        Collections.sort(jobQueue, (j1, j2) -> Double.compare(j1.predictedRuntime, j2.predictedRuntime));

        // Bước 3: Cập nhật lên giao diện bảng kết quả
        int order = 1;
        for (Job j : jobQueue) {
            outputModel.addRow(new Object[]{
                order++, 
                j.id, 
                j.type, 
                String.format("%.4f", j.predictedRuntime)
            });
        }
        
        JOptionPane.showMessageDialog(this, "🎉 Lập lịch hệ thống tối ưu hoàn tất thành công!", "Thông báo", JOptionPane.INFORMATION_MESSAGE);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new DatacenterDemo().setVisible(true);
        });
    }
}