#!/usr/bin/env python3
"""this is a flask app"""


from flask import Flask, abort, jsonify, redirect, request
from auth import Auth
from user import User
app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index():
    """index page"""
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'])
def users():
    """users page"""
    try:
        email = request.form['email']
        password = request.form['password']
        newuser = AUTH.register_user(email=email, password=password)
        return jsonify({"email": newuser.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """login page"""
    email = request.form['email']
    password = request.form['password']
    if not AUTH.valid_login(email=email, password=password):
        abort(401)
    else:
        newuserid = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', newuserid)
    return response


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """logout page"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user:
        AUTH.destroy_session(user_id=user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    """profile page"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({'email': user.email}), 200
    else:
        abort(403)

@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """get reset password token
    """
    email = request.get['email']
    user = AUTH._db._session.query(User).filter_by(email=email).first()
    if user is None:
        abort(403)
    resettoken = AUTH.get_reset_password_token(email=email)
    return jsonify({"email": email, "reset_token": resettoken}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
