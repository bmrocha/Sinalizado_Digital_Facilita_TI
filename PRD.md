# 📋 Product Requirements Document (PRD)
## Sistema de Sinalização Digital - Facilita TI

---

## 🎯 Visão Geral do Produto

### Nome do Produto
**Sistema de Sinalização Digital - Facilita TI**

### Versão
1.0.0

### Data
Outubro 2024

### Autor
Bruno Martins Rocha - Facilita TI

---

## 📈 Resumo Executivo

O Sistema de Sinalização Digital é uma solução completa para exibição de conteúdo digital em TVs conectadas a Raspberry Pi. O sistema oferece controle remoto via painel web, agendamento flexível de conteúdo, e automação de hibernação para economia de energia.

### 🎯 Objetivo Principal
Fornecer uma solução própria e completa de sinalização digital que permita às agências exibirem conteúdo personalizado (links, imagens, vídeos) em TVs de forma automatizada e controlada remotamente.

---

## 👥 Personas e Usuários

### 1. **Administrador do Sistema**
- **Perfil:** Técnico responsável pela manutenção do sistema
- **Necessidades:**
  - Gerenciar usuários e permissões
  - Monitorar status dos dispositivos
  - Configurar agências e dispositivos
  - Acessar logs e relatórios

### 2. **Gestor de Agência**
- **Perfil:** Gerente responsável pelo conteúdo da agência
- **Necessidades:**
  - Cadastrar e gerenciar conteúdo
  - Criar agendamentos por horário/dia
  - Visualizar relatórios de exibição
  - Configurar dispositivos da agência

### 3. **Usuário Final (Cliente da Agência)**
- **Perfil:** Cliente que visualiza o conteúdo nas TVs
- **Necessidades:**
  - Visualizar conteúdo relevante e atualizado
  - Experiência visual agradável
  - Conteúdo exibido nos horários corretos

---

## 🔍 Análise de Mercado

### 🎯 Concorrentes
- **Soluções Comerciais:** Scala, BrightSign, ScreenCloud
- **Soluções Open Source:** Xibo, Conceiva
- **Vantagem Competitiva:** Solução própria, customizável, sem custos de licenciamento

### 📊 Oportunidades de Mercado
- **Setor Bancário:** Agências precisam de sinalização profissional
- **Empresas:** Comunicação interna e externa
- **Escolas/Universidades:** Avisos e informações
- **Shoppings/Hospitais:** Orientação e publicidade

---

## 🎯 Requisitos Funcionais

### 🔐 Autenticação e Autorização
- [x] Sistema de login com JWT
- [x] Controle de acesso por roles (admin, gestor, técnico)
- [x] Expiração automática de tokens
- [x] Recuperação de senha

### 👥 Gerenciamento de Usuários
- [x] CRUD completo de usuários
- [x] Perfis de acesso diferenciados
- [x] Associação usuário-agência
- [x] Histórico de atividades

### 🏢 Gerenciamento de Agências
- [x] Cadastro de agências
- [x] Configurações específicas por agência
- [x] Upload de logos
- [x] Controle de orientação de tela

### 📺 Gerenciamento de Dispositivos
- [x] Registro de Raspberry Pi
- [x] Monitoramento de status online/offline
- [x] Controle remoto de dispositivos
- [x] Relatórios de atividade

### 🎬 Gerenciamento de Conteúdo
- [x] Suporte a múltiplos tipos: links, imagens, vídeos
- [x] Upload de arquivos
- [x] Metadados e descrições
- [x] Validação de arquivos

### 📅 Sistema de Agendamento
- [x] Agendamento por horário específico
- [x] Seleção de dias da semana
- [x] Controle de prioridade
- [x] Validação de conflitos
- [x] Agendamento recorrente

### ⚡ Controle de Hibernação
- [x] Configuração de horários de hibernação
- [x] Controle HDMI-CEC
- [x] Economia de energia
- [x] Wake-up automático

### 📊 Dashboard e Relatórios
- [x] Dashboard com métricas em tempo real
- [x] Status dos dispositivos
- [x] Relatórios de uso
- [x] Gráficos e estatísticas

---

## 🛠️ Requisitos Não Funcionais

### ⚡ Performance
- **Tempo de resposta da API:** < 500ms para operações CRUD
- **Tempo de boot do Raspberry Pi:** < 30 segundos
- **Consumo de memória:** < 512MB no Raspberry Pi
- **Uptime:** 99.9% para serviços críticos

### 🔒 Segurança
- **Criptografia:** JWT com HS256
- **Validação de entrada:** Pydantic/Django Forms
- **CORS:** Configurado para origens específicas
- **Logs de auditoria:** Todas as operações críticas

### 📱 Usabilidade
- **Interface responsiva:** Bootstrap 5
- **Acessibilidade:** WCAG 2.1 AA
- **Navegação intuitiva:** Menus organizados
- **Feedback visual:** Loading states e mensagens

### 🔧 Manutenibilidade
- **Código documentado:** Docstrings em todas as funções
- **Estrutura modular:** Separação clara de responsabilidades
- **Testes automatizados:** Cobertura > 80%
- **Logs estruturados:** JSON format

### 🚀 Escalabilidade
- **Banco de dados:** PostgreSQL para produção
- **Cache:** Redis (planejado para v2.0)
- **Load balancing:** Nginx (planejado)
- **Microserviços:** Arquitetura preparada

---

## 🏗️ Arquitetura do Sistema

### 📊 Diagrama de Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │  Raspberry Pi   │
│   (React)       │◄──►│   (Django)      │◄──►│   (Python)      │
│                 │    │                 │    │                 │
│ - Dashboard     │    │ - API REST      │    │ - Player        │
│ - Forms         │    │ - JWT Auth      │    │ - Chromium      │
│ - Upload        │    │ - Models        │    │ - VLC           │
│ - Charts        │    │ - Views         │    │ - CEC Control   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Database      │
                    │  (PostgreSQL)   │
                    └─────────────────┘
```

### 🗂️ Estrutura de Dados

#### Users (Usuários)
```json
{
  "id": "uuid",
  "username": "string",
  "email": "string",
  "role": "admin|gestor|tecnico",
  "agency_id": "uuid",
  "is_active": true,
  "created_at": "datetime"
}
```

#### Agencies (Agências)
```json
{
  "id": "uuid",
  "name": "string",
  "logo_url": "string",
  "orientation": "horizontal|vertical",
  "hibernation_enabled": true,
  "hibernation_start": "18:00",
  "hibernation_end": "08:00"
}
```

#### Contents (Conteúdos)
```json
{
  "id": "uuid",
  "title": "string",
  "type": "link|image|video",
  "url": "string",
  "duration": 30,
  "agency_id": "uuid",
  "uploaded_by": "uuid",
  "created_at": "datetime"
}
```

#### Schedules (Agendamentos)
```json
{
  "id": "uuid",
  "content_id": "uuid",
  "agency_id": "uuid",
  "start_time": "08:00",
  "end_time": "18:00",
  "days_of_week": "1,2,3,4,5",
  "priority": 1,
  "is_active": true
}
```

#### Devices (Dispositivos)
```json
{
  "id": "uuid",
  "name": "string",
  "agency_id": "uuid",
  "ip_address": "string",
  "mac_address": "string",
  "status": "online|offline",
  "last_seen": "datetime"
}
```

---

## 🔄 Fluxos de Usuário

### 📝 Fluxo de Cadastro de Conteúdo

1. **Usuário faz login** no painel web
2. **Acessa seção "Conteúdo"**
3. **Clica "Novo Conteúdo"**
4. **Seleciona tipo:** Link, Imagem ou Vídeo
5. **Preenche metadados:** Título, descrição, duração
6. **Faz upload do arquivo** (se aplicável)
7. **Salva conteúdo**
8. **Sistema valida e armazena**

### 📅 Fluxo de Agendamento

1. **Usuário acessa "Agendamentos"**
2. **Seleciona conteúdo**
3. **Escolhe agência/dispositivo**
4. **Define horário de início/fim**
5. **Seleciona dias da semana**
6. **Define prioridade**
7. **Salva agendamento**
8. **Sistema valida conflitos**

### 📺 Fluxo de Exibição no Raspberry Pi

1. **Raspberry Pi inicia** e executa player
2. **Player consulta API** por agendamentos ativos
3. **API retorna conteúdo** baseado em horário atual
4. **Player exibe conteúdo** (Chromium/VLC/feh)
5. **Player monitora hibernação** e controla TV
6. **Player envia status** para API periodicamente

---

## 🎨 Design System

### 🎨 Paleta de Cores
- **Primária:** #006633 (Verde Facilita)
- **Secundária:** #FFFFFF (Branco)
- **Background:** #F8F9FA (Cinza claro)
- **Texto:** #212529 (Cinza escuro)
- **Erro:** #DC3545 (Vermelho)

### 🔤 Tipografia
- **Fonte Principal:** Montserrat
- **Tamanhos:** 14px (body), 16px (h6), 18px (h5), 24px (h4), 32px (h3), 48px (h2), 64px (h1)
- **Pesos:** Regular (400), Medium (500), Bold (700)

### 📏 Componentes
- **Botões:** Primary, Secondary, Success, Danger
- **Formulários:** Input, Select, Textarea, File Upload
- **Cards:** Com sombra e bordas arredondadas
- **Modais:** Para confirmações e formulários
- **Tabelas:** Com paginação e filtros

---

## 🧪 Critérios de Aceitação

### ✅ Funcionalidades Core
- [x] Usuário pode fazer login/logout
- [x] Usuário pode gerenciar agências
- [x] Usuário pode fazer upload de conteúdo
- [x] Usuário pode criar agendamentos
- [x] Raspberry Pi exibe conteúdo agendado
- [x] Sistema hiberna TV fora do horário

### ✅ Qualidade
- [x] Interface responsiva em desktop/tablet/mobile
- [x] Validação de formulários no frontend/backend
- [x] Tratamento de erros graceful
- [x] Logs de todas as operações críticas

### ✅ Performance
- [x] API responde em < 500ms
- [x] Frontend carrega em < 3 segundos
- [x] Raspberry Pi inicia player em < 30 segundos

---

## 📋 Plano de Release

### 🚀 Versão 1.0 (Atual)
- ✅ MVP completo e funcional
- ✅ Todas as funcionalidades core implementadas
- ✅ Documentação básica
- ✅ Scripts de instalação

### 🔄 Versão 1.1 (Próxima)
- 🔄 Melhorias na documentação
- 🔄 Correção de bugs identificados
- 🔄 Otimização de performance
- 🔄 Testes automatizados

### 🚀 Versão 2.0 (Planejada)
- 📊 Relatórios avançados
- 🔔 Notificações push
- 💳 Integração com pagamentos
- 📱 App mobile para gestão

---

## 📊 Métricas de Sucesso

### 🎯 KPIs Técnicos
- **Uptime do Sistema:** > 99.5%
- **Tempo Médio de Resposta:** < 300ms
- **Taxa de Sucesso de Upload:** > 95%
- **Tempo de Instalação Raspberry:** < 15 minutos

### 💼 KPIs de Negócio
- **Satisfação do Usuário:** > 4.5/5
- **Tempo de Implementação:** < 2 horas por dispositivo
- **Custo por Dispositivo:** < R$ 500,00
- **ROI:** payback em < 6 meses

---

## 🔧 Dependências Técnicas

### Backend
- **Django:** 4.2.7
- **Django REST Framework:** 3.14.0
- **PostgreSQL:** 13+
- **Redis:** (planejado)

### Frontend
- **React:** 18.2.0
- **Bootstrap:** 5.3.2
- **Axios:** 1.6.0

### Raspberry Pi
- **Python:** 3.9+
- **Chromium:** Browser
- **VLC:** Player de vídeo
- **cec-utils:** Controle HDMI

---

## 📞 Suporte e Manutenção

### 🆘 Níveis de Suporte
- **Nível 1:** Suporte básico via documentação
- **Nível 2:** Suporte técnico via email/telefone
- **Nível 3:** Desenvolvimento de customizações

### 📋 SLA
- **Resposta Inicial:** < 4 horas úteis
- **Resolução Crítica:** < 24 horas
- **Resolução Normal:** < 72 horas

### 🔄 Manutenção
- **Atualizações de Segurança:** Mensais
- **Bug Fixes:** Semanais
- **Novas Features:** Trimestrais

---

## 📈 Roadmap

### ✅ Q4 2024
- [x] Lançamento da versão 1.0
- [x] Documentação completa
- [x] Scripts de instalação refinados

### 🔄 Q1 2025
- [ ] Melhorias de performance
- [ ] Testes automatizados
- [ ] Monitoramento avançado

### 🚀 Q2 2025
- [ ] Relatórios executivos
- [ ] Notificações push
- [ ] App mobile

### 🎯 Q3 2025
- [ ] Integração com sistemas externos
- [ ] IA para otimização de conteúdo
- [ ] Analytics avançado

---

## 📋 Riscos e Mitigações

### ⚠️ Riscos Técnicos
- **Risco:** Instabilidade do Raspberry Pi
  - **Mitigação:** Testes extensivos, fallback automático

- **Risco:** Problemas de conectividade
  - **Mitigação:** Cache local, sincronização offline

### 💼 Riscos de Negócio
- **Risco:** Concorrência de soluções comerciais
  - **Mitigação:** Foco em customização e suporte

- **Risco:** Dependência de hardware específico
  - **Mitigação:** Suporte a múltiplas plataformas

---

## 📞 Contato

**Facilita TI**
- **CEO:** Bruno Martins Rocha
- **Email:** brunomartinsrocha@outlook.com
- **Telefone:** (31) 98439-0045
- **LinkedIn:** https://www.linkedin.com/in/brunomartinsrocha/

---

**Documento Vivo - Última Atualização:** Outubro 2024
