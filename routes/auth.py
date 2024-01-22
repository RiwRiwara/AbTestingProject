from . import authAPI
from flask import jsonify, render_template, request, session, redirect, url_for
from config.db import db
from flask import flash

@authAPI.route('/testapi', methods=['GET'])
def api_entry():
    collection_names = db.list_collection_names()
    response = {
        'data': "API Running",
        'collection_names': collection_names
    }
    return jsonify(response)

@authAPI.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict()
        user = db.users.find_one({'email': data['email'], 'password': data['password']})
        if user:
            session['user_id'] = str(user['_id'])
            return redirect(url_for('defaultAPI.index'))
        else:
            return render_template('auth/login.html', title='Login', error='Invalid email or password')
    else:
        return render_template('auth/login.html', title='Login')

@authAPI.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form.to_dict()
        existing_user = db.users.find_one({'email': data['email']})
        if existing_user:
            
            return render_template('auth/register.html', title='Register', error='email already taken')
        else:
            db.users.insert_one(data)
            flash('Registration successful', 'success')
            return redirect(url_for('defaultAPI.index'))
    else:
        return render_template('auth/register.html', title='Register')
