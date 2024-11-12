import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# ANN 모델 정의
ann_model = Sequential()

# 입력층과 은닉층 1 (ReLU 활성화 함수 사용)
ann_model.add(Dense(64, input_dim=X_train_scaled.shape[1], activation='relu'))

# 은닉층 2
ann_model.add(Dense(32, activation='relu'))

# 출력층 (sigmoid 활성화 함수 사용, 이진 분류이므로 1 출력)
ann_model.add(Dense(1, activation='sigmoid'))

# 모델 컴파일
ann_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 모델 학습
ann_model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, validation_split=0.2)

# 테스트 데이터로 예측
y_pred_ann = (ann_model.predict(X_test_scaled) > 0.5).astype(int)

# 성능 평가
print("ANN Accuracy:", accuracy_score(y_test, y_pred_ann))
print(classification_report(y_test, y_pred_ann))
