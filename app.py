import time
from flask import Flask, request, jsonify, send_from_directory
from bson import json_util, ObjectId
import pymongo
from base64 import b64decode, b64encode
from apitest import getHindiText

from pdfminer2.tools.split import pdf_to_arr

app = Flask(__name__)

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['sls']
col = db['files']


@app.route('/readyFiles', methods=['GET'])
def ready_files():
    if request.method == 'GET':
        all_files = col.find()
        x = list(all_files)
        return json_util.dumps(x)


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == "POST":
        file_name = request.json['file_name']
        file_inserted = db['files'].insert_one({"file_name": file_name, "status": 0})
        print(file_inserted.inserted_id)
        file_name += str(file_inserted.inserted_id)
        # status mongo set 0
        print(file_name + 'received')

        # get pdf
        file = request.json["file"]
        #
        base64file = b64decode(file, validate=True)
        #
        if base64file[0:4] != b'%PDF':
            raise ValueError('Missing the PDF file signature')

        f = open('file.pdf', 'wb')
        f.write(base64file)
        f.close()

        # pdf rec Create object return response

        # convert pdf to text

        englishConvertedArray = pdf_to_arr('/Users/shubham/Desktop/SlS_OnE/file.pdf')

        hindiArrayList = []

        for x in englishConvertedArray:
            v = getHindiText(x)
            hindiArrayList.append(v)
            time.sleep(1.5)

        print("-->", hindiArrayList)
        finale = ""
        for i in hindiArrayList:
            finale = finale + "\n\n" + i

        print(finale)
        path = './converted_files/' + file_name + '.txt'
        f = open(path, 'w')
        f.write(finale)
        f.close()

        file_inserted = db['files'].update_one({"file_name": request.json['file_name']}, {"$set": {"status": 1, "path": path}})
        print(file_inserted)
        # status mongo set 1
        return 'successful'
        # return "asd"


# @app.route('/status',methods=['GET'])
# def

@app.route('/view_file/<file_name>', methods=['GET'])
def view_file(file_name):
    if request.method == "GET":
        # return send_from_directory('converted_files', file_name+'.txt')
        data = open('./converted_files/' + file_name + '.txt').read()
        data_bytes = data.encode("utf-8")
        print(data)
        encoded = b64encode(data_bytes)
        return encoded


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
