from tensorflow.keras import layers, models, utils
from sklearn.datasets import fetch_lfw_people
from sklearn.model_selection import train_test_split
import numpy as np

# Уменьшение размера изображений и фильтрация данных
lfw_people = fetch_lfw_people(min_faces_per_person=50, resize=0.3)  # Уменьшение разрешения

# Размеры изображений
n_samples, h, w = lfw_people.images.shape
X = lfw_people.data
y = lfw_people.target

# Нормализация данных
X = X / 255.0

# Разделение данных
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Преобразование в 4D-тензор (добавляем канал)
X_train = X_train.reshape(-1, h, w, 1)
X_test = X_test.reshape(-1, h, w, 1)

# Создание облегченной модели
def create_light_model(input_shape, num_classes):
    model = models.Sequential([
        # Первый сверточный блок
        layers.Conv2D(16, (3,3), activation='relu', padding='same', input_shape=input_shape),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2,2)),
        
        # Второй сверточный блок
        layers.Conv2D(32, (3,3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2,2)),
        
        # Третий сверточный блок
        layers.Conv2D(64, (3,3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2,2)),
        
        # Глобальный средний пулинг вместо полносвязных слоев
        layers.GlobalAveragePooling2D(),
        
        # Выходной слой
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

# Параметры модели
input_shape = (h, w, 1)
num_classes = len(np.unique(y))

model = create_light_model(input_shape, num_classes)
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

# Обучение с уменьшенными параметрами
history = model.fit(
    X_train, y_train,
    epochs=30,
    batch_size=32,  # Меньший размер батча для экономии памяти
    validation_split=0.1,
    verbose=1
)

# Оценка модели
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"\nTest accuracy: {test_acc:.4f}")

# Сохранение модели
model.save('light_face_recognition.h5')