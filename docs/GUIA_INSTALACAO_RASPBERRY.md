# 🚀 Guia de Instalação - Raspberry Pi OS Lite

## 📋 Visão Geral

Este guia mostra como instalar o **Sistema de Sinalização Digital** da **Facilita TI** em um Raspberry Pi com **Raspberry Pi OS Lite** e cartão de **32GB**.

### ✅ Vantagens da Versão Lite

- **Instalação rápida** (menos de 5 minutos)
- **Baixo consumo de espaço** (~50MB para o sistema)
- **Otimizado para cartões 32GB**
- **Interface simplificada**
- **Fácil configuração**

---

## 🛠️ Pré-requisitos

### Hardware
- ✅ **Raspberry Pi 4** (recomendado) ou Raspberry Pi 3B+
- ✅ **Cartão microSD 32GB** (Classe 10 ou superior)
- ✅ **Fonte de alimentação 5V/3A**
- ✅ **TV/Monitor com HDMI**
- ✅ **Cabo HDMI**
- ✅ **Teclado USB** (para configuração inicial)

### Software
- ✅ **Raspberry Pi OS Lite** instalado no cartão
- ✅ **Conexão com internet**

---

## 📦 Instalação Passo a Passo

### Passo 1: Preparar o Raspberry Pi

1. **Insira o cartão SD** no Raspberry Pi
2. **Conecte o HDMI** à TV/Monitor
3. **Conecte o teclado USB**
4. **Ligue a fonte de alimentação**

### Passo 2: Configuração Inicial

1. **Aguarde o sistema iniciar**
2. **Faça login:**
   ```
   Usuário: pi
   Senha: raspberry
   ```

3. **Configure a rede WiFi** (se necessário):
   ```bash
   sudo raspi-config
   ```
   - Selecione: **System Options** → **Wireless LAN**
   - Digite SSID e senha da sua rede

4. **Atualize o sistema:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

### Passo 3: Instalar o Sistema de Sinalização

1. **Baixe o script de instalação:**
   ```bash
   cd ~
   curl -o install_lite.sh https://raw.githubusercontent.com/facilitati/sinalizacao_digital/main/raspberry_pi/install_lite.sh
   ```

2. **Torne o script executável:**
   ```bash
   chmod +x install_lite.sh
   ```

3. **Execute a instalação:**
   ```bash
   ./install_lite.sh
   ```

   O script irá:
   - ✅ Instalar dependências essenciais
   - ✅ Baixar o player otimizado
   - ✅ Criar configuração inicial
   - ✅ Configurar serviço automático
   - ✅ Otimizar Chromium para kiosk

### Passo 4: Configurar o Sistema

1. **Edite a configuração:**
   ```bash
   nano ~/sinalizacao_digital/config.json
   ```

2. **Configure os seguintes campos:**
   ```json
   {
       "agency_id": 1,
       "device_id": "raspberry_001",
       "api_url": "http://192.168.1.100:8000/api/v1",
       "orientation": "horizontal",
       "hibernation_enabled": true,
       "hibernation_start": "18:00",
       "hibernation_end": "08:00",
       "check_interval": 30
   }
   ```

   **Importante:** Substitua `192.168.1.100` pelo IP do seu servidor API.

### Passo 5: Reiniciar e Testar

1. **Reinicie o Raspberry Pi:**
   ```bash
   sudo reboot
   ```

2. **Verifique se o serviço está rodando:**
   ```bash
   sudo systemctl status sinalizacao
   ```

3. **Veja os logs em tempo real:**
   ```bash
   sudo journalctl -u sinalizacao -f
   ```

---

## 📊 Análise de Espaço Utilizado

### 📈 Distribuição do Espaço (Cartão 32GB)

| Componente | Espaço | Descrição |
|------------|--------|-----------|
| **Sistema Operacional** | ~2.5GB | Raspberry Pi OS Lite |
| **Sistema de Sinalização** | ~50MB | Player + dependências |
| **Logs e Cache** | ~100MB | Arquivos temporários |
| **Conteúdo Local** | ~29GB | Vídeos e imagens |
| **Espaço Livre** | ~350MB | Buffer de segurança |

### 💾 Otimizações Implementadas

- ✅ **Dependências mínimas** (apenas pacotes essenciais)
- ✅ **Player compacto** (código otimizado)
- ✅ **Logs rotativos** (evita crescimento excessivo)
- ✅ **Cache inteligente** (limpeza automática)
- ✅ **Sem interface gráfica** (modo console)

---

## 🔧 Configurações Avançadas

### Rotação de Tela

Para tela vertical, edite o arquivo `/boot/config.txt`:
```bash
sudo nano /boot/config.txt
```

Adicione no final:
```bash
display_rotate=1  # 90 graus
# display_rotate=3  # 270 graus
```

### Hibernação Personalizada

Edite `config.json`:
```json
{
    "hibernation_enabled": true,
    "hibernation_start": "19:00",  // Início da hibernação
    "hibernation_end": "07:00"     // Fim da hibernação
}
```

### Gerenciamento de Conteúdo Local

O sistema suporta armazenamento local de conteúdo:

1. **Crie diretório para conteúdo:**
   ```bash
   mkdir -p ~/sinalizacao_digital/conteudo
   ```

2. **Configure no painel web** para usar URLs locais:
   ```
   file:///home/pi/sinalizacao_digital/conteudo/video.mp4
   ```

---

## 🆘 Solução de Problemas

### Problema: Serviço não inicia
```bash
# Verificar status
sudo systemctl status sinalizacao

# Ver logs detalhados
sudo journalctl -u sinalizacao --no-pager

# Reiniciar serviço
sudo systemctl restart sinalizacao
```

### Problema: Chromium não abre
```bash
# Resetar configuração do Chromium
rm -rf ~/.config/chromium

# Reinstalar se necessário
sudo apt install --reinstall chromium-browser
```

### Problema: API não conecta
```bash
# Testar conexão
ping SEU_SERVIDOR

# Testar API
curl http://SEU_SERVIDOR:8000/api/v1/schedules/current
```

### Problema: Sem espaço no cartão
```bash
# Limpar cache
sudo apt autoremove -y
sudo apt autoclean

# Limpar logs antigos
sudo journalctl --vacuum-time=7d

# Verificar espaço
df -h
```

---

## 📱 Monitoramento Remoto

### Verificar Status via SSH
```bash
# Conectar ao Raspberry Pi
ssh pi@IP_DO_RASPBERRY

# Verificar serviço
sudo systemctl status sinalizacao

# Ver logs
sudo journalctl -u sinalizacao -f
```

### Status via API
O Raspberry Pi envia status automaticamente para a API:
- ✅ **Online/Offline**
- ✅ **Última atividade**
- ✅ **Status do conteúdo**

---

## 🔄 Atualizações

### Atualizar o Sistema
```bash
# Via SSH
ssh pi@IP_DO_RASPBERRY

# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Atualizar player
cd ~/sinalizacao_digital
curl -o player.py https://raw.githubusercontent.com/facilitati/sinalizacao_digital/main/raspberry_pi/player_lite.py
sudo systemctl restart sinalizacao
```

---

## 📞 Suporte

Para suporte técnico, entre em contato:

**Facilita TI**
- 📧 Email: suporte@facilitati.com.br
- 📱 WhatsApp: (31) 98439-0045
- 💻 Sistema: Monitoramento 24/7

---

## 🎯 Resumo da Instalação

| Etapa | Tempo | Status |
|-------|-------|--------|
| 1. Configuração inicial | 5 min | ✅ |
| 2. Instalação do sistema | 3 min | ✅ |
| 3. Configuração | 2 min | ✅ |
| 4. Testes | 2 min | ✅ |
| **TOTAL** | **12 min** | ✅ |

**🎉 Parabéns! Seu Raspberry Pi está pronto para exibir sinalização digital!**

---

*Desenvolvido pela Facilita TI - Sistema de Sinalização Digital*
