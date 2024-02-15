import pandas as pd
import tkinter as tk
from tkinter import filedialog

def read_excel_and_export_types():
    file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel files", "*.xlsx;*.xls")])

    if file_path:
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
            data_types = df.dtypes

            result_text.delete(1.0, tk.END)  # Clear previous result

            for column, dtype in data_types.iteritems():
                result_text.insert(tk.END, f"{column}: {dtype}\n")

        except Exception as e:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Error reading Excel file: {str(e)}")

# GUI 생성
root = tk.Tk()
root.title("Excel Data Types Reader")

# 파일 선택 버튼
select_button = tk.Button(root, text="Select Excel File", command=read_excel_and_export_types)
select_button.pack(pady=10)

# 결과 텍스트 박스
result_text = tk.Text(root, height=20, width=50)
result_text.pack(pady=10)

# GUI 실행
root.mainloop()
