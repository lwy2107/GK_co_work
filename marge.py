import pandas as pd
import glob

file_list = glob.glob("C:/Users/moonboat/클로로필포함측정치/*.csv")
df_all = pd.DataFrame()

for file in file_list:
    try:
        # Open the file with the specified encoding (replace 'ansi' with the actual encoding)
        with open(file, 'r', encoding='ansi') as f:
            df = pd.read_csv(f)
            df = df[['날짜 시간', '온도 (°C) (1068851)', 'pH (pH) (1057024)','ORP (mV) (1057024)','총 용존 고형물 (TDS) (ppt) (1066342)','깊이 (m) (1064654)','RDO 농도 (mg/L) (954526)','RDO 포화 (%Sat) (954526)', '산소분압 (Torr) (954526)', 'Chlorophyll-a Fluorescence (RFU) (945787)', 'Chlorophyll-a 농도 (μg/L) (945787)']]
            df_all = pd.concat([df_all, df], ignore_index=True)
    except Exception as e:
        print(f"파일 {file} 처리 중 오류 발생: {e}")

df_all.to_csv("10-04-포인트1.csv", index=False)