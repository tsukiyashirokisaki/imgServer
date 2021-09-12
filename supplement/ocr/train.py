
import zipfile
import datetime
import string
import glob
import math
import os

import tqdm
import tensorflow as tf
import sklearn.model_selection

import keras_ocr
import cv2
import pandas as pd
import numpy as np
import itertools
import mlflow

detector_batch_size = 1
recognizer_epoch = 1
detector_epoch = 1
detector_learning_rate = 1e-5
recognizer_learning_rate = 1e-5
alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
recognizer_alphabet = ''.join(sorted(set(alphabet.lower())))
label_dir = "label/"
image_dir = "image/"

def get_train_val_test_split(arr):
    train, valtest = sklearn.model_selection.train_test_split(arr, train_size=0.8, random_state=42)
    val, test = sklearn.model_selection.train_test_split(valtest, train_size=0.5, random_state=42)
    return train, val, test

imgs = []
labels = []
for name in os.listdir(image_dir):
    name = name.replace(".png","")
    imgs.append(cv2.imread("%s%s.png"%(image_dir,name)))
    label = pd.read_csv("%s%s.csv"%(label_dir,name),header=None).values
    line = []
    group = []
    index = label[0,0]
    for l in label:
        if l[0] != index:
            line.append(group)
            group = []
            index = l[0]
        group.append((l[2:].reshape(4,2).astype("float32"),l[1]))
    line.append(group)
    labels.append(line)
image_generators = []
lens = []
for i,l in zip(get_train_val_test_split(imgs),get_train_val_test_split(labels)):
    image_generators.append(itertools.cycle(zip(i,l)))
    lens.append(len(i))

detector = keras_ocr.detection.Detector(weights='clovaai_general')
recognizer = keras_ocr.recognition.Recognizer(
    alphabet=recognizer_alphabet,
    weights='kurapan',
)
recognizer.compile()
for layer in recognizer.backbone.layers:
    layer.trainable = False



detection_train_generator, detection_val_generator, detection_test_generator = [
    detector.get_batch_generator(
        image_generator=image_generator,
        batch_size=detector_batch_size
    ) for image_generator in image_generators
]
# fine tune
detector.model.compile(loss="mse", optimizer=tf.optimizers.Adam(learning_rate=detector_learning_rate))
mlflow.keras.autolog()
detector.model.fit(
    detection_train_generator,
    steps_per_epoch=math.ceil(lens[0] / detector_batch_size),
    epochs=detector_epoch,
    workers=0,
    validation_data=detection_val_generator,
    validation_steps=math.ceil(lens[1] / detector_batch_size)
)

max_length = 10
recognition_image_generators = [
    keras_ocr.data_generation.convert_image_generator_to_recognizer_input(
        image_generator=image_generator,
        max_string_length=min(recognizer.training_model.input_shape[1][1], max_length),
        target_width=recognizer.model.input_shape[2],
        target_height=recognizer.model.input_shape[1],
        margin=1
    ) for image_generator in image_generators
]

recognition_batch_size = 8
recognition_train_generator, recognition_val_generator, recogntion_test_generator = [
    recognizer.get_batch_generator(
      image_generator=image_generator,
      batch_size=recognition_batch_size,
      lowercase=True
    ) for image_generator in recognition_image_generators
]
recognizer.training_model.compile(loss=lambda _, y_pred: y_pred,optimizer=tf.optimizers.RMSprop(learning_rate=recognizer_learning_rate))
mlflow.keras.autolog()
recognizer.training_model.fit(
    recognition_train_generator,
    epochs=recognizer_epoch,
    steps_per_epoch=math.ceil(lens[0] / recognition_batch_size),
    validation_data=recognition_val_generator,
    validation_steps=math.ceil(lens[1]/ recognition_batch_size),
    workers=0
)

