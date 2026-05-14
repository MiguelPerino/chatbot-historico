from flask_login import LoginManager
from dotenv import load_dotenv
load_dotenv()  
 
from flask import Flask
from pymongo import MongoClient
import os
#serve para ler o arquivo .env e carrregar as variáveis
#de ambiente definidas nele

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')

    client = MongoClient(app.config['MONGO_URI'])
    app.db = client.get_database('chatbot')
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from bson import ObjectId
        from app.models.user import User
        user = app.db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            return User(user['_id'], user['username'], user['password'])
        return None
    
    try:
        client.admin.command('ping')
        print('✅ MongoDB conectado com sucesso!')

    except Exception as e:
        print(f'❌ Erro ao conectar no MongoDB: {e}')

    from app.routes.chat import chat_bp
    app.register_blueprint(chat_bp)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    return app