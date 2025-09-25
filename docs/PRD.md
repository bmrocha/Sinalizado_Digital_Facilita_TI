# Product Requirements Document (PRD)
## Sistema de Sinalização Digital - Facilita TI

### 📋 Visão Geral do Produto

O Sistema de Sinalização Digital da Facilita TI é uma solução completa para gerenciamento remoto de conteúdo em TVs conectadas a Raspberry Pi. O sistema permite exibir conteúdos diversos (links web, imagens, vídeos) com controle total sobre agendamentos, rotação de tela, hibernação automática e monitoramento em tempo real.

### 🎯 Objetivos do Produto

- **Exibição Inteligente**: Mostrar conteúdo relevante em TVs de agências bancárias
- **Gerenciamento Remoto**: Painel web intuitivo para controle completo do sistema
- **Automação**: Hibernação automática fora do horário comercial via HDMI-CEC
- **Monitoramento**: Status em tempo real dos dispositivos Raspberry Pi
- **Escalabilidade**: Suporte a múltiplas agências e dispositivos
- **Segurança**: Autenticação robusta e controle de acesso por agência

### 👥 Personas do Usuário

#### 1. **Administrador do Sistema**
- **Perfil**: Gerente de TI ou administrador técnico
- **Necessidades**:
  - Configurar e gerenciar múltiplas agências
  - Monitorar status de todos os dispositivos
  - Gerenciar usuários e permissões
  - Receber alertas de falhas
- **Cenário de Uso**: Configura nova agência, adiciona dispositivos, monitora performance

#### 2. **Gerente de Agência**
- **Perfil**: Responsável pela agência bancária
- **Necessidades**:
  - Agendar conteúdo específico da agência
  - Visualizar relatórios de exibição
  - Personalizar identidade visual (logo)
  - Controlar horários de funcionamento
- **Cenário de Uso**: Agenda promoção especial, verifica se conteúdo foi exibido

#### 3. **Usuário Final (Cliente da Agência)**
- **Perfil**: Cliente que vê o conteúdo nas TVs
- **Necessidades**:
  - Visualizar informações relevantes (promoções, produtos, avisos)
  - Experiência visual agradável e profissional
- **Cenário de Uso**: Vê informações sobre novos produtos enquanto aguarda atendimento

### 🔧 Requisitos Funcionais

#### RF001: Autenticação e Autorização
- Sistema de login seguro com JWT
- Controle de acesso baseado em roles (admin, manager, user)
- Recuperação de senha
- Sessão expirável

#### RF002: Gerenciamento de Agências
- CRUD completo de agências
- Configuração de IP, orientação de tela, hibernação
- Upload de logotipo personalizado
- Associação de dispositivos por agência

#### RF003: Gerenciamento de Conteúdo
- Suporte a múltiplos tipos: links web, imagens, vídeos
- Upload de arquivos com validação
- Metadados: título, descrição, duração
- Controle de versão de conteúdo

#### RF004: Sistema de Agendamento
- Agendamento por horário e dias da semana
- Priorização de conteúdo
- Conflito de horários automático
- Agendamento recorrente

#### RF005: Controle de Dispositivos
- Registro automático de Raspberry Pi
- Monitoramento de status (online/offline)
- Controle remoto de orientação de tela
- Sincronização automática de configuração

#### RF006: Exibição de Conteúdo
- Reprodução em tela cheia (kiosk mode)
- Rotação automática de tela (horizontal/vertical)
- Hibernação automática via HDMI-CEC
- Fallback para conteúdo padrão

#### RF007: Interface Web
- Dashboard responsivo com métricas
- Formulários intuitivos para CRUD
- Visualização de calendário de agendamentos
- Monitor em tempo real de dispositivos

### 📱 Requisitos Não Funcionais

#### RNF001: Performance
- Tempo de resposta da API < 500ms
- Sincronização de dispositivos a cada 30 segundos
- Suporte a até 100 dispositivos simultâneos
- Carregamento do frontend < 3 segundos

#### RNF002: Segurança
- Criptografia de senhas (bcrypt)
- Tokens JWT com expiração
- Validação de entrada em todas as APIs
- Logs de auditoria para ações críticas

#### RNF003: Usabilidade
- Interface responsiva (desktop/tablet/mobile)
- Navegação intuitiva com breadcrumbs
- Feedback visual para ações do usuário
- Acessibilidade WCAG 2.1 AA

#### RNF004: Compatibilidade
- Raspberry Pi 4 com Raspberry Pi OS Lite
- Navegadores modernos (Chrome, Firefox, Safari)
- TVs com HDMI-CEC (Samsung, LG, Sony)

#### RNF005: Escalabilidade
- Arquitetura modular para expansão
- Banco de dados PostgreSQL para produção
- Cache Redis (futuro)
- Load balancing preparado

#### RNF006: Manutenibilidade
- Código bem documentado
- Testes automatizados (meta: 80% cobertura)
- Logs estruturados
- Documentação técnica completa

### 🏗️ Arquitetura do Sistema

#### Componentes Principais

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │     Backend     │    │  Raspberry Pi   │
│   (React)       │◄──►│   (Django)      │◄──►│   (Python)      │
│                 │    │                 │    │                 │
│ - Dashboard     │    │ - API REST      │    │ - Player        │
│ - Forms         │    │ - Auth JWT      │    │ - Chromium      │
│ - Charts        │    │ - Database      │    │ - VLC           │
│ - Real-time     │    │ - File Upload   │    │ - CEC Control   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

#### Fluxo de Dados

1. **Configuração**: Admin configura agência e conteúdo via painel web
2. **Agendamento**: Sistema calcula conteúdo atual baseado em horário
3. **Sincronização**: Raspberry Pi consulta API a cada 30 segundos
4. **Exibição**: Player local reproduz conteúdo apropriado
5. **Monitoramento**: Status enviado para API em tempo real

### 🔄 Fluxos de Usuário

#### FU001: Configuração Inicial
1. Admin acessa painel web
2. Faz login com credenciais padrão
3. Cria primeira agência
4. Configura dispositivo Raspberry Pi
5. Testa conexão e exibição

#### FU002: Agendamento de Conteúdo
1. Manager acessa seção de conteúdo
2. Faz upload de imagem/vídeo ou insere URL
3. Define metadados e duração
4. Cria agendamento com horário e prioridade
5. Sistema valida conflitos automaticamente

#### FU003: Monitoramento de Dispositivos
1. Admin visualiza dashboard
2. Verifica status de todos os dispositivos
3. Identifica dispositivos offline
4. Recebe alertas automáticos
5. Toma ações corretivas

### 🎨 Design System

#### Paleta de Cores (Sicoob)
- **Primária**: Verde (#006600)
- **Secundária**: Azul (#003399)
- **Neutro**: Cinza (#666666)
- **Background**: Branco (#FFFFFF)
- **Texto**: Preto (#000000)

#### Tipografia
- **Fonte Principal**: Arial, sans-serif
- **Títulos**: 24px, bold
- **Corpo**: 14px, regular
- **Labels**: 12px, medium

#### Componentes
- **Botões**: Rounded corners, hover effects
- **Formulários**: Labels acima dos campos, validação visual
- **Cards**: Shadow sutil, bordas arredondadas
- **Tabelas**: Headers fixos, paginação

### ✅ Critérios de Aceitação

#### CA001: Autenticação
- [ ] Login funciona com credenciais corretas
- [ ] Token JWT válido por 24 horas
- [ ] Logout limpa sessão corretamente
- [ ] Tentativas de acesso não autorizado bloqueadas

#### CA002: Gerenciamento de Conteúdo
- [ ] Upload de arquivos até 100MB
- [ ] Validação de tipos MIME
- [ ] Preview de imagens e vídeos
- [ ] Exclusão remove arquivo do servidor

#### CA003: Agendamento
- [ ] Conflitos detectados automaticamente
- [ ] Prioridade respeitada
- [ ] Agendamentos recorrentes funcionam
- [ ] Fuso horário correto

#### CA004: Raspberry Pi
- [ ] Instalação automática em < 5 minutos
- [ ] Sincronização a cada 30 segundos
- [ ] Hibernação funciona com TVs compatíveis
- [ ] Recuperação automática de falhas

### 📊 Métricas de Sucesso

#### Métricas Técnicas
- **Uptime**: > 99.5%
- **Tempo Médio de Resposta**: < 300ms
- **Taxa de Erro da API**: < 0.1%
- **Cobertura de Testes**: > 80%

#### Métricas de Negócio
- **Facilidade de Instalação**: < 15 minutos por dispositivo
- **Tempo de Configuração**: < 30 minutos por agência
- **Satisfação do Usuário**: > 4.5/5 (pesquisa)
- **Redução de Custos**: 70% vs soluções comerciais

### 🗺️ Roadmap do Produto

#### Fase 1: MVP (Atual)
- ✅ Autenticação básica
- ✅ CRUD de agências e conteúdo
- ✅ Agendamento simples
- ✅ Player Raspberry Pi básico
- ✅ Interface web responsiva

#### Fase 2: Melhorias (Próximas 3 meses)
- 🔄 Notificações push
- 🔄 Relatórios avançados
- 🔄 Suporte a múltiplos idiomas
- 🔄 Cache Redis
- 🔄 Testes automatizados

#### Fase 3: Expansão (Próximos 6 meses)
- 📋 Integração com sistemas externos
- 📋 Analytics em tempo real
- 📋 Suporte a playlists
- 📋 API webhooks
- 📋 Mobile app para gerenciamento

#### Fase 4: Enterprise (Próximo ano)
- 🏢 Multi-tenancy completo
- 🏢 SLA garantido
- 🏢 Suporte 24/7
- 🏢 Integração com Active Directory
- 🏢 Backup automático

### 📋 Riscos e Mitigações

#### Risco Técnico
- **Perda de conectividade**: Sistema offline-graceful com cache local
- **Falha de hardware**: Redundância de dispositivos por agência
- **Atualização problemática**: Rollback automático e testes A/B

#### Risco de Negócio
- **Adoção baixa**: Treinamento obrigatório e suporte dedicado
- **Concorrência**: Foco em customização para Sicoob
- **Mudanças regulatórias**: Arquitetura flexível para compliance

### 📞 Suporte e Manutenção

#### Níveis de Suporte
- **L1**: Helpdesk básico (documentação, FAQs)
- **L2**: Suporte técnico (configuração, troubleshooting)
- **L3**: Desenvolvimento (bugs críticos, melhorias)

#### SLA de Suporte
- **Crítico**: Resposta em 1 hora, resolução em 4 horas
- **Alto**: Resposta em 4 horas, resolução em 24 horas
- **Médio**: Resposta em 24 horas, resolução em 72 horas
- **Baixo**: Resposta em 72 horas, resolução em 1 semana

---

**Versão**: 1.0
**Data**: Outubro 2024
**Autor**: Bruno Martins Rocha - Facilita TI
**Aprovado por**: Equipe Técnica Sicoob Credisete
