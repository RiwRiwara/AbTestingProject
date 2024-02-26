from . import labAPI
from flask import jsonify, render_template, request, session, redirect, url_for
from config.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash
from .frequentist import Frequentist
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as scs
import matplotlib.ticker as mtick
import seaborn as sns
from io import BytesIO
import base64

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
            'bar_chart': {
                'labels': "[A, B]",
                'data': [visitors_count_A, visitors_count_B]
            }
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
    
# Calucator ---------------------
@labAPI.route('/calculator')
def calculator():
    if is_logged_in() and session['admin']:
        # get args from url
        visitors_A = int(request.args.get('visitors_a') or 5000)
        visitors_B = int(request.args.get('visitors_b') or 5000)
        conversion_A = float(request.args.get('conversions_a') or 1000)
        conversion_B = float(request.args.get('conversions_b') or 1560)

        alpha = float(request.args.get('significance_level') or 0.05) 
        two_tails = request.args.get('method') or 'two'

        # Change twotails to bool
        if two_tails == 'two':
            two_tails = True
        else:
            two_tails = False

        # Calculate
        test = Frequentist(5000, 1000, 5000, 1560)
        test.get_z_value()

        # Print all the attributes
        print("Test Visitor A", test.visitors_A)
        print("Test Visitor B", test.visitors_B)
        print("Test Conversion A", test.conversions_A)
        print("Test Conversion B", test.conversions_B)
        print("Test Alpha", test.alpha)
        print("Test Two Tails", test.two_tails)
        print("Test Control CR", test.control_cr)
        print("Test Variant CR", test.variant_cr)
        print("Test Relative Difference", test.relative_difference)
        print("Test Control SE", test.control_se)
        print("Test Variant SE", test.variant_se)
        print("Test SE Difference", test.se_difference)
    
        z_score, p_value = test.z_test()
        print("Z Score", z_score)
        print("P Value", p_value)

        power = test.get_power()
        print("Power", power)

        
        fig_test = test.plot_test_visualisation()
        fig_power = test.plot_power()

        # Convert the test figure to a bytes-like object
        buf_test = BytesIO()
        fig_test.savefig(buf_test, format='png')
        buf_test.seek(0)

        # Encode the bytes-like object of the test figure as a base64 string
        fig_test_base64 = base64.b64encode(buf_test.read()).decode('utf-8')

        # Close the test figure to release memory
        plt.close(fig_test)

        # Convert the power figure to a bytes-like object
        buf_power = BytesIO()
        fig_power.savefig(buf_power, format='png')
        buf_power.seek(0)

        # Encode the bytes-like object of the power figure as a base64 string
        fig_power_base64 = base64.b64encode(buf_power.read()).decode('utf-8')

        # Close the power figure to release memory
        plt.close(fig_power)

        # Pass the base64 strings to the template
        return render_template('lab/calculator.html', title='Calculator', fig_test=fig_test_base64, fig_power=fig_power_base64)
    else:
        return redirect(url_for('labAPI.login_admin_lab'))

    