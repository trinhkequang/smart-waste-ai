import tensorflow as tf
from tensorflow.keras import layers, models

train = tf.keras.preprocessing.image_dataset_from_directory(
    "dataset",
    image_size=(224, 224),
    batch_size=32
)

model = models.Sequential([
    layers.Rescaling(1./255),
    layers.Conv2D(32, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(3, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(train, epochs=5)

model.save("model.h5")