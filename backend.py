from flask import Flask, jsonify, request, send_file, send_from_directory
import datetime
from flask_pymongo import PyMongo
from flask_cors import CORS
import json
import os
from sklearn.model_selection import train_test_split
from utils import Colors,plot_one_box,sampleName,readLabels,xywhn2xyxy
import cv2
from PIL import Image
import io
import yaml
from flask_socketio import SocketIO
from threading import Lock
import pathlib
app = Flask(__name__)
CORS(app)
root = "./upload/"    
test_size = 0.1
sampleNum = 5
colors = Colors()
socketio = SocketIO(app,cors_allowed_origins='http://localhost:8080' ,async_mode='gevent',engineio_logger=True, logger=True)
thread = None
thread_lock = Lock()

with open(root+"coco128.yaml") as f:
    id2name = yaml.safe_load(f)["names"]  
@app.route('/uploadImg', methods=["POST"])
def uploadImg():
    flist = request.files.getlist("images[]")
    folderName = ["images","labels"]
    types = ["train","val"]
    for folder in folderName:
        path = root+folder
        if folder not in os.listdir(root):
            os.mkdir(path)
        for t in types:
            if t not in os.listdir(path):
                os.mkdir(path+"/"+t)
    jpgs = []
    txts = []
    for f in flist:
        if ".txt" in f.filename:
            txts.append(f)
        elif ".jpg" in f.filename:
            jpgs.append(f)
        app.logger.info(f)
        app.logger.info(f.filename)
    if len(jpgs)!=len(txts):
        app.logger.info("filesize not match")
        return jsonify({"result":"error"})
    for jpg,txt in zip(jpgs,txts):
        if jpg.filename.replace(".jpg","")!=txt.filename.replace(".txt",""):
            app.logger.info("filename not match")
            return jsonify({"result":"error"})
    if len(jpgs)==1:
        jpgs[0].save(root+"images/train/"+jpg.filename)
        txts[0].save(root+"labels/train/"+txt.filename)
    jpgTrain,jpgVal,txtTrain,txtVal = train_test_split(jpgs,txts,test_size=0.1)
    for jpg,txt in zip(jpgTrain,txtTrain):
        jpg.save(root+"images/train/"+jpg.filename)
        txt.save(root+"labels/train/"+txt.filename)
    for jpg,txt in zip(jpgVal,txtVal):
        jpg.save(root+"images/val/"+jpg.filename)
        txt.save(root+"labels/val/"+txt.filename)
    return jsonify({"result":"ok"})
@app.route('/addBox')
def addBox():
    types = ["train","val"]
    names = dict()
    for t in types:
        names[t]=sampleName(root+"images/"+t,"addBox",sampleNum)
    return {"boxList":names}
@app.route('/addBox/<path:path>')
def sendAddBox(path):
    img = cv2.imread(path)
    cs,xywhns = readLabels(path.replace("/images/","/labels/").replace(".jpg",".txt"))
    xyxys = xywhn2xyxy(xywhns,img.shape[1],img.shape[0])
    for c,xyxy in zip(cs,xyxys):
        plot_one_box(xyxy,img,label=id2name[c],color=colors(c, True))
    file_object = io.BytesIO()
    Image.fromarray(img[:,:,::-1]).save(file_object, 'PNG')
    file_object.seek(0)
    return send_file(file_object, mimetype='image/PNG')
    
@app.route('/file/<path:path>')
def sendData(path):
    return send_from_directory("model/",path)
@socketio.on('log')
def initLog(msg):
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(sendLog)
    
def sendLog():
    prevMtime = None
    logPath = "train.log"
    fname = pathlib.Path(logPath)
    while True:    
        mtime = datetime.datetime.fromtimestamp(fname.stat().st_mtime)
        if mtime != prevMtime:
            f = open(logPath,"r",encoding="utf-8")
            # socketio.emit('log', {'data': f.read().replace("\n","<br>")})
            socketio.emit('log', {'data': f.read()})
            f.close()
        socketio.sleep(1)
        prevMtime = mtime
    
        

    

# @app.route('/test')
# def test():
#     return jsonify({"status":"ok"})
if __name__ == "__main__":
    socketio.run(app=app,host="0.0.0.0", debug=False)
