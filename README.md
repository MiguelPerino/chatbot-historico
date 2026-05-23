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

- Registro e login de usuários com senha criptografada com bcrypt
- Criação de múltiplas conversas por usuário
- Exclusão de conversas
- Histórico de mensagens persistido no MongoDB
- Geração automática de título da conversa baseado na primeira mensagem via LLM
- Renderização de Markdown nas respostas do bot
- Cada usuário acessa apenas suas próprias conversas
- Rotas protegidas com autenticação obrigatória (`@login_required`)
- Interface responsiva com sidebar listando conversas anteriores
- Envio de mensagem com Enter ou clique no botão

## Estrutura do Projeto

```
chatbot/
├── app/
│   ├── __init__.py          # factory do app Flask, configuração do LoginManager
│   ├── models/
│   │   ├── talk.py          # operações no MongoDB para conversas (CRUD)
│   │   └── user.py          # classe User compatível com Flask-Login
│   ├── routes/
│   │   ├── chat.py          # rotas do chat (protegidas com @login_required)
│   │   └── auth.py          # rotas de registro, login e logout
│   └── services/
│       └── llm.py           # integração com a API do Gemini
├── static/
│   ├── css/
│   │   ├── style.css        # estilos da interface do chat
│   │   └── login.css        # estilos da página de login
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
| GET | `/` | Interface principal do chat | Sim |
| GET | `/login` | Página de login | Não |
| POST | `/login` | Autenticar usuário | Não |
| POST | `/register` | Registrar novo usuário | Não |
| POST | `/logout` | Encerrar sessão | Sim |
| POST | `/chat/create` | Criar nova conversa | Sim |
| POST | `/chat/<id>/message` | Enviar mensagem e receber resposta da IA | Sim |
| GET | `/chat/<id>/history` | Buscar histórico de uma conversa | Sim |
| GET | `/chats` | Listar todas as conversas do usuário | Sim |
| DELETE | `/delete/<id>` | Deletar uma conversa | Sim |

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