from . import apiAPI
from flask import jsonify, render_template, request, session, redirect, url_for
from config.db import db
from datetime import datetime
import random
from datetime import timedelta

@apiAPI.route('/v1', methods=['GET'])
def api_entry():
    response = {
        'data': "API Running",
    }
    return jsonify(response)


@apiAPI.route('/save-click-action', methods=['POST'])
def save_click_action():
    data = request.json

    page = data.get('page')
    if not page:
        return jsonify({'error': 'Page parameter is missing'}), 400

    user_id = session.get('user_id') or 'anonymous'

    try:
        db.click_actions.insert_one({
            'date_click': datetime.now(),
            'user_id': user_id,
            'button': data.get('button'),
            'page': page
        })
        return jsonify({'success': 'Click action saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@apiAPI.route('/testpage', methods=['GET'])
def testpage():
    return render_template('test.html')

# Define a function to generate a random datetime within a specified range
def random_datetime(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

@apiAPI.route('/generate-random-click-action', methods=['POST'])
def generate_random_click_action():
    data = request.json
    num_actions = data.get('num_actions', 1)  # Default to generating 1 action if num_actions not provided

    buttons = ['register', 'best-seller', 'save']
    pages = ['A', 'B']
    start_date = datetime.now() - timedelta(days=60)  # Two months ago

    user_id = session.get('user_id') or 'anonymous'

    try:
        for _ in range(num_actions):
            # Generate random click action
            random_button = random.choice(buttons)
            random_page = random.choice(pages)
            random_date = random_datetime(start_date, datetime.now())

            db.click_actions.insert_one({
                'date_click': random_date,
                'user_id': user_id,
                'button': random_button,
                'page': random_page
            })

            # Generate random visitor data
            random_page = random.choice(pages)
            random_date = random_datetime(start_date, datetime.now())

        for _ in range(num_actions+100):
            db.visitors.insert_one({
                'date_visit': random_date,
                'user_id': user_id,
                'page': random_page
            })

        return jsonify({'success': f'{num_actions} random click actions and visitor data saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
