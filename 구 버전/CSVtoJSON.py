import os
import pandas as pd
from tkinter import Tk, filedialog

def convert_csv_to_json(csv_file, json_file):
    try:
        df = pd.read_csv(csv_file)
        df.to_json(json_file, orient='records')
        print(f"Converted {csv_file} to {json_file}")
    except Exception as e:
        print(f"Error converting {csv_file} to JSON: {e}")

def convert_csv_files_in_folder(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            csv_file_path = os.path.join(folder_path, file_name)
            json_file_path = os.path.join(folder_path, f"{os.path.splitext(file_name)[0]}.json")
            convert_csv_to_json(csv_file_path, json_file_path)

def convert_folder_csv_to_json():
    root = Tk()
    root.withdraw()  # 기본 창 숨기기
    folder_path = filedialog.askdirectory(title="변환할 CSV 파일이 들어있는 폴더를 선택하세요")

    if folder_path:
        convert_csv_files_in_folder(folder_path)
        print("모든 CSV 파일을 JSON으로 변환하였습니다.")
    else:
        print("폴더 선택이 취소되었습니다.")

if __name__ == "__main__":
    convert_folder_csv_to_json()
