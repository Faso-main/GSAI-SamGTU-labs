import autokeras as ak
from sklearn.preprocessing import LabelEncoder
from sklearn.datasets import fetch_lfw_people
import numpy as np

# Загрузка датасета LFW
lfw_people = fetch_lfw_people(min_faces_per_person=70, resize=0.4)

# Размеры изображений
n_samples, h, w = lfw_people.images.shape
X = lfw_people.data
y = lfw_people.target
target_names = lfw_people.target_names
n_classes = target_names.shape[0]

print("Размер датасета:")
print("Количество образцов: %d" % n_samples)
print("Количество классов: %d" % n_classes)
print("Размер изображений: %d x %d" % (h, w))

# Разделение на train/test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)


# Преобразование данных в 4D-тензор (для CNN)
X_train_4d = X_train.reshape(X_train.shape[0], h, w, 1)
X_test_4d = X_test.reshape(X_test.shape[0], h, w, 1)

# Кодирование меток
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# Создание и обучение классификатора изображений
clf = ak.ImageClassifier(max_trials=10, overwrite=True)
clf.fit(X_train_4d, y_train_encoded, epochs=10)

# Оценка модели
accuracy = clf.evaluate(X_test_4d, y_test_encoded)[1]
print(f"Точность: {accuracy}")

# Экспорт лучшей модели
model = clf.export_model()
try:
    model.save("face_recognition_autokeras", save_format="tf")
except:
    model.save("face_recognition_autokeras.h5")