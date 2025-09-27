 usu# Sistema de Sinalização Digital - Facilita TI

Um sistema completo de sinalização digital desenvolvido por Bruno Martins Rocha da Facilita TI, utilizando Raspberry Pi 4 como dispositivo de exibição e um painel web moderno para gerenciamento remoto. Esse projeto precisa de uma aplicação para validar instalação da plataforma e para cada raspberry ativada.

## 📋 Visão Geral

Este projeto oferece uma solução própria de sinalização digital com controle total sobre conteúdos, agendamentos, rotação de tela, hibernação automática via HDMI-CEC, autenticação segura e integração via API REST. A interface é personalizada com identidade visual moderna e profissional.

## 🎯 Objetivos do Produto

- ✅ Exibir conteúdos digitais (links, imagens, vídeos) em TVs conectadas a Raspberry Pi
- ✅ Gerenciar conteúdos e agendamentos remotamente via painel web
- ✅ Controlar rotação da tela (horizontal ou vertical)
- ✅ Automatizar hibernação da TV fora do horário comercial
- ✅ Permitir login seguro e gerenciamento por agência
- ✅ Integrar com API REST para futuras expansões
- ✅ Aplicar identidade visual moderna (cores, logo, tipografia)

## 🛠️ Tecnologias Utilizadas

### Frontend (Painel Web)
- **React.js** - Framework para interface web
- **Bootstrap 5** - Framework CSS para design responsivo
- **Axios** - Cliente HTTP para chamadas à API
- **React Router** - Roteamento para SPA
- **Context API** - Gerenciamento de estado global

### Backend (API e lógica de negócio)
- **Django** - Framework Python web
- **Django REST Framework** - API REST
- **PostgreSQL** - Banco de dados relacional
- **JWT Authentication** - Autenticação segura
- **Bcrypt** - Hash de senhas

### Banco de Dados
- **PostgreSQL** (produção)
- **SQLite** (desenvolvimento/local)

### Dispositivo Raspberry Pi
- **Raspberry Pi OS Lite**
- **Python 3**
- **Chromium** em modo kiosk para exibir links
- **VLC** para reprodução de vídeos
- **cec-utils** para controle HDMI-CEC

## 📁 Estrutura do Projeto

```
sinalizado_digital/
├── backend/                 # API Django REST Framework
│   ├── sinalizacao_digital/ # Configurações Django
│   ├── apps/               # Aplicações Django
│   │   ├── users/          # Gerenciamento de usuários
│   │   ├── agencies/       # Gerenciamento de agências
│   │   ├── contents/       # Gerenciamento de conteúdos
│   │   ├── schedules/      # Sistema de agendamentos
│   │   └── devices/        # Controle de dispositivos
│   ├── requirements.txt    # Dependências Python
│   └── manage.py          # Comando Django
├── frontend/               # Aplicação React
│   ├── public/            # Arquivos estáticos
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── context/       # Context API
│   │   └── App.js         # Componente principal
│   └── package.json       # Dependências Node.js
├── raspberry_pi/          # Scripts para Raspberry Pi
├── docs/                  # Documentação
└── README.md             # Este arquivo
```

## 🚀 Instalação e Configuração

### Pré-requisitos

- **Python 3.11+** (para backend)
- **Node.js 18+** (para frontend)
- **PostgreSQL** (opcional, SQLite por padrão)
- **Git**

### Backend Setup

1. **Navegue para o diretório backend:**
   ```bash
   cd backend
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   Edite o arquivo `.env` com suas configurações:
   ```env
   DATABASE_URL=sqlite:///./digital_signage.db
   SECRET_KEY=your-super-secret-key-change-this-in-production
   API_HOST=0.0.0.0
   API_PORT=8000
   ```

5. **Execute as migrações do banco:**
   ```bash
   python manage.py migrate
   ```

6. **Execute o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

7. **Acesse a documentação da API:**
   - **Django REST Framework browsable API:** http://localhost:8000/api/
   - **Admin Django:** http://localhost:8000/admin/

### Frontend Setup

1. **Navegue para o diretório frontend:**
   ```bash
   cd frontend
   ```

2. **Instale as dependências:**
   ```bash
   npm install
   ```

3. **Configure a API base URL:**
   Edite o arquivo `src/context/AuthContext.js` e ajuste:
   ```javascript
   axios.defaults.baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
   ```

4. **Execute o servidor de desenvolvimento:**
   ```bash
   npm start
   ```

5. **Acesse a aplicação:**
   - **Frontend:** http://localhost:3000
   - **Login:** http://localhost:3000/login

## 🔧 Funcionalidades Implementadas

### Painel Web
- ✅ Sistema de autenticação com JWT
- ✅ Dashboard com estatísticas em tempo real
- ✅ Gerenciamento de agências
- ✅ Cadastro e upload de conteúdos
- ✅ Sistema de agendamentos
- ✅ Monitoramento de dispositivos
- ✅ Interface responsiva com tema moderno

### API REST
- ✅ Autenticação e autorização
- ✅ CRUD completo para todas as entidades
- ✅ Upload de arquivos
- ✅ Validação de dados
- ✅ Documentação automática

### Raspberry Pi Scripts
- 🔄 Consulta à API para conteúdo
- 🔄 Controle de exibição (Chromium/VLC)
- 🔄 Rotação de tela
- 🔄 Hibernação HDMI-CEC
- 🔄 Sincronização de status

## 📊 Modelos de Dados

### Usuários (Users)
- Gerenciamento de usuários do sistema
- Perfis: admin, gestor, técnico
- Autenticação JWT

### Agências (Agencies)
- Cadastro de agências
- Configurações específicas (logo, orientação)
- Relacionamento com usuários

### Conteúdos (Contents)
- Links, imagens e vídeos
- Upload e armazenamento
- Metadados e descrições

### Agendamentos (Schedules)
- Programação por horário
- Dias da semana
- Controle de conflitos

### Dispositivos (Devices)
- Raspberry Pi registrados
- Status online/offline
- Última sincronização

## 🔐 Segurança

- **Autenticação JWT** com expiração de tokens
- **Hash de senhas** com bcrypt
- **CORS configurado** para origens específicas
- **Validação de dados** com Django Forms e Serializers
- **Logs de auditoria** para todas as operações

## 🎨 Identidade Visual

- **Paleta de cores:** Verde moderno (#006633), branco, cinza
- **Tipografia:** Montserrat
- **Layout:** Limpo, moderno e responsivo
- **Componentes:** Cards, modals e navegação personalizados

## 📱 Interface Responsiva

- **Mobile-first** design
- **Breakpoints** otimizados para tablets e desktop
- **Touch-friendly** para dispositivos móveis
- **Acessibilidade** com ARIA labels

## 🔄 Raspberry Pi Integration

### Instalação no Raspberry Pi

1. **Clone o repositório:**
   ```bash
   git clone <repository-url>
   cd sinalizado_digital/raspberry_pi
   ```

2. **Instale dependências:**
   ```bash
   sudo apt update
   sudo apt install chromium-browser vlc cec-utils python3-pip
   pip3 install requests
   ```

3. **Configure o script:**
   Edite `player.py` com as configurações da agência

4. **Execute o player:**
   ```bash
   python3 player.py
   ```

## 📚 Documentação da API

A documentação completa da API está disponível em:
- **Django REST Framework browsable API:** http://localhost:8000/api/
- **Admin Django:** http://localhost:8000/admin/

### Endpoints Principais

- `POST /api/auth/login/` - Autenticação JWT
- `GET /api/agencies/` - Listar agências
- `POST /api/contents/` - Criar conteúdo
- `GET /api/schedules/current/` - Agendamento atual
- `POST /api/devices/status/` - Atualizar status do dispositivo

## 🧪 Testes

### Backend Tests
```bash
cd backend
python -m pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚀 Deploy

### Backend (Produção)
```bash
cd backend
# Usando Gunicorn (recomendado para Django)
gunicorn sinalizacao_digital.wsgi:application --bind 0.0.0.0:8000 --workers 4

# Ou usando o servidor de desenvolvimento (não recomendado para produção)
python manage.py runserver 0.0.0.0:8000
```

### Frontend (Produção)
```bash
cd frontend
npm run build
# Servir com Nginx ou Apache, ou usar serve para desenvolvimento
serve -s build -l 3000
```

## 📝 Manual de Instalação Raspberry Pi

Consulte o arquivo `docs/RASPBERRY_PI_SETUP.md` para instruções detalhadas de instalação e configuração do Raspberry Pi.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é propriedade da Facilta TI.

## 📞 Suporte

Para suporte técnico, entre em contato com Bruno Martins Rocha:

- **Email:** bmrocha7l@gmail.com
- **Telefone:** 31-98439-0045
- **LinkedIn:** https://www.linkedin.com/in/brunomartinsrocha/

## 🔄 Roadmap

- [ ] Implementar notificações push
- [ ] Adicionar suporte a múltiplos idiomas
- [ ] Integrar com sistemas externos
- [ ] Implementar cache Redis
- [ ] Adicionar métricas e monitoramento
- [ ] Suporte a playlists de conteúdo

---

**Desenvolvido por Bruno Martins Rocha - Facilta TI**
