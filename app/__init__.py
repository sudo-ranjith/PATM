from crypt import methods
from email.policy import default
import json
from app import transport_agent
from flask import Flask, Blueprint, jsonify, make_response, render_template
from flask_restplus import Api
from flask_cors import CORS
from flask_mail import Mail
import os
import sys
import socket
from datetime import datetime
from utils.helpers import calculate_proc_time
from flask_pymongo import PyMongo
from app.config import BaseConfig
from flask_bcrypt import Bcrypt
from flask_jwt_simple import JWTManager
from werkzeug.contrib.fixers import ProxyFix


# Initialize application
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
# Enabling cores
CORS(app)
if os.environ.get('FLASK_ENV'):
    env = os.environ.get('FLASK_ENV')
    if env == "development":
        app_settings = os.getenv('APP_SETTINGS', 'app.config.DevelopmentConfig')
    elif env == "qa":
        app_settings = os.getenv('APP_SETTINGS', 'app.config.TestingConfig')
    elif env == "prod":
        app_settings = os.getenv('APP_SETTINGS', 'app.config.ProductionConfig')
    else:
        print("Given ENV is not configured")
else:
    app_settings = os.getenv('APP_SETTINGS', 'app.config.DevelopmentConfig')
# app configuration
app.config.from_object(app_settings)
mail = Mail(app)

# each module should be import here

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

blueprint = Blueprint('api', __name__)
api = Api(blueprint, version='1.0', title='API', prefix = '/api',
          description='description of swagger')

import app.login.view as login_view
import app.Register.view as register_view
import app.purchase_module.view as purchase_module_view
import app.transport_agent.view as transport_agent_view
import app.event_module.view as event_module_view

# register namespace for swagger UI
api.add_namespace(register_view.register)
api.add_namespace(login_view.login_ns)
api.add_namespace(purchase_module_view.purchase_cal)
api.add_namespace(transport_agent_view.transport_agent)
api.add_namespace(event_module_view.event_module)

api.namespaces.clear()
app.register_blueprint(blueprint)

api.add_namespace(register_view.register)
api.add_namespace(login_view.login_ns)
api.add_namespace(purchase_module_view.purchase_cal)
api.add_namespace(transport_agent_view.transport_agent)
api.add_namespace(event_module_view.event_module)


import os
import shutil


from flask import Flask, redirect, url_for, request, flash, jsonify
from flask import render_template
from flask import send_file
from app.main_model import RegisterCurb
from utils.helpers import get_image_text

img_db = RegisterCurb()
img_path = os.path.join(os.getcwd(), 'images')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["IMAGES"] = 'images'
app.config["LABELS"] = []
app.config["HEAD"] = 0
app.config["OUT"] = "out.csv"
with open("out.csv",'w') as f:
    f.write("image,id,name,xMin,xMax,yMin,yMax\n")

@app.route('/label',methods = ['GET', 'POST'])
def index():
    print(f"**** 1")
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No files selected')
            return redirect('/')
        try:
            shutil.rmtree(img_path)
        except:
            pass
        os.mkdir(img_path)
        files = request.files.getlist("file")
        for f in files:
            img_file_path = os.path.join(img_path, f.filename)
            # app.config["img_file_path"] = img_file_path
            f.save(img_file_path)
        for (dirpath, dirnames, filenames) in os.walk(img_path):
            files = filenames
            break
        app.config["FILES"] = files
        return redirect('/tagger', code=302)
    else:
        return render_template('index.html')

@app.route('/tagger')
def tagger():
    print(f"**** 2")
    if (app.config["HEAD"] == len(app.config["FILES"])):
        return redirect(url_for('final'))
    directory = img_path
    image = app.config["FILES"][app.config["HEAD"]]
    labels = app.config["LABELS"]
    not_end = not(app.config["HEAD"] == len(app.config["FILES"]) - 1)
    print(not_end)
    return render_template('tagger.html', not_end=not_end, directory=directory, image=image, labels=labels, head=app.config["HEAD"] + 1, len=len(app.config["FILES"]))


@app.route('/image/<f>')
def images(f):
    path = os.path.join(img_path, f)
    print(f"**** 3 {f} and {path}")
    return send_file(path)

@app.route('/label/<id>')
def label(id):
    print(f"**** 4")
    name = request.args.get("name")
    app.config["LABELS"][int(id) - 1]["name"] = name
    return redirect(url_for('tagger'))


@app.route('/add/<id>')
def add(id):
    print(f"**** 5")
    xMin = request.args.get("xMin")
    xMax = request.args.get("xMax")
    yMin = request.args.get("yMin")
    yMax = request.args.get("yMax")
    app.config["LABELS"].append({"id":id, "name":"", "xMin":xMin, "xMax":xMax, "yMin":yMin, "yMax":yMax})
    return redirect(url_for('tagger'))

@app.route('/remove/<id>')
def remove(id):
    print(f"**** 6")
    index = int(id) - 1
    del app.config["LABELS"][index]
    for label in app.config["LABELS"][index:]:
        label["id"] = str(int(label["id"]) - 1)
    return redirect(url_for('tagger'))

@app.route('/next')
def next():
    """
    in this api we are getting the selected image points
    """
    print(f"**** 7 app.config type : {type(app.config)} {app.config} ")
    print("***************")
    image = app.config["FILES"][app.config["HEAD"]]
    app.config["HEAD"] = app.config["HEAD"] + 1
    # print app.config["LABELS"] as pretty
    print(app.config["LABELS"])
    to_insert = {}
    to_insert["image"] = app.config["FILES"][0]
    to_insert["labels"] = app.config["LABELS"]

    # check already exists image in db or not
    if img_db.read_data({"image":image})["exists"]:
        print(f"it is going to update the data {image}")
        img_db.find_modify({"image":image}, {"$set":to_insert})
    else:
        print(f"it is going to insert the data {image}")
        img_db.insert_data(to_insert)
    print("***************")
    with open(app.config["OUT"],'a') as f:
        for label in app.config["LABELS"]:
            f.write(image + "," +
            label["id"] + "," +
            label["name"] + "," +
            str(round(float(label["xMin"]))) + "," +
            str(round(float(label["xMax"]))) + "," +
            str(round(float(label["yMin"]))) + "," +
            str(round(float(label["yMax"]))) + "\n")
    app.config["LABELS"] = []
    return redirect(url_for('tagger'))

@app.route("/final")
def final():
    print(f"**** 8")
    return render_template('final.html')

@app.route('/download')
def download():
    print(f"**** 9")
    shutil.copyfile('out.csv', 'images/annotations.csv')
    res = shutil.make_archive('final', 'zip', 'images')
    return send_file(res,
                     mimetype='text/csv',
                     attachment_filename='final.zip',
                     as_attachment=True)

@app.route('/view')
def view():
    result = img_db.read_all_data()
    print("+++++++++++++++++")
    print(result)
    return json.dumps({"result": result["data"]}, default=str)
 
@app.route('/extract')
def extract_im():
     return render_template('extract.html')

# select data based on field image from db
@app.route('/get_image/<image>')
def get_image(image):
    print("it is wokring good")
    return json.dumps({"result": img_db.read_data({"image":image})["data"]}, default=str)

@app.route('/fetch_image', methods=["POST"])
def fetch_image():
    print(f"request.method : {request.method}")
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No files selected')
            return redirect('/')
        try:
            shutil.rmtree(img_path)
        except:
            pass
        os.mkdir(img_path)
        files = request.files.getlist("file")
        for f in files:
            img_file_path = os.path.join(img_path, f.filename)
            f.save(img_file_path)
    file_name = request.files['file']
    print(f"file_name.filename : {file_name.filename}")
    file_co_ords = img_db.read_data({"image":f"{file_name.filename}"})
    if file_co_ords["exists"]:
        print(file_co_ords)
        res = get_image_text(img_file_path, file_co_ords["data"]["labels"])
        # insert into extract collection
        img_db.insert_extracted_data(res)
        return json.dumps(res, default=str)
    
    print("it is not wokring good")
    return jsonify({"result": "something went wrong"})

@app.route('/about')
@calculate_proc_time
def test():
    func_resp = dict()
    pc_name = socket.gethostname()
    func_resp['message'] = "Application API working fine."
    func_resp['build_version'] = "1.0"
    func_resp['status'] = "success"
    func_resp['server_name'] = pc_name
    func_resp['os'] = sys.platform
    func_resp['now_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return func_resp

# create home api to call the home.html
@app.route('/home')
# @calculate_proc_time
def home():
    return render_template('home.html')

@app.errorhandler(404)
def not_found(error):
    func_resp = {'now_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 'message': "Please check the End Point, API End Point is not available", 'status': "failed"}
    return make_response(jsonify(func_resp), 404)
