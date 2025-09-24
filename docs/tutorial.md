# Tutorial: Sistema de Sinalização Digital - Sicoob Credisete

Este tutorial fornece instruções passo a passo para configurar, instalar e usar o Sistema de Sinalização Digital desenvolvido para o Sicoob Credisete.

## 📋 Pré-requisitos

### Para o Backend (API)
- Python 3.8 ou superior
- PostgreSQL (produção) ou SQLite (desenvolvimento)
- Git

### Para o Frontend (Painel Web)
- Node.js 16 ou superior
- npm ou yarn

### Para o Raspberry Pi
- Raspberry Pi 4 com Raspberry Pi OS Lite
- Conexão à internet
- TV compatível com HDMI-CEC (opcional para hibernação)

## 🚀 1. Configuração do Backend

### 1.1 Clone o Repositório
```bash
git clone <repository-url>
cd sinalizado_digital/backend
```

### 1.2 Configure o Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 1.3 Instale as Dependências
```bash
pip install -r requirements.txt
```

### 1.4 Configure as Variáveis de Ambiente
Edite o arquivo `.env` com suas configurações:
```env
DATABASE_URL=postgresql://user:password@localhost/digital_signage
SECRET_KEY=sua-chave-secreta-aqui
API_HOST=0.0.0.0
API_PORT=8000
```

### 1.5 Execute as Migrações do Banco de Dados
```bash
alembic upgrade head
```

### 1.6 Inicie o Servidor
```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`

## 🌐 2. Configuração do Frontend

### 2.1 Navegue para o Diretório do Frontend
```bash
cd ../frontend
```

### 2.2 Instale as Dependências
```bash
npm install
# ou
yarn install
```

### 2.3 Configure as Variáveis de Ambiente
Crie um arquivo `.env.local`:
```env
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_UPLOAD_URL=http://localhost:8000/uploads
```

### 2.4 Inicie o Servidor de Desenvolvimento
```bash
npm start
# ou
yarn start
```

O painel web estará disponível em `http://localhost:3000`

## 📺 3. Configuração do Raspberry Pi

### 3.1 Instale o Sistema Operacional
1. Baixe o Raspberry Pi OS Lite do site oficial
2. Use o Raspberry Pi Imager para gravar o SD card
3. Configure Wi-Fi e SSH no boot

### 3.2 Clone o Repositório no Raspberry Pi
```bash
git clone <repository-url>
cd sinalizado_digital/raspberry_pi
```

### 3.3 Instale as Dependências
```bash
sudo apt update
sudo apt install python3-pip chromium-browser vlc cec-utils
pip3 install -r requirements.txt
```

### 3.4 Configure o Script de Inicialização
Edite `config.json` com as configurações da agência:
```json
{
  "api_url": "http://seu-servidor:8000/api/v1",
  "agency_id": "sua-agencia-id",
  "device_id": "seu-device-id",
  "orientation": "horizontal",
  "hibernation_enabled": true,
  "hibernation_start": "18:00",
  "hibernation_end": "08:00"
}
```

### 3.5 Configure o Modo Kiosk
Edite `/etc/xdg/lxsession/LXDE-pi/autostart`:
```
@chromium-browser --kiosk --disable-restore-session-state http://localhost:8000
```

### 3.6 Inicie o Player
```bash
python3 player.py
```

## 📖 4. Como Usar o Sistema

### 4.1 Primeiro Acesso
1. Acesse o painel web: `http://localhost:3000`
2. Faça login com as credenciais padrão (admin/admin)
3. Altere a senha no primeiro acesso

### 4.2 Gerenciando Agências
1. No dashboard, clique em "Agências"
2. Adicione uma nova agência com nome, IP e configurações
3. Faça upload do logotipo da agência

### 4.3 Adicionando Conteúdo
1. Vá para "Conteúdo" > "Novo Conteúdo"
2. Selecione o tipo (link, imagem, vídeo)
3. Faça upload do arquivo ou insira a URL
4. Defina data de início e fim

### 4.4 Criando Agendamentos
1. Acesse "Agendamentos"
2. Selecione o conteúdo e a agência
3. Defina horários e dias da semana
4. Salve o agendamento

### 4.5 Monitorando Dispositivos
1. No dashboard, visualize o status dos dispositivos
2. Verifique a última sincronização
3. Monitore logs de erro

## 🔧 5. Configurações Avançadas

### 5.1 Rotação da Tela
- No Raspberry Pi, edite `/boot/config.txt`:
```
display_rotate=1  # 90 graus
display_rotate=3  # 270 graus
```

### 5.2 Hibernação HDMI-CEC
- Configure no painel web as horas de hibernação
- O script automaticamente controlará a TV

### 5.3 Backup do Banco de Dados
```bash
# PostgreSQL
pg_dump digital_signage > backup.sql

# SQLite
cp digital_signage.db digital_signage_backup.db
```

## 🐛 6. Solução de Problemas

### Problemas Comuns
- **Erro de CORS**: Verifique as origens no `.env`
- **Banco não conecta**: Confirme DATABASE_URL
- **Uploads falham**: Verifique permissões da pasta uploads
- **Raspberry Pi não sincroniza**: Verifique conexão com a API

### Logs
- Backend: Verifique logs no console do uvicorn
- Frontend: Abra DevTools no navegador
- Raspberry Pi: Verifique `player.log`

## 📞 7. Suporte e Contato

Para suporte técnico:
- Email: suporte@sicoobcredisete.com.br
- Documentação da API: `http://localhost:8000/docs`
- Repositório: <repository-url>

## 🎯 8. Próximos Passos

- [ ] Implementar notificações push
- [ ] Adicionar suporte a múltiplos idiomas
- [ ] Integrar com sistemas externos
- [ ] Melhorar relatórios e analytics
- [ ] Adicionar testes automatizados

---

**Versão**: 1.0.0
**Última Atualização**: 24/09/2025
**Desenvolvido para**: Sicoob Credisete
