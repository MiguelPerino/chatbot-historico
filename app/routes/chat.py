from flask import render_template, request, jsonify, Blueprint, current_app
from app.models.talk import create_talk, search_talk, add_message
from app.services.llm import call_llm

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/')
def home():
    return render_template('index.html')


@chat_bp.route('/chat/create', methods=['POST'])
def create_chat():
    db = current_app.db
    return jsonify({'id': create_talk(db)})
    

@chat_bp.route('/chat/<id>/message', methods=['POST'])
def receive_message(id):
    #pegar a mensagem, buscar no banco, montar a lista de mensagempro gemini, chamar ele
    # salvar no banco a resposta e retornar em JSON
    db = current_app.db
    data = request.get_json()
    message = data['message']

    chat = search_talk(db, id)
    history = chat['message']

    # gemini_history = [{'role': m['role'], 'parts': m['content']} for m in history]    // nao aceita esse 'tipo de entrada
    # gemini_history.append({'role': 'user', 'parts': [message]})

    #ele aceita assim, como uma string normal
    prompt ="Você é um assistente descontraído, amigável e usa linguagem informal.\n\n"

    for m in history:
        role = "Usuário" if m['role'] == 'user' else "Assistente"
        prompt += f"{role}: {m['content']}\n"

    prompt += f"Usuário: {message}\nAssistente:"


    # response = call_llm(gemini_history)
    response = call_llm(prompt)
    # response = 'teste'

    add_message(db, id, 'user', message)
    add_message(db, id, 'model', response)

    return jsonify({'response': response})
    


@chat_bp.route('/chat/<id>/history', methods=['GET'])
def return_history(id):
    pass


@chat_bp.route('/chats', methods=['GET'])
def chats():
    pass


