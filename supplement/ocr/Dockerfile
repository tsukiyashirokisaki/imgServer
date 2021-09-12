FROM tensorflow/tensorflow:latest-gpu
MAINTAINER tsukiyashirokisaki
RUN pip install opencv-python==4.1.2.30
RUN apt update && apt install -y libsm6 libxext6
RUN apt-get install -y libxrender-dev
RUN pip install Pillow
RUN pip install numpy
RUN pip install sklearn
RUN pip install mlflow
RUN pip install keras-ocr
RUN pip install pandas
