import os
from flask import Flask, jsonify, request
from subprocess import Popen
from flask_cors import cross_origin, CORS
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Server works!', 200

@app.route('/detect', methods=['POST'])
def detect():
    imgFile = request.files['img']
    if imgFile.filename == '':
        res = jsonify('No file selected for uploading')
        res.status_code = 400
        return res
    if (not imgFile.filename.lower().endswith(('.jpg', '.png'))):
        res = jsonify('The file type must be jpg or png')
        res.status_code = 400
        return res
    imgFile.save('testing.jpg')
    basepath = os.path.dirname(__file__)
    process = Popen(["python", "detect.py", '--source', os.path.join(basepath, 'testing.jpg'), "--weights", "best4.pt"])
    process.wait()
    output_filepath = os.path.join(basepath, 'output.txt')
    with open(output_filepath, 'r+') as output_file:
        output_content = output_file.readlines()
        output_content = [line.strip() for line in output_content]
    device = output_content[0].split(':')[-1].strip()
    if device == "Blood Pressure":
        Systolic = float(output_content[1].split(':')[-1].strip())
        Diastolic = float(output_content[2].split(':')[-1].strip())
        Heart_rate = float(output_content[3].split(':')[-1].strip())
        output_json = {
            "device": device,
            "systolic": Systolic,
            "diastolic": Diastolic,
            "heart_rate": Heart_rate
        }
    elif device == "Oxymetre":
        Spo2 = float(output_content[1].split(':')[-1].strip())
        Heart_rate = float(output_content[2].split(':')[-1].strip())
        output_json = {
            "device": device,
            "spo2": Spo2,
            "heart_rate": Heart_rate
        }
    elif device == "Glucometer":
        Glucose = float(output_content[1].split(':')[-1].strip())
        output_json = {
            "device": device,
            "glucose": Glucose
        }
    elif device == "Thermometer":
        Temperature = float(output_content[1].split(':')[-1].strip())
        output_json = {
            "device": device,
            "temperature": Temperature
        }
    else:
        output_json = {"error": " Try again . Unknown device"}
    process.wait()
    return jsonify(output_json), 200
if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
    CORS(app, origins=['http://192.168.1.40:5000'],
         methods=['GET', 'POST'], allow_headers=['Content-Type'])
   