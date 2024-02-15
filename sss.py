import tkinter as tk
from tkinter import filedialog
import openpyxl
import pandas as pd
from sqlalchemy import create_engine
import re
from datetime import datetime

class YourClass:
    def __init__(self):
        self.selected_option = "1"

    def filename(self, filename):
        # 파일명에서 "YYYYMMDD" 형식의 날짜를 추출
        match = re.search(r'(\d{8})', filename)
        if match:
            date_str = match.group()
            return str(date_str)  # 연도를 문자열로 변환
        else:
            return None

    def extract_year_from_filename(self, filename):
        # 파일명에서 "YYYYMMDD" 형식의 날짜를 추출
        match = re.search(r'(\d{8})', filename)
        if match:
            date_str = match.group()
            date_obj = datetime.strptime(date_str, "%Y%m%d")
            return str(date_obj.year)  # 연도를 문자열로 변환
        else:
            return None

    def convert_excel_to_database(self, data_ranges):
        # 엑셀 파일 선택
        excel_file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel files", "*.xlsx;*.xls")])

        # 선택된 파일이 없으면 함수 종료
        if not excel_file_path:
            return

        try:
            # 엑셀 파일을 열기
            workbook = openpyxl.load_workbook(excel_file_path, data_only=True)
            sheet = workbook.active

            # 선택된 데이터 범위에 해당하는 열을 추출하여 리스트에 추가
            selected_columns = []
            for data_range in data_ranges:
                for column in sheet[data_range]:
                    column_data = [cell.value for cell in column]
                    selected_columns.append(column_data)

            # 리스트를 DataFrame으로 변환
            df = pd.DataFrame(selected_columns)

            # 파일명에서 전체 날짜 추출filename
            year_filename = self.filename(excel_file_path)
            year_from_filename = self.extract_year_from_filename(excel_file_path)
            if year_from_filename is None:
                raise ValueError("파일명에서 날짜를 추출할 수 없습니다.")

            # self.selected_option이 2인 경우 '_s'를 추가
            if self.selected_option == "2":
                year_from_filename += "_s"

            # 데이터베이스 연결 정보
            db_config = {
                'host': '220.69.222.136',
                'user': 'tester',
                'password': 'moonboat1124',
                'database': year_from_filename  # 연도를 테이블명으로 사용
            }

            # 데이터베이스에 연결
            engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")

            # DataFrame을 데이터베이스에 삽입, 테이블명을 동적으로 생성
            df.to_sql(name=year_filename, con=engine, if_exists='replace', index=False)

            print(f"Conversion completed. Data saved to the table '{year_filename}'.")

        except Exception as e:
            print(f"오류 발생: {e}")

# Tkinter 창 생성
root = tk.Tk()
root.withdraw()  # 창이 표시되지 않도록 설정

# 클래스 인스턴스 생성
your_instance = YourClass()

# 데이터 범위 설정
data_ranges = [
    'A4:I16', 'J5:R16', 'S5:AA16', 'AB5:AJ16', 'AK5:AS16', 'AT5:BB16',
    'BC5:BK16', 'BL5:BT16', 'BU5:CC16', 'CD5:CL16', 'CM5:CU16', 'CV5:DD16',
    'DE5:DM16', 'DN5:DV16', 'DW5:EE16', 'EF5:EN16', 'EO5:EW16', 'EX5:FF16',
    'FG5:FO16', 'FP5:FX16', 'FY5:GG16', 'GH5:GP16', 'GQ5:GY16', 'GZ5:HH16',
    'HI5:HQ16', 'HR5:HZ16', 'IA5:II16', 'IJ5:IR16', 'IS5:JA16', 'JB5:JJ16',
    'JK5:JS16', 'JT5:KB16'
]

# 함수 호출
your_instance.convert_excel_to_database(data_ranges)
