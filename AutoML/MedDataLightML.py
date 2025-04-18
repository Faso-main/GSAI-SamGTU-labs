import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
from  medica_data import *



test_patient_1 = [0.15, 0.20, 0.52, 0.26, 0.33, 0.40, 0.29, 0.37]
test_patient_2 = [0.60, 0.82, 0.70, 0.51, 0.66, 0.55, 0.58, 0.62]

# Подготовка данных
X = np.array(medical_data_extended_1)
y = np.array(labels_extended_1).flatten()

# Разделение данных на обучающую и тестовую выборки (для оценки модели)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание и обучение модели LightGBM
lgbm = lgb.LGBMClassifier(random_state=42)
lgbm.fit(X_train, y_train)

# Прогнозирование на тестовых данных
y_pred = lgbm.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Точность модели LightGBM на тестовых данных: {accuracy:.2f}")

# Прогнозирование для тестового пациента
test_patient = np.array([test_patient_1])
probability_diabetes = lgbm.predict_proba(test_patient)[:, 1][0]
predicted_class = lgbm.predict(test_patient)[0]

print(f"\nВероятность диабета у тестового пациента (LightGBM): {probability_diabetes*100:.2f}%")
print(f"Диагноз (LightGBM): {'Диабет' if predicted_class == 1 else 'Нет диабета'}")