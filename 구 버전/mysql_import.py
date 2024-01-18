import os
import pandas as pd
from sqlalchemy import create_engine

def csv_to_mysql(csv_file, table_name, db_engine):
    # CSV 파일을 DataFrame으로 읽기
    df = pd.read_csv(csv_file, encoding='ANSI')

    # MySQL 테이블에 DataFrame 쓰기
    df.to_sql(table_name, con=db_engine, index=False, if_exists='replace')

def process_folder(folder_path, db_engine):
    # 폴더 내의 모든 CSV 파일에 대한 처리
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith(".csv"):
            table_name = os.path.splitext(filename)[0]
            csv_to_mysql(file_path, table_name, db_engine)
            print(f"Table '{table_name}' created and data inserted.")

if __name__ == "__main__":
    # MySQL 연결 정보 설정
    db_url = "mysql+mysqlconnector://root:dnjsdud2@localhost:3306/2022_s"
    engine = create_engine(db_url)

    # 폴더 경로 설정
    folder_path = "C:\\Users\\moonboat\\Desktop\\새 폴더 (2)\\11월"

    # CSV 파일을 MySQL에 넣는 함수 호출
    process_folder(folder_path, engine)
