# Assignment #3

## Goal
The goals of assignment #3 are to incorporate a SQLite database into our backend and
to implement authentication/authorization.

## Dependencies
We need some new dependencies for this work:

- sqlmodel (database ORM built on sqlalchemy and pydantic)
- passlib (password hashing / verification)
- python-jose (JWTs)
- bcrypt (cryptographic backend for passlib)
- cryptography (cryptographic backend for python-jose)
- python-multipart (support for form requests)

If you are using `poetry`, you can add the following lines to your `pyproject.toml` under
`[tool.poetry.dependencies]` and then run `poetry install`.

```
sqlmodel = "0.0.16"
passlib = "1.7.4"
python-jose = "3.3.0"
bcrypt = "4.1.2"
cryptography = "42.0.2"
python-multipart = "0.0.9"
```

If you are using a virtual environment, you can add the following lines to your
`requirements.txt` and then run `python -m pip install -r requirements.txt` from within
your virtual environment.

```
sqlmodel==0.0.16
passlib==1.7.4
python-jose==3.3.0
bcrypt==4.1.2
cryptography==42.0.2
python-multipart==0.0.9
```

## Database
The data in `fake_db.json` has been converted into a sqlite database called `sample.db`.
It is recommended that you download the database and copy it to the location
`backend/pony_express.db`.

The schema for the database is located in `schema.py`. You can either download the schema
and copy it to the location `backend/schema.py` or you can replace appropriate entities in
your codebase with those from `schema.py`.

In your database file `backend/database.py` you need to do the following.

1. Import all of the database schema models

2. Create a database engine using `sqlmodel.create_engine`

3. Define a function for creating the database and tables

4. Define a FastAPI dependency `get_session` that we can use in our routes. In order for
   the autograder to work, this function must be located in `backend/database.py` and must
   be defined as `def get_session():`.

5. Update your database functions to use the database session and the database schema
   models. Each function should take `session: Session` as a parameter.

6. Note that the `id` of each model is an `int` instead of a `str`. Make sure to update
   that in all of your entities and routes.

```python
...

from sqlmodel import Session, SQLModel, create_engine

...

engine = create_engine(
    "sqlite:///backend/pony_express.db",
    echo=True,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
```

In your `backend/main.py` file, you should create a `lifespan` function and include it
when building your FastAPI application. The lifespan is a function that will run when the
application is first initialized. We will use it to create the database and tables.

```python
from contextlib import asynccontextmanager

...

from backend.database import create_db_and_tables

...

@asynccontextmanager
def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

...

app = FastAPI(
    ...
    lifespan=lifespan,
)
```

In each of your routers that uses a database function, you need to add a session
dependency `session: Session = Depends(db.get_session)` as a parameter and pass the
session to the database function.

### Database testing

In order to use an in-memory database for testing, we need to build two fixtures: a
database `session` fixture and a test `client` fixture. We will put these in a
`conftest.py` file at the top level of your test folder, eg, at `tests/conftest.py`. This
will allow us to pass in `session` and/or `client` as a parameter to any test function so
that the tests don't interfere with each other or with the actual database.

```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine

from backend.main import app
from backend import database as db


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session):
    def _get_session_override():
        return session

    app.dependency_overrides[db.get_session] = _get_session_override

    yield TestClient(app)

    app.dependency_overrides.clear()
```

## Existing Routes

With the database implementation, there are new _response_ formats for chats, messages and
users.

The new user format has `id` as an integer and has two new fields `username` and `email`,
eg,
```json
{
  "id": 1,
  "username": "juniper",
  "email": "juniper@cool.email",
  "created_at": "2023-10-31T18:33:09"
}
```

The new chat format has `id` as an integer, replaces the `owner_id` key with `owner`, and
no longer has `user_ids`, eg,
```json
{
  "id": 1,
  "name": "chat name",
  "owner": {
    "id": 1,
    "username": "juniper",
    "email": "juniper@cool.email",
    "created_at": "2023-10-31T18:33:09"
  }
  "created_at": "2023-11-22T10:41:23"
}
```

The new message format has `id` as an integer, has a new key `chat_id` as an integer, and
replaces the `user_id` key with `user`, eg,
```json
{
  "id": 1,
  "text": "message text",
  "chat_id": 1,
  "user": {
    "id": 1,
    "username": "juniper",
    "email": "juniper@cool.email",
    "created_at": "2023-10-31T18:33:09"
  },
  "created_at": "2024-01-05T14:13:12"
}
```

### Users

- The `POST /users` route should be deleted. This will be replaced by the
`POST /auth/registration` route below.

- The `GET /users` route should be updated so that the response matches the new user
  format, eg,
  ```json
  {
    "meta": {
      "count": 1
    }
    "users": [
      {
        "id": 1,
        "username": "juniper",
        "email": "juniper@cool.email",
        "created_at": "2023-10-31T18:33:09"
      }
    ]
  }
  ```

- The `GET /users/{user_id}` route should be updated so that the response matches the new
  user format, eg,
  ```json
  {
    "user": {
      "id": 1,
      "username": "juniper",
      "email": "juniper@cool.email",
      "created_at": "2023-10-31T18:33:09"
    }
  }
  ```

- The `GET /users/{user_id}/chats` route should be updated so that the response matches the
  new chat format, eg,
  ```json
  {
    "meta": {
      "count": 1
    },
    "chats": [
      {
        "id": 1,
        "name": "chat name",
        "owner": {
          "id": 1,
          "username": "juniper",
          "email": "juniper@cool.email",
          "created_at": "2023-10-31T18:33:09"
        }
        "created_at": "2023-11-22T10:41:23"
      }
    ]
  }
  ```

### Chats

- The `GET /chats` route should be updated so that the response matches the new chat format,
  eg,
  ```json
  {
    "meta": {
      "count": 1
    },
    "chats": [
      {
        "id": 1,
        "name": "chat name",
        "owner": {
          "id": 1,
          "username": "juniper",
          "email": "juniper@cool.email",
          "created_at": "2023-10-31T18:33:09"
        }
        "created_at": "2023-11-22T10:41:23"
      }
    ]
  }
  ```

- The `GET /chats/{chat_id}` will be enhanced with new functionality, see below.

- The `PUT /chats/{chat_id}` route should be updated so that the response matches the new
  chat format, eg,
  ```json
  {
    "chat": {
      "id": 1,
      "name": "chat name",
      "owner": {
        "id": 1,
        "username": "juniper",
        "email": "juniper@cool.email",
        "created_at": "2023-10-31T18:33:09"
      }
      "created_at": "2023-11-22T10:41:23"
    },
  }
  ```

- The `GET /chats/{chat_id}/messages` route should be updated so that the response matches
  the new message format, eg,
  ```json
  {
    "meta": {
      "count": 1
    },
    "messages: [
      {
        "id": 1,
        "text": "message text",
        "chat_id": {chat_id},
        "user": {
          "id": 1,
          "username": "juniper",
          "email": "juniper@cool.email",
          "created_at": "2023-10-31T18:33:09"
        },
        "created_at": "2024-01-05T14:13:12"
      }
    ]
  }
  ```

- The `GET /chats/{chat_id}/users` route should be updated so that the response matches
  the new user format, eg,
  ```json
  {
    "meta": {
      "count": 1
    }
    "users": [
      {
        "id": 1,
        "username": "juniper",
        "email": "juniper@cool.email",
        "created_at": "2023-10-31T18:33:09"
      }
    ]
  }
  ```

## Authentication

I recommend putting the authentication logic and router into `backend/auth.py`. You are
free to define helper methods as needed. It should include the following.

1. Define a password context (`CryptContext` from `passlib.context`) which will be used to
   hash passwords and verify passwords against hashed passwords.
   ```python
   pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
   ```

2. Create a JWT signing key that is **NOT** stored in your codebase. You can use `openssl`
   to generate a random signing key. For example, in a linux or mac os terminal, you can
   run `openssl rand -hex 32` and then store in the environment using
   `export JWT_KEY = {generated_key}`. Define a variable in `backend/auth.py` that stores
   this value.
   ```python
   jwt_key = os.environ.get("JWT_KEY")
   ```

3. Define a FastAPI dependency called `oauth2_scheme` using `OAuth2PasswordBearer` from
   `fastapi.security` as follows:
   ```python
   oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
   ```

4. Define an `auth_router` with `"/auth"` as prefix and `"Authentication"` as tag. Make
   sure to include the `auth_router` in the main application.

5. `POST /auth/registration` is to register a new user. The request body is of the form
   ```json
   {
     "username": "new_username",
     "email": "new_user_email@example.com",
     "password": "new_user_password",
   }
   ```
   If the `username` and `email` fields do not match any existing users (the database
   schema has uniqueness constraints on these fields), a new user is added to the database
   with the appropriate `hashed_password`, and the response has HTTP status code 201 and
   adheres to the following format:
   ```json
   {
     "user": {
       "id": 1,
       "username": "new_username",
       "email": "new_user_email@example.com",
       "created_at": "2024-01-20T15:17:19.382"
     }
   }
   ```
   If the field `username` or `email` has a value that matches an existing user, the
   response has HTTP status code 422 and the response adheres to the format:
   ```json
   {
     "detail": {
       "type": "duplicate_value",
       "entity_name": "User",
       "entity_field": "{field}",
       "entity_value": "{value}"
     }
   }
   ```

6. `POST /auth/token` retrieves a JWT token for a user. The request body has content type
   `x-www-form-urlencoded` with the fields `username` and `password`. You should use the
   class `OAuth2PasswordRequestForm` from `fastapi.security` as the body parameter, eg,
   `form: OAuth2PasswordRequestForm = Depends()`.
   If a user with the corresponding `username` exists and the `password` is verified
   against the user's `hashed_password`, an `access_token` JWT is generated for the user,
   and the response has HTTP status code 200 and adheres to the following format:
   ```json
   {
     "access_token": "{access_token}",
     "token_type": "Bearer",
     "expires_in": 3600
   }
   ```
   The JSON Web Token should be encoded using the `"HS256"` algorithm and the key you
   generated above. The payload should have two keys: the `sub` key (subject) has a value
   that is the user's `id` as a _string_; the `exp` key (expiration) has a value that is
   equal to 3600 plus the current timestamp as an _integer_. In other words, the payload
   adheres to the following format:
   ```json
   {
     "sub": "{user_id}",
     "exp": {expiration_timestamp}
   }
   ```
   If there is no user with the given `username` OR if the `password` is not verified with
   the user's `hashed_password`, the response has HTTP status code 401 and adheres to the
   following format:
   ```json
   {
     "detail": {
       "error": "invalid_client",
       "error_description": "invalid username or password"
     }
   }
   ```

7. Define a FastAPI dependency called `get_current_user` in `auth.py` as
   follows:
   ```python
   def get_current_user(
       session: Session = Depends(db.get_session),
       token: str = Depends(oauth2_scheme),
   ) -> UserInDB:
       # insert code to decode the token and return the corresponding user
   ```
   This dependency should be defined such that any route depending on it has the following
   behavior:

    - If the token is expired, the response has HTTP status code 401 and the adheres to
      the format
      ```json
      {
        "detail": {
          "error": "invalid_client",
          "error_description": "expired access token"
        }
      }
      ```

    - If the token is invalid, the response has HTTP status code 401 and the adheres to
      the format
      ```json
      {
        "detail": {
          "error": "invalid_client",
          "error_description": "invalid access token"
        }
      }
      ```
   Any route that requires a bearer token should have `get_current_user` as a dependency.
   This is accomplished by including the following parameter in the function signature.
   ```python
   user: UserInDB = Depends(get_current_user)
   ```

## New Routes

1. `GET /users/me` returns the current user. It requires a valid bearer token. If the
   token is valid, the response has HTTP status code 200 and the response adheres to the
   format:
   ```json
   {
     "user": {
       "id": 1,
       "username": "juniper",
       "email": "juniper@cool.email",
       "created_at": "2023-10-31T18:33:09"
     }
   }
   ```

2. `PUT /users/me` can be used to update the username or email of the current user. It
   requires a valid bearer token. The request body has two **optional** fields `username`
   and `email`, ie, it is of the form
   ```json
   {
     "username": "new_username",
     "email": "new_email@example.com"
   }
   ```
   If the token is valid, the fields provided are updated on the current user, the
   response has HTTP status code 200, and the response adheres to the format:
   ```json
   {
     "user": {
       "id": 1,
       "username": "new_username",
       "email": "new_email@example.com",
       "created_at": "2023-10-31T18:33:09"
     }
   }
   ```

3. `POST /chats/{chat_id}/messages` creates a new message in the chat, authored by the
   current user. It requires a valid bearer token. The request body adheres to the format:
   ```json
   {
     "text": "new message text"
   }
   ```
   If the token is valid and a chat with the given `id` exists, a new message is added to
   the database with `chat_id` matching the chat and `user_id` matching the current user.
   The response has HTTP status code 201 and adheres to the format:
   ```json
   {
     "message: {
       "id": 1,
       "text": "new message text",
       "chat_id": {chat_id},
       "user": {
         "id": 1,
         "username": "juniper",
         "email": "juniper@cool.email",
         "created_at": "2023-10-31T18:33:09"
       },
       "created_at": "2024-01-05T14:13:12"
     }
   }
   ```
   If there is no chat with the given `chat_id`, then the response has HTTP status code
   404 and adheres to the format:
   ```json
   {
     "detail": {
       "type": "entity_not_found",
       "entity_name": "Chat",
       "entity_id": {chat_id}
     }
   }
   ```

## Updated Route

The `GET /chats/{chat_id}` will be updated to be more flexible. Firstly, we will define
the metadata for a chat to be of the form
```json
{
  "message_count": 50,
  "user_count": 3
}
```
where `message_count` is the number of messages in the chat and `user_count` is the number
of users in the chat.

Secondly, we will define a chat response to have four keys: the `meta` key will have the
chat metadata defined above; the `chat` key will have the new chat response format defined
above; the `users` key is optional, but if included will have the list of users in the new
user response format; and the `messages` key is optional, but if included will have the
list of messages in the new message response format.

A full response adheres to the format
```json
{
  "meta": {
    "message_count": 1,
    "user_count": 1
  }
  "chat": {
    "id": 1,
    "name": "chat name",
    "owner": {
      "id": 1,
      "username": "juniper",
      "email": "juniper@cool.email",
      "created_at": "2023-10-31T18:33:09"
    }
    "created_at": "2023-11-22T10:41:23"
  },
  "messages": [
    {
      "id": 1,
      "text": "new message text",
      "chat_id": {chat_id},
      "user": {
        "id": 1,
        "username": "juniper",
        "email": "juniper@cool.email",
        "created_at": "2023-10-31T18:33:09"
      },
      "created_at": "2024-01-05T14:13:12"
    }
  ],
  "users": [
    {
      "id": 1,
      "username": "new_username",
      "email": "new_email@example.com",
      "created_at": "2023-10-31T18:33:09"
    }
  ]
}
```

We will have a query parameter `include` that is a list of keys to include in the
response. The valid entries to the `include` list are `"messages"` and `"users"`. The
shape of the response will depend on the value of the `include` query parameter.

- Without the query parameter, `GET /chats/{chat_id}` will have a response with the keys
  `meta` and `chat`.

- With `include=messages` as the query parameter,
  `GET /chats/{chat_id}?include=messages` will have a response with the keys `meta`,
  `chat`, and `messages`.

- With the `include=users` as the query parameter,
  `GET /chats/{chat_id}?include=users` will have a response with the keys `meta`, `chat`,
  and `users`.

- With both `include=messages&include=users` as the query parameter,
  `GET /chats/{chat_id}?include=messages&include=users` will have a response with the
  keys `meta`, `chat`, `messages`, and `users`.

If a chat with the given `chat_id` exists, the response has HTTP status code 200 and the
response format follows that indicated above. If there is no chat with the given
`chat_id`, then the response has HTTP status code 404 with the same `entity_not_found`
data as before.

