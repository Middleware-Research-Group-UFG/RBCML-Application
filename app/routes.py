from flask import Blueprint, render_template, redirect, request

from .RBCMLModel import RBCMLModel
from .events import get_user_role

import sqlite3
import validation as v

main = Blueprint('main', __name__)


@main.route('/ping')
def view_ping():
    return 'pong'

@main.route('/')
def view_index():
    return redirect('/login')

@main.route('/login', methods=['GET', 'POST'])
def view_login():
    if request.method == 'GET':
        return render_template('login.html', roles=RBCMLModel.get_role_names())
    else:
        role = request.form.get('option')
        return redirect(f'/user/{role}')

@main.route('/user/<user>')
def view_user(user):
    return render_template('user.html', user=user)

@main.route('/user/<user>/session/<session>')
def view_session(user, session):
    role = get_user_role(user, session)
    return render_template('session.html', user=user, session=session, role=role)

@main.route('/createRole', methods=['GET', 'POST'])
def view_create_role():
    if request.method == 'GET':
        return render_template('createRole.html')
    else:
        role = request.form
        sV = 'sendVideo' in role
        rV = 'receiveVideo' in role
        sA = 'sendAudio' in role
        rA = 'receiveAudio' in role
        sS = 'sendString' in role
        rS = 'receiveString' in role
        capability = (sV, rV, sA, rA, sS, rS)

        if RBCMLModel.set_role(role.get('roleName'), capability):
           return "Role created successfully"
        else:
           return "Role not created"

@main.route('/signup', methods=['GET', 'POST'])
def view_signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        tag = request.form.get('tag')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([tag, name, email, password]):
            return "All fields are required", 400

        if not all(v.validate_string(field) for field in [tag, name, email, password]):
            return "Invalid characters in input fields", 400

        length_checks = [
            (tag, 20, "Tag"),
            (name, 64, "Name"),
            (email, 254, "Email"),
            (password, 128, "Password")
        ]
        
        for value, max_len, field_name in length_checks:
            if len(value) > max_len:
                return f"{field_name} exceeds maximum length of {max_len} characters", 400

        conn = None
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            cursor.execute('SELECT Tag FROM User WHERE Tag = ?', (tag,))
            if cursor.fetchone():
                return "User tag already exists", 400

            cursor.execute('''
                INSERT INTO User (Tag, Name, Email, Password)
                VALUES (?, ?, ?, ?)
            ''', (tag, name, email, password))
            conn.commit()
            return "User created successfully"
        
        except sqlite3.IntegrityError as e:
            return f"Database constraint error: {str(e)}", 400
        except sqlite3.Error as e:
            return f"Database error: {str(e)}", 500
        finally:
            if conn:
                conn.close()