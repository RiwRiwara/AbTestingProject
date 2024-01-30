from . import defaultAPI
from flask import  jsonify, render_template, request, session, redirect, url_for, send_file, send_from_directory
import json
from .auth import is_logged_in, login_required

@defaultAPI.route('/')
def index():
    return render_template('index.html', title='Home A')
@defaultAPI.route('/A')
def indexA():
    return render_template('index.html', title='Home A')

@defaultAPI.route('/B')
def indexB():
    return render_template('indexB.html', title='Home B')

@defaultAPI.route('/img/<filename>')
def send_img(filename):
    return send_from_directory('./static/img', filename)

@defaultAPI.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))
