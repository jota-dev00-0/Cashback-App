# 💰 Cashback App

Aplicação fullstack simples para cálculo de cashback com histórico por IP.

---

## 🚀 Visão Geral

Este projeto permite que o usuário:

* Informe o **tipo de cliente** (`vip` ou `standard`)
* Informe o **valor da compra**
* Receba o valor de **cashback calculado (base + bônus)**
* Visualize o **histórico de consultas**, limitado ao seu próprio IP

---

## 🧱 Arquitetura

```
Frontend (HTML + CSS + JS)
        ↓ HTTP
Backend (FastAPI - Python)
        ↓ SQLAlchemy
Banco de Dados (PostgreSQL)
```

---

## ⚙️ Tecnologias Utilizadas

### Backend

* Python
* FastAPI
* Uvicorn
* SQLAlchemy (ORM)
* PostgreSQL
* psycopg2-binary
* python-dotenv

### Frontend

* HTML
* CSS
* JavaScript (puro)

### Deploy (sugestão)

* Backend: Render
* Frontend: Vercel
* Banco: Supabase

---

## 📡 Endpoints da API

### 🔹 Calcular Cashback

```
POST /api/v1/cashback
```

**Request Body:**

```json
{
  "client_type": "vip",
  "purchase_value": 600
}
```

**Response:**

```json
{
  "client_type": "vip",
  "purchase_value": 600,
  "cashback_base": 60,
  "cashback_bonus": 6,
  "cashback_total": 66
}
```

---

### 🔹 Histórico por IP

```
GET /api/v1/cashback/history
```

**Response:**

```json
[
  {
    "id": 2,
    "client_type": "standard",
    "purchase_value": 600,
    "cashback_base": 60,
    "cashback_bonus": 0,
    "cashback_total": 60,
    "created_at": "2026-04-13T05:09:29.436783"
  },
  {
    "id": 1,
    "client_type": "standard",
    "purchase_value": 500,
    "cashback_base": 25,
    "cashback_bonus": 0,
    "cashback_total": 25,
    "created_at": "2026-04-13T05:08:47.716888"
  }
]
```

---

## 🧠 Regras de Negócio

* Cashback base: **10% do valor da compra**
* Cliente `vip`: recebe **+10% sobre o cashback base**
* Cliente `standard`: não recebe bônus
* O retorno contém:

  * `cashback_base`
  * `cashback_bonus`
  * `cashback_total`

---

## 🗄️ Banco de Dados

### Tabela: `historico`

```sql
CREATE TABLE historico (
    id SERIAL PRIMARY KEY,
    ip VARCHAR(50),
    client_type VARCHAR(10),
    purchase_value DECIMAL,
    cashback_base DECIMAL,
    cashback_bonus DECIMAL,
    cashback_total DECIMAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🖥️ Como Rodar o Projeto Localmente

### 🔹 Backend

```bash
cd backend

poetry install

poetry run uvicorn main:app --reload
```

A API estará disponível em:

```
http://localhost:8000
```

Documentação automática:

```
http://localhost:8000/docs
```

---

### 🔹 Frontend

Abra o arquivo:

```
frontend/index.html
```

Ou utilize uma extensão como Live Server no VSCode.

---

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` no backend:

```env
DATABASE_URL=postgresql://user:password@host:port/database
```

---

## 🌐 Deploy

### Backend (Render)

* Conectar repositório
* Configurar:

  * Start command:

    ```
    uvicorn main:app --host 0.0.0.0 --port 10000
    ```
  * Variável de ambiente: `DATABASE_URL`

---

### Frontend (Vercel / Netlify)

* Upload da pasta `frontend/`
* Configurar URL da API no JS

---

## ⚠️ Observações

* O histórico é filtrado por IP
* Em produção, o IP pode ser obtido via:

  ```
  x-forwarded-for
  ```
* O plano gratuito pode ter cold start (delay inicial)

---

## 📌 Melhorias Futuras

* Validação com Pydantic
* Paginação no histórico
* Melhor tratamento de erros
* Autenticação (JWT)
* UI mais elaborada

---

## 👨‍💻 Autor

Projeto desenvolvido como desafio técnico com foco em:

* Backend com FastAPI
* Integração com banco de dados relacional
* Arquitetura simples e escalável
* Deploy em ambiente real

---
