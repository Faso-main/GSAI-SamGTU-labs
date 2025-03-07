import numpy as np


def sigmoid(x):  return 1 / (1 + np.exp(-x)) # Сигмоидная функция (для нормализации)

def sigmoid_derivative(x): return x * (1 - x) # Производная сигмоидной функции


# Класс для нейронной сети
class SimpleNeuronLL:
    def __init__(self):
        # Инициализация весов случайными значениями
        self.weights = np.random.rand(1)  # Один вес для линейной регрессии
        self.bias = np.random.rand(1)  # отклонение
        print(f'Веса: {self.weights}\nОтклонение: {self.bias}')    # Свободный член
    
    def predict(self, x):
        
        return self.weights * x + self.bias # линейная регрессия
        # y=w*x+b
        #w — это вес, 
        #x — входное значение, и 
        #b — смещение (отклонение).

    def train(self, x_train, y_train, epochs, learning_rate):
        for itr in range(epochs):
            
            y_pred = self.predict(x_train) # предсказание
            error = y_train - y_pred # вычисление ошибки

            # обновление весов и смещения
            self.weights += learning_rate * np.dot(error, x_train) / len(x_train)
            self.bias += learning_rate * np.sum(error) / len(x_train)


# входные данные
data_input=[item for item in range(2,11,2)] # [2,4,6,8,10]
x_train = np.array(data_input)  # входные данные
y_train = np.array([itr*2 for itr in data_input]) # y = 2x

model = SimpleNeuronLL()
model.train(x_train, y_train, epochs=1000, learning_rate=0.01)

test_batch = np.array([3, 5, 7]) # test batch
predictions = model.predict(test_batch)


for validation, prediction in zip(test_batch, predictions):
    print(f"x: {validation}, Предсказание y: {prediction}")

print(f"\nОбнаруженные веса: {model.weights[0]}")
print(f"Обнаруженное смещение: {model.bias[0]}")
