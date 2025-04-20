import numpy as np

# Параметры (8 показателей):
# [P1, P2, P3, P4, P5, P6, P7, P8] 
# (например: глюкоза, инсулин, BMI и т.д.)

np.random.seed(42)  # для воспроизводимости

# Генерация данных для "Нет диабета" (0)
def generate_healthy(n):
    data = []
    for _ in range(n):
        base = np.random.uniform(low=0.05, high=0.45)
        row = [
            abs(base + np.random.normal(0, 0.03)),  # P1
            abs(base + np.random.normal(0, 0.05)),  # P2
            abs(base * 1.3 + np.random.normal(0, 0.04)),  # P3
            abs(base * 0.7 + np.random.normal(0, 0.02)),  # P4
            abs(base * 0.9 + np.random.normal(0, 0.03)),  # P5
            abs(base * 1.1 + np.random.normal(0, 0.03)),  # P6
            abs(base * 0.8 + np.random.normal(0, 0.02)),  # P7
            abs(base * 0.9 + np.random.normal(0, 0.03))   # P8
        ]
        data.append([round(x, 2) for x in row])
    return data

# Генерация данных для "Диабет" (1)
def generate_diabetic(n):
    data = []
    for _ in range(n):
        base = np.random.uniform(low=0.5, high=0.95)
        row = [
            abs(base + np.random.normal(0, 0.05)),  # P1
            abs(base * 1.2 + np.random.normal(0, 0.1)),  # P2
            abs(base * 0.9 + np.random.normal(0, 0.06)),  # P3
            abs(base * 0.6 + np.random.normal(0, 0.05)),  # P4
            abs(base * 0.8 + np.random.normal(0, 0.04)),  # P5
            abs(base * 0.7 + np.random.normal(0, 0.05)),  # P6
            abs(base * 0.9 + np.random.normal(0, 0.04)),  # P7
            abs(base * 0.7 + np.random.normal(0, 0.05))   # P8
        ]
        data.append([round(x, 2) for x in row])
    return data

# Создаем базу (520 здоровых, 520 с диабетом)
half_size=1024
medical_data_expended = generate_healthy(half_size) + generate_diabetic(half_size)
labels_expended = [0] * half_size + [1] * half_size

#print(f'{medical_data_expended}\n\n\n{labels_expended}')