from flask import Blueprint, render_template, redirect, request, make_response
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from . import token_handler
from .RBCMLModel import RBCMLModel
from .events import get_user_role
from .validation import *
from .database import db
from .user import User

main = Blueprint('main', __name__)


@main.route('/ping')
def view_ping():
    return 'pong'

@main.route('/')
def view_index():
    if request.cookies.get('jwt'):
        return redirect('/welcome')
    return redirect('/temporary_login')

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
        return render_template('TEMPORARYsignup.html')
    else:
        user = request.form.to_dict(flat=True)
        if validate_user(user):
            if not db.exists(user["tag"], "Tag", "User"):
                return db.insert(user, "User")
            return "User already exists.", 400
        return "Invalid user.", 400

@main.route('/temporary_login', methods=['GET','POST'])
def view_temporary_login():
    if request.method == 'GET':
        if request.cookies.get('jwt'):
            return redirect('/welcome')
        return render_template('TEMPORARYlogin.html')
    else:
        login = request.form.to_dict(flat=True)
        if validate_login(login):
            payload = {
                'tag': login['tag'],
                'iat': datetime.now(ZoneInfo('America/Sao_Paulo')),
                'nbf': datetime.now(ZoneInfo('America/Sao_Paulo')),
                'exp': datetime.now(ZoneInfo('America/Sao_Paulo')) + timedelta(days=1)
            }
            jwt = token_handler.create(payload)
            msg, status = db.insert({'token': jwt}, 'JWT')
            if status == 201:
                response = make_response(('Successfully authenticated', 200))
                response.set_cookie('jwt', jwt, expires=payload['exp'], secure=True, httponly=True, samesite='Strict')
                return response
            return 'Something went wrong while creating JWT', 400
        return 'Invalid login', 400

@main.route('/logout')
def view_logout():
    response = redirect('/')
    token = request.cookies.get('jwt')
    if token and validate_jwt(token, token_handler.generate_default_decode_options(['tag'])):
        db.delete(token, 'Token', 'JWT') 
    response.delete_cookie('jwt')
    return response

@main.route('/welcome', methods=['GET'])
def view_welcome():
    generic_response = redirect('/')
    token = request.cookies.get('jwt')
    if token:
        payload = validate_jwt(token, token_handler.generate_default_decode_options(['tag']))
        if payload:
            user_info = db.search(payload['tag'], 'tag', 'User')[0][:3]
            user = User(*user_info)
            return render_template('TEMPORARYwelcome.html', user=user)
        generic_response.delete_cookie('jwt')
    return generic_response

