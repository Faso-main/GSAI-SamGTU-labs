import numpy as np
import random


# Генерация данных
def generate_healthy(n):
    data = []
    for _ in range(n):
        base = np.random.uniform(low=0.05, high=0.45)
        row = [
            abs(base + np.random.normal(0, 0.03)),
            abs(base + np.random.normal(0, 0.05)),
            abs(base * 1.3 + np.random.normal(0, 0.04)),
            abs(base * 0.7 + np.random.normal(0, 0.02)),
            abs(base * 0.9 + np.random.normal(0, 0.03)),
            abs(base * 1.1 + np.random.normal(0, 0.03)),
            abs(base * 0.8 + np.random.normal(0, 0.02)),
            abs(base * 0.9 + np.random.normal(0, 0.03))
        ]
        data.append([round(x, 2) for x in row])
    return data

def generate_diabetic(n):
    data = []
    for _ in range(n):
        base = np.random.uniform(low=0.5, high=0.95)
        row = [
            abs(base + np.random.normal(0, 0.05)),
            abs(base * 1.2 + np.random.normal(0, 0.1)),
            abs(base * 0.9 + np.random.normal(0, 0.06)),
            abs(base * 0.6 + np.random.normal(0, 0.05)),
            abs(base * 0.8 + np.random.normal(0, 0.04)),
            abs(base * 0.7 + np.random.normal(0, 0.05)),
            abs(base * 0.9 + np.random.normal(0, 0.04)),
            abs(base * 0.7 + np.random.normal(0, 0.05))
        ]
        data.append([round(x, 2) for x in row])
    return data

# Создаем данные
half_size = 1024
medical_data_expended = generate_healthy(half_size) + generate_diabetic(half_size)
labels_expended = [[0] for _ in range(half_size)] + [[1] for _ in range(half_size)]  # Исправленный формат меток