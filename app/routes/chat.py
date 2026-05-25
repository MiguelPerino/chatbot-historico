from flask import render_template, request, jsonify, Blueprint, current_app
from flask_login import current_user, login_required
from app.models.talk import create_talk, search_talk, add_message, new_title, delete_talk
from app.services.llm import call_llm

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/')
@login_required
def home():
    return render_template('index.html')


@chat_bp.route('/chat/create', methods=['POST'])
@login_required
def create_chat():
    db = current_app.db
    return jsonify({'id': create_talk(db, current_user.id)})
#colocar um render_template para conversa aq
    
@chat_bp.route('/chat/<id>/message', methods=['POST'])
@login_required
def receive_message(id):
    #pegar a mensagem, buscar no banco, montar a lista de mensagempro gemini, chamar ele
    # salvar no banco a resposta e retornar em JSON
    db = current_app.db
    data = request.get_json()
    message = data['message']

    chat = search_talk(db, id)
    history = chat['message']

    if len(history) == 0:
        prompt = f'Gere um título curto de no máximo 5 palavras para uma conversa que começa com: "{message}". Responda APENAS o título, sem explicações, sem pontuação.'
        title = call_llm(prompt)

        new_title(db, id, title)

    # gemini_history = [{'role': m['role'], 'parts': m['content']} for m in history]    // nao aceita esse 'tipo de entrada
    # gemini_history.append({'role': 'user', 'parts': [message]})


    #MUDE AQUI O PROMPT DE COMO DESEJA QUE ELE TE RESPONDA 
    prompt ='''
        Você é um assistente profissional altamente qualificado, especializado em fornecer respostas claras, precisas e bem estruturadas.

        Diretrizes de comportamento:

        Utilize linguagem formal, mas acessível.
        Seja direto e evite respostas vagas ou genéricas.
        Quando possível, forneça exemplos práticos para facilitar o entendimento.
        Caso a pergunta seja ambígua, peça esclarecimentos antes de responder.
        Evite opiniões pessoais; priorize informações baseadas em fatos.
        Mantenha um tom respeitoso e profissional em todas as interações.
        Adapte o nível de detalhamento conforme a complexidade da pergunta.

        Seu objetivo é atuar como um especialista confiável, auxiliando o usuário de forma eficiente e profissional..\n\n'''

    for m in history:
        role = "Usuário" if m['role'] == 'user' else "Assistente"
        prompt += f"{role}: {m['content']}\n"

    prompt += f"Usuário: {message}\nAssistente:"

    
    # response = call_llm(gemini_history)
    response = call_llm(prompt)
    # response = 'teste'

    add_message(db, id, 'user', message)
    add_message(db, id, 'model', response)

    return jsonify({
        'response': response,
        'is_first_message': len(history) == 0   #para mudar o nome da conversa quando for a primeira msg
        
    })
    


@chat_bp.route('/chat/<id>/history', methods=['GET'])
@login_required
def return_history(id):
    db = current_app.db

    conversations = search_talk(db, id)
    if not conversations:
        return jsonify({'message': "Conversa não encontrada"}), 404
    
    conversations['_id'] = str(conversations['_id'])
    return jsonify(conversations)

@chat_bp.route('/chats', methods=['GET'])
@login_required
def chats():
    db = current_app.db 

    # Primeiro {}, filtro com user_id, ou seja, traz todos os documentos daquele usuário, que está logado no momento com current_user
    # Segundo {'title': 1}, projeção, diz quais campos retornar. Aqui traz só o title e o _id
    conversations = list(db.conversas.find({'user_id': current_user.id}, {'title': 1}))   #conversas é o nome que esta no banco
    for c in conversations:
        c['_id'] = str(c['_id'])
    #transforma tudo em str o ObjectId

    return jsonify(conversations)


@chat_bp.route('/delete/<id>', methods=['DELETE'])
@login_required
def delete_chat(id):
    db = current_app.db 
    delete_talk(db, id)
    return jsonify({'message': 'Conversa deletada.'})