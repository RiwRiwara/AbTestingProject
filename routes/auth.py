from . import authAPI
from flask import jsonify, render_template, request, session, redirect, url_for
from config.db import db
from werkzeug.security import generate_password_hash, check_password_hash
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
        user = db.users.find_one({'email': data['email']})

        if user and user['password'] == data['password']:
            session['user_id'] = str(user['_id'])
            return redirect(url_for('defaultAPI.indexA')) 
        else:
            error = 'Invalid email or password'
            return render_template('auth/login.html', title='Login', error=error)
    else:  
        if is_logged_in():
            return redirect(url_for('defaultAPI.indexA'))
        return render_template('auth/login.html', title='Login', error='')
    
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
        if is_logged_in():
            return redirect(url_for('defaultAPI.index'))
        return render_template('auth/register.html', title='Register')

@authAPI.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('defaultAPI.index'))

@authAPI.route('/test-session')
def test_session():
    if 'user_id' in session:
        return 'User is logged in. User ID: ' + session['user_id']
    else:
        return 'User is not logged in.'

def is_logged_in():
    return 'user_id' in session
def is_not_logged_in():
    return not is_logged_in()

def login_required(func):
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('authAPI.login'))
        return func(*args, **kwargs)
    return decorated_function
