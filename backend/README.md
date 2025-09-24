# Sistema de Sinalização Digital - Backend (FastAPI)

API REST para o sistema de sinalização digital do Sicoob Credisete.

## Funcionalidades Implementadas

### ✅ Autenticação JWT
- Login e registro de usuários
- Tokens de acesso com expiração
- Middleware de autenticação
- Controle de permissões por role (admin, manager, technician)

### ✅ Modelos de Dados
- **User**: Usuários do sistema com roles e agência associada
- **Agency**: Agências do Sicoob com configurações específicas
- **Content**: Conteúdos (links, imagens, vídeos) para exibição
- **Schedule**: Agendamentos de exibição de conteúdo
- **Device**: Dispositivos Raspberry Pi conectados

### ✅ API Endpoints
- `/api/v1/auth/*` - Autenticação
- `/api/v1/users/*` - Gerenciamento de usuários
- `/api/v1/agencies/*` - Gerenciamento de agências
- `/api/v1/contents/*` - Gerenciamento de conteúdo
- `/api/v1/schedules/*` - Gerenciamento de agendamentos
- `/api/v1/devices/*` - Gerenciamento de dispositivos

### ✅ Recursos Avançados
- Upload de arquivos (logos, imagens, vídeos)
- Validação de conflitos de agendamento
- Controle de status de dispositivos
- Consultas otimizadas com relacionamentos
- Paginação e filtros

## Como Executar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente
Copie o arquivo `.env` e ajuste as configurações:
```bash
cp .env .env.local
# Edite .env.local com suas configurações
```

### 3. Executar a API
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Acessar a Documentação
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Estrutura do Projeto

```
backend/
├── app/
│   ├── api/v1/          # API routes
│   ├── core/            # Configuração e segurança
│   ├── models/          # Modelos SQLAlchemy
│   └── schemas/         # Schemas Pydantic
├── uploads/             # Arquivos enviados
├── requirements.txt     # Dependências Python
├── .env                 # Variáveis de ambiente
└── README.md           # Este arquivo
```

## Endpoints Principais

### Autenticação
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/register` - Registrar usuário
- `GET /api/v1/auth/me` - Dados do usuário atual

### Agências
- `GET /api/v1/agencies` - Listar agências
- `POST /api/v1/agencies` - Criar agência
- `PUT /api/v1/agencies/{id}` - Atualizar agência
- `POST /api/v1/agencies/{id}/upload-logo` - Upload de logo

### Conteúdo
- `GET /api/v1/contents` - Listar conteúdos
- `POST /api/v1/contents` - Criar conteúdo
- `POST /api/v1/contents/{id}/upload` - Upload de arquivo

### Agendamentos
- `GET /api/v1/schedules` - Listar agendamentos
- `GET /api/v1/schedules/agency/{id}/current` - Agendamento atual

### Dispositivos
- `GET /api/v1/devices` - Listar dispositivos
- `POST /api/v1/devices/{id}/status` - Atualizar status do dispositivo

## Próximos Passos

1. **Frontend React**: Implementar painel web
2. **Scripts Raspberry Pi**: Criar player para dispositivos
3. **Banco de Dados**: Configurar PostgreSQL para produção
4. **Testes**: Adicionar testes unitários e de integração
5. **Documentação**: Expandir documentação da API

## Tecnologias Utilizadas

- **FastAPI**: Framework web assíncrono
- **SQLAlchemy**: ORM para banco de dados
- **Pydantic**: Validação de dados
- **JWT**: Autenticação baseada em tokens
- **SQLite**: Banco de dados para desenvolvimento
- **Python 3.8+**: Linguagem de programação
