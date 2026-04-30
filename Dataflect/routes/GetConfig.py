import os
import json
from flask import Blueprint, request, session, jsonify
from config_generator import load_config_yaml, ensure_config_yaml

config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Deteflect.yaml")
config = ensure_config_yaml(config_path)

GetConfig = Blueprint('GetConfig', __name__)
SECRET_KEY = config.get("SecretKey", "DataFlect_Secure_Key_2024")
SESSION_TIMEOUT = 91800


@GetConfig.route('/config/get', methods=['GET'])
def get_config():
    config = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Deteflect.yaml")
    return jsonify(ensure_config_yaml(config))


@GetConfig.route('/config/security/<senha>/<user>', methods=['POST'])
def login(senha, user):
    stored_password = config.get("Senha", "admin123")
    stored_user = config.get("Usuario", "administrador")
    
    if senha == stored_password and user == stored_user:
        session['logged_in'] = True
        session['user'] = user
        session['login_time'] = __import__('time').time()
        session.permanent = True
        
        return jsonify({
            "success": True,
            "message": "Login realizado com sucesso",
            "user": user
        })
    else:
        return jsonify({
            "success": False,
            "message": "Credenciais inválidas"
        }), 401


@GetConfig.route('/config/checklogin', methods=['GET'])
def check_login():
    if 'logged_in' not in session or not session.get('logged_in'):
        return jsonify({
            "logged_in": False,
            "message": "Usuário não está logado"
        })

    login_time = session.get('login_time', 0)
    current_time = __import__('time').time()
    elapsed_time = current_time - login_time
    
    if elapsed_time > SESSION_TIMEOUT:
        session.clear()
        return jsonify({
            "logged_in": False,
            "message": "Sessão expirada"
        })
    
    return jsonify({
        "logged_in": True,
        "user": session.get('user'),
        "remaining_time": SESSION_TIMEOUT - elapsed_time
    })


@GetConfig.route('/config/logout', methods=['POST'])
def logout():
    user = session.get('user', 'Unknown')
    session.clear()
    
    return jsonify({
        "success": True,
        "message": f"Logout realizado com sucesso para o usuário {user}"
    })