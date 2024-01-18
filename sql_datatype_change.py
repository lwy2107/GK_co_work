import mysql.connector

# 데이터베이스 연결 정보 설정
database_config = {
    'user': 'root',
    'password': 'dnjsdud2',
    'host': 'localhost',
    'database': '2021_s'
}

# MySQL 연결
conn = mysql.connector.connect(**database_config)
cursor = conn.cursor()

try:
    # 특정 데이터베이스의 모든 테이블 리스트 가져오기
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    # 특정 칼럼의 데이터형 변경
    for table in tables:
        table_name = table[0]
        print(f"테이블 수정 중: {table_name}")
        cursor.execute(f"ALTER TABLE `{table_name}` MODIFY COLUMN `회차` bigint")
        cursor.execute(f"ALTER TABLE `{table_name}` MODIFY COLUMN `요일` varchar(255)")
        cursor.execute(f"ALTER TABLE `{table_name}` MODIFY COLUMN `출항시간` time")
        cursor.execute(f"ALTER TABLE `{table_name}` MODIFY COLUMN `입항시간` time")
        cursor.execute(f"ALTER TABLE `{table_name}` MODIFY COLUMN `연락처` varchar(255)")
        cursor.execute(f"ALTER TABLE `{table_name}` MODIFY COLUMN `지역` varchar(255)")
        cursor.execute(f"ALTER TABLE `{table_name}` MODIFY COLUMN `온도` double")
        cursor.execute(f"ALTER TABLE `{table_name}` MODIFY COLUMN `대인` bigint")
        cursor.execute(f"ALTER TABLE `{table_name}` MODIFY COLUMN `소인` bigint")
        cursor.execute(f"ALTER TABLE `{table_name}` MODIFY COLUMN `소계` bigint")
        cursor.execute(f"ALTER TABLE `{table_name}` MODIFY COLUMN `합계` bigint")
        cursor.execute(f"ALTER TABLE `{table_name}` MODIFY COLUMN `승선인원` bigint")
        cursor.execute(f"ALTER TABLE `{table_name}` MODIFY COLUMN `비고` varchar(255)")

    # 변경사항 커밋
    conn.commit()

except Exception as e:
    print(f"에러: {e}")

finally:
    # 연결 종료
    cursor.close()
    conn.close()
