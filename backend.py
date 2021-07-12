from flask import Flask, jsonify, request
import datetime
from flask_pymongo import PyMongo
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)
root = "./upload/"
@app.route('/uploadImg', methods=["POST"])
def uploadImg():
    flist = request.files.getlist("images[]")
    for f in flist:
        app.logger.info(f)
        app.logger.info(f.filename)
        f.save(root+f.filename)
    return jsonify({"result":"ok"})
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)