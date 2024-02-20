from . import labAPI
from flask import jsonify, render_template, request, session, redirect, url_for
from config.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash

@labAPI.route('/testapi', methods=['GET'])
def api_entry():
    collection_names = db.list_collection_names()
    response = {
        'data': "API Running",
        'collection_names': collection_names
    }
    return jsonify(response)


def is_logged_in():
    return 'user_id' in session

@labAPI.route('/login', methods=['GET', 'POST'])
def login_admin_lab():
    if request.method == 'POST':
        data = request.form.to_dict()
        user = db.users.find_one({'email': data['email']})
        if user and user['password'] == data['password']:
            session['user_id'] = str(user['_id'])
            session['admin'] = True
            return redirect(url_for('labAPI.dashboard'))
        else:
            error = 'Invalid email or password'
            return render_template('lab/login.html', title='Login', error=error)
    else:
        if is_logged_in():
            return redirect(url_for('labAPI.dashboard'))
        return render_template('lab/login.html', title='Login', error='')
    
@labAPI.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('labAPI.login_admin_lab'))

@labAPI.route('/dashboard')
def dashboard():
    if is_logged_in() and session['admin']:
        page = request.args.get('page') or 'all'
        button = request.args.get('button') or 'all'

        visitors_count_A = db.visitors.count_documents({'page': 'A'})
        visitors_count_B = db.visitors.count_documents({'page': 'B'})

        if page == 'all':
            visitors_count_display = visitors_count_A + visitors_count_B
        else:
            visitors_count_display = db.visitors.count_documents({'page': page})


        data = {
            'page': page,
            'button': button,
            'visitors_count_display': visitors_count_display,
            'visitors_count': {
                'A': visitors_count_A,
                'B': visitors_count_B
            },
        }
        return render_template('lab/dashboard.html', title='Dashboard', data=data)
    else:
        return redirect(url_for('labAPI.login_admin_lab'))
@labAPI.route('/reach', methods=['GET'])
def reach():
    if is_logged_in() and session['admin']:

        visitors_count_A = db.visitors.count_documents({'page': 'A'})
        visitors_click_A = db.click_actions.count_documents({'page': 'A'})
        visitors_count_B = db.visitors.count_documents({'page': 'B'})
        visitors_click_B = db.click_actions.count_documents({'page': 'B'})


        data = {
            'visitors_count': {
                'A': visitors_count_A,
                'B': visitors_count_B
            },
            'visitors_click': {
                'A': visitors_click_A,
                'B': visitors_click_B
            },
        }
        return render_template('lab/reach.html', title='Reach', data=data)
    else:
        return redirect(url_for('labAPI.login_admin_lab'))
    