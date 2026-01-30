
# Banking System API

This project implements a secure banking system built with **FastAPI**, **SQLModel**, and **SQLite**.  
It features user accounts, client accounts, JWT authentication, transactions, and money transfers.  
Automated tests cover **~96%** of code.

---

## Running the Server

To start the FastAPI development server, run:

```sh
uvicorn app.main:app --reload
```

API documentation (Swagger UI):

- http://127.0.0.1:8000/docs

---

## Project Structure

```
app/
 ├── auth/            # JWT auth, hashing, permissions
 ├── models/          # SQLModel ORM models
 ├── routes/          # API endpoints
 ├── schemas/         # Request/response schemas
 ├── services/        # Business logic
 ├── validators/      # Optional input validators
 ├── database.py      # DB engine and Session
 └── main.py          # FastAPI app initialization
```

---

## Authentication Endpoints

### Register User  
**POST** `/auth/register`

Creates a new user and automatically creates a linked client account.

Example:

```json
{
  "username": "john",
  "password": "abcd1234",
  "balance": 200
}
```

---

### Login  
**POST** `/auth/login`

Form-data:

```
username=<name>
password=<password>
```

Response contains JWT token.

---

### Current User  
**GET** `/auth/me`

Returns the authenticated user.

---

### Delete My Account  
**DELETE** `/auth/delete`

Deletes the user, linked client, and all transactions.

---

## Client Endpoints

### Get My Client  
**GET** `/clients/me/`

Returns client data for the authenticated user.

---

### Get My Transactions  
**GET** `/clients/me/transactions`

Returns all transactions of the authenticated client.

---

## Transaction Endpoints

### Create Transaction  
**POST** `/transactions/`

Example:

```json
{
  "transaction_type": "deposit",
  "amount": 300
}
```

---

## Transfer Endpoints

### Create Transfer  
**POST** `/transfers/`

Transfers money from the logged-in user to another client.

Example:

```json
{
  "receiver_id": 4,
  "amount": 50
}
```

---

## Admin Endpoints

(Require user role = admin)

```
GET    /admin/users/
GET    /admin/clients/
GET    /admin/transactions/
GET    /admin/clients/{client_id}
DELETE /admin/users/{username}
```

---

## Input Rules

- amounts must be positive  
- transfer amount cannot be 0  
- withdrawal/transfer requires sufficient balance  
- user cannot transfer to themselves  
- all protected routes require JWT token  
- admin routes require admin role  

---

## Tests

The project contains an extensive Pytest suite covering:

- authentication  
- client operations  
- transactions  
- transfers  
- admin routes  
- permissions and JWT flow  

**Approx. 96% of code is covered by automated tests.**

---
