# AI Code Assistant

Assistente de programação com IA que gera, explica e corrige código automaticamente.

[![Backend CI](https://github.com/seu-usuario/ai-code-assistant/workflows/Backend%20CI/badge.svg)](https://github.com/seu-usuario/ai-code-assistant/actions)
[![Frontend CI](https://github.com/seu-usuario/ai-code-assistant/workflows/Frontend%20CI/badge.svg)](https://github.com/seu-usuario/ai-code-assistant/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node 20+](https://img.shields.io/badge/node-20+-green.svg)](https://nodejs.org/)

## ✨ Novidades v2.0

- 🚀 **Redis Cache** - 80% de redução de custos com cache inteligente
- 🔐 **JWT Auth** - Sistema de autenticação seguro
- 📊 **Structured Logging** - Observabilidade completa com request tracking
- 💻 **Monaco Editor** - Editor profissional (VSCode engine)
- ⚙️ **CI/CD Pipeline** - GitHub Actions para integração e deploy contínuo

[Ver todas as novidades →](docs/NEW_FEATURES.md)

## Funcionalidades

- 💻 **Geração de código** - Crie código a partir de descrições em linguagem natural
- 📖 **Explicação de código** - Entenda o que seu código faz
- 🐛 **Detecção de bugs** - Encontre vulnerabilidades e problemas no código
- ✨ **Code refactoring** - Melhore a qualidade do seu código
- 📝 **Documentação automática** - Gere documentação completa automaticamente

## Tecnologias

### Backend
- **Python 3.11+** - Linguagem de programação
- **FastAPI** - Framework web moderno e rápido
- **OpenAI API** - Integração com modelos GPT-4
- **LangChain** - Framework para aplicações LLM
- **Redis** - Cache distribuído para performance
- **Pydantic** - Validação de dados
- **Structlog** - Logging estruturado
- **JWT** - Autenticação segura
- **Pytest** - Testes automatizados

### Frontend
- **React 18** - Biblioteca UI
- **TypeScript** - Tipagem estática
- **Monaco Editor** - Editor de código profissional (VSCode engine)
- **Vite** - Build tool e dev server
- **Axios** - Cliente HTTP
- **Vitest** - Framework de testes

### DevOps
- **Docker** - Containerização
- **Docker Compose** - Orquestração de containers
- **GitHub Actions** - CI/CD pipeline
- **Nginx** - Servidor web para frontend

## Arquitetura

```
ai-code-assistant/
├── backend/              # Microserviço FastAPI
│   ├── app/
│   │   ├── api/         # Endpoints da API
│   │   ├── core/        # Configurações
│   │   ├── services/    # Serviços de IA
│   │   ├── schemas/     # Schemas Pydantic
│   │   ├── tests/       # Testes do backend
│   │   └── main.py      # Aplicação principal
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/            # Microserviço React
│   ├── src/
│   │   ├── components/  # Componentes React
│   │   ├── services/    # Serviços API
│   │   ├── styles/      # CSS
│   │   ├── tests/       # Testes do frontend
│   │   └── main.tsx     # Entrada da aplicação
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
│
└── docker-compose.yml   # Orquestração
```

## Instalação e Uso

### Pré-requisitos

- Docker e Docker Compose instalados
- Chave API da OpenAI

### Configuração

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/ai-code-assistant.git
cd ai-code-assistant
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

3. Edite o arquivo `.env` e adicione sua chave da OpenAI:
```env
OPENAI_API_KEY=sua_chave_api_aqui
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7
MAX_TOKENS=2000
```

### Executando com Docker Compose

1. Inicie os serviços:
```bash
docker-compose up -d
```

2. Acesse a aplicação:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentação API**: http://localhost:8000/api/v1/docs

3. Para parar os serviços:
```bash
docker-compose down
```

### Desenvolvimento Local

#### Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Edite o .env com sua chave da OpenAI

# Executar servidor de desenvolvimento
python -m app.main

# Executar testes
pytest

# Executar testes com cobertura
pytest --cov=app --cov-report=html
```

#### Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Configurar variáveis de ambiente
cp .env.example .env

# Executar servidor de desenvolvimento
npm run dev

# Executar testes
npm test

# Executar testes com cobertura
npm run test:coverage

# Build para produção
npm run build
```

## API Endpoints

### Health Check
```
GET /api/v1/health
```
Verifica o status da API.

### Geração de Código
```
POST /api/v1/generate
Content-Type: application/json

{
  "prompt": "Crie uma função para calcular fibonacci",
  "language": "python",
  "context": "Opcional: contexto adicional"
}
```

### Explicação de Código
```
POST /api/v1/explain
Content-Type: application/json

{
  "code": "def fibonacci(n): ...",
  "language": "python"
}
```

### Detecção de Bugs
```
POST /api/v1/detect-bugs
Content-Type: application/json

{
  "code": "seu código aqui",
  "language": "python"
}
```

### Refatoração
```
POST /api/v1/refactor
Content-Type: application/json

{
  "code": "código para refatorar",
  "language": "python",
  "instructions": "Opcional: instruções específicas"
}
```

### Documentação
```
POST /api/v1/document
Content-Type: application/json

{
  "code": "código sem documentação",
  "language": "python",
  "style": "google"  // google, numpy, ou sphinx
}
```

## Testes

### Backend

O backend possui testes abrangentes com pytest:

```bash
cd backend
pytest --cov=app --cov-report=html
```

Cobertura mínima: 80%

### Frontend

O frontend utiliza Vitest para testes:

```bash
cd frontend
npm test
npm run test:coverage
```

## Segurança

- Nunca commite o arquivo `.env` com chaves reais
- Use variáveis de ambiente para credenciais sensíveis
- O código detecta e alerta sobre vulnerabilidades como:
  - SQL Injection
  - XSS (Cross-Site Scripting)
  - Command Injection
  - OWASP Top 10

## Monitoramento

### Health Checks

Ambos os serviços possuem health checks configurados:

- **Backend**: `http://localhost:8000/api/v1/health`
- **Frontend**: `http://localhost:3000/`

### Logs

```bash
# Ver logs de todos os serviços
docker-compose logs -f

# Ver logs apenas do backend
docker-compose logs -f backend

# Ver logs apenas do frontend
docker-compose logs -f frontend
```

## Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Suporte

Para reportar bugs ou solicitar features, abra uma issue no GitHub.

## Roadmap

- [ ] Suporte para mais modelos de IA (Claude, Llama, etc.)
- [ ] Extensão para VSCode
- [ ] API para integração com outras ferramentas
- [ ] Sistema de cache para respostas
- [ ] Autenticação de usuários
- [ ] Dashboard de métricas
- [ ] Suporte para mais linguagens de programação
- [ ] Modo offline com modelos locais

## Autores

- Equipe de Desenvolvimento AI Code Assistant

## Agradecimentos

- OpenAI pela API GPT-4
- Comunidade FastAPI
- Comunidade React
