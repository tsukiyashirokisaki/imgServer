FROM public.ecr.aws/lts/ubuntu:latest
MAINTAINER tsukiyashirokisaki
RUN apt update -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa 
RUN apt update -y
RUN apt install python3.8 -y
RUN ln -s /usr/bin/python3.8 /usr/bin/python
RUN apt-get update -y
RUN apt-get install git -y
RUN apt-get install python3-pip -y
RUN git clone https://github.com/tsukiyashirokisaki/imgServer
RUN pip3 install flask
RUN pip3 install Flask-Cors
RUN pip3 install Flask-PyMongo
RUN pip3 install sklearn
CMD nohup python imgServer/backend.py


