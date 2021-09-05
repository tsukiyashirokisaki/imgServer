# load weights
import keras_ocr
from keras_ocr.detection import build_keras_model
import string
import os
import matplotlib.pyplot as plt
use_pretrained = False
if not os.path.exists("test_image.jpg"):
    os.system("curl https://raw.githubusercontent.com/faustomorales/keras-ocr/master/tests/test_image.jpg --output test_image.jpg")
if use_pretrained:
    pipeline = keras_ocr.pipeline.Pipeline()
else:    
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
    recognizer_alphabet = ''.join(sorted(set(alphabet.lower())))
    detector = keras_ocr.detection.Detector(weights='clovaai_general')
    detector.model = build_keras_model(weights_path="detector_2021-09-06T01:01:57.333361.h5", backbone_name="vgg")
    detector.model.compile(loss="mse", optimizer="adam")
    recognizer = keras_ocr.recognition.Recognizer(
        alphabet = recognizer_alphabet ,
        weights='kurapan',
    )
    recognizer.model.load_weights("recognizer_2021-09-06T01:20:05.838326.h5")
    pipeline = keras_ocr.pipeline.Pipeline(detector,recognizer)
image = keras_ocr.tools.read('test_image.jpg')
predictions = pipeline.recognize(images=[image])[0]
drawn = keras_ocr.tools.drawBoxes(image=image, boxes=predictions, boxes_format='predictions')
print('Predicted:', [text for text, box in predictions])
plt.imshow(drawn)