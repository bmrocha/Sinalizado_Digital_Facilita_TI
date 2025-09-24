# Sistema de Sinalização Digital - Facilta TI

## Visão Geral

Este é um sistema completo de sinalização digital desenvolvido especificamente para a empresas que precisa digitalizar seus anuncios e sistemas de chamados senhas da  Facilta TI.

## Arquitetura do Sistema

### Componentes Principais

1. **Backend (FastAPI)**
   - API REST para gerenciamento de dados
   - Autenticação JWT
   - Gerenciamento de usuários, agências, conteúdos, agendamentos e dispositivos

2. **Frontend (React)**
   - Painel web moderno e responsivo
   - Interface com identidade visual do Sicoob
   - Gerenciamento completo do sistema

3. **Raspberry Pi Player**
   - Script Python para execução de conteúdo
   - Suporte a links, imagens e vídeos
   - Controle HDMI-CEC para hibernação
   - Sincronização automática com API

### Tecnologias Utilizadas

- **Backend**: Python 3.11, FastAPI, SQLAlchemy, PostgreSQL/SQLite
- **Frontend**: React.js, Bootstrap 5, Axios
- **Raspberry Pi**: Python 3, Chromium, VLC, cec-utils
- **Banco de Dados**: PostgreSQL (produção), SQLite (desenvolvimento)

## Funcionalidades

### Painel Web
- ✅ Login seguro com JWT
- ✅ Dashboard com status dos dispositivos
- ✅ Gerenciamento de agências
- ✅ Cadastro de conteúdo (links, imagens, vídeos)
- ✅ Sistema de agendamento por horário e dias da semana
- ✅ Configuração de orientação da tela
- ✅ Controle de hibernação automática
- ✅ Upload de logotipos personalizados
- ✅ Interface responsiva com tema Sicoob

### Raspberry Pi Player
- ✅ Execução de conteúdo em modo kiosk
- ✅ Reprodução de vídeos com VLC
- ✅ Exibição de imagens com feh
- ✅ Rotação automática de tela
- ✅ Hibernação via HDMI-CEC
- ✅ Sincronização automática com API
- ✅ Monitoramento de status do sistema

## Instalação e Configuração

### Backend (API)

1. **Pré-requisitos**
   ```bash
   Python 3.11+
   PostgreSQL (produção) ou SQLite (desenvolvimento)
   ```

2. **Instalação**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configuração**
   - Edite o arquivo `.env` com suas configurações
   - Configure a URL do banco de dados
   - Defina a chave secreta JWT

4. **Execução**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend (Painel Web)

1. **Pré-requisitos**
   ```bash
   Node.js 16+
   npm ou yarn
   ```

2. **Instalação**
   ```bash
   cd frontend
   npm install
   ```

3. **Configuração**
   - Edite `src/services/api.js` com a URL da API
   - Configure variáveis de ambiente se necessário

4. **Execução**
   ```bash
   npm start
   ```

### Raspberry Pi Player

1. **Pré-requisitos**
   - Raspberry Pi 4 com Raspberry Pi OS Lite
   - Conexão com internet
   - TV compatível com HDMI-CEC

2. **Instalação**
   ```bash
   cd raspberry_pi
   chmod +x install.sh
   ./install.sh
   ```

3. **Configuração**
   - Edite `digital_signage_config.json` com as configurações da agência
   - Configure a URL da API
   - Defina o ID do dispositivo

## Estrutura do Banco de Dados

### Tabelas Principais

- **users**: Usuários do sistema (admin, gestor, técnico)
- **agencies**: Agências com configurações específicas
- **contents**: Conteúdos digitais (links, imagens, vídeos)
- **schedules**: Agendamentos de exibição
- **devices**: Dispositivos Raspberry Pi

### Relacionamentos

```
users ──┬── agencies (1:N)
        ├── contents (1:N)
        └── schedules (1:N)

agencies ──┬── devices (1:N)
            └── schedules (1:N)

contents ─── schedules (1:N)
```

## API REST

### Endpoints Principais

#### Autenticação
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/register` - Registrar usuário
- `GET /api/v1/auth/me` - Perfil do usuário

#### Agências
- `GET /api/v1/agencies` - Listar agências
- `POST /api/v1/agencies` - Criar agência
- `PUT /api/v1/agencies/{id}` - Atualizar agência
- `DELETE /api/v1/agencies/{id}` - Excluir agência

#### Conteúdos
- `GET /api/v1/contents` - Listar conteúdos
- `POST /api/v1/contents` - Criar conteúdo
- `POST /api/v1/contents/upload` - Upload de arquivo
- `PUT /api/v1/contents/{id}` - Atualizar conteúdo
- `DELETE /api/v1/contents/{id}` - Excluir conteúdo

#### Agendamentos
- `GET /api/v1/schedules` - Listar agendamentos
- `GET /api/v1/schedules/current` - Agendamentos ativos
- `POST /api/v1/schedules` - Criar agendamento
- `PUT /api/v1/schedules/{id}` - Atualizar agendamento
- `DELETE /api/v1/schedules/{id}` - Excluir agendamento

#### Dispositivos
- `GET /api/v1/devices` - Listar dispositivos
- `POST /api/v1/devices` - Registrar dispositivo
- `PUT /api/v1/devices/{id}` - Atualizar dispositivo
- `PUT /api/v1/devices/{id}/status` - Atualizar status
- `DELETE /api/v1/devices/{id}` - Remover dispositivo

## Configuração do Raspberry Pi

### Orientação da Tela
A rotação da tela é configurada automaticamente baseado nas configurações da agência:
- **Horizontal**: `display_rotate=0`
- **Vertical**: `display_rotate=1`

### Hibernação HDMI-CEC
A hibernação é controlada via comandos CEC:
- **Hibernar**: `echo "standby 0" | cec-client -s`
- **Acordar**: `echo "on 0" | cec-client -s`

### Monitoramento
O sistema monitora:
- CPU e memória
- Temperatura
- Espaço em disco
- Uptime do sistema

## Segurança

### Autenticação
- JWT tokens com expiração
- Hash de senhas com bcrypt
- Controle de permissões por perfil

### Comunicação
- HTTPS para painel web
- VPN para acesso remoto
- Validação de entrada de dados

## Identidade Visual

### Paleta de Cores
- **Verde Sicoob**: `#006633`
- **Branco**: `#FFFFFF`
- **Cinza Claro**: `#F8F9FA`

### Tipografia
- **Principal**: Montserrat
- **Alternativa**: Open Sans

### Layout
- Design responsivo
- Interface limpa e moderna
- Logotipo personalizável por agência

## Troubleshooting

### Problemas Comuns

1. **API não responde**
   - Verifique se o backend está rodando
   - Confirme a URL da API no frontend
   - Verifique configurações de firewall

2. **Raspberry Pi não exibe conteúdo**
   - Verifique conexão com internet
   - Confirme configurações no `digital_signage_config.json`
   - Verifique logs: `sudo journalctl -u digital-signage -f`

3. **Problemas de autenticação**
   - Verifique se o token JWT é válido
   - Confirme configurações de CORS
   - Verifique credenciais no banco de dados

### Logs

- **Backend**: Arquivos de log configurados no FastAPI
- **Frontend**: Console do navegador (F12)
- **Raspberry Pi**: `sudo journalctl -u digital-signage -f`

## Suporte

Para suporte técnico, entre em contato com a equipe de desenvolvimento:

- **Email**: bmrocha7l@gmail.com
- **Telefone**: 31-98439-0045
- **LinkedIn**: https://www.linkedin.com/in/brunomartinsrocha/
- **Documentação**: Este README e documentação da API

## Licença

Este sistema foi desenvolvido exclusivamente para empresas que necessitam publicar e rodar links sistema modo kiosk centralizados da Facilta TI.
Todos os direitos reservados © 2025 Facilta TI.
