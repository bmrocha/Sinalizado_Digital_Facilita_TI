#!/bin/bash

# Script de Início - Sistema de Sinalização Digital
# Facilita TI - Ponto de entrada para instalação

echo "🎯 SISTEMA DE SINALIZAÇÃO DIGITAL - FACILITA TI"
echo "=============================================="
echo ""
echo "📍 Repositório: https://github.com/bmrocha/Sinalizado_Digital_Facilita_TI.git"
echo ""
echo "Este é o ponto de entrada para instalação do sistema."
echo "Escolha uma opção abaixo:"
echo ""
echo "1) 📚 Ler o guia de instalação completo"
echo "2) 📊 Verificar espaço disponível no cartão"
echo "3) 🚀 Instalar o sistema de sinalização"
echo "4) 🔧 Apenas baixar scripts (sem instalar)"
echo "5) 📖 Ver documentação do projeto"
echo "6) ❌ Sair"
echo ""
echo "Digite o número da opção desejada:"

read -r opcao

case $opcao in
    1)
        echo ""
        echo "📚 Abrindo guia de instalação..."
        if [ -f "mostrar_guia.sh" ]; then
            ./mostrar_guia.sh
        else
            curl -s -o mostrar_guia.sh https://raw.githubusercontent.com/bmrocha/Sinalizado_Digital_Facilita_TI/main/raspberry_pi/mostrar_guia.sh
            chmod +x mostrar_guia.sh
            ./mostrar_guia.sh
        fi
        ;;
    2)
        echo ""
        echo "📊 Verificando espaço disponível..."
        if [ -f "verificar_espaco.sh" ]; then
            ./verificar_espaco.sh
        else
            curl -s -o verificar_espaco.sh https://raw.githubusercontent.com/bmrocha/Sinalizado_Digital_Facilita_TI/main/raspberry_pi/verificar_espaco.sh
            chmod +x verificar_espaco.sh
            ./verificar_espaco.sh
        fi
        ;;
    3)
        echo ""
        echo "🚀 Iniciando instalação..."
        if [ -f "install_lite.sh" ]; then
            ./install_lite.sh
        else
            curl -s -o install_lite.sh https://raw.githubusercontent.com/bmrocha/Sinalizado_Digital_Facilita_TI/main/raspberry_pi/install_lite.sh
            chmod +x install_lite.sh
            ./install_lite.sh
        fi
        ;;
    4)
        echo ""
        echo "📥 Baixando scripts..."
        echo "Baixando script de instalação..."
        curl -o install_lite.sh https://raw.githubusercontent.com/bmrocha/Sinalizado_Digital_Facilita_TI/main/raspberry_pi/install_lite.sh
        chmod +x install_lite.sh

        echo "Baixando analisador de espaço..."
        curl -o verificar_espaco.sh https://raw.githubusercontent.com/bmrocha/Sinalizado_Digital_Facilita_TI/main/raspberry_pi/verificar_espaco.sh
        chmod +x verificar_espaco.sh

        echo "Baixando visualizador de guia..."
        curl -o mostrar_guia.sh https://raw.githubusercontent.com/bmrocha/Sinalizado_Digital_Facilita_TI/main/raspberry_pi/mostrar_guia.sh
        chmod +x mostrar_guia.sh

        echo "Baixando player otimizado..."
        curl -o player_lite.py https://raw.githubusercontent.com/bmrocha/Sinalizado_Digital_Facilita_TI/main/raspberry_pi/player_lite.py

        echo ""
        echo "✅ Todos os scripts baixados!"
        echo "Agora você pode:"
        echo "  - Ler o guia: ./mostrar_guia.sh"
        echo "  - Verificar espaço: ./verificar_espaco.sh"
        echo "  - Instalar: ./install_lite.sh"
        ;;
    5)
        echo ""
        echo "📖 Abrindo documentação..."
        echo "Acesse no navegador: https://github.com/bmrocha/Sinalizado_Digital_Facilita_TI/blob/main/README.md"
        echo ""
        echo "Ou baixe localmente:"
        curl -o README.md https://raw.githubusercontent.com/bmrocha/Sinalizado_Digital_Facilita_TI/main/README.md
        echo "✅ README.md baixado!"
        ;;
    6)
        echo ""
        echo "👋 Até logo!"
        exit 0
        ;;
    *)
        echo ""
        echo "❌ Opção inválida. Execute o script novamente."
        exit 1
        ;;
esac

echo ""
echo "🔄 Voltando ao menu principal..."
echo "Execute ./inicio.sh novamente para outras opções."
