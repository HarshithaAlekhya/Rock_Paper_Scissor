# -*- coding: utf-8 -*-
"""fcc_sms_text_classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/github/freeCodeCamp/boilerplate-neural-network-sms-text-classifier/blob/master/fcc_sms_text_classification.ipynb
"""

# import libraries
try:
  # %tensorflow_version only exists in Colab.
  !pip install tf-nightly
except Exception:
  pass
import tensorflow as tf
import pandas as pd
from tensorflow import keras
!pip install tensorflow-datasets
import tensorflow_datasets as tfds
import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)

# get data files
!wget https://cdn.freecodecamp.org/project-data/sms/train-data.tsv
!wget https://cdn.freecodecamp.org/project-data/sms/valid-data.tsv

train_file_path = "train-data.tsv"
test_file_path = "valid-data.tsv"

# Load and preprocess the data
train_df = pd.read_csv(train_file_path, sep="\t", header=None, names=["label", "message"])
test_df = pd.read_csv(test_file_path, sep="\t", header=None, names=["label", "message"])

# Convert labels to binary (0 for ham, 1 for spam)
train_df["label"] = train_df["label"].map({"ham": 0, "spam": 1})
test_df["label"] = test_df["label"].map({"ham": 0, "spam": 1})

# Split into features and labels
train_messages = train_df["message"].values
train_labels = train_df["label"].values
test_messages = test_df["message"].values
test_labels = test_df["label"].values

# Enhanced text preprocessing
def preprocess_text(text):
    text = text.lower()  # Lowercase
    text = ''.join([char for char in text if char.isalnum() or char == ' '])  # Remove special chars
    return text

train_messages = [preprocess_text(msg) for msg in train_messages]
test_messages = [preprocess_text(msg) for msg in test_messages]

# Tokenize the text with larger vocabulary
vocab_size = 2000  # Increased from 1000
max_length = 120   # Increased from 100
trunc_type = "post"
padding_type = "post"
oov_tok = "<OOV>"

tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(train_messages)

# Create sequences
train_sequences = tokenizer.texts_to_sequences(train_messages)
train_padded = tf.keras.preprocessing.sequence.pad_sequences(
    train_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type
)

test_sequences = tokenizer.texts_to_sequences(test_messages)
test_padded = tf.keras.preprocessing.sequence.pad_sequences(
    test_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type
)

# Convert to numpy arrays
train_padded = np.array(train_padded)
train_labels = np.array(train_labels)
test_padded = np.array(test_padded)
test_labels = np.array(test_labels)

# Enhanced model architecture
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, 64, input_length=max_length),  # Increased embedding dimension
    tf.keras.layers.Dropout(0.2),  # Added dropout for regularization
    tf.keras.layers.Conv1D(64, 5, activation='relu'),  # Added convolutional layer
    tf.keras.layers.GlobalMaxPooling1D(),  # Changed to Max pooling
    tf.keras.layers.Dense(64, activation='relu'),  # Additional dense layer
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy',
              optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),  # Custom learning rate
              metrics=['accuracy'])

# Early stopping callback
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

# Train the model with more epochs
num_epochs = 20  # Increased from 10
history = model.fit(
    train_padded,
    train_labels,
    epochs=num_epochs,
    validation_data=(test_padded, test_labels),
    callbacks=[early_stopping],
    verbose=2
)

# Prediction function
def predict_message(pred_text):
    # Preprocess the input text
    pred_text = preprocess_text(pred_text)
    sequence = tokenizer.texts_to_sequences([pred_text])
    padded = tf.keras.preprocessing.sequence.pad_sequences(
        sequence, maxlen=max_length, padding=padding_type, truncating=trunc_type
    )

    # Make prediction
    prediction = model.predict(padded, verbose=0)[0][0]

    # Determine label
    label = "spam" if prediction >= 0.5 else "ham"

    return [prediction, label]

# Test the function
pred_text = "how are you doing today?"
prediction = predict_message(pred_text)
print(prediction)

# function to predict messages based on model
# (should return list containing prediction and label, ex. [0.008318834938108921, 'ham'])
def predict_message(pred_text):
  # Preprocess the input text
    pred_text = preprocess_text(pred_text)
    sequence = tokenizer.texts_to_sequences([pred_text])
    padded = tf.keras.preprocessing.sequence.pad_sequences(
        sequence, maxlen=max_length, padding=padding_type, truncating=trunc_type
    )

    # Make prediction
    prediction = model.predict(padded, verbose=0)[0][0]

    # Determine label
    label = "spam" if prediction >= 0.5 else "ham"

    return [prediction, label]


  # return (prediction)

pred_text = "how are you doing today?"

prediction = predict_message(pred_text)
print(prediction)

# Run this cell to test your function and model. Do not modify contents.
def test_predictions():
  test_messages = ["how are you doing today",
                   "sale today! to stop texts call 98912460324",
                   "i dont want to go. can we try it a different day? available sat",
                   "our new mobile video service is live. just install on your phone to start watching.",
                   "you have won £1000 cash! call to claim your prize.",
                   "i'll bring it tomorrow. don't forget the milk.",
                   "wow, is your arm alright. that happened to me one time too"
                  ]

  test_answers = ["ham", "spam", "ham", "spam", "spam", "ham", "ham"]
  passed = True

  for msg, ans in zip(test_messages, test_answers):
    prediction = predict_message(msg)
    if prediction[1] != ans:
      passed = False

  if passed:
    print("You passed the challenge. Great job!")
  else:
    print("You haven't passed yet. Keep trying.")

test_predictions()