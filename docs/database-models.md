# Database models

Here you will find the database models of the application:
- [users](#users)
- [accounts](#accounts)
- [requests](#requests)
- [tokens](#tokens)
- [password_resets](#password_resets)

## users

| name         | type    | primary key | not null | default | description |
|--------------|---------|-------------|----------|---------|-------------|
| id           | integer | yes         |          |         |             |
| uuid         | text    |             | yes      |         |             |
| account_uuid | text    |             | yes      |         |             |
| name         | text    |             | yes      |         |             |
| email        | text    |             | yes      |         |             |
| password     | text    |             | yes      |         |             |
| token        | text    |             | yes      |         |             |
| enabled      | boolean |             |          | 0       |             |
| role         | text    |             |          | 'admin' |             |
| created_at   | text    |             | yes      |         |             |
| updated_at   | text    |             | yes      |         |             |

## accounts

| name         | type    | primary key | not null | default | description |
|--------------|---------|-------------|----------|---------|-------------|
| id           | integer | yes         |          |         |             |
| account_uuid | text    |             | yes      |         | FK → users.account_uuid |
| plan         | text    |             | yes      |         |             |
| periodicity  | text    |             | yes      |         |             |
| removed      | boolean |             |          | 0       |             |
| created_at   | text    |             | yes      |         |             |
| updated_at   | text    |             | yes      |         |             |
| removed_at   | text    |             | yes      |         |             |

## requests

| name           | type    | primary key | not null | default | description |
|----------------|---------|-------------|----------|---------|-------------|
| id             | integer | yes         |          |         |             |
| account_uuid   | text    |             | yes      |         | FK → accounts.account_uuid |
| request_uuid   | text    |             | yes      |         |             |
| active         | integer |             |          | 0       |             |
| periodicity    | text    |             | yes      |         |             |
| name           | text    |             | yes      |         |             |
| url            | text    |             | yes      |         |             |
| method         | text    |             | yes      |         |             |
| headers        | text    |             |          |         |             |
| user_agent     | text    |             |          |         |             |
| authentication | text    |             | yes      |         |             |
| credentials    | text    |             |          |         |             |
| body           | text    |             |          |         |             |
| tags           | text    |             |          |         |             |
| created_at     | text    |             | yes      |         |             |
| updated_at     | text    |             | yes      |         |             |

## tokens

| name              | type    | primary key | not null | description |
|-------------------|---------|-------------|----------|-------------|
| id                | integer | yes         |          |             |
| user_id           | integer |             | yes      | FK → users.id |
| access_token      | text    |             | yes      |             |
| refresh_token     | text    |             | yes      |             |
| created_at        | text    |             | yes      |             |
| access_expires_at | text    |             | yes      |             |
| refresh_expires_at| text    |             | yes      |             |

## password_resets

| name       | type    | primary key | not null | description |
|------------|---------|-------------|----------|-------------|
| id         | integer | yes         |          |             |
| user_id    | integer |             | yes      | FK → users.id |
| token      | text    |             | yes      |             |
| expires_at | text    |             | yes      |             |

