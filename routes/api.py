from . import apiAPI
from flask import jsonify, render_template, request, session, redirect, url_for
from config.db import db
from datetime import datetime

@apiAPI.route('/v1', methods=['GET'])
def api_entry():
    response = {
        'data': "API Running",
    }
    return jsonify(response)


@apiAPI.route('/save-click-action', methods=['POST'])
def save_click_action():
    # Extract data from the request
    data = request.json

    # Validate and extract necessary data
    page = data.get('page')
    if not page:
        return jsonify({'error': 'Page parameter is missing'}), 400

    user_id = session.get('user_id') or 'anonymous'

    try:
        db.click_actions.insert_one({
            'date_click': datetime.now(),
            'user_id': user_id,
            'page': page
        })
        return jsonify({'success': 'Click action saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500