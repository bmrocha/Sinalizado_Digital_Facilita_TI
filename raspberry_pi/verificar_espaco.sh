#!/bin/bash

# Script de Verificação de Espaço - Raspberry Pi OS Lite
# Facilita TI - Sistema de Sinalização Digital

echo "🔍 ANÁLISE DE ESPAÇO - RASPBERRY PI OS LITE"
echo "============================================="
echo ""

# Verificar espaço total do cartão
echo "💾 Espaço total do cartão:"
df -h / | awk 'NR==2 {print "   Total: " $2 " (" $3 " usado, " $4 " disponível)"}'
echo ""

# Verificar espaço ocupado pelo sistema
echo "📊 Espaço ocupado pelo sistema:"
du -sh /usr /lib /bin /sbin 2>/dev/null | sort -hr | head -5
echo ""

# Simular instalação do sistema de sinalização
echo "📦 Simulação da instalação do Sistema de Sinalização:"
echo "   - Chromium Browser: ~45MB"
echo "   - VLC Player: ~25MB"
echo "   - Python + dependências: ~15MB"
echo "   - Scripts e configuração: ~2MB"
echo "   - Logs e cache: ~5MB"
echo "   -----------------------------"
echo "   TOTAL ESTIMADO: ~92MB"
echo ""

# Calcular espaço disponível para conteúdo
TOTAL_GB=$(df / | awk 'NR==2 {print int($2/1024/1024)}')
USADO_GB=$(df / | awk 'NR==2 {print int($3/1024/1024)}')
DISPONIVEL_GB=$(df / | awk 'NR==2 {print int($4/1024/1024)}')

echo "🎯 PROJEÇÃO DE USO (Cartão 32GB):"
echo "   Sistema Operacional: ${USADO_GB}GB"
echo "   Sistema de Sinalização: ~0.1GB"
echo "   Conteúdo (vídeos/imagens): ~${DISPONIVEL_GB}GB"
echo "   -----------------------------"
echo "   ESPAÇO TOTAL: 32GB"
echo ""

# Verificar se há espaço suficiente
if [ $DISPONIVEL_GB -gt 25 ]; then
    echo "✅ EXCELENTE! Você terá aproximadamente ${DISPONIVEL_GB}GB para conteúdo!"
elif [ $DISPONIVEL_GB -gt 15 ]; then
    echo "✅ BOM! Você terá aproximadamente ${DISPONIVEL_GB}GB para conteúdo."
elif [ $DISPONIVEL_GB -gt 5 ]; then
    echo "⚠️  ATENÇÃO! Apenas ${DISPONIVEL_GB}GB disponíveis para conteúdo."
    echo "   Considere limpar o sistema ou usar cartão maior."
else
    echo "❌ PROBLEMA! Pouco espaço disponível (${DISPONIVEL_GB}GB)."
    echo "   Recomendamos usar cartão de 64GB ou maior."
fi

echo ""
echo "💡 DICAS PARA ECONOMIZAR ESPAÇO:"
echo "   • Use Raspberry Pi OS Lite (sem interface gráfica)"
echo "   • Limpe cache: sudo apt autoremove && sudo apt autoclean"
echo "   • Configure logs rotativos"
echo "   • Armazene conteúdo em servidor remoto"
echo "   • Use compressão para vídeos"

echo ""
echo "📋 RECOMENDAÇÕES FINAIS:"
echo "   ✅ Sistema de Sinalização: ~92MB"
echo "   ✅ Instalação: ~3 minutos"
echo "   ✅ Configuração: ~2 minutos"
echo "   ✅ Espaço para conteúdo: ~${DISPONIVEL_GB}GB"
echo ""
echo "🎉 Pronto para instalar!"
