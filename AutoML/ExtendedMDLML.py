import lightgbm as lgb
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from scipy.stats import randint, uniform
import pandas as pd
from medica_data import *

# Тестовые пациенты
test_patient_1 = [0.15, 0.20, 0.52, 0.26, 0.33, 0.40, 0.29, 0.37] # нет диабета
test_patient_2 = [0.60, 0.82, 0.70, 0.51, 0.66, 0.55, 0.58, 0.62] # диабет

# Подготовка данных
X = np.array(medical_data_expended)
y = np.array(labels_expended).flatten()

# Проверка баланса классов (исходного набора данных)
unique_original, counts_original = np.unique(y, return_counts=True)
print("\nРаспределение классов (исходный):", dict(zip(unique_original, counts_original)))

# Нормализация данных
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Разделение данных с сохранением баланса классов
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y)

# Проверка баланса классов в обучающей выборке
unique_train, counts_train = np.unique(y_train, return_counts=True)
print("\nРаспределение классов (обучающая выборка):", dict(zip(unique_train, counts_train)))

# Автоматический подбор количества фолдов для кросс-валидации на основе обучающей выборки
min_samples_train = min(counts_train)
n_splits = min(5, min_samples_train)  # Не больше чем минимальное количество образцов в классе обучающей выборки
print(f"Используется {n_splits}-кратная кросс-валидация")

# Параметры для RandomizedSearch
param_dist = {
    'n_estimators': randint(50, 300),
    'learning_rate': uniform(0.01, 0.3),
    'max_depth': randint(3, 10),
    'num_leaves': randint(20, 100),
    'min_child_samples': randint(10, 50),
    'subsample': uniform(0.6, 0.4),
    'colsample_bytree': uniform(0.6, 0.4),
    'reg_alpha': uniform(0, 1),
    'reg_lambda': uniform(0, 1)
}

# Создание модели с автоматическим подбором параметров
lgbm = lgb.LGBMClassifier(random_state=42, n_jobs=-1)
kfold = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

random_search = RandomizedSearchCV(
    estimator=lgbm,
    param_distributions=param_dist,
    n_iter=min(50, 10*n_splits),  # Адаптивное количество итераций
    cv=kfold,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=1,
    random_state=42
)

print("\nНачало автоматического подбора параметров...")
random_search.fit(X_train, y_train)
print("Подбор параметров завершен!")

# Лучшая модель
best_model = random_search.best_estimator_

# Оценка модели
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        'Accuracy': accuracy_score(y_test, y_pred),
        'Precision': precision_score(y_test, y_pred, zero_division=0),
        'Recall': recall_score(y_test, y_pred, zero_division=0),
        'F1-score': f1_score(y_test, y_pred, zero_division=0),
        'ROC-AUC': roc_auc_score(y_test, y_proba) if len(np.unique(y_test)) > 1 else float('nan'),
        'Best params': random_search.best_params_
    }

    print("\nМетрики модели:")
    for name, value in metrics.items():
        if name != 'Best params':
            print(f"{name}: {value:.4f}")

    print("\nМатрица ошибок:")
    print(confusion_matrix(y_test, y_pred))

    return metrics

# Оценка лучшей модели
metrics = evaluate_model(best_model, X_test, y_test)

# Прогнозирование для тестовых пациентов
def predict_patient(model, patient_data):
    try:
        patient_scaled = scaler.transform([patient_data])
        proba = model.predict_proba(patient_scaled)[0][1]
        diagnosis = 'Диабет' if model.predict(patient_scaled)[0] == 1 else 'Нет диабета'

        print(f"\nРезультат для пациента:")
        print(f"- Вероятность диабета: {proba*100:.2f}%")
        print(f"- Диагноз: {diagnosis}")
        return proba, diagnosis
    except Exception as e:
        print(f"\nОшибка при прогнозировании: {str(e)}")
        return None, None

# Предсказание для тестовых пациентов
print("\n" + "="*50)
predict_patient(best_model, test_patient_1)
print("\n" + "="*50)
predict_patient(best_model, test_patient_2)

# Важность признаков (если модель была обучена)
if hasattr(best_model, 'feature_importances_'):
    feature_importance = pd.DataFrame({
        'Feature': [f'Feature_{i}' for i in range(X.shape[1])],
        'Importance': best_model.feature_importances_
    }).sort_values('Importance', ascending=False)

    print("\nВажность признаков:")
    print(feature_importance.head(10))
else:
    print("\nМодель не поддерживает оценку важности признаков")