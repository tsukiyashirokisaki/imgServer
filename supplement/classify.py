
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.layers import Flatten,Dense
from tensorflow.keras.models import Model
import numpy as np
import tensorflow.keras.applications as applications
import tensorflow as tf
import mlflow
from keras import optimizers
from keras.utils.np_utils import to_categorical
from sklearn.model_selection import train_test_split
import os
import cv2
import math
import mlflow
import argparse
models = "Xception,VGG16,VGG19,ResNet50,ResNet101,ResNet152,ResNet50V2,ResNet101V2,ResNet152V2,\
InceptionV3,InceptionResNetV2,MobileNet,MobileNetV2,\
DenseNet121,DenseNet169,DenseNet201,NASNetMobile,NASNetLarge,\
EfficientNetB0,EfficientNetB1,EfficientNetB2,EfficientNetB3,EfficientNetB4,EfficientNetB5,EfficientNetB6,EfficientNetB7"
optimizers = "SGD,RMSprop,Adam,Adadelta,Adagrad,Adamax,Nadam,Ftrl"
def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--imgsz', type=int, default=224, help='training size (pixels)')
    parser.add_argument('--num_classes', type=int, default=1000, help='num of classes to predict')
    parser.add_argument('--lr', type=float, default=1e-3, help='learning rate')
    parser.add_argument('--val_frac',type=float,default=0.1, help='validation fraction')
    parser.add_argument('--optimizer',type=str,default='Adam', help=optimizers)
    parser.add_argument('--model_name',type=str,default='ResNet50',help=models)
    parser.add_argument('--batch_size',type=int,default=32,help='bacth size')
    parser.add_argument('--epoch',type=int,default=10,help='epoch')
    parser.add_argument('--label_path',type=str,default='data/label.txt',help='label path')
    parser.add_argument('--img_path',type=str,default='data/images/',help='images path')
    opt = parser.parse_args()
    return opt
opt = parse_opt()
INPUT_SHAPE = (opt.imgsz,opt.imgsz,3)
NUM_CLASSES = opt.num_classes
LR = opt.lr
VAL_FRAC = opt.val_frac
OPTIMIZER = opt.optimizer
MODEL_NAME = opt.model_name
BATCH_SIZE = opt.batch_size
EPOCH = opt.epoch
label_path = opt.label_path
img_path = opt.img_path

with open(label_path) as f:
    label = f.read().split("\n")
while "" in label:
    label.remove("")
label = np.array(label).astype("int") - 1
imgNames = np.array(os.listdir(img_path))
# label = label
# imgNames = imgNames
imgTrain,imgVal,labelTrain,labelVal = train_test_split(imgNames,label,test_size=VAL_FRAC)
base = getattr(applications,MODEL_NAME)(include_top=False,input_shape=INPUT_SHAPE)
x = base.output
x = Flatten()(x)
output_layer = Dense(NUM_CLASSES, activation='softmax', name='softmax')(x)
model = Model(inputs=base.input, outputs=output_layer)
model.compile(optimizer=getattr(tf.keras.optimizers, OPTIMIZER)(learning_rate=LR),
              loss=tf.keras.losses.CategoricalCrossentropy(),
              metrics=[tf.keras.metrics.CategoricalAccuracy()])
mlflow.keras.autolog()

def batch_generator(imgNames,label,batch_size=8):
    length = len(imgNames)
    idx = 0
    while True:
        cur_data = []
        cur_label = []
        for i in range(batch_size):
            if idx+i >= length:
                idx -= length
                yield load_data(cur_data,cur_label)
            cur_data.append(imgNames[idx+i])
            cur_label.append(label[idx+i])
        yield load_data(cur_data,cur_label)
def load_data(cur_data,cur_label):
    x = []
    for name in cur_data:
        img = cv2.imread(img_path+name)
        img = cv2.resize(img,(INPUT_SHAPE[0],INPUT_SHAPE[1]))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)/255.
        x.append(img)
    return (np.array(x), to_categorical(cur_label,NUM_CLASSES))
train_generator = batch_generator(imgTrain,labelTrain,batch_size=BATCH_SIZE)
val_generator = batch_generator(imgVal,labelVal,batch_size=BATCH_SIZE)

result = model.fit(train_generator,
epochs=EPOCH,steps_per_epoch=math.ceil(len(imgTrain)/BATCH_SIZE),
 verbose=1, validation_data=val_generator,
validation_steps=math.ceil(len(imgVal)/BATCH_SIZE))
model.save("model.h5")



