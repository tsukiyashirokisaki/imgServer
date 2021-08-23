FROM tensorflow/tensorflow:latest-gpu
MAINTAINER tsukiyashirokisaki
RUN apt-get update -y
RUN apt-get install git -y
RUN pip install opencv-python
RUN pip install Pillow
RUN pip install numpy
RUN pip install sklearn
RUN pip install mlflow
RUN git clone https://github.com/tsukiyashirokisaki/imgServer
RUN cp imgServer/supplement/classify.py .

