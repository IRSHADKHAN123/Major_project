import tensorflow as tf
from sklearn.model_selection import train_test_split
import numpy as np
from model1 import load_data
import pickle

# Define the model
m = tf.keras.Sequential([
    tf.keras.layers.Dense(100, activation='relu', input_shape=(12,)),
    tf.keras.layers.Dense(3, activation='softmax')
])

# Compile the model
m.compile(optimizer='adam',
          loss='sparse_categorical_crossentropy',
          metrics=['accuracy'])

filename = './generate_dataset/dataset/dataset.csv'

X,Y = load_data(filename)   
X = np.array(X)
Y = np.array(Y)

X_training, X_testing, y_training, y_testing = train_test_split(
X, Y, test_size=0.4,random_state=42
)
print("length",len(X_training))
# Train the model
m.fit(X_training, y_training, epochs=20)

m.save("./saved_models/ffn.keras")

test_loss, test_accuracy = m.evaluate(X_testing, y_testing)

print("Test Accuracy:", test_accuracy)

predictions = m.predict(X_testing)
correct = 0.0

# Count correct predictions
for i in range(len(predictions)):
    if y_testing[i] == tf.argmax(predictions[i]):
        correct += 1

print("Correct:", correct / len(predictions) * 100)
