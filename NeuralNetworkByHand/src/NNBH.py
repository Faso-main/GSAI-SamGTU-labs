import numpy as np
import random, os
import pandas as pd


# Configuration
CSV_PATH=os.path.join('NeuralNetworkByHand','src','medical_data.csv')
EPOCHS=1000
LEARNING_RATE=0.1
THRESHOLD=0.5


# Загрузка данных из CSV файла
def load_data_from_csv(filename):
    data = pd.read_csv(filename)
    X = data.drop('diabetic', axis=1).values.tolist()
    y = [[label] for label in data['diabetic'].values]  
    return X, y


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
    def __init__(self, layers: any):
        self.layers = []
        for i in range(1, len(layers)):
            layer = [Neuron(layers[i-1]) for itr in range(layers[i])]
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
    
    def train(self, X, y, epochs=EPOCHS, learning_rate=LEARNING_RATE):
        for epoch in range(epochs):
            total_error = 0
            for x, target in zip(X, y):
                output = self.forward(x)
                self.backward(target)
                self.update(learning_rate)
                total_error += sum((t - o)**2 for t, o in zip(target, output))
            
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Error: {total_error/len(X)}")

# Основной код
if __name__ == "__main__":
    try:
        X, y = load_data_from_csv(CSV_PATH)
        print(f"Успешно загружено {len(X)} примеров")
        
        nn = NeuralNetwork([8, 4, 1]) # входной - скрытый - выходной
        nn.train(X, y, epochs=1000, learning_rate=0.1)

        # Тестовые пациенты
        test_patient_1 = [0.15, 0.20, 0.52, 0.26, 0.33, 0.40, 0.29, 0.37]  # нет диабета
        test_patient_2 = [0.60, 0.82, 0.70, 0.51, 0.66, 0.55, 0.58, 0.62]  # диабет

        # Тестирование
        def test_patient(network, patient_data):
            prediction = network.forward(patient_data)
            print(f"\nВероятность диабета: {prediction[0]*100:.2f}%")
            threshold = THRESHOLD
            result = "Диабет" if prediction[0] > threshold else "Нет диабета"
            print(f"Диагноз: {result} (порог {threshold})")

        print("\nТестирование пациентов:")
        print("\nПациент 1 (ожидается: нет диабета):")
        test_patient(nn, test_patient_1)
        
        print("\nПациент 2 (ожидается: диабет):")
        test_patient(nn, test_patient_2)

    except Exception as e: print(f"Ошибка: {str(e)}")
