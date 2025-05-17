from flask import Blueprint, render_template, redirect, request

from .RBCMLModel import RBCMLModel
from .events import get_user_role
from .validation import validate_user
from .database import db

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
    method = request.method
    if method == 'GET':
        return render_template('TEMPORARYsignup.html')
    elif method == 'POST':
        user = request.form.to_dict(flat=True)
        if validate_user(user):
            if not db.exists(user["tag"], "Tag", "User"):
                return db.insert(user, "User")
            return "User already exists.", 400
        
        return "Invalid user.", 400

    return "Method '{method}' is not allowed."

