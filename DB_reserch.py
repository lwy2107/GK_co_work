import mysql.connector
import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("데이터 조회 프로그램")

        # 년도 입력
        self.year_label = ttk.Label(root, text="년도:")
        self.year_label.grid(row=0, column=0, padx=5, pady=5)
        self.year_entry = ttk.Entry(root)
        self.year_entry.grid(row=0, column=0, padx=5, pady=5)

        # 월 선택
        self.month_label = ttk.Label(root, text="월:")
        self.month_label.grid(row=0, column=2, padx=5, pady=5)
        self.month_combobox = ttk.Combobox(root, values=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
        self.month_combobox.grid(row=0, column=2, padx=5, pady=5)

        # 옵션 선택
        self.option_label = ttk.Label(root, text="옵션:")
        self.option_label.grid(row=0, column=4, padx=5, pady=5)
        self.option_combobox = ttk.Combobox(root, values=["1", "2"])
        self.option_combobox.grid(row=0, column=4, padx=5, pady=5)
        self.option_combobox.set("1")  # 초기값 설정

        # 검색어 입력
        self.search_label = ttk.Label(root, text="검색어:")
        self.search_label.grid(row=0, column=6, padx=5, pady=5)
        self.search_entry = ttk.Entry(root)
        self.search_entry.grid(row=0, column=6, padx=5, pady=5)

        # 조회 버튼
        self.submit_button = ttk.Button(root, text="조회", command=self.fetch_and_display_data)
        self.submit_button.grid(row=0, column=8, padx=5, pady=5)

        # 데이터 표시를 위한 Treeview
        self.tree = ttk.Treeview(root)

        # 초기화할 때는 1번 옵션을 선택한 것처럼 설정
        self.selected_option = "1"
        self.configure_tree_columns()

        # 열의 너비 설정
        self.tree.column("#0", width=0, anchor="center")
        for col in self.tree["columns"]:
            self.tree.column(col, width=80, anchor="center")

        # Treeview 스크롤바 추가
        self.tree_scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree_scrollbar.grid(row=1, column=9, sticky="ns")
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)

        # Treeview 표시
        self.tree.grid(row=1, column=0, columnspan=9, padx=5, pady=5)

    def configure_tree_columns(self):
        if self.selected_option == "1":
            columns = ("테이블명", "회차", "출항시간", "입항시간", "연락처", "지역", "인원", "비고")
        elif self.selected_option == "2":
            columns = ("테이블명", "회차", "출항시간", "입항시간", "연락처", "지역", "대인", "소인", "승선인원", "비고")

        self.tree["columns"] = columns

        # 각 열의 제목 설정
        for col in columns:
            self.tree.heading(col, text=col)



    def fetch_and_display_data(self):
        year = self.year_entry.get()
        month = self.month_combobox.get()
        search_keyword = self.search_entry.get()
        self.selected_option = self.option_combobox.get()

        # 테이블명 일부 입력 시, '09'를 '202309'로 처리
        table_prefix = f"{year}{month}"

        # MySQL 연결 설정
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'dnjsdud2',
            'database': f"{year}_s" if self.selected_option == "2" else str(year)
        }

        # 연결 생성
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        try:
            # 선택한 월의 모든 테이블을 조회하는 쿼리 생성
            tables_query = f"SHOW TABLES LIKE '{table_prefix}%'"
            cursor.execute(tables_query)

            # 조회된 테이블 목록을 가져오기
            tables = cursor.fetchall()

            # Treeview 초기화
            for item in self.tree.get_children():
                self.tree.delete(item)

            # 각 테이블의 열 수를 일치시키기 위해 첫 번째 테이블의 열 정보를 가져옴
            first_table_name = tables[0][0]
            column_query = f"DESCRIBE `{first_table_name}`"
            cursor.execute(column_query)
            columns = cursor.fetchall()
            column_names = [column[0] for column in columns]

            # 선택한 열들을 조회하는 쿼리 생성
            if self.selected_option == "1":
                select_query = ", ".join([f"`{col}`" for col in ("회차", "출항시간", "입항시간", "연락처", "지역", "인원", "비고")])
            elif self.selected_option == "2":
                select_query = ", ".join([f"`{col}`" for col in ( "회차", "출항시간", "입항시간", "연락처", "지역", "대인", "소인", "승선인원", "비고")])

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

            # 열의 너비 다시 설정
            self.configure_tree_columns()

        except mysql.connector.Error as err:
            print(f"에러: {err}")

        finally:
            # 연결 종료
            connection.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
