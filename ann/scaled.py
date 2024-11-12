import pandas as pd
import glob

# CSV 파일 경로 (예: 현재 디렉토리의 모든 CSV 파일)
file_path = 'C:/Users/moonboat/Desktop/24년작업/9월/수심측정값_차트데이터/2024_07_15(개목선착장근처)/*.csv'  # 경로를 실제 CSV 파일이 있는 경로로 바꿔주세요.

# 결과를 저장할 빈 데이터프레임 생성
all_data = pd.DataFrame()

# 모든 CSV 파일을 읽어들임
for filename in glob.glob(file_path):
    # ANSI 인코딩으로 CSV 파일 읽기
    df = pd.read_csv(filename, encoding='cp1252')  # 또는 encoding='latin1'
    
    # 열 이름의 앞뒤 공백 제거
    df.columns = df.columns.str.strip()
    
    # 각 CSV 파일의 열 이름 출력 (디버깅용)
    print(f"파일: {filename}, 열 이름: {df.columns.tolist()}")

    # 필요한 칼럼만 선택 (올바른 칼럼 이름으로 수정)
    selected_columns = df[['날짜 시간', '온도 (°C) (958671)', '염도 (PSU) (1041604)', 'pH (pH) (926722)', '총 용존 고형물 (TDS) (ppt) (1041604)', 'ORP (mV) (926722)']]
    
    # 선택한 데이터프레임을 모두 합침
    all_data = pd.concat([all_data, selected_columns], ignore_index=True)

# '날짜 시간'을 기준으로 오름차순 정렬
all_data['날짜 시간'] = pd.to_datetime(all_data['날짜 시간'], format='%p %I:%M:%S')  # 날짜 시간 형식 변환
all_data = all_data.sort_values(by='날짜 시간').reset_index(drop=True)

# 결과를 새로운 CSV 파일로 저장
all_data.to_csv('결과파일.csv', index=False, encoding='cp1252')  # 또는 encoding='latin1'
