FROM tensorflow/tensorflow:latest-gpu
MAINTAINER tsukiyashirokisaki
RUN apt-get update -y
RUN apt-get install git -y
RUN pip install opencv-python
RUN apt install libgl1-mesa-glx -y
RUN pip install Pillow
RUN pip install numpy
RUN pip install sklearn
RUN pip install mlflow
RUN git clone https://github.com/tsukiyashirokisaki/imgServer
RUN cp imgServer/supplement/classify.py .
CMD python classify.py --imgsz 224 --num_classes 1000 --lr 0.001 --val_frac 0.1 --optimizer Adam --model_name ResNet50 --batch_size 32 --epoch 10 --label_path mlruns/label.txt --img_path mlruns/images/

