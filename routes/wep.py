from . import defaultAPI
from flask import  jsonify, render_template, request, session, redirect, url_for, send_file, send_from_directory
import json
from config.db import db


@defaultAPI.route('/testapi', methods=['GET'])
def api_entry():
    collection_names = db.list_collection_names()
    response = {
        'data': "API Running",
        'collection_names': collection_names
    }
    return jsonify(response)


@defaultAPI.route('/')
def index():
    return render_template('index.html')

@defaultAPI.route('/login')
def login():
    return render_template('login.html')

@defaultAPI.route('/img/<filename>')
def send_img(filename):
    return send_from_directory('./static/img', filename)

@defaultAPI.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))
