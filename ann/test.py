import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
import glob

# 1. 여러 CSV 파일 읽기 및 통합
file_path_pattern = 'C:/Users/moonboat/Desktop/24년작업/9월/수심측정값_차트데이터/2024_07_15(개목선착장근처)/*.csv'
all_files = glob.glob(file_path_pattern)

if not all_files:
    raise FileNotFoundError("해당 경로에 CSV 파일이 존재하지 않습니다.")

df_list = []
for file in all_files:
    df = pd.read_csv(file, encoding='ANSI')
    df_list.append(df)

# 모든 데이터프레임을 하나로 통합
if not df_list:
    raise ValueError("통합할 데이터프레임이 없습니다.")
full_df = pd.concat(df_list, ignore_index=True)

# 2. 필요한 칼럼만 추출
needed_columns = [
    '날짜 시간',
    '온도 (°C) (957959)', 
    '염도 (PSU) (1041604)', 
    'pH (pH) (926722)', 
    '총 용존 고형물 (TDS) (ppt) (1041604)', 
    'ORP (mV) (926722)'
]
filtered_df = full_df[needed_columns]

# 날짜 시간 형식 변환 (한국어 형식 처리)
def convert_to_datetime(date_str):
    try:
        return pd.to_datetime(date_str, format='%Y-%m-%d %p %I:%M:%S')
    except ValueError:
        return pd.NaT  # 변환 실패 시 NaT 반환

# '날짜 시간' 열에 적용
filtered_df['날짜 시간'] = filtered_df['날짜 시간'].apply(convert_to_datetime)

# 결측치 제거
filtered_df = filtered_df.dropna()

# 데이터 확인
print("결측치 제거 후 데이터프레임의 크기:", filtered_df.shape)  # 데이터프레임의 크기 출력
print("결과 데이터프레임:\n", filtered_df.head())  # 데이터프레임의 처음 몇 줄 출력

# 3. 라벨링
def label_algae_bloom(row):
    if (row['온도 (°C) (957959)'] == 24 and 
        row['염도 (PSU) (1041604)'] == 0 and 
        row['pH (pH) (926722)'] >= 8 and 
        row['총 용존 고형물 (TDS) (ppt) (1041604)'] >= 3.516361E-05 and 
        row['ORP (mV) (926722)'] >= 120.02256):
        return 1  # 녹조 발생
    else:
        return 0  # 녹조 미발생

# 라벨 추가
filtered_df['녹조 발생'] = filtered_df.apply(label_algae_bloom, axis=1)

# 피처와 라벨 분리
X = filtered_df[['온도 (°C) (957959)', '염도 (PSU) (1041604)', 'pH (pH) (926722)', '총 용존 고형물 (TDS) (ppt) (1041604)', 'ORP (mV) (926722)']]
y = filtered_df['녹조 발생']

# 데이터 확인
print("X 데이터프레임 크기:", X.shape)  # X 데이터프레임의 크기 출력
print("y 데이터프레임 크기:", y.shape)  # y 데이터프레임의 크기 출력

# 데이터 정규화
if X.shape[0] > 0:  # X가 비어있지 않을 때만 정규화 진행
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
else:
    raise ValueError("X 데이터가 비어 있습니다. 결측치를 제거한 후에도 데이터가 없습니다.")

# 데이터 시퀀스 생성 (LSTM 입력 형식으로 변환)
def create_dataset(data, labels, time_step=1):
    Xs, ys = [], []
    for i in range(len(data) - time_step):
        Xs.append(data[i:(i + time_step)])
        ys.append(labels[i + time_step])
    return np.array(Xs), np.array(ys)

# 시퀀스 길이 설정
time_step = 5  # 과거 5개 측정값 사용
X_seq, y_seq = create_dataset(X_scaled, y.values, time_step)

# 데이터 분할 (훈련 세트와 테스트 세트)
X_train, X_test, y_train, y_test = train_test_split(X_seq, y_seq, test_size=0.2, random_state=42)

# 5. LSTM 모델 구성
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(50, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))  # 이진 분류

# 모델 컴파일
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 6. 모델 학습
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

# 7. 예측
y_pred = (model.predict(X_test) > 0.5).astype("int32")

# 8. 결과 평가
from sklearn.metrics import classification_report, confusion_matrix

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# 9. 원본 데이터와 예측 결과 시각화
# 예측된 데이터 생성
future_steps = 10  # 예측할 미래 단계 수
predictions = []

# 마지막 데이터 포인트부터 future_steps 만큼 예측
last_data = X_scaled[-time_step:].reshape(1, time_step, -1)

for _ in range(future_steps):
    pred = model.predict(last_data)
    predictions.append(pred[0][0])
    
    # 다음 예측을 위한 데이터 준비
    next_input = np.zeros((1, time_step, last_data.shape[2]))  # 새로운 입력 배열 초기화
    next_input[:, :-1, :] = last_data[:, 1:, :]  # 이전 데이터를 채움
    next_input[:, -1, :] = pred  # 마지막 타임스텝에 예측값 삽입
    last_data = next_input  # last_data를 업데이트

# 예측된 데이터의 원본 스케일로 변환
predictions = np.array(predictions).flatten()

# 날짜 생성
last_date = pd.to_datetime(filtered_df['날짜 시간'].iloc[-1])
predicted_dates = pd.date_range(start=last_date + pd.Timedelta(minutes=5), periods=future_steps, freq='5T')

# 결과 데이터프레임 생성
predicted_df = pd.DataFrame({
    '날짜 시간': predicted_dates,
    '예측된 녹조 발생': predictions
})

# 기존 데이터와 예측 데이터 병합
result_df = pd.concat([filtered_df[['날짜 시간', '녹조 발생']], predicted_df], ignore_index=True)

# 그래프 시각화
plt.figure(figsize=(14, 7))
plt.plot(result_df['날짜 시간'], result_df['녹조 발생'], label='실제 녹조 발생', color='blue')
plt.plot(predicted_df['날짜 시간'], predicted_df['예측된 녹조 발생'], label='예측된 녹조 발생', color='orange', linestyle='--')
plt.xlabel('날짜 시간')
plt.ylabel('녹조 발생')
plt.title('녹조 발생 예측')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# 결과 데이터프레임을 CSV로 저장
result_df.to_csv('labeled_and_predicted_data_lstm_with_graph.csv', index=False, encoding='utf-8-sig')
