import numpy as np
import random

class Neuron:
    def __init__(self, num_inputs):
        self.weights = [random.uniform(-1, 1) for _ in range(num_inputs)]
        self.bias = random.uniform(-1, 1)
        self.output = 0
        self.error = 0
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def forward(self, inputs):
        self.inputs = inputs
        self.output = self.sigmoid(sum(w * x for w, x in zip(self.weights, inputs)) + self.bias)
        return self.output
    
    def backward(self, error):
        self.error = error * self.sigmoid_derivative(self.output)
        return self.error
    
    def update_weights(self, learning_rate):
        for i in range(len(self.weights)):
            self.weights[i] += learning_rate * self.error * self.inputs[i]
        self.bias += learning_rate * self.error

class NeuralNetwork:
    def __init__(self, layers):
        self.layers = []
        for i in range(1, len(layers)):
            layer = [Neuron(layers[i-1]) for _ in range(layers[i])]
            self.layers.append(layer)
    
    def forward(self, inputs):
        for layer in self.layers:
            inputs = [neuron.forward(inputs) for neuron in layer]
        return inputs
    
    def backward(self, target):
        # Обратное распространение для выходного слоя
        for i, neuron in enumerate(self.layers[-1]):
            neuron.backward(target[i] - neuron.output)
        
        # Обратное распространение для скрытых слоев
        for i in range(len(self.layers)-2, -1, -1):
            for j, neuron in enumerate(self.layers[i]):
                error = sum(n.weights[j] * n.error for n in self.layers[i+1])
                neuron.backward(error)
    
    def update(self, learning_rate):
        for layer in self.layers:
            for neuron in layer:
                neuron.update_weights(learning_rate)
    
    def train(self, X, y, epochs=1000, learning_rate=0.1):
        for epoch in range(epochs):
            total_error = 0
            for x, target in zip(X, y):
                output = self.forward(x)
                self.backward(target)
                self.update(learning_rate)
                total_error += sum((t - o)**2 for t, o in zip(target, output))
            
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Error: {total_error/len(X)}")

# Упрощенные медицинские данные (нормализованные)
# [беременности, глюкоза, давление, толщина кожи, инсулин, ИМТ, родословная, возраст]
medical_data = [
    [0.08, 0.14, 0.47, 0.22, 0.30, 0.37, 0.25, 0.29],  # нет диабета
    [0.42, 0.85, 0.72, 0.51, 0.63, 0.46, 0.51, 0.54],  # диабет
    [0.17, 0.13, 0.44, 0.19, 0.28, 0.34, 0.19, 0.31],  # нет
    [0.33, 0.68, 0.63, 0.42, 0.58, 0.52, 0.47, 0.48],  # диабет
    [0.25, 0.15, 0.51, 0.25, 0.32, 0.39, 0.22, 0.35],  # нет
]

# Метки (1 - диабет, 0 - нет диабета)
labels = [
    [0],
    [1],
    [0],
    [1],
    [0]
]

# Создаем сеть: 8 входов, 4 нейрона в скрытом слое, 1 выход
nn = NeuralNetwork([8, 4, 1])

# Обучаем сеть
nn.train(medical_data, labels, epochs=1000, learning_rate=0.1)

# Тестируем на новых данных
test_patient = [0.38, 0.72, 0.68, 0.47, 0.61, 0.49, 0.53, 0.51]  # Ожидаем диабет
prediction = nn.forward(test_patient)
print(f"\nВероятность диабета у тестового пациента: {prediction[0]*100:.2f}%")

# Интерпретация результата
threshold = 0.5
result = "Диабет" if prediction[0] > threshold else "Нет диабета"
print(f"Диагноз: {result} (порог {threshold})")