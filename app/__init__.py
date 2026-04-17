from dotenv import load_dotenv
load_dotenv()  
 
from flask import Flask
from pymongo import MongoClient
import os
from app.routes.chat import chat_bp
#serve para ler o arquivo .env e carrregar as variáveis
#de ambiente definidas nele

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')

    client = MongoClient(app.config['MONGO_URI'])
    app.db = client.get_database('chatbot')
    app.register_blueprint(chat_bp)

    try:
        client.admin.command('ping')
        print('✅ MongoDB conectado com sucesso!')

    except Exception as e:
        print(f'❌ Erro ao conectar no MongoDB: {e}')

    return app