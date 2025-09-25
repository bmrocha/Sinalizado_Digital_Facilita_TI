fuo # API REST - Sistema de Sinalização Digital

## Visão Geral
no 
Esta documentação descreve a API REST do Sistema de Sinalização Digital da Facilita TI. A API é construída com Django REST Framework e fornece endpoints para gerenciamento completo do sistema.
## Autenticação
Base URL: `http://localhost:8000/api`

A API utiliza autenticação JWT (JSON Web Tokens). Para acessar endpoints protegidos, inclua o token no header:

```
Authorization: Bearer <your-jwt-token>
```

### Login

**POST** `/auth/login`

Faz login e retorna token JWT.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "string",
    "email": "string",
    "role": "admin"
  }
}
```

### Registrar Usuário

**POST** `/auth/register`

Cria um novo usuário.

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "role": "admin"
}
```

### Perfil do Usuário

**GET** `/auth/me`

Retorna informações do usuário autenticado.

## Usuários

### Listar Usuários

**GET** `/users`

Retorna lista paginada de usuários.

**Query Parameters:**
- `skip` (int): Número de registros para pular (default: 0)
- `limit` (int): Número máximo de registros (default: 100)

### Criar Usuário

**POST** `/users`

Cria um novo usuário.

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "role": "admin"
}
```

### Atualizar Usuário

**PUT** `/users/{user_id}`

Atualiza um usuário existente.

### Excluir Usuário

**DELETE** `/users/{user_id}`

Exclui um usuário.

## Agências

### Listar Agências

**GET** `/agencies`

Retorna lista de agências.

### Criar Agência

**POST** `/agencies`

Cria uma nova agência.

**Request Body:**
```json
{
  "name": "string",
  "ip_address": "192.168.1.100",
  "orientation": "horizontal",
  "hibernation_enabled": true,
  "hibernation_start": "18:00",
  "hibernation_end": "08:00"
}
```

### Atualizar Agência

**PUT** `/agencies/{agency_id}`

Atualiza uma agência existente.

### Excluir Agência

**DELETE** `/agencies/{agency_id}`

Exclui uma agência.

### Upload de Logo

**POST** `/agencies/{agency_id}/logo`

Faz upload do logotipo da agência.

**Content-Type:** `multipart/form-data`

## Conteúdos

### Listar Conteúdos

**GET** `/contents`

Retorna lista de conteúdos.

### Criar Conteúdo

**POST** `/contents`

Cria um novo conteúdo.

**Request Body:**
```json
{
  "title": "string",
  "type": "link",
  "url": "https://example.com",
  "description": "string",
  "duration": 30
}
```

### Upload de Arquivo

**POST** `/contents/upload`

Faz upload de arquivo (imagem/vídeo).

**Content-Type:** `multipart/form-data`

### Atualizar Conteúdo

**PUT** `/contents/{content_id}`

Atualiza um conteúdo existente.

### Excluir Conteúdo

**DELETE** `/contents/{content_id}`

Exclui um conteúdo.

## Agendamentos

### Listar Agendamentos

**GET** `/schedules`

Retorna lista de agendamentos.

### Agendamentos Ativos

**GET** `/schedules/current`

Retorna agendamentos ativos no momento atual.

**Query Parameters:**
- `current_time` (string): Horário atual (HH:MM)
- `current_weekday` (string): Dia da semana (0-6)

### Criar Agendamento

**POST** `/schedules`

Cria um novo agendamento.

**Request Body:**
```json
{
  "content_id": 1,
  "agency_id": 1,
  "start_time": "08:00",
  "end_time": "18:00",
  "days_of_week": "1,2,3,4,5",
  "priority": 1,
  "is_active": true
}
```

### Atualizar Agendamento

**PUT** `/schedules/{schedule_id}`

Atualiza um agendamento existente.

### Excluir Agendamento

**DELETE** `/schedules/{schedule_id}`

Exclui um agendamento.

## Dispositivos

### Listar Dispositivos

**GET** `/devices`

Retorna lista de dispositivos.

### Registrar Dispositivo

**POST** `/devices`

Registra um novo dispositivo Raspberry Pi.

**Request Body:**
```json
{
  "name": "Raspberry Pi Agência Centro",
  "agency_id": 1,
  "ip_address": "192.168.1.100",
  "mac_address": "AA:BB:CC:DD:EE:FF",
  "version": "1.0.0"
}
```

### Atualizar Dispositivo

**PUT** `/devices/{device_id}`

Atualiza um dispositivo existente.

### Atualizar Status

**PUT** `/devices/{device_id}/status`

Atualiza o status de um dispositivo.

**Request Body:**
```json
{
  "status": "online",
  "details": {
    "cpu_percent": 45.2,
    "memory_percent": 67.8,
    "temperature": 52.3
  }
}
```

### Remover Dispositivo

**DELETE** `/devices/{device_id}`

Remove um dispositivo.

## Códigos de Status HTTP

- **200**: OK - Requisição bem-sucedida
- **201**: Created - Recurso criado com sucesso
- **400**: Bad Request - Dados inválidos
- **401**: Unauthorized - Token inválido ou ausente
- **403**: Forbidden - Acesso negado
- **404**: Not Found - Recurso não encontrado
- **422**: Unprocessable Entity - Dados de validação inválidos
- **500**: Internal Server Error - Erro interno do servidor

## Tratamento de Erros

Todos os endpoints retornam erros no formato:

```json
{
  "detail": "Mensagem de erro descritiva"
}
```

## Rate Limiting

A API implementa rate limiting para prevenir abuso:
- 100 requisições por minuto para endpoints de leitura
- 10 requisições por minuto para endpoints de escrita

## Versionamento

A API utiliza versionamento no path:
- Versão atual: `v1`
- Futuras versões: `v2`, `v3`, etc.

## Exemplos de Uso

### Login e Obtenção de Token

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "password123"
  }'
```

### Criar Agência

```bash
curl -X POST "http://localhost:8000/api/agencies" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "Agência Centro",
    "ip_address": "192.168.1.100",
    "orientation": "horizontal",
    "hibernation_enabled": true,
    "hibernation_start": "18:00",
    "hibernation_end": "08:00"
  }'
```

### Upload de Logo

```bash
curl -X POST "http://localhost:8000/api/agencies/1/logo" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@logo.png"
```
## WebSocket (Futuro)

Para funcionalidades em tempo real, considere implementar WebSocket para:
- Notificações push para dispositivos
- Monitoramento em tempo real
- Sincronização instantânea de status

## Testes

Para testar a API, use ferramentas como:
- **curl** (linha de comando)
- **Postman** (interface gráfica)
- **Insomnia** (interface gráfica)
- **Swagger UI** (disponível em `/docs`)

## Suporte

Para dúvidas sobre a API, consulte:
- Documentação completa: `/docs` (Swagger UI)
- Schema OpenAPI: `/openapi.json`
- Equipe de desenvolvimento: suporte@sicoobcredisete.com.br
