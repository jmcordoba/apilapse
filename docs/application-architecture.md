# Application Architecture

## Overview

**Apilapse** is a Flask-based REST API application that allows users to register, manage accounts, and configure HTTP requests to be monitored. It follows a **3-tier Layered Architecture** with the **Repository Pattern** for data access.

---

## Directory Structure

```
app/
├── app.py                          # Main Flask entry point
├── conf/
│   └── dev.json                    # Runtime configuration (host, port, DB, email, JWT)
├── db/
│   └── apilapse.db                 # SQLite database file
├── exceptions.py                   # Custom exception classes
├── logs/
│   └── app.log                     # Application logs
├── requirements.txt                # Python dependencies
├── routes/                         # Presentation layer — HTTP route handlers
│   ├── health.py                   # Health check endpoints
│   ├── hello.py                    # Hello endpoint
│   ├── ip.py                       # User authentication & management endpoints
│   ├── requests.py                 # HTTP request management endpoints
│   └── web.py                      # Web template routes
├── src/
│   ├── app/                        # Business logic layer
│   │   ├── request/                # Request use cases (create, get, update, delete)
│   │   ├── shared/                 # Shared validators (email, password, method, etc.)
│   │   └── user/                   # User use cases (create, login, validate, etc.)
│   └── infra/                      # Infrastructure layer
│       ├── account/sqlite.py       # Account repository
│       ├── db/init.py              # Database schema initialization
│       ├── email/gmail.py          # Gmail SMTP email service
│       ├── request/sqlite.py       # Request repository
│       ├── shared/                 # Shared infra utilities (config, auth, params)
│       ├── sqlite3.py              # Generic SQLite database wrapper
│       ├── status.py               # Application status helper
│       └── user/sqlite.py          # User repository
├── test/                           # Unit tests
└── web/                            # Frontend templates and static files
    ├── static/
    └── templates/
        ├── account/
        ├── requests/
        └── user/
```

---

## Architectural Pattern

The application follows a **3-tier Layered Architecture** where each layer has a clear responsibility and communicates only with the layer below it.

```
┌──────────────────────────────────────────────────┐
│             Presentation Layer                   │
│   routes/health.py  routes/ip.py                 │
│   routes/requests.py  routes/web.py              │
│   HTTP endpoints, error handling, responses      │
└──────────────────┬───────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────┐
│          Business Logic Layer                    │
│   src/app/user/*   src/app/request/*             │
│   src/app/shared/* (validators)                  │
│   Use cases, validation, orchestration           │
└──────────────────┬───────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────┐
│           Infrastructure Layer                   │
│   src/infra/user/sqlite.py                       │
│   src/infra/account/sqlite.py                    │
│   src/infra/request/sqlite.py                    │
│   src/infra/sqlite3.py  (DB wrapper)             │
│   src/infra/email/gmail.py  (email service)      │
│   src/infra/shared/*  (config, auth, params)     │
└──────────────────┬───────────────────────────────┘
                   │
                   ▼
          ┌─────────────────┐
          │   SQLite DB     │
          │  apilapse.db    │
          └─────────────────┘
```

---

## Layer Descriptions

### Presentation Layer (`routes/`)

Handles HTTP requests and responses. Each route file groups a set of related endpoints:

| File | Endpoints |
|------|-----------|
| `health.py` | `GET /health/v1/status` |
| `hello.py` | `GET /hello` |
| `ip.py` | `/ip/v1/*` — user registration, login, logout, profile, password management |
| `requests.py` | `/requests/v1/*` — create, read, update, delete request configurations |
| `web.py` | `/` `/login` `/signup` `/home` `/requests` — HTML template rendering |

Routes catch exceptions raised by the business layer and map them to appropriate HTTP status codes.

### Business Logic Layer (`src/app/`)

Contains the application use cases organized by domain:

**User domain (`src/app/user/`):**

| Module | Responsibility |
|--------|----------------|
| `create.py` | User registration — validates input, hashes credentials, sends validation email |
| `login.py` | Authenticates user, generates JWT access and refresh tokens |
| `validate.py` | Activates user account via email token |
| `logout.py` | Clears authentication cookies |
| `change_password.py` | Validates and updates user password |
| `info.py` | Retrieves authenticated user details from JWT |
| `delete.py` / `user_remove.py` | User deletion logic |

**Request domain (`src/app/request/`):**

| Module | Responsibility |
|--------|----------------|
| `create.py` | Validates and stores an HTTP request configuration |
| `update.py` | Updates an existing request configuration |
| `get.py` | Retrieves a single request or all requests for an account |
| `delete.py` | Removes a request configuration |

**Shared validators (`src/app/shared/`):**

| Module | Validates |
|--------|-----------|
| `email.py` | Email format (regex) |
| `password.py` | Password strength (8+ chars, upper, lower, digit, symbol) |
| `method.py` | HTTP method (`GET`, `POST`, `PUT`, `DELETE`) |
| `authentication.py` | JWT token presence and validity |
| `periodicity.py` | Periodicity values (`hourly`, `daily`, `weekly`) |

### Infrastructure Layer (`src/infra/`)

Handles all external concerns: database access, email delivery, configuration, and JWT decoding.

**Database repositories:**

| Module | Entity | Key operations |
|--------|--------|---------------|
| `user/sqlite.py` | `users` | `create_user`, `get_user_by_email`, `get_user_by_uuid`, `update_current_password`, `disable_user_by_uuid` |
| `account/sqlite.py` | `accounts` | `create_account`, `get_active_account_by_uuid`, `update_account_as_removed_by_uuid` |
| `request/sqlite.py` | `requests` | `create_request`, `update_request`, `get_request_by_request_uuid`, `get_all_requests_by_account_uuid`, `delete_request_by_request_uuid` |

**Shared utilities (`src/infra/shared/`):**

| Module | Purpose |
|--------|---------|
| `conf.py` | Loads `conf/dev.json` configuration |
| `authentication.py` | Decodes JWT and extracts `user_uuid` from cookies |
| `body_params.py` | Extracts parameters from JSON request body |
| `form_params.py` | Extracts parameters from HTML form submissions |

**Other infrastructure:**

| Module | Purpose |
|--------|---------|
| `sqlite3.py` | Generic SQLite wrapper (`create_connection`, `execute_query`, `fetch_all`, `fetch_one`) |
| `db/init.py` | Creates all database tables on startup |
| `email/gmail.py` | Sends emails via Gmail SMTP |
| `status.py` | Extracts request metadata (IP, user-agent, method) for health checks |

---

## Data Flows

### User Registration

```
POST /ip/v1/signin
  → routes/ip.py
    → src/app/user/create.py
        → Validate email (EmailValidator)
        → Validate password (PasswordValidator)
        → Generate UUID, account_uuid, hash password & token
        → src/infra/user/sqlite.py — check email not already registered
        → src/infra/user/sqlite.py — INSERT user
        → src/infra/account/sqlite.py — INSERT account
        → src/infra/email/gmail.py — send validation email
  ← 201 Created {user_uuid, email, token}
```

### User Login

```
POST /ip/v1/login
  → routes/ip.py
    → src/app/user/login.py
        → src/infra/user/sqlite.py — get user by email
        → Validate password hash
        → Generate JWT access token (1 hour) + refresh token (15 days)
        → src/infra/email/gmail.py — send login notification email
  ← 200 OK — sets httponly cookies: Access-Token, Refresh-Token
```

### Create HTTP Request Configuration

```
POST /requests/v1/request  (Cookie: Access-Token)
  → routes/requests.py
    → src/app/request/create.py
        → src/infra/shared/authentication.py — decode JWT, extract user_uuid
        → src/infra/request/sqlite.py — get account_uuid from user_uuid
        → Validate periodicity, method, URL, authentication type
        → src/infra/request/sqlite.py — INSERT request
  ← 201 Created {request_uuid}
```

---

## Authentication & Authorization

- Login issues two **JWT tokens** stored as `httponly` cookies:
  - `Access-Token` — expires in **1 hour**
  - `Refresh-Token` — expires in **15 days**
- Protected endpoints decode the `Access-Token` cookie using the `secret_key` from config.
- The `user_uuid` extracted from the token is used to identify the caller and scope data access.
- Invalid or expired tokens raise `AuthenticationValidationError` → HTTP 401.

---

## Key Design Patterns

| Pattern | Where used |
|---------|------------|
| **Repository Pattern** | `src/infra/user/`, `src/infra/account/`, `src/infra/request/` — data access abstracted behind repository classes |
| **Use Case / Service Layer** | `src/app/user/`, `src/app/request/` — each use case is a dedicated class |
| **Validator Objects** | `src/app/shared/` — reusable, single-responsibility validators |
| **Soft Delete** | `accounts.removed` flag set instead of removing rows |
| **UUID-based Identity** | Users, accounts, and requests are identified by UUID in addition to DB `id` |
| **Configuration Externalization** | All runtime config in `conf/dev.json`, loaded via `Config` class |

---

## Key Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| Flask | 3.0.3 | Web framework |
| Flask-CORS | — | Cross-origin request support |
| PyJWT | 2.9.0 | JWT token encoding / decoding |
| SQLite3 | stdlib | Embedded relational database |
| smtplib | stdlib | Gmail SMTP email delivery |
| hashlib | stdlib | SHA256 password and token hashing |
| pytest | — | Unit testing |
| playwright | — | Browser automation / E2E testing |
| pylint | 3.2.6 | Static code analysis |

---

## Configuration

All runtime configuration is stored in `conf/dev.json`:

| Key | Description |
|-----|-------------|
| `host` | Server bind address |
| `port` | Server port |
| `database_name` | Path to the SQLite database file |
| `email` | Gmail sender address |
| `email_password` | Gmail app password |
| `email_enabled` | Feature toggle for email sending |
| `secret_key` | JWT signing secret |

---

## Deployment

The application is containerized with Docker:

- **`Dockerfile`** — builds a Python 3.12 Alpine image, runs pylint checks, exposes the app
- **`docker-compose.yml`** — maps host port `80` to container port `8080`, applies CPU/memory resource limits
