# LingoLearn 📚

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
git clone <url-do-repositorio>
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
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**⚠️ IMPORTANTE:** Gere uma chave JWT segura:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Crie o banco de dados

```bash
cd app
python database/create_db.py
cd ..
```

### 6. Inicie o servidor backend

```bash
cd app
python main.py
```

O backend estará rodando em `http://localhost:5000`

---

## 🎨 Configuração do Frontend

### 1. Navegue até a pasta do frontend

```bash
cd lingolearn-frontend
```

### 2. Instale as dependências

Escolha seu gerenciador de pacotes preferido:

```bash
# npm
npm install

# yarn
yarn install

# pnpm
pnpm install

# bun
bun install
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na pasta `lingolearn-frontend` baseado no `.env.example`:

```env
VITE_API_URL=http://localhost:5000
VITE_ACCESS_TOKEN_EXPIRE=60
```

### 4. Inicie o servidor de desenvolvimento

```bash
# npm
npm run dev

# yarn
yarn dev

# pnpm
pnpm dev

# bun
bun dev
```

O frontend estará rodando em `http://localhost:5173`

### 5. Build para produção

```bash
# npm
npm run build

# yarn
yarn build

# pnpm
pnpm build

# bun
bun run build
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

## 🔌 API Endpoints

### Autenticação (`/auth`)

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `POST` | `/auth/` | Login (retorna token JWT) | Não |
| `GET` | `/auth/` | Validar token | Sim |

### Usuários (`/users`)

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `POST` | `/users/` | Registrar novo usuário | Não |
| `PUT` | `/users/{id}` | Atualizar usuário | Sim |

### Textos (`/texts`)

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `POST` | `/texts/` | Importar novo texto | Sim |
| `GET` | `/texts/` | Listar textos do usuário | Sim |
| `GET` | `/texts/{id}/pages/{page}` | Obter página específica | Sim |

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

## 📝 Exemplos de Uso

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

---

## 🔒 Segurança

- ✅ Senhas hasheadas com bcrypt
- ✅ Autenticação via JWT com expiração configurável
- ✅ CORS configurado para frontend local
- ✅ Validação de dados com Pydantic
- ✅ Cookies HTTP-only para tokens
- ✅ Proteção de rotas no frontend e backend

---

## 🐛 Troubleshooting

### Backend

**Erro: "Could not validate credentials"**
- Verifique se o token JWT está válido e não expirou
- Confirme se a chave JWT no `.env` está correta

**Erro: "Database is locked"**
- Certifique-se de que apenas uma instância do servidor está rodando
- Reinicie o servidor

**Erro ao importar textos**
- Verifique se a pasta `uploads/text_covers` existe
- Confirme se o usuário tem permissões de escrita

### Frontend

**Erro: "Failed to fetch"**
- Verifique se o backend está rodando em `http://localhost:5000`
- Confirme se `VITE_API_URL` está configurado corretamente no `.env`

**Erro de CORS**
- Verifique as configurações de CORS no backend
- Certifique-se de que o frontend está rodando na porta esperada

**Página em branco após build**
- Execute `npm run preview` para testar o build
- Verifique o console do navegador para erros

---

## 🎯 Roadmap

- [ ] Sistema de flashcards
- [ ] Estatísticas detalhadas de progresso
- [ ] Modo escuro
- [ ] Exportação de vocabulário
- [ ] Suporte para áudio/pronúncia
- [ ] Aplicativo mobile
- [ ] Integração com dicionários externos

---

## 📄 Licença

Este projeto é de código aberto e está disponível para uso educacional.

---

## 👥 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Convenções de Código

**Backend:**
- Siga PEP 8
- Use type hints
- Documente funções complexas

**Frontend:**
- Siga o ESLint configurado
- Use Prettier para formatação
- Componentes em PascalCase

---

## 📞 Suporte

Se encontrar problemas ou tiver dúvidas:

- Abra uma [issue](../../issues)
- Entre em contato através do email do projeto

---

**Desenvolvido com ❤️ para facilitar o aprendizado de idiomas**
