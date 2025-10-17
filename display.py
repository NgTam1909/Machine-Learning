import tkinter as tk
from tkinter import ttk
import pandas as pd

# Đọc dữ liệu từ file CSV
df = pd.read_csv("comments_labels.csv")

# Kiểm tra cột có tồn tại không
if "sentiment" not in df.columns or "comment_cleaned" not in df.columns:
    raise ValueError("File CSV phải có cột 'sentiment' và 'comment_cleaned'")

# Lấy danh sách nhãn duy nhất và thêm lựa chọn "Tất cả"
labels = ["Tất cả"] + sorted(df['sentiment'].dropna().unique().tolist())

# Hàm cập nhật danh sách comment theo nhãn
def update_comments(*args):
    selected_label = label_var.get()
    if selected_label == "Tất cả":
        filtered_comments = df['comment_cleaned']
    else:
        filtered_comments = df[df['sentiment'] == selected_label]['comment_cleaned']

    # Cập nhật số lượng comment
    count_label.config(text=f"Số lượng comment: {len(filtered_comments)}")
    
    text_box.config(state=tk.NORMAL)
    text_box.delete(1.0, tk.END)
    if filtered_comments.empty:
        text_box.insert(tk.END, "Không có comment nào cho nhãn này.")
    else:
        for i, c in enumerate(filtered_comments, start=1):
            text_box.insert(tk.END, f"{i}. {c}\n\n")  # thêm số thứ tự
    text_box.config(state=tk.DISABLED)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Danh sách comment theo nhãn")
root.geometry("750x500")

# Tiêu đề
title = tk.Label(root, text="Danh sách comment", font=("Arial", 16, "bold"))
title.pack(pady=10)

# Dropdown chọn nhãn
frame = tk.Frame(root)
frame.pack(pady=5)

label_text = tk.Label(frame, text="Nhãn:", font=("Arial", 12, "bold"))
label_text.pack(side=tk.LEFT)

label_var = tk.StringVar(value="Tất cả")  # Đặt mặc định ở đây
label_dropdown = ttk.Combobox(frame, textvariable=label_var, values=labels, state="readonly", width=20)
label_dropdown.pack(side=tk.LEFT, padx=10)
label_dropdown.bind("<<ComboboxSelected>>", update_comments)

# Label hiển thị số lượng comment
count_label = tk.Label(root, text="Số lượng comment: 0", font=("Arial", 12), fg="blue")
count_label.pack(pady=5)

# Frame chứa Text + Scrollbar
text_frame = tk.Frame(root)
text_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_box = tk.Text(text_frame, wrap=tk.WORD, font=("Arial", 11), yscrollcommand=scrollbar.set)
text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=text_box.yview)

# Lần đầu load sẽ hiển thị tất cả comment
update_comments()

# Disable edit textbox
text_box.config(state=tk.DISABLED)
root.mainloop()


