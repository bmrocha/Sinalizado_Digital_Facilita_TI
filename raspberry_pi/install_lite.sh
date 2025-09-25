#!/bin/bash

# Digital Signage Installation Script - VERSÃO LITE
# Facilita TI - Sistema de Sinalização Digital
# Otimizado para Raspberry Pi OS Lite com cartão 32GB

set -e

echo "=== Instalação do Sistema de Sinalização Digital ==="
echo "Versão Otimizada para Raspberry Pi OS Lite"
echo ""
echo "📚 ANTES DE COMEÇAR:"
echo "   Recomendamos ler o guia de instalação completo."
echo "   Deseja ver o guia agora? (s/n)"
echo ""

read -r resposta
if [[ "$resposta" =~ ^[Ss]$ ]]; then
    # Tentar mostrar o guia
    if [ -f "mostrar_guia.sh" ]; then
        ./mostrar_guia.sh
    else
        echo "Baixando guia..."
        curl -s -o mostrar_guia.sh https://raw.githubusercontent.com/bmrocha/Sinalizado_Digital/main/raspberry_pi/mostrar_guia.sh
        chmod +x mostrar_guia.sh
        ./mostrar_guia.sh
    fi

    echo ""
    echo "✅ Pronto para continuar com a instalação? (s/n)"
    read -r continuar
    if [[ ! "$continuar" =~ ^[Ss]$ ]]; then
        echo "Instalação cancelada. Execute o script novamente quando estiver pronto."
        exit 0
    fi
fi

echo ""
echo "🚀 Iniciando instalação..."
echo ""

# Verificar se está rodando como root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Execute este script como usuário normal, não como root"
    exit 1
fi

# Atualizar lista de pacotes
echo "📦 Atualizando lista de pacotes..."
sudo apt update

# Instalar apenas pacotes essenciais
echo "📦 Instalando pacotes essenciais..."
sudo apt install -y \
    python3-pip \
    chromium-browser \
    vlc \
    cec-utils \
    curl

# Instalar dependências Python
echo "🐍 Instalando dependências Python..."
pip3 install requests psutil

# Criar diretório do sistema
echo "📁 Criando diretório do sistema..."
mkdir -p ~/sinalizacao_digital
cd ~/sinalizacao_digital

# Baixar script do player otimizado
echo "⬇️  Baixando script do player..."
curl -o player.py https://raw.githubusercontent.com/bmrocha/Sinalizado_Digital_Facilita_TI/main/raspberry_pi/player_lite.py

# Tornar executável
chmod +x player.py

# Criar arquivo de configuração
echo "⚙️  Criando configuração..."
cat > config.json << 'EOF'
{
    "agency_id": 1,
    "device_id": "raspberry_$(hostname)",
    "api_url": "http://SEU_SERVIDOR:8000/api/v1",
    "orientation": "horizontal",
    "hibernation_enabled": true,
    "hibernation_start": "18:00",
    "hibernation_end": "08:00",
    "check_interval": 30
}
EOF

# Criar serviço systemd
echo "🔧 Criando serviço do sistema..."
sudo tee /etc/systemd/system/sinalizacao.service > /dev/null <<EOF
[Unit]
Description=Sistema de Sinalização Digital
After=network.target
Wants=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/sinalizacao_digital
ExecStart=/usr/bin/python3 $HOME/sinalizacao_digital/player.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Habilitar e iniciar serviço
echo "🚀 Habilitando serviço..."
sudo systemctl daemon-reload
sudo systemctl enable sinalizacao.service
sudo systemctl start sinalizacao.service

# Configurar Chromium para modo kiosk
echo "🖥️  Configurando Chromium..."
mkdir -p ~/.config/chromium/Default
echo '{"first_run":false,"optimize_webui_for_touch":true}' > ~/.config/chromium/Default/Preferences

echo ""
echo "✅ Instalação concluída com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "1. Edite o arquivo config.json com os dados do seu servidor"
echo "2. Reinicie o Raspberry Pi: sudo reboot"
echo "3. Verifique o status: sudo systemctl status sinalizacao"
echo "4. Veja os logs: sudo journalctl -u sinalizacao -f"
echo ""
echo "💾 Espaço ocupado: ~50MB (incluindo dependências)"
echo "📺 O sistema iniciará automaticamente após a reinicialização"
