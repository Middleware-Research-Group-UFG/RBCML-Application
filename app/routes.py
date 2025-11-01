from flask import Blueprint, render_template, redirect, request, make_response
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import json
from . import token_handler
from .RBCMLModel import RBCMLModel
from .events import get_user_role
from .validation import *
from .database import db
from .user import User
from .session import Session

main = Blueprint('main', __name__)

@main.route('/ping')
def view_ping():
    return 'pong'

@main.route('/')
def view_index():
        return redirect('/home')
    
@main.route('/home')
def view_home():
    return render_template('home.html')

@main.route('/sessionsPage')
def view_sessionsPage():
    return render_template('sessionsPage.html')

@main.route('/createcall')
def view_createcall():
    token = request.cookies.get('jwt')
    if not token or not token_handler.decode(token, token_handler.generate_default_decode_options(['tag'])):
        resp = redirect('/home?action=login')
        resp.delete_cookie('jwt')
        return resp

    model_id = request.args.get('model_id')
    if not model_id:
        return redirect('/home')

    return render_template('createcall.html')

@main.route('/cadastro', methods=['POST'])
def view_signup():
    user = request.form.to_dict(flat=True)
    if validate_user(user):
        if not db.exists(user["tag"], "Tag", "User"):
            db.insert(user, "User")
            return "Cadastro realizado com sucesso!", 200
        return "Usuário já existe.", 400
    return "Usuário inválido.", 400

@main.route('/login', methods=['POST'])
def view_login():
    login = request.form.to_dict(flat=True)
    if validate_login(login):
        payload = {
            'tag': login['tag'],
            'iat': datetime.now(ZoneInfo('America/Sao_Paulo')),
            'nbf': datetime.now(ZoneInfo('America/Sao_Paulo')),
            'exp': datetime.now(ZoneInfo('America/Sao_Paulo')) + timedelta(days=1)
        }
        jwt = token_handler.create(payload)
        response = make_response("Login realizado com sucesso!", 200)
        response.set_cookie('jwt', jwt, expires=payload['exp'], secure=True, httponly=True, samesite='Strict')
        return response
    return 'Tag ou senha inválidos.', 400

@main.route('/createsession', methods=['GET', 'POST'])
def view_create_session():
    generic_response = redirect('/home?action=login')
    token = request.cookies.get('jwt')
    if token:
        payload = token_handler.decode(token, token_handler.generate_default_decode_options(['tag']))
        if payload:
            if request.method == 'GET':
                return render_template('TEMPORARYcreateSession.html')
            else:
                session = request.form.to_dict(flat=True)
                json_file = request.files.get('jsonparticipants')

                try:
                    participants = json.load(json_file)
                    participants = json.dumps(participants)
                except json.JSONDecodeError:
                    return "Unable to decode participants file.", 400
                
                data = {
                        "Creator": payload['tag'],
                        "ModelId": int(session["modelid"]),
                        "StartDate": session["startdate"],
                        "ExpirationDate": session["expirationdate"],
                        "Participants": participants
                    }

                if validate_session(data):
                    result = db.insert(data, "Session")
                    if result[1] == 201:
                        # Buscar a sessão recém-criada para enviar emails
                        try:
                            session_data = db.search(payload['tag'], 'Creator', 'Session')
                            if session_data:
                                # Pegar a última sessão criada (a mais recente)
                                latest_session = session_data[-1]
                                session_obj = Session(*latest_session)
                                
                                # Enviar emails para os participantes
                                # Pegar IP e porta do servidor (pode ser configurável)
                                url_ip = request.host.split(':')[0]
                                url_port = request.host.split(':')[1] if ':' in request.host else '443'
                                session_obj.invite_participants(url_ip, url_port)
                        except Exception as e:
                            print(f"Erro ao enviar emails: {e}")
                    return result
                return "Invalid Session format.", 400
        generic_response.delete_cookie('jwt')
    return generic_response

@main.route('/createModel', methods=['GET', 'POST'])
def view_create_model():
    generic_response = redirect('/home?action=login')
    token = request.cookies.get('jwt')
    if token:
        payload = token_handler.decode(token, token_handler.generate_default_decode_options(['tag']))
        if payload:
            if request.method == 'GET':
                return render_template('createModel.html')
            else:
                model = request.form.to_dict(flat=True)
                json_file = request.files.get('jsonModel')
                
                try:
                    model_data = json.load(json_file)
                except json.JSONDecodeError:
                    return "Unable to decode file.", 400

                if validate_model(model,model_data):
                    if not db.exists(model["name"], "name", "Model"):
                        json_content = json.dumps(model_data)

                        data = {
                            "Name": model["name"],
                            "Description": model["description"],
                            "Definition": json_content,
                        }
                        return db.insert(data, "Model")
                    return "Model name already exists.", 400
                return "Invalid Model format.", 400
        generic_response.delete_cookie('jwt')
    return generic_response


@main.route('/logout')
def view_logout():
    response = redirect('/home')
    response.delete_cookie('jwt')
    return response

@main.route('/session/<session_id>')
def view_session(session_id):
    generic_response = redirect('/home?action=login')
    token = request.cookies.get('jwt')
    if token:
        payload = token_handler.decode(token, token_handler.generate_default_decode_options(['tag']))
        if payload:
            user_tag = payload['tag']
            role = get_user_role(user_tag, session_id)
            if role:
                return render_template('session.html', user=user_tag, session=session_id, role=role)
            return "Você não tem permissão para acessar esta sessão.", 403
        generic_response.delete_cookie('jwt')
    return generic_response

@main.route('/invite')
def view_invite():
    session_id = request.args.get('session')
    user_tag = request.args.get('user')
    
    if not session_id or not user_tag:
        return redirect('/home')
    
    # Verificar se a sessão existe e se o usuário está convidado
    if db.exists(session_id, 'Id', 'Session'):
        response = redirect(f'/session/{session_id}')
        # Criar token temporário para o usuário
        payload = {
            'tag': user_tag,
            'iat': datetime.now(ZoneInfo('America/Sao_Paulo')),
            'nbf': datetime.now(ZoneInfo('America/Sao_Paulo')),
            'exp': datetime.now(ZoneInfo('America/Sao_Paulo')) + timedelta(hours=24)
        }
        jwt = token_handler.create(payload)
        response.set_cookie('jwt', jwt, expires=payload['exp'], secure=True, httponly=True, samesite='Strict')
        return response
    
    return "Sessão não encontrada.", 404

@main.route('/howtojson')
def view_howtojson():
    return render_template('howtojson.html')

# API Routes
@main.route('/api/models')
def api_get_models():
    """Retorna lista de modelos disponíveis em formato JSON"""
    try:
        models = db.search_all('Model')
        models_list = []
        
        for model in models:
            model_id, name, description, definition = model[:4]
            # Parsear a definição JSON para pegar os roles
            try:
                definition_data = json.loads(definition)
                roles = definition_data.get('roles', [])
            except:
                roles = []
            
            models_list.append({
                "id": model_id,
                "name": name,
                "description": description,
                "roles": roles,
                "imagem": {
                    "src": "images/SalaDeAula.jpg",  # Imagem padrão
                    "alt": name
                }
            })
        
        return json.dumps(models_list), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return json.dumps({"error": str(e)}), 500, {'Content-Type': 'application/json'}

@main.route('/api/sessions')
def api_get_sessions():
    """Retorna lista de sessões do usuário logado"""
    token = request.cookies.get('jwt')
    if not token:
        return json.dumps({"error": "Não autenticado"}), 401, {'Content-Type': 'application/json'}
    
    payload = token_handler.decode(token, token_handler.generate_default_decode_options(['tag']))
    if not payload:
        return json.dumps({"error": "Token inválido"}), 401, {'Content-Type': 'application/json'}
    
    try:
        user_tag = payload['tag']
        # Buscar sessões criadas pelo usuário
        sessions = db.search(user_tag, 'Creator', 'Session')
        
        sessions_list = []
        for session in sessions:
            session_id, creator, model_id, creation_date, start_date, expiration_date, participants = session
            
            # Buscar nome do modelo
            model_data = db.search(model_id, 'Id', 'Model')
            model_name = model_data[0][1] if model_data else "Modelo desconhecido"
            
            sessions_list.append({
                "id": session_id,
                "creator": creator,
                "model_id": model_id,
                "model_name": model_name,
                "creation_date": creation_date,
                "start_date": start_date,
                "expiration_date": expiration_date,
                "participants": json.loads(participants) if participants else {}
            })
        
        return json.dumps(sessions_list), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return json.dumps({"error": str(e)}), 500, {'Content-Type': 'application/json'}

@main.route('/api/model/<int:model_id>')
def api_get_model(model_id):
    """Retorna detalhes de um modelo específico"""
    try:
        model_data = db.search(model_id, 'Id', 'Model')
        if not model_data:
            return json.dumps({"error": "Modelo não encontrado"}), 404, {'Content-Type': 'application/json'}
        
        model_id, name, description, definition = model_data[0][:4]
        definition_data = json.loads(definition)
        
        result = {
            "id": model_id,
            "name": name,
            "description": description,
            "definition": definition_data
        }
        
        return json.dumps(result), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return json.dumps({"error": str(e)}), 500, {'Content-Type': 'application/json'}
