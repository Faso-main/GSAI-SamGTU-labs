import numpy as np

# Сигмоидная функция (для нормализации)
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Производная сигмоидной функции
def sigmoid_derivative(x):
    return x * (1 - x)

# Класс для нейронной сети
class SimpleLinearRegressionNN:
    def __init__(self):
        # Инициализация весов случайными значениями
        self.weights = np.random.rand(1)  # Один вес для линейной регрессии
        self.bias = np.random.rand(1)      # Свободный член
    
    def predict(self, x):
        # Линейная регрессия
        return self.weights * x + self.bias

    def train(self, x_train, y_train, epochs, learning_rate):
        for _ in range(epochs):
            # Предсказание
            y_pred = self.predict(x_train)

            # Вычисление ошибки
            error = y_train - y_pred

            # Обновление весов и смещения
            self.weights += learning_rate * np.dot(error, x_train) / len(x_train)
            self.bias += learning_rate * np.sum(error) / len(x_train)

# Данные для обучения
data_input=[item for item in range(2,11,2)] # [2,4,6,8,10]
x_train = np.array(data_input)  # Входные данные
y_train = np.array([itr*2 for itr in data_input]) #y=2x

# Создание и обучение модели
model = SimpleLinearRegressionNN()
model.train(x_train, y_train, epochs=1000, learning_rate=0.01)

# Проверка результата
test_data = np.array([3, 5, 7])
predictions = model.predict(test_data)

print("Предсказания для входных данных:")
for val, pred in zip(test_data, predictions):
    print(f"x: {val}, Предсказание y: {pred}")

# Печать конечных весов и смещения
print(f"\nОбнаруженные веса: {model.weights[0]}")
print(f"Обнаруженное смещение: {model.bias[0]}")
