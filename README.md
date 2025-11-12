F# LingoLearn 📚

Aplicação completa para aprendizado de idiomas através da leitura de textos, com sistema de gerenciamento de vocabulário e acompanhamento de progresso.

## 🎯 Sobre o Projeto

O LingoLearn é uma plataforma moderna que facilita o aprendizado de novos idiomas através da importação e leitura de textos. Com recursos de rastreamento de vocabulário e progresso gamificado, a ferramenta torna o aprendizado mais eficiente e motivador.

### ✨ Principais Funcionalidades

- 📖 **Biblioteca de Textos**: Importe e organize seus textos de aprendizado
- 🎯 **Sistema de Vocabulário**: Rastreie palavras por níveis de conhecimento
- 📊 **Acompanhamento de Progresso**: Visualize sua evolução no aprendizado
- 🌐 **Suporte Multi-idiomas**: Aprenda português, inglês, espanhol e mais
- 🔐 **Autenticação Segura**: Sistema completo de login e registro
- 📱 **Interface Moderna**: Design responsivo e intuitivo

---

## 📋 Pré-requisitos

### Backend
- Python 3.10+
- pip (gerenciador de pacotes Python)

### Frontend
- Node.js 18+ (recomendado: 20+)
- npm, yarn, pnpm ou bun

---

## 🚀 Instalação e Configuração

### 1. Clone o Repositório

```bash
git clone https://github.com/gstavoscherer/LingoLearn
cd LingoLearn
```

---

## 🔧 Configuração do Backend

### 1. Navegue até a pasta do backend

```bash
cd lingolearn-backend
```

### 2. Crie e ative o ambiente virtual

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

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na pasta `lingolearn-backend`:

```env
DATABASE_URL=sqlite:///./app/lingolearn.db
JWT_KEY=sua_chave_secreta_aqui_minimo_32_caracteres
JWT_ALGORITHM=HS256
API_PORT=5000
ACCESS_TOKEN_EXPIRE_MINUTES=1440
FRONTEND_URL=https://lingolearn.gustavoscherer.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
```

**⚠️ IMPORTANTE:** Gere uma chave JWT segura:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Crie o banco de dados

```bash
cd app
python -m app.database.create_db
cd ..
```

### 6. Inicie o servidor backend

```bash
cd app
python -m app.main
```

O backend estará rodando em `http://localhost:5000`

---

## 🎨 Configuração do Frontend

### 1. Navegue até a pasta do frontend

```bash
cd lingolearn-frontend
```

### 2. Instale as dependências

Rode o seguinte comando npm:

```bash
# npm
npm install

```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na pasta `lingolearn-frontend` baseado no `.env.example`:

```env
VITE_API_URL=http://localhost:5000
VITE_ACCESS_TOKEN_EXPIRE=86400
```

### 4. Inicie o servidor de desenvolvimento

```bash
# npm
npm run dev

```

O frontend estará rodando em `http://localhost:5173`

### 5. Build para produção

```bash
# npm
npm run build

```

---

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
│   ├── .env                   # Variáveis de ambiente
│   ├── .venv/                 # Ambiente virtual
│   └── requirements.txt       # Dependências Python
│
├── lingolearn-frontend/
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/    # Componentes reutilizáveis
│   │   │   │   ├── layout/    # Componentes de layout
│   │   │   │   ├── modals/    # Modais da aplicação
│   │   │   │   ├── page/      # Componentes de página
│   │   │   │   ├── sections/  # Seções da landing page
│   │   │   │   ├── text/      # Componentes relacionados a textos
│   │   │   │   └── ui/        # Componentes UI base
│   │   │   ├── toast-state.svelte.ts  # Gerenciamento de toasts
│   │   │   └── types.ts       # Tipos TypeScript
│   │   ├── routes/
│   │   │   ├── (app)/         # Rotas autenticadas
│   │   │   │   ├── home/      # Página inicial
│   │   │   │   ├── profile/   # Perfil do usuário
│   │   │   │   └── texts/     # Biblioteca de textos
│   │   │   ├── (auth)/        # Rotas de autenticação
│   │   │   │   ├── login/     # Login
│   │   │   │   └── register/  # Registro
│   │   │   └── +page.svelte   # Landing page
│   │   └── styles/
│   │       └── global.scss    # Estilos globais
│   ├── .env                   # Variáveis de ambiente
│   ├── package.json           # Dependências e scripts
│   ├── svelte.config.js       # Configuração do Svelte
│   ├── tsconfig.json          # Configuração do TypeScript
│   └── vite.config.ts         # Configuração do Vite
│
└── README.md                  # Este arquivo
```

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python
- **SQLite** - Banco de dados
- **Pydantic** - Validação de dados
- **JWT** - Autenticação via tokens
- **Bcrypt** - Hash de senhas
- **Uvicorn** - Servidor ASGI

### Frontend
- **SvelteKit** - Framework Svelte full-stack
- **TypeScript** - Tipagem estática
- **Vite** - Build tool moderna
- **SCSS** - Pré-processador CSS
- **Lucide Icons** - Biblioteca de ícones
- **Svelte Motion** - Animações

---

## 📄 Licença

Este projeto é de código aberto e está disponível para uso educacional.

---

**Desenvolvido com ❤️ para facilitar o aprendizado de idiomas**
