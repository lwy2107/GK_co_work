import mysql.connector
import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd  

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("데이터 조회 프로그램")

        # 년도 선택 콤보박스
        self.year_label = ttk.Label(root, text="년도:",width=4)
        self.year_label.grid(row=0, column=0, padx=0, pady=0)
        self.year_combobox = ttk.Combobox(root, values=["2021", "2022", "2023"], width=5)
        self.year_combobox.grid(row=0, column=1, padx=0, pady=0)
        self.year_combobox.set("2021")  # 초기값 설정
        
                # 출력 버튼
        self.export_button = ttk.Button(root, text="출력", command=self.export_to_excel, width=5)
        self.export_button.grid(row=0, column=12, padx=0, pady=0)

        # 옵션 선택
        self.option_label = ttk.Label(root, text="옵션:",width=5)
        self.option_label.grid(row=0, column=3, padx=0, pady=0)
        self.option_combobox = ttk.Combobox(root, values=["1", "2"], width=2)
        self.option_combobox.grid(row=0, column=4, padx=0, pady=0)
        self.option_combobox.set("1")  # 초기값 설정

        # 검색어 입력
        self.search_label = ttk.Label(root, text="검색어:",width=5)
        self.search_label.grid(row=0, column=5, padx=0, pady=0)
        self.search_entry = ttk.Entry(root, width=5)
        self.search_entry.grid(row=0, column=6, padx=0, pady=0)

        # 조회 버튼
        self.submit_button = ttk.Button(root, text="조회", command=self.fetch_and_display_data, width=5)
        self.submit_button.grid(row=0, column=7, padx=0, pady=0)

        self.start_month_label = ttk.Label(root, text="시작 월:",width=6)
        self.start_month_label.grid(row=0, column=8, padx=0, pady=0)
        self.start_month_combobox = ttk.Combobox(root, values=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], width=2)
        self.start_month_combobox.grid(row=0, column=9, padx=0, pady=0)
        self.start_month_combobox.set("01")  # 초기값 설정

        # 끝 월 선택 콤보박스
        self.end_month_label = ttk.Label(root, text="끝 월:",width=5)
        self.end_month_label.grid(row=0, column=10, padx=0, pady=0)
        self.end_month_combobox = ttk.Combobox(root, values=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], width=2)
        self.end_month_combobox.grid(row=0, column=11, padx=0, pady=0)
        self.end_month_combobox.set("03")  # 초기값 설정

        self.tree = ttk.Treeview(root, show="headings")  # height 제거하여 동적으로 크기 조절
        self.tree.grid(row=1, column=0, columnspan=9, padx=0, pady=0, sticky="nsew")

        self.tree_scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree_scrollbar.grid(row=1, column=9, sticky="nsew")
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)
        self.tree_scrollbar.grid(row=1, column=10, sticky="ns") 

        # 옵션 콤보박스 값 변경 이벤트에 메서드 바인딩
        self.option_combobox.bind("<<ComboboxSelected>>", self.update_columns)

        # 창 크기 변경 시 Treeview 크기 조정
        self.root.bind("<Configure>", self.on_window_resize)

    def on_window_resize(self, event):
        # 창 크기가 변경될 때 Treeview의 높이를 동적으로 조절
        self.tree.configure(height=20)
    def update_columns(self, event):
        # 옵션 콤보박스 값이 변경될 때마다 열을 업데이트
        self.selected_option = self.option_combobox.get()
        self.configure_tree_columns()
        for item in self.tree.get_children():
            self.tree.delete(item)
    def configure_tree_columns(self):
        
        if self.selected_option == "1":
            columns = ("테이블명", "회차", "출항시간", "입항시간", "연락처", "인원")
        elif self.selected_option == "2":
            columns = ("테이블명", "회차", "출항시간", "입항시간", "연락처", "지역", "합계")

        self.tree["columns"] = columns

        for i, col in enumerate(columns):
            self.tree.heading(col, text=col)
            if i == len(columns) - 1:
                # 마지막 열의 너비를 충분히 줄임
                self.tree.column(col, width=100, anchor="center", stretch=False)
            else:
                self.tree.column(col, width=100, anchor="center", stretch=False)


    def fetch_and_display_data(self):
        year = self.year_combobox.get()
        start_month = self.start_month_combobox.get()
        end_month = self.end_month_combobox.get()
        search_keyword = self.search_entry.get()
        self.selected_option = self.option_combobox.get()
        
        # 테이블명 범위 입력 시, '09'를 '202309'로 처리
        table_start_prefix = f"{year}{start_month}"
        table_end_prefix = f"{year}{end_month}"

        # MySQL 연결 설정
        db_config = {
            'host': '220.69.222.136',
            'user': 'tester',
            'password': 'moonboat1124',
            'database': f"{year}_s" if self.selected_option == "2" else str(year)
        }

        try:
            # 연결 생성
            with mysql.connector.connect(**db_config) as connection:
                cursor = connection.cursor()

                # 선택한 월 범위의 테이블 조회 쿼리 생성
                tables_query = f"""
                    SELECT TABLE_NAME
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_SCHEMA = '{db_config['database']}'
                    AND TABLE_NAME BETWEEN '{table_start_prefix}01' AND '{table_end_prefix}31'
                """
                cursor.execute(tables_query)
                tables = cursor.fetchall()

                # Treeview 초기화
                for item in self.tree.get_children():
                    self.tree.delete(item)

                # 테이블이 하나도 없으면 메시지 표시 후 종료
                if not tables:
                    print(f"No tables found with prefix: {table_start_prefix} or {table_end_prefix}")
                    return

                # 각 테이블의 열 수를 일치시키기 위해 첫 번째 테이블의 열 정보를 가져옴
                first_table_name = tables[0][0]
                column_query = f"DESCRIBE `{first_table_name}`"
                cursor.execute(column_query)
                columns = cursor.fetchall()
                column_names = [column[0] for column in columns]

                # 선택한 열들을 조회하는 쿼리 생성
                if self.selected_option == "1":
                    existing_columns = ["회차", "출항시간", "입항시간", "연락처","인원"]
                    select_query = ", ".join([f"`{col}`" if col in column_names else "''" for col in existing_columns])

                elif self.selected_option == "2":
                    existing_columns = ["회차", "출항시간", "입항시간", "연락처", "지역", "합계"]
                    select_query = ", ".join([f"`{col}`" if col in column_names else "''" for col in existing_columns])


                # 테이블별로 데이터 Treeview에 추가
                for table in tables:
                    table_name = table[0]
                    union_query = f"SELECT '{table_name}' AS 'Table', {select_query} FROM `{table_name}`"
                    cursor.execute(union_query)
                    table_data = cursor.fetchall()

                    # 검색어에 해당하는 데이터만 Treeview에 추가
                    for row in table_data:
                        if search_keyword.lower() in str(row).lower():
                            self.tree.insert("", "end", values=row)

        except mysql.connector.Error as err:
            print(f"에러: {err}")

    def export_to_excel(self):
        # 트리뷰의 열 이름 가져오기
        columns = self.tree['columns']
        column_names = [self.tree.heading(col)['text'] for col in columns]

        # 트리뷰의 내용을 DataFrame으로 변환
        data = []
        for row_id in self.tree.get_children():
            row_data = [self.tree.set(row_id, col) for col in columns]
            data.append(row_data)

        df = pd.DataFrame(data, columns=column_names)

        # 엑셀 파일로 내보내기
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                print(f"엑셀 파일이 저장되었습니다: {file_path}")
            except Exception as e:
                print(f"엑셀 파일을 저장하는 중 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()