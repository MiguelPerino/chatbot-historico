# Chatbot com Histórico Persistente

Aplicação web de chatbot com inteligência artificial, histórico de conversas persistido em banco de dados e autenticação de usuários.

## Tecnologias

- **Python** com **Flask** — back-end e API REST
- **MongoDB Atlas** — banco de dados NoSQL para persistência das conversas e usuários
- **Google Gemini API** (`gemini-2.5-flash-lite`) — modelo de linguagem para geração de respostas
- **Flask-Login** — gerenciamento de sessões e autenticação
- **Flask-Bcrypt** — criptografia de senhas
- **HTML, CSS e JavaScript** — interface web sem frameworks externos
- **Gunicorn** — servidor WSGI para produção

## Funcionalidades

- Registro e login de usuários com senha criptografada
- Criação de múltiplas conversas por usuário
- Histórico de mensagens persistido no MongoDB
- Geração automática de título da conversa baseado na primeira mensagem
- Cada usuário acessa apenas suas próprias conversas
- Rotas protegidas com autenticação obrigatória
- Interface com sidebar listando conversas anteriores

## Estrutura do Projeto

```
chatbot/
├── app/
│   ├── __init__.py          # factory do app Flask, configuração do LoginManager
│   ├── models/
│   │   ├── talk.py          # operações no MongoDB para conversas
│   │   └── user.py          # classe User compatível com Flask-Login
│   ├── routes/
│   │   ├── chat.py          # rotas do chat (protegidas com @login_required)
│   │   └── auth.py          # rotas de registro, login e logout
│   └── services/
│       └── llm.py           # integração com a API do Gemini
├── static/
│   ├── css/style.css
│   └── js/
│       ├── chat.js          # lógica do chat no front-end
│       └── auth.js          # lógica de login e registro
├── templates/
│   ├── index.html           # interface principal do chat
│   └── login.html           # página de login e registro
├── .env.example
├── Procfile
├── requirements.txt
└── run.py
```

## Rotas da API

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| GET | `/` | Interface principal | Não |
| GET | `/login` | Página de login | Não |
| POST | `/login` | Autenticar usuário | Não |
| POST | `/register` | Registrar usuário | Não |
| POST | `/logout` | Encerrar sessão | Sim |
| POST | `/chat/create` | Criar nova conversa | Sim |
| POST | `/chat/<id>/message` | Enviar mensagem e receber resposta da IA | Sim |
| GET | `/chat/<id>/history` | Buscar histórico de uma conversa | Sim |
| GET | `/chats` | Listar todas as conversas do usuário | Sim |

## Como rodar localmente

**1. Clone o repositório e crie o ambiente virtual**
```bash
git clone https://github.com/seu-usuario/chatbot-historico.git
cd chatbot-historico
python -m venv venv
venv\Scripts\activate  # Windows
```

**2. Instale as dependências**
```bash
pip install -r requirements.txt
```

**3. Configure as variáveis de ambiente**

Crie um arquivo `.env` baseado no `.env.example`:
```
GEMINI_API_KEY=sua_chave_aqui
MONGO_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/chatbot
SECRET_KEY=sua_secret_key_aqui
FLASK_ENV=development
```

**4. Rode a aplicação**
```bash
python run.py
```

Acesse `http://127.0.0.1:5000`

## Variáveis de Ambiente

| Variável | Descrição |
|----------|-----------|
| `GEMINI_API_KEY` | Chave da API do Google AI Studio |
| `MONGO_URI` | Connection string do MongoDB Atlas |
| `SECRET_KEY` | Chave secreta do Flask para sessões |
| `FLASK_ENV` | `development` ou `production` |
