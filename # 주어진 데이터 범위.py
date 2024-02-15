import tkinter as tk
from tkinter import filedialog
import openpyxl
import csv
import os

def process_excel(file_path, data_ranges):
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        all_data = []
        for data_range in data_ranges:
            for row in sheet[data_range]:
                row_data = [cell.value for cell in row]
                all_data.append(row_data)

        workbook.close()

        return all_data

    except Exception as e:
        print(f"오류 발생: {e}")
        return None

def save_to_csv(data, csv_file_path):
    try:
        # 파일 경로를 분리
        file_path, ext = os.path.splitext(csv_file_path)

        # 파일명에 날짜 및 시간 추가
        new_file_path = f"{file_path}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"

        with open(new_file_path, 'w', newline='', encoding='ANSI') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(data)
        print(f"CSV 파일이 성공적으로 저장되었습니다: {new_file_path}")

    except Exception as e:
        print(f"CSV 파일 저장 중 오류 발생: {e}")

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    entry_path.delete(0, tk.END)
    entry_path.insert(tk.END, file_path)

def process_file():
    file_path = entry_path.get()
    data = process_excel(file_path, data_ranges)
    if data:
        # 파일명 추출
        file_name, ext = os.path.splitext(file_path)
        csv_file_path = f"{file_name}_processed{ext}"
        save_to_csv(data, csv_file_path)
        print("처리가 완료되었습니다.")

# 주어진 데이터 범위
data_ranges = [
    'A4:I16', 'J5:R16', 'S5:AA16', 'AB5:AJ16', 'AK5:AS16', 'AT5:BB16',
    'BC5:BK16', 'BL5:BT16', 'BU5:CC16', 'CD5:CL16', 'CM5:CU16', 'CV5:DD16',
    'DE5:DM16', 'DN5:DV16', 'DW5:EE16', 'EF5:EN16', 'EO5:EW16', 'EX5:FF16',
    'FG5:FO16', 'FP5:FX16', 'FY5:GG16', 'GH5:GP16', 'GQ5:GY16', 'GZ5:HH16',
    'HI5:HQ16', 'HR5:HZ16', 'IA5:II16', 'IJ5:IR16', 'IS5:JA16', 'JB5:JJ16',
    'JK5:JS16', 'JT5:KB16'
]

# GUI 생성
root = tk.Tk()
root.title("Excel Data Processor")

# 파일 경로 입력 창
entry_path = tk.Entry(root, width=50)
entry_path.pack(pady=10)

# 파일 선택 버튼
button_browse = tk.Button(root, text="파일 선택", command=browse_file)
button_browse.pack(pady=5)

# 처리 버튼
button_process = tk.Button(root, text="처리 및 CSV 저장 및 정렬", command=process_file)
button_process.pack(pady=20)

root.mainloop()
