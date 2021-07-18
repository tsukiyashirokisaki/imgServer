from flask import Flask, jsonify, request
import datetime
from flask_pymongo import PyMongo
from flask_cors import CORS
import json
import os
from sklearn.model_selection import train_test_split

app = Flask(__name__)
CORS(app)
root = "./upload/"
test_size = 0.1
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
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)