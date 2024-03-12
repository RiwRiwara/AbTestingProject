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
import random

def is_logged_in():
    return 'user_id' in session

def calculate_frequentist(visitors_A, visitors_B, conversion_A, conversion_B, alpha, two_tails):
    test = Frequentist(visitors_A, conversion_A, visitors_B, conversion_B, alpha=alpha, two_tails=two_tails)
    return  test

@labAPI.route('/dashboard')
def dashboard():
    if is_logged_in() and session['admin']:
        page = request.args.get('page') or 'all'
        button = request.args.get('button') or 'all'

        visitors_count_A = db.visitors.count_documents({'page': 'A'})
        visitors_count_B = db.visitors.count_documents({'page': 'B'})

        visitors_click_A = db.click_actions.count_documents({'page': 'A'})
        visitors_click_B = db.click_actions.count_documents({'page': 'B'})
        
        

        if page == 'all':
            visitors_count_display = visitors_count_A + visitors_count_B
        else:
            visitors_count_display = db.visitors.count_documents({'page': page})

        test = calculate_frequentist(visitors_count_A, visitors_count_B, visitors_click_A, visitors_click_B, 0.05, True)

        test.get_z_value()
        z_score, p_value = test.z_test()
        power = test.get_power()

        z_score, p_value = test.z_test()
        isSignificant = p_value < 0.05


        data = {
            'page': page,
            'visitors_click_A': visitors_click_A,
            'visitors_click_B': visitors_click_B,
            'button': button,
            'visitors_count_display': visitors_count_display,
            'frequentist': {
                'z_score': z_score,
                'p_value': p_value,
                'power': power,
                'test' : test
            },
            'visitors_count': {
                'A': visitors_count_A,
                'B': visitors_count_B
            },
            'bar_chart': {
                'labels': "[A, B]",
                'data': [visitors_count_A, visitors_count_B]
            }
        }

        return render_template('lab/dashboard.html', title='Dashboard', data=data, isSignificant=isSignificant)
    else:
        return redirect(url_for('labAPI.login_admin_lab'))