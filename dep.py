import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import EarlyStopping

# Step 1: CSV 파일 로드
file_path = 'C:/Users/moonboat/total.csv'  # 실제 파일 경로로 변경하세요
df = pd.read_csv(file_path, encoding='cp949')

# Step 2: 데이터 전처리
df['날짜 시간'] = pd.to_datetime(df['날짜 시간'])
df.set_index('날짜 시간', inplace=True)
df = df.dropna()

# 필요한 컬럼 선택
features = ['온도 (°C) (957959)', 'pH (pH) (926722)', 'ORP (mV) (926722)', '총 용존 고형물 (TDS) (ppt) (1041604)']
data = df[features]

# Step 3: 데이터 정규화
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

# Step 4: 시퀀스 데이터 생성
def create_dataset(data, time_step=1):
    X, y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i:(i + time_step), :])
        y.append(data[i + time_step, :])
    return np.array(X), np.array(y)

time_step = 10  # 시퀀스 길이
X, y = create_dataset(data_scaled, time_step)

# Step 5: 데이터 분할
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Step 6: LSTM 모델 구축
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(50, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(len(features)))

model.compile(optimizer='adam', loss='mean_squared_error')

# Step 7: 모델 학습
early_stopping = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
model.fit(X_train, y_train, epochs=100, batch_size=32, callbacks=[early_stopping])

# Step 8: 예측
y_pred = model.predict(X_test)

# Step 9: 스케일 역변환
y_pred_inv = scaler.inverse_transform(y_pred)
y_test_inv = scaler.inverse_transform(y_test)

# Step 10: 그래프 그리기
plt.figure(figsize=(14, 7))

# 실제 값
plt.plot(df.index[-len(y_test):], y_test_inv[:, 0], label='Actual Temperature', color='blue')
plt.plot(df.index[-len(y_test):], y_test_inv[:, 1], label='Actual pH', color='green')
plt.plot(df.index[-len(y_test):], y_test_inv[:, 2], label='Actual ORP', color='purple')
plt.plot(df.index[-len(y_test):], y_test_inv[:, 3], label='Actual TDS', color='cyan')

# 예측 값 (단일 그래프에 두 번 나오지 않도록 수정)
plt.plot(df.index[-len(y_pred):], y_pred_inv[:, 0], label='Predicted Temperature', color='red', linestyle='--')
plt.plot(df.index[-len(y_pred):], y_pred_inv[:, 1], label='Predicted pH', color='orange', linestyle='--')
plt.plot(df.index[-len(y_pred):], y_pred_inv[:, 2], label='Predicted ORP', color='magenta', linestyle='--')
plt.plot(df.index[-len(y_pred):], y_pred_inv[:, 3], label='Predicted TDS', color='yellow', linestyle='--')

plt.xlabel('날짜 시간')
plt.ylabel('수질 측정 값')
plt.title('LSTM을 이용한 수질 예측')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
