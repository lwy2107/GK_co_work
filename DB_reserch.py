import mysql.connector
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd  
from datetime import datetime as dt, timedelta
import datetime

class App:
    def __init__(self, root):
        self.db_config = {
            'host': '220.69.222.136',
            'user': 'tester',
            'password': 'moonboat1124',
            'database': '',  # Leave it empty for now
        }

        self.selected_data_id = None
        self.selected_data_num = None
        self.column_value = None
        self.auto_fill_var = tk.BooleanVar(value=True)  # Variable to track the checkbox state

        self.root = root
        self.root.title("데이터 조회 프로그램")

        self.insert_button = ttk.Button(root, text="추가", command=self.open_insert_window, width=5)
        self.insert_button.grid(row=0, column=13, padx=0, pady=0)

        # 년도 선택 콤보박스
        self.year_label = ttk.Label(root, text="년도:",width=4)
        self.year_label.grid(row=0, column=0, padx=0, pady=0)
        self.year_combobox = ttk.Combobox(root, values=["2021", "2022", "2023", "2024"], width=5)
        self.year_combobox.grid(row=0, column=1, padx=0, pady=0)
        self.year_combobox.set(str(datetime.datetime.now().year))  # Set to the current year
        
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
        self.search_label = ttk.Label(root, text="검색어:", width=5)
        self.search_label.grid(row=0, column=5, padx=0, pady=0)
        self.search_entry = ttk.Entry(root, width=5)
        self.search_entry.grid(row=0, column=6, padx=0, pady=0)
        self.search_entry.insert(0, datetime.datetime.now().strftime("%m%d"))  # Set to the current date

        # 조회 버튼
        self.submit_button = ttk.Button(root, text="조회", command=self.fetch_and_display_data, width=5)
        self.submit_button.grid(row=0, column=7, padx=0, pady=0)

        # 시작 월 선택 콤보박스
        self.start_month_label = ttk.Label(root, text="시작 월:", width=6)
        self.start_month_label.grid(row=0, column=8, padx=0, pady=0)
        self.start_month_combobox = ttk.Combobox(root, values=[str(i).zfill(2) for i in range(1, 13)], width=2)
        self.start_month_combobox.grid(row=0, column=9, padx=0, pady=0)
        self.start_month_combobox.set(str(datetime.datetime.now().month).zfill(2))  # Set to the current month

        # 끝 월 선택 콤보박스
        self.end_month_label = ttk.Label(root, text="끝 월:", width=5)
        self.end_month_label.grid(row=0, column=10, padx=0, pady=0)
        self.end_month_combobox = ttk.Combobox(root, values=[str(i).zfill(2) for i in range(1, 13)], width=2)
        self.end_month_combobox.grid(row=0, column=11, padx=0, pady=0)
        self.end_month_combobox.set(str(datetime.datetime.now().month).zfill(2))  # Set to the current month


        self.tree = ttk.Treeview(root, show="headings")  # height 제거하여 동적으로 크기 조절
        self.tree.grid(row=1, column=0, columnspan=9, padx=0, pady=0, sticky="nsew")

        self.tree_scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree_scrollbar.grid(row=1, column=9, sticky="nsew")
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)
        self.tree_scrollbar.grid(row=1, column=10, sticky="ns") 

        # 옵션 콤보박스 값 변경 이벤트에 메서드 바인딩
        self.option_combobox.bind("<<ComboboxSelected>>", self.update_columns)

        
        self.delete_button = ttk.Button(root, text="삭제", command=self.delete_data, width=5)
        self.delete_button.grid(row=0, column=14, padx=0, pady=0)

        # 더블 클릭 이벤트에 메서드 바인딩
        self.tree.bind("<Double-1>", self.edit_data)

        # 창 크기 변경 시 Treeview 크기 조정
        self.root.bind("<Configure>", self.on_window_resize)
        self.departure_button = ttk.Button(root, text="출항체크", command=self.check_departure, width=7)
        self.departure_button.grid(row=0, column=15, padx=5, pady=5)

    def check_departure(self):
        item = self.tree.selection()
        if item:
            # 옵션과 연도에 기반하여 선택된 데이터베이스 설정
            self.set_selected_database()

            # 트리뷰에서 선택된 데이터 가져오기
            selected_data = self.tree.item(item, "values")

            # "출항여부" 열을 True로 업데이트
            try:
                with mysql.connector.connect(**self.db_config) as connection:
                    cursor = connection.cursor()

                    # 트리뷰의 첫 번째 열이 테이블 이름이라고 가정
                    table_name = selected_data[0]

                    # 테이블 구조에 따라 UPDATE 쿼리 조정
                    update_query = f"UPDATE `{table_name}` SET 출항여부 = TRUE WHERE `회차` = %s"
                    cursor.execute(update_query, (selected_data[1],))  # '회차'가 두 번째 열이라고 가정

                    connection.commit()
                    cursor.close()
                    print(f"출항여부가 True로 업데이트되었습니다. '회차' {selected_data[1]}, 테이블 {table_name}.")

                    # 변경 사항을 반영하기 위해 트리뷰를 새로고침
                    self.fetch_and_display_data()

            except mysql.connector.Error as err:
                print(f"출항여부 업데이트 오류: {err}")

    def configure_tree_columns(self):
        if self.selected_option == "1":
            columns = ("테이블명", "회차", "출항시간", "입항시간", "연락처", "지역", "인원", "비고",  "요일","출항여부",)  # "요일" 열 추가
        elif self.selected_option == "2":
            columns = ("테이블명", "회차", "출항시간", "입항시간", "연락처", "지역", "대인", "소인", "요일", "인원", "비고", "출항여부")  # "요일" 열 추가

        self.tree["columns"] = columns

        for i, col in enumerate(columns):
            self.tree.heading(col, text=col)
            if i == len(columns) - 1:
                self.tree.column(col, width=100, anchor="center", stretch=False)
            else:
                self.tree.column(col, width=100, anchor="center", stretch=False)

    def on_window_resize(self, event):
        # 창 크기가 변경될 때 Treeview의 높이를 동적으로 조절
        self.tree.configure(height=20)
    def update_columns(self, event):
        # 옵션 콤보박스 값이 변경될 때마다 열을 업데이트
        self.selected_option = self.option_combobox.get()
        self.configure_tree_columns()
        for item in self.tree.get_children():
            self.tree.delete(item)

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
                    existing_columns = ["회차", "출항시간", "입항시간", "연락처", "지역", "인원", "비고", "출항여부"]
                    select_query = ", ".join([f"`{col}`" if col in column_names else "''" for col in existing_columns])

                elif self.selected_option == "2":
                    existing_columns = ["회차", "출항시간", "입항시간", "연락처", "지역", "대인", "소인", "요일", "소계", "비고", "출항여부"]
                    select_query = ", ".join([f"`{col}`" if col in column_names else "''" for col in existing_columns])

                # 테이블별로 데이터 Treeview에 추가
                for table in tables:
                    table_name = table[0]

                    # 테이블명에서 날짜 정보 추출
                    date_str = table_name[len(year):]  # 테이블명에서 년도 이후의 문자열 추출
                    date_object = dt.strptime(date_str, "%m%d")
                    weekday = date_object.strftime("%A")

                    select_query_with_weekday = f"{select_query}, '{self.get_korean_weekday(weekday)}' AS '요일'"  # 요일을 그대로 사용

                    union_query = f"SELECT '{table_name}' AS 'Table', {select_query_with_weekday} FROM `{table_name}`"
                    cursor.execute(union_query)
                    table_data = cursor.fetchall()

                    # Process and add table data to the Treeview
                    for row in table_data:
                        # Check and handle missing or None values in the "지역" column
                        if self.selected_option == "2" and (row[5] is None or row[5] == ''):
                            row = list(row)
                            row[5] = "No Data Available"  # Replace empty or None values with a placeholder
                            row = tuple(row)

                        # Check if the search keyword matches any row data
                        if search_keyword.lower() in str(row).lower():
                            self.tree.insert("", "end", values=row)
        except mysql.connector.Error as err:
            print(f"에러: {err}")

    def get_korean_weekday(self, weekday):
        # 요일을 한글로 변환하는 함수
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        korean_weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        
        if weekday in weekdays:
            return korean_weekdays[weekdays.index(weekday)]
        else:
            return weekday

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

    def open_insert_window(self):
        self.insert_window = tk.Toplevel(self.root)
        self.insert_window.title("데이터 추가")

        self.create_common_widgets()

        self.auto_fill_checkbox = tk.Checkbutton(self.insert_window, text="자동 입력", variable=self.auto_fill_var, command=self.update_fields)
        self.auto_fill_checkbox.grid(row=8, columnspan=2)

        if self.selected_option == "1":
            self.personnel_label = ttk.Label(self.insert_window, text="인원:")
            self.personnel_label.grid(row=3, column=0)
            self.personnel_entry = ttk.Entry(self.insert_window)
            self.personnel_entry.grid(row=3, column=1)
        elif self.selected_option == "2":
            self.personnel_label = ttk.Label(self.insert_window, text="대인:")
            self.personnel_label.grid(row=3, column=0)
            self.personnel_entry = ttk.Entry(self.insert_window)
            self.personnel_entry.grid(row=3, column=1)

            self.kid_label = ttk.Label(self.insert_window, text="소인:")
            self.kid_label.grid(row=4, column=0)
            self.kid_entry = ttk.Entry(self.insert_window)
            self.kid_entry.grid(row=4, column=1)

        self.confirm_button = ttk.Button(self.insert_window, text="확인", command=self.save_data_and_close)
        self.confirm_button.grid(row=9, columnspan=2)

        # Initialize fields based on auto_fill_var
        self.update_fields()

    def create_common_widgets(self):
        self.date_label = ttk.Label(self.insert_window, text="날짜 (YYYYMMDD):")
        self.date_label.grid(row=0, column=0)
        self.date_entry = ttk.Entry(self.insert_window)
        self.date_entry.grid(row=0, column=1)

        self.time_label = ttk.Label(self.insert_window, text="시간 (HH:MM):")
        self.time_label.grid(row=1, column=0)
        self.time_entry = ttk.Entry(self.insert_window)
        self.time_entry.grid(row=1, column=1)
        self.time_entry.insert(0, "HH:MM")  # Initial placeholder text

        self.location_label = ttk.Label(self.insert_window, text="지역:")
        self.location_label.grid(row=2, column=0)
        self.location_entry = ttk.Entry(self.insert_window)
        self.location_entry.grid(row=2, column=1)

        self.phone_label = ttk.Label(self.insert_window, text="연락처:")
        self.phone_label.grid(row=5, column=0)
        self.phone_entry = ttk.Entry(self.insert_window)
        self.phone_entry.grid(row=5, column=1)

        self.remarks_label = ttk.Label(self.insert_window, text="비고:")
        self.remarks_label.grid(row=6, column=0)
        self.remarks_entry = ttk.Entry(self.insert_window)
        self.remarks_entry.grid(row=6, column=1)

    def update_fields(self):
        # Update date and time fields based on the state of auto_fill_var
        if self.auto_fill_var.get():
            # Auto-fill with current date and time
            now = datetime.datetime.now()
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, now.strftime("%Y%m%d"))
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, now.strftime("%H:%M"))
        else:
            # Clear the entries for manual input
            self.date_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)
    def save_data(self):
        year = self.year_combobox.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        location = self.location_entry.get()
        personnel = self.personnel_entry.get()
        remarks = self.remarks_entry.get()
        self.selected_option = self.option_combobox.get()
        
        # kid 값 설정 (옵션 2에서만 사용되는 값이므로 디폴트는 None)
        kid = self.kid_entry.get() if self.selected_option == "2" else None

        self.db_config = {
            'host': '220.69.222.136',
            'user': 'tester',
            'password': 'moonboat1124',
            'database': f"{year}_s" if self.selected_option == "2" else str(year)
        }

        try:
            with mysql.connector.connect(**self.db_config) as connection:
                cursor = connection.cursor()

                table_name = f"{date}"
                cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
                result = cursor.fetchone()

                if not result:
                    create_table_query = self.get_create_table_query()
                    cursor.execute(create_table_query)

                cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                count = cursor.fetchone()[0]

                arrival_time = (dt.strptime(time, "%H:%M") + timedelta(minutes=30)).strftime("%H:%M")
                insert_query = self.get_insert_query(table_name)

                # 엔트리 위젯에서 값을 가져와서 전달
                phone_value = self.phone_entry.get()
                
                # kid 값이 사용되는 경우에만 해당 값을 가져와서 전달
                kid_value = self.kid_entry.get() if self.selected_option == "2" else None

                insert_values = self.get_insert_values(count, time, arrival_time, personnel, kid_value, location, remarks, phone_value)
                print("INSERT VALUES:", insert_values)
                cursor.execute(insert_query, insert_values)
                connection.commit()
                cursor.close()
                print("데이터가 성공적으로 저장되었습니다!")

        except mysql.connector.Error as err:
            print(f"저장 오류: {err}")

    # App 클래스의 get_create_table_query 메서드 수정
    def get_create_table_query(self):
        table_name = self.date_entry.get()
        if self.selected_option == "1":
            query = f"CREATE TABLE `{table_name}` (회차 INT DEFAULT 0, 출항시간 TIME, 입항시간 TIME, 연락처 VARCHAR(255), 지역 VARCHAR(255), 인원 INT, 비고 VARCHAR(255), 요일 VARCHAR(255), 출항여부 BOOLEAN DEFAULT FALSE)"
        elif self.selected_option == "2":
            query = f"CREATE TABLE `{table_name}` (회차 INT DEFAULT 0, 출항시간 TIME, 입항시간 TIME, 연락처 VARCHAR(255), 지역 VARCHAR(255), 대인 INT, 소인 INT, 요일 VARCHAR(255), 소계 INT, 합계 INT, 승선인원 INT, 비고 VARCHAR(255), 출항여부 BOOLEAN DEFAULT FALSE)"
        
        print("CREATE TABLE QUERY:", query)
        return query


    # App 클래스의 get_insert_query 메서드 수정
    def get_insert_query(self, table_name):
        if self.selected_option == "1":
            return f"INSERT INTO `{table_name}` (출항시간, 입항시간, 회차, 연락처, 지역, 인원, 비고, 요일) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        elif self.selected_option == "2":
            return f"INSERT INTO `{table_name}` (출항시간, 입항시간, 회차, 연락처, 지역, 대인, 소인, 요일, 소계, 합계, 승선인원, 비고) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    # App 클래스의 get_insert_values 메서드 수정
    def get_insert_values(self, count, time, arrival_time, personnel, kid, location, remarks, phone):
        table_name = self.date_entry.get()
        date_object = dt.strptime(self.date_entry.get(), "%Y%m%d")
        weekday = date_object.strftime("%A")
        kid = 0 if kid is None or not kid.isdigit() else int(kid)
        personnel = 0 if not personnel.isdigit() else int(personnel)
        total = kid + personnel

        try:
            with mysql.connector.connect(**self.db_config) as connection:
                cursor = connection.cursor()
                cursor.execute(f"SELECT MAX(회차) FROM `{table_name}`")
                max_count = cursor.fetchone()[0]
                count = max_count + 1 if max_count is not None else 1
        except mysql.connector.Error as err:
            print(f"회차 확인 오류: {err}")
            count = None

        if self.selected_option == "1":
            return (time, arrival_time, count, phone, location, personnel, remarks, self.get_korean_weekday(weekday))
        elif self.selected_option == "2":
            return (time, arrival_time, count, phone, location, personnel, kid, self.get_korean_weekday(weekday), total, total, total, remarks)

        try:
            with mysql.connector.connect(**self.db_config) as connection:
                cursor = connection.cursor()
                cursor.execute(f"SELECT MAX(회차) FROM `{table_name}`")
                max_count = cursor.fetchone()[0]
                count = max_count + 1 if max_count is not None else 1
        except mysql.connector.Error as err:
            print(f"회차 확인 오류: {err}")
            count = None
        if self.selected_option == "1":
            return (time, arrival_time, phone, location, personnel, remarks)
        elif self.selected_option == "2":
            return (time, arrival_time, phone, location, personnel, kid, self.get_korean_weekday(weekday), total, total, total, remarks)

    def get_user_input(self, title, prompt):
        root = tk.Tk()
        root.title(title)

        label = tk.Label(root, text=prompt)
        label.pack(padx=10, pady=10)

        entry = tk.Entry(root)
        entry.pack(padx=10, pady=10)

        def on_confirm():
            new_value = entry.get()
            root.destroy()

            # 데이터베이스 연결 및 업데이트 수행
            self.update_database(new_value)

        confirm_button = tk.Button(root, text="Confirm", command=on_confirm)
        confirm_button.pack(pady=10)

        root.mainloop()

    def save_data_and_close(self):
        # 데이터 저장
        self.save_data()

        # 입력 창 닫기
        self.insert_window.destroy()

    def update_database(self, new_value):
        # 수정 쿼리 실행
        update_query = f"""
            UPDATE `{self.selected_data_id}`
            SET `{self.column_value}` = %s
            WHERE `회차` = {self.selected_data_num}
        """

        try:
            with mysql.connector.connect(**self.db_config) as connection:
                cursor = connection.cursor()

                # 수정할 데이터를 토대로 쿼리 실행
                cursor.execute(update_query, (new_value,))
                connection.commit()

                cursor.close()
                print(f"Data with ID {self.selected_data_num} updated in the database.")

        except mysql.connector.Error as err:
            print(f"Database update error: {err}")

    def set_selected_database(self):
        # Assuming you have a combo box named database_combobox
        self.selected_option = self.option_combobox.get()
        year = self.year_combobox.get()

        if self.selected_option == "2":
            self.db_config['database'] = f"{year}_s"
        else:
            self.db_config['database'] = str(year)

    def edit_data(self, event):
        year = self.year_combobox.get()
        item = self.tree.selection()
        self.set_selected_database()

        if item:
            # 선택된 데이터의 ID와 테이블명을 저장
            self.selected_data_id = self.tree.item(item, "values")[0]
            self.selected_data_num = self.tree.item(item, "values")[1]

            # 더블클릭한 열(column)의 정보를 얻기
            column = self.tree.identify_column(event.x)  # 더블클릭한 열의 정보

            # 열의 정보를 출력
            print(f"Double-clicked column: {column}")

            # 선택된 열(column)의 값에 대한 정보 출력
            self.column_value = self.tree.column(self.tree.identify_column(event.x), 'id')
            print(f"Value of the selected column: {self.column_value}")

            # 수정할 데이터를 받아오기
            self.get_user_input(f"수정 - {self.column_value}", f"{self.column_value} 값을 입력하세요")


    def delete_data(self):
        self.selected_data_id = None
        year = self.year_combobox.get()
        self.db_config = {
            'host': '220.69.222.136',
            'user': 'tester',
            'password': 'moonboat1124',
            'database': f"{year}_s" if self.selected_option == "2" else str(year)
        }
        item = self.tree.selection()
        if item:
            confirm = messagebox.askyesno("삭제 확인", "선택한 데이터를 삭제하시겠습니까?")
            if confirm:
                # Get the selected data from the TreeView
                selected_data = self.tree.item(item, "values")

                # Execute the DELETE query to remove the data from the database
                try:
                    with mysql.connector.connect(**self.db_config) as connection:
                        cursor = connection.cursor()

                        # Assuming the first column in the TreeView is the table name
                        table_name = selected_data[0]

                        # Adjust the DELETE query based on your table structure
                        delete_query = f"DELETE FROM `{table_name}` WHERE `회차` = %s"
                        cursor.execute(delete_query, (selected_data[1],))  # Assuming '회차' is the second column

                        connection.commit()
                        cursor.close()
                        print(f"Data with '회차' {selected_data[1]} deleted from the database in table {table_name}.")

                        # Check if the table is empty after deletion
                        cursor = connection.cursor()
                        cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                        count = cursor.fetchone()[0]

                        # If the table is empty, drop the table
                        if count == 0:
                            drop_query = f"DROP TABLE `{table_name}`"
                            cursor.execute(drop_query)
                            connection.commit()
                            print(f"Table {table_name} dropped since it is empty.")

                except mysql.connector.Error as err:
                    print(f"Database deletion error: {err}")

                # Now, remove the selected item from the TreeView
                self.tree.delete(item)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()