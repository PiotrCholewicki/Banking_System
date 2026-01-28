
# Banking System API

This project implements a simple banking system built with **FastAPI**, **SQLModel**, and **SQLite**.
It provides endpoints for managing clients, balances, and financial transactions.
The API includes validation, error handling, and full CRUD operations.

---
## Running the Server
To start the FastAPI development server, run:

```sh
uvicorn app.main:app --reload
```

The service will start at:
- http://127.0.0.1:8000

Interactive API documentation (Swagger UI) is available at:
- http://127.0.0.1:8000/docs

---
## Project Structure
```
app/
 ├── models/          # SQLModel database models
 ├── routes/          # FastAPI routers
 ├── schemas/         # Request/response schemas
 ├── services/        # Business logic
 ├── validators/      # Input validation functions
 ├── database.py      # Database configuration
 └── main.py          # FastAPI application initialization
```

---
## API Endpoints Documentation

### Clients Endpoints

#### **Create a Client**
**POST** `/clients/`

Creates a new client with an initial balance.

**Request body:**
```json
{
  "name": "John Doe",
  "balance": 200.00
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "balance": "200.00"
}
```

---
#### **Get Client by ID**
**GET** `/clients/{client_id}`

Returns client details including transactions.

**Response example:**
```json
{
  "id": 1,
  "name": "John Doe",
  "balance": "200.00",
  "transactions": []
}
```

---
#### **List All Clients**
**GET** `/clients/`

**Response:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "balance": "200.00"
  }
]
```

---
#### **Delete Client**
**DELETE** `/clients/{client_id}`

Deletes a client and all related transactions.

**Response:**
- Status code **204 No Content**



---
### Transactions Endpoints

#### **Create Transaction**
**POST** `/transactions/`

**Request body:**
```json
{
  "client_id": 1,
  "transaction_type": "deposit",
  "amount": 300.00
}
```

**Response:**
```json
{
  "id": 1,
  "client_id": 1,
  "transaction_type": "deposit",
  "amount": "300.00"
}
```

---
#### **List All Transactions**
**GET** `/transactions/`

**Response:**
```json
[
  {
    "id": 1,
    "client_id": 1,
    "transaction_type": "deposit",
    "amount": "300.00"
  }
]
```

---
## Input Validation Rules
Validation is handled in `app/validators/` and includes:

- Client name must start with a capital letter and contain only letters.
- Balance and amount must be numeric, positive values.
- Transaction type must be either *deposit* or *withdrawal*.
- Client ID must be a positive integer.
- Dates must be valid and not from the future.


****
