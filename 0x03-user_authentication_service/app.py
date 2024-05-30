#!/usr/bin/env python3
"""this is a flask app"""


from flask import Flask, abort, jsonify, request
from auth import Auth
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
