# Database models

Here you will find the database models of the application:
- [users](#users)
- [accounts](#accounts)
- [requests](#requests)

## users

id, integer and primary key
uuid, text
account_uuid, text
name, text
email, text
password, text
token, text
enabled, boolead
role, text
created_at, text
updated_at, text

## accounts

| name         | type    | primary key | description |
|--------------|---------|-------------|-------------|
| id           | integer | yes         |  |
| account_uuid | text    |             |  |
| plan         | text    |             |  |
| periodicity  | text    |             |  |
| removed      | boolean |             |  |
| created_at   | text    |             |  |
| updated_at   | text    |             |  |
| removed_at   | text    |             |  |

## requests

id, integer and primery key
account_uuid, text
request_uuid, text
active, integer
periodicity, text
name, text
url, text
method, text
headers, text
user_agent, text
authentication, text
credentials, text
body, text
tags, text
created_at, text
updated_at, text

