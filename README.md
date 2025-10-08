# LingoLearn

Aplicação para aprendizado de idiomas através da leitura de textos, com sistema de gerenciamento de vocabulário e acompanhamento de progresso.

## 📋 Pré-requisitos

- Python 3.10+
- pip (gerenciador de pacotes Python)

## 🚀 Instalação e Configuração

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd LingoLearn
```

### 2. Configure o Backend

#### 2.1. Navegue até a pasta do backend

```bash
cd lingolearn-backend
```

#### 2.2. Crie e ative o ambiente virtual

**Linux/macOS:**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### 2.3. Instale as dependências

```bash
pip install -r requirements.txt
```

#### 2.4. Configure as variáveis de ambiente

Crie um arquivo `.env` na pasta `lingolearn-backend` com as seguintes variáveis:

```env
DATABASE_URL=sqlite:///./app/lingolearn.db
JWT_KEY=sua_chave_secreta_aqui_minimo_32_caracteres
JWT_ALGORITHM=HS256
API_PORT=5000
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**⚠️ IMPORTANTE:** Gere uma chave JWT segura. Você pode usar o seguinte comando Python:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 2.5. Crie o banco de dados

```bash
cd app
python database/create_db.py
cd ..
```

#### 2.6. Inicie o servidor

```bash
cd app
python main.py
```

O servidor estará rodando em `http://localhost:5000`

## 📁 Estrutura do Projeto

```
LingoLearn/
├── lingolearn-backend/
│   ├── app/
│   │   ├── core/              # Configurações, segurança e utilitários
│   │   ├── database/          # Conexão com banco de dados
│   │   ├── models/            # Modelos SQLAlchemy
│   │   ├── repositories/      # Camada de acesso a dados
│   │   ├── routers/           # Endpoints da API
│   │   ├── schemas/           # Schemas Pydantic
│   │   ├── services/          # Lógica de negócio
│   │   ├── utils/             # Funções auxiliares
│   │   ├── uploads/           # Arquivos enviados (capas de textos)
│   │   └── main.py            # Ponto de entrada da aplicação
│   ├── .env                   # Variáveis de ambiente (criar)
│   ├── .venv/                 # Ambiente virtual
│   └── requirements.txt       # Dependências Python
└── README.md
```

## 🔧 Funcionalidades

### Autenticação
- Registro de usuários
- Login com JWT
- Validação de tokens

### Gerenciamento de Textos
- Importação de textos com metadados (título, autor, idioma)
- Upload de capas para textos
- Divisão automática em páginas
- Análise de palavras únicas e frequência
- Listagem e busca de textos

### Vocabulário
- Rastreamento de palavras por texto
- Sistema de progresso de aprendizado

## 📡 Endpoints da API

### Autenticação (`/auth`)
- `POST /auth/` - Login (retorna token JWT)
- `GET /auth/` - Validar token

### Usuários (`/users`)
- `POST /users/` - Registrar novo usuário
- `PUT /users/{id}` - Atualizar usuário

### Textos (`/texts`)
- `POST /texts/` - Importar novo texto (com upload opcional de imagem)
- `GET /texts/` - Listar textos do usuário (com paginação e busca)

## 🛠️ Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python
- **SQLite** - Banco de dados
- **Pydantic** - Validação de dados
- **JWT** - Autenticação via tokens
- **Bcrypt** - Hash de senhas
- **Uvicorn** - Servidor ASGI

## 📝 Exemplo de Uso

### 1. Registrar um usuário

```bash
curl -X POST http://localhost:5000/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "João Silva",
    "email": "joao@email.com",
    "password": "senha123"
  }'
```

### 2. Fazer login

```bash
curl -X POST http://localhost:5000/auth/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=joao@email.com&password=senha123"
```

### 3. Importar um texto

```bash
curl -X POST http://localhost:5000/texts/ \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -F "title=Meu Primeiro Texto" \
  -F "author=Autor Exemplo" \
  -F "language=pt" \
  -F "content=Conteúdo do texto aqui..." \
  -F "user_id=1" \
  -F "image=@caminho/para/imagem.jpg"
```

## 🔒 Segurança

- Senhas são hasheadas com bcrypt
- Autenticação via JWT com expiração configurável
- CORS configurado para frontend local
- Validação de dados com Pydantic

## 🐛 Troubleshooting

### Erro: "Could not validate credentials"
- Verifique se o token JWT está válido e não expirou
- Confirme se a chave JWT no `.env` está correta

### Erro: "Database is locked"
- Certifique-se de que apenas uma instância do servidor está rodando
- Reinicie o servidor

### Erro ao importar textos
- Verifique se a pasta `uploads/text_covers` existe
- Confirme se o usuário tem permissões de escrita

## 📄 Licença

Este projeto é de código aberto e está disponível para uso educacional.

## 👥 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

---

**Desenvolvido com ❤️ para facilitar o aprendizado de idiomas**