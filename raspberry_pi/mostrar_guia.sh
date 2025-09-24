#!/bin/bash

# Script para mostrar o Guia de Instalação
# Facilita TI - Sistema de Sinalização Digital

GUIA_URL="https://raw.githubusercontent.com/bmrocha/Sinalizado_Digital_Facilita_TI/main/docs/GUIA_INSTALACAO_RASPBERRY.md"

echo "📚 GUIA DE INSTALAÇÃO - SISTEMA DE SINALIZAÇÃO DIGITAL"
echo "=================================================="
echo ""
echo "Baixando guia de instalação..."
echo ""

# Tentar baixar o guia
if curl -s "$GUIA_URL" > guia_temp.md 2>/dev/null; then
    echo "✅ Guia baixado com sucesso!"
    echo ""
    echo "Pressione ENTER para continuar lendo o guia..."
    read

    # Mostrar o guia página por página
    less guia_temp.md

    # Limpar arquivo temporário
    rm -f guia_temp.md

    echo ""
    echo "📋 Guia concluído!"
    echo ""
    echo "Agora você pode:"
    echo "1. Continuar com a instalação: ./install_lite.sh"
    echo "2. Verificar espaço: ./verificar_espaco.sh"
    echo "3. Ler novamente: ./mostrar_guia.sh"
    echo ""

elif [ -f "GUIA_INSTALACAO_RASPBERRY.md" ]; then
    echo "📖 Abrindo guia local..."
    echo ""
    less GUIA_INSTALACAO_RASPBERRY.md

else
    echo "❌ Erro ao baixar o guia."
    echo ""
    echo "Para baixar manualmente:"
    echo "curl -o GUIA_INSTALACAO.md $GUIA_URL"
    echo ""
    echo "Ou acesse: https://github.com/bmrocha/Sinalizado_Digital_Facilita_TI/blob/main/docs/GUIA_INSTALACAO_RASPBERRY.md"
    echo ""
fi
