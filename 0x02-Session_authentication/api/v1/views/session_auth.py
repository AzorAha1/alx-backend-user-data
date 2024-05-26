#!/usr/bin/env python3
"""this will contain session route"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from api.v1.auth.session_auth import SessionAuth
from models.user import User

session_auth = SessionAuth()


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """user login and creates a session"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({'error': 'email missing'}), 400
    if not password:
        return jsonify({'error': 'password missing'}), 400

    try:
        getuserinstance = User.search({'email': email})
        if not getuserinstance:
            return jsonify({'error': 'no user found for this email'}), 404
        user = getuserinstance[0]
    except Exception:
        return jsonify({'error': 'no user found for this email'}), 404
    if not user.is_valid_password(password):
        return jsonify({'error': 'wrong password'}), 401
    sessionid = session_auth.create_session(user_id=user.id)
    response = jsonify(user.to_dict())
    response.set_cookie('SESSION_NAME', sessionid)
    return response
