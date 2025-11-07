from flask import Blueprint, render_template, redirect, request, make_response, jsonify
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import json
import uuid
from pathlib import Path
from . import token_handler
from .RBCMLModel import RBCMLModel
from .events import get_user_role
from .validation import *
from .database import db
from .user import User

main = Blueprint('main', __name__)

# Armazenamento em memória de chamadas ativas
# Em produção, use Redis ou banco de dados
active_calls = {}

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

    model_name = request.args.get('nome')
    if not model_name:
        return redirect('/home')

    return render_template('createcall.html')

@main.route('/cadastro', methods=['GET', 'POST'])
def view_signup():
    if request.method == 'GET':
        return render_template('/home?action=cadastro')
    else:
        user = request.form.to_dict(flat=True)
        if validate_user(user):
            if not db.exists(user["tag"], "Tag", "User"):
                return "Cadastro realizado com sucesso!", 200
            return "Usuário já existe.", 400
        return "Usuário inválido.", 400

# Adaptar para as mudanças do login (pagina new login retirada)
@main.route('/login', methods=['GET','POST'])
def view_temporary_login():
    if request.method == 'GET':
        if request.cookies.get('jwt'):
            return redirect('/home')
        return render_template('/home?action=login')
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
            response = redirect('/home')
            response.set_cookie('jwt', jwt, expires=payload['exp'], secure=True, httponly=True, samesite='Strict')
            return response
        return 'Invalid login', 400

# mudar newlogin
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
                    return db.insert(data, "Session")
                return "Invalid Session format.", 400
        generic_response.delete_cookie('jwt')
    return generic_response

# mudar newlogin
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


# Remover rota
@main.route('/welcome', methods=['GET'])
def view_welcome():
    generic_response = redirect('/')
    token = request.cookies.get('jwt')
    if token:
        payload = token_handler.decode(token, token_handler.generate_default_decode_options(['tag']))
        if payload:
            user_info = db.search(payload['tag'], 'tag', 'User')[0][:3]
            user = User(*user_info)
            return render_template('TEMPORARYwelcome.html', user=user)
        generic_response.delete_cookie('jwt')
    return generic_response
#########################################

# possivelmente remover essa rota depois
@main.route('/login', methods=['GET', 'POST'])
def view_login():
    if request.method == 'GET':
        return render_template('login.html', roles=RBCMLModel.get_role_names())
    else:
        role = request.form.get('option')
        return redirect(f'/user/{role}')
#########################################


# possivelmente remover essa rota depois
@main.route('/logout')
def view_logout():
    response = redirect('/')
    response.delete_cookie('jwt')
    return response
#########################################

# possivelmente remover essa rota depois
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
###########################################

# possivelmente remover essa rota depois
@main.route('/user/<user>')
def view_user(user):
    return render_template('user.html', user=user)
##########################################

# possivelmente remover essa rota depois
@main.route('/user/<user>/session/<session>')
def view_session(user, session):
    role = get_user_role(user, session)
    return render_template('session.html', user=user, session=session, role=role)
###########################################

# ============= NOVAS FUNCIONALIDADES DE CHAMADAS =============

@main.route('/api/create-call', methods=['POST'])
def api_create_call():
    """
    Cria uma nova chamada de vídeo
    - Usa modelos do model.json (não do banco)
    - Não requer usuários pré-cadastrados
    - Gera link genérico compartilhável
    """
    token = request.cookies.get('jwt')
    if not token:
        return jsonify({'error': 'Unauthorized - Login required'}), 401
    
    payload = token_handler.decode(token, token_handler.generate_default_decode_options(['tag']))
    if not payload:
        return jsonify({'error': 'Invalid token'}), 401
    
    try:
        data = request.get_json()
        model_name = data.get('model_name')
        participants = data.get('participants', {})
        
        if not model_name:
            return jsonify({'error': 'Model name is required'}), 400
        
        # Carregar modelos do model.json
        model_json_path = Path(__file__).parent / 'static' / 'model.json'
        with open(model_json_path, 'r', encoding='utf-8') as f:
            models = json.load(f)
        
        # Encontrar o modelo selecionado
        selected_model = next((m for m in models if m.get('name') == model_name), None)
        if not selected_model or not selected_model.get('roles'):
            return jsonify({'error': 'Model not found or has no roles'}), 404
        
        # Gerar ID único para a chamada
        call_id = str(uuid.uuid4())[:8]  # ID curto para facilitar compartilhamento
        creator_tag = payload['tag']
        
        # Adicionar criador aos participantes se não estiver
        if creator_tag not in participants:
            participants[creator_tag] = {
                'name': creator_tag,
                'roles': [selected_model['roles'][0]]
            }
        
        # Criar dados da chamada
        call_data = {
            'call_id': call_id,
            'model_name': model_name,
            'model': selected_model,
            'creator': creator_tag,
            'participants': participants,
            'created_at': datetime.now(ZoneInfo('America/Sao_Paulo')).isoformat(),
            'expires_at': (datetime.now(ZoneInfo('America/Sao_Paulo')) + timedelta(hours=24)).isoformat()
        }
        
        # Armazenar chamada ativa
        active_calls[call_id] = call_data
        
        return jsonify({
            'success': True,
            'call_id': call_id,
            'call_url': f'/call/{call_id}',
            'share_url': f'{request.host_url}call/{call_id}'
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error creating call: {str(e)}'}), 500

@main.route('/call/<call_id>')
def view_call(call_id):
    """
    Acessa uma chamada ativa
    - Link genérico (não requer role específica)
    - Qualquer pessoa com o link pode entrar
    - Usuários não precisam estar pré-cadastrados
    """
    # Verificar se a chamada existe
    if call_id not in active_calls:
        return render_template('error.html', 
                             message='Chamada não encontrada ou expirada'), 404
    
    call_data = active_calls[call_id]
    
    # Verificar se expirou
    expires_at = datetime.fromisoformat(call_data['expires_at'])
    if datetime.now(ZoneInfo('America/Sao_Paulo')) > expires_at:
        del active_calls[call_id]
        return render_template('error.html', 
                             message='Esta chamada expirou'), 410
    
    # Obter informações do usuário (ou gerar guest)
    token = request.cookies.get('jwt')
    user_tag = f'guest_{uuid.uuid4().hex[:6]}'
    user_role = 'Participant'
    
    if token:
        payload = token_handler.decode(token, token_handler.generate_default_decode_options(['tag']))
        if payload:
            user_tag = payload['tag']
    
    # Verificar se é participante conhecido
    if user_tag in call_data['participants']:
        participant_info = call_data['participants'][user_tag]
        if isinstance(participant_info, dict) and 'roles' in participant_info:
            user_role = participant_info['roles'][0] if participant_info['roles'] else 'Participant'
        elif isinstance(participant_info, list):
            user_role = participant_info[0] if participant_info else 'Participant'
    else:
        # Atribuir primeira role disponível para novos participantes
        roles = call_data['model'].get('roles', ['Participant'])
        user_role = roles[0] if roles else 'Participant'
    
    # Renderizar página de chamada
    return render_template('session.html', 
                         user=user_tag, 
                         session=call_id,
                         role=user_role)

@main.route('/api/send-invites', methods=['POST'])
def api_send_invites():
    """
    Envia convites por email para participantes
    """
    token = request.cookies.get('jwt')
    if not token:
        return jsonify({'error': 'Unauthorized'}), 401
    
    payload = token_handler.decode(token, token_handler.generate_default_decode_options(['tag']))
    if not payload:
        return jsonify({'error': 'Invalid token'}), 401
    
    try:
        from .email import send
        
        data = request.get_json()
        call_id = data.get('call_id')
        invites = data.get('invites', [])  # Lista de {email, role}
        
        if not call_id or call_id not in active_calls:
            return jsonify({'error': 'Invalid call ID'}), 400
        
        call_data = active_calls[call_id]
        call_url = f"{request.host_url}call/{call_id}"
        
        sent = 0
        failed = 0
        
        for invite in invites:
            email = invite.get('email')
            role = invite.get('role', 'Participant')
            
            if not email:
                continue
            
            try:
                subject = f"Convite para videochamada - {call_data['model_name']}"
                content = f"""
Olá!

{payload['tag']} convidou você para participar de uma videochamada.

Modelo: {call_data['model_name']}
Sua role: {role}

Clique no link abaixo para entrar:
{call_url}

A chamada expira em: {call_data['expires_at']}

---
RBCML Application
"""
                send(subject, content, email)
                sent += 1
            except Exception as e:
                print(f"Erro ao enviar email para {email}: {e}")
                failed += 1
        
        return jsonify({
            'success': True,
            'sent': sent,
            'failed': failed
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error sending invites: {str(e)}'}), 500

@main.route('/api/active-calls', methods=['GET'])
def api_active_calls():
    """Lista chamadas ativas do usuário"""
    token = request.cookies.get('jwt')
    if not token:
        return jsonify({'error': 'Unauthorized'}), 401
    
    payload = token_handler.decode(token, token_handler.generate_default_decode_options(['tag']))
    if not payload:
        return jsonify({'error': 'Invalid token'}), 401
    
    user_tag = payload['tag']
    user_calls = []
    
    for call_id, call_data in active_calls.items():
        if call_data['creator'] == user_tag or user_tag in call_data['participants']:
            user_calls.append({
                'call_id': call_id,
                'model_name': call_data['model_name'],
                'created_at': call_data['created_at'],
                'call_url': f'/call/{call_id}',
                'is_creator': call_data['creator'] == user_tag
            })
    
    return jsonify({'calls': user_calls}), 200

@main.route('/api/models/<model_name>', methods=['GET'])
def api_get_model(model_name):
    """Retorna dados de um modelo do model.json"""
    try:
        model_json_path = Path(__file__).parent / 'static' / 'model.json'
        with open(model_json_path, 'r', encoding='utf-8') as f:
            models = json.load(f)
        
        selected_model = next((m for m in models if m.get('name') == model_name), None)
        if not selected_model:
            return jsonify({'error': 'Model not found'}), 404
        
        return jsonify(selected_model), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
