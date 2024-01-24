# assignment #1

Goal: Create an API for a chat application with title "Pony Express" with a
subset of the eventual functionality.

## File structure
When you submit via gradescope, the script will assume your local app is located
at `backend.main:app`. In order to accomplish this, you should have a top-level
folder called `backend`. This folder must contain at least two files:

- `__init__.py`: an empty file that signifies that `backend` is a python module
- `main.py`: a file that contains a variable `app` which is an instance object of
  the `FastAPI` class.

To ensure that your app runs properly, you should be able to run your local
server using the command `uvicorn backend.main:app`.

## Data
A file `fake_db.json` has been provided with some chat and user data to develop
against. This exact same dataset will be used to test your application when you
submit to gradescope. You may add, modify, or remove content from your copy of
the test data, but make sure you do not change the fundamental structure of the
test data. Any modifications you make to your copy of the test data will not be
used when tested in gradescope. It is assumed that the file is located at 
`backend/fake_db.json`.

## Dependencies
When you submit via gradescope, your server will be run in a virtual environment
with the following dependencies.

- `fastapi` version `0.108.0`
- `uvicorn` version `0.25.0`
- `pytest` version `7.4.0`
- `httpx` version `0.26.0`

It is a good idea to develop against the same dependencies and versions. 

If you are using `poetry`, your `pyproject.toml` file should have the following
section:
```toml
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "0.108.0"
uvicorn = "0.25.0"
pytest = "7.4.0"
httpx = "0.26.0"
```
You can run `poetry install` to install the proper versions of the
dependencies.

If you are using a virtual environment, your `requirements.txt` file should be
```
fastapi==0.108.0
uvicorn==0.25.0
pytest==7.4.0
httpx==0.26.0
```
From within your virtual environment, you can run 
`python -m pip install -r requirements.txt`
to install the proper versions of the dependencies.

## Tests
Your code should be well-tested.

- each route should have at least one test
- if the specification for the route includes handling unknown or duplicate
  ids, you should have a test around that response.
- it can be helpful to also write unit tests for the inner workings of your
  application; for example, you may want tests around database or other
  utility functions that you write.

The tests should live under a directory `tests` at the same level as the `backend`
directory.
    
## Specification

The API should have a description should have two sections ("tags") -- "Chats"
and "Users". Under each tag, there will be a collection of routes. Each route
should have a description and should behave as specified below.

### User specification

Under the tag "Users", there are 3 routes. For the routes that return a user or
a collection of users, each user will have 2 fields.  

- `id`: the id of the user (string)
- `created_at`: the datetime the user was created in ISO format
  (string of the form `yyyy-mm-ddThh:mm:ss`)

1. `GET /users` returns a list of users sorted by `id` alongside some metadata.
    The metadata has the count of users (integer). The response has HTTP status
    code 200 and adheres to the following format: 
    ```json
    {
        "meta": {
            "count": 1
        },
        "users": [
            {
                "id": "user1",
                "created_at": "2024-01-16T09:15:10"
            }
        ]
    }
    ```

2. `POST /users` creates a new user. The body of the request adheres to the format:
    ```json
    {
        "id": "new_user_id"
    }
    ```
    If the `id` provided does not match an existing user, a new user is added to
    the database with the provided id and `created_at` the current datetime, and
    the response has status code 200 and adheres to the format: 
    ```json
    {
        "user": {
            "id": "new_user_id",
            "created_at": "2024-01-16T09:15:10"
        }
    }
    ```
    If the `id` provided matches an existing user, the response has the HTTP
    status code `422` and the response adheres to the format:
    ```json
    {
        "detail": {
            "type": "duplicate_entity",
            "entity_name": "User",
            "entity_id": "new_user_id"
        }
    }
    ```
    
3. `GET /users/{user_id}` returns a user for a given `id`. If a user with the
    `id` exists, the response has status code 200 and adheres to the format:
    ```json
    {
        "user": {
            "id": "user1",
            "created_at": "2024-01-16T09:15:10"
        }
    }
    ```
    If the `id` provided does not correspond to an existing user, the response
    has the HTTP status code `404` and the response adheres to the format:
    ```json
    {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "User",
            "entity_id": "user1"
        }
    }
    ```

4. `GET /users/{user_id}/chats` returns a list of chats for a given user `id`
    alongside some metadata. The list of chats consists of only those chats
    where the given user is a participating user and is sorted by `name`. The
    metadata contains the count of chats (integer). If a user with the `id`
    exists, the response has status code 200 and adheres to the format:
    ```json
    {
        "meta": {
            "count": 1
        },
        "chats": [
            {
                "id": "abc123xyz",
                "name": "chat name",
                "user_ids": [
                    "user1",
                    "user2",
                    "user3",
                ],
                "owner_id": "user2",
                "created_at": "2024-01-16T09:15:10"
            }
        ]
    }
    ```
    If the `id` provided does not correspond to an existing user, the response
    has the HTTP status code `404` and the response adheres to the format:
    ```json
    {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "User",
            "entity_id": "user1"
        }
    }
    ```



### Chat specification

Under the tag "Chats", there are 6 routes. For the routes that return a chat or
a collection of chats, each chat will have 5 fields.

- `id`: the id of the chat (string)
- `name`: the name of the chat (string)
- `user_ids`: the ids of the users in the chat (list of strings)
- `owner_id`: the id of the user that owns the chat (string)
- `created_at`: the datetime the chat was created in ISO format 
  (string of the form `yyyy-mm-ddThh:mm:ss`)
    
1. `GET /chats` returns a list of chats sorted by `name` alongside some
    metadata. The metadata has the count of chats (integer). The response has
    the HTTP status code 200 and adheres to the following format: 
    ```json
    {
        "meta": {
            "count": 1
        },
        "chats": [
            {
                "id": "abc123xyz",
                "name": "chat name",
                "user_ids": [
                    "user1",
                    "user2",
                    "user3",
                ],
                "owner_id": "user2",
                "created_at": "2024-01-16T09:15:10"
            }
        ]
    }
    ```

2. `GET /chats/{chat_id}` returns a chat for a given `id`. If a chat with the
    `id` exists, the response has HTTP status code 200 and adheres to the format:
    ```json
    {
        "chat": {
            "id": "abc123xyz",
            "name": "chat name",
            "user_ids": [
                "user1",
                "user2",
                "user3",
            ],
            "owner_id": "user2",
            "created_at": "2024-01-16T09:15:10"
        }
    }
    ```
    If the `id` provided does not correspond to an existing chat, the response
    has the HTTP status code `404` and the response adheres to the format:
    ```json
    {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": "abc123xyz"
        }
    }
    ```

3. `PUT /chats/{chat_id}` updates a chat for a given `id`. The body for the
    request adheres to the format: 
    ```json
    {
        "name": "updated chat name"
    }
    ```
    If a chat with the `id` exists, the chat name is updated in the database,
    and the response has the HTTP status code 200 and adheres to the format:
    ```json
    {
        "chat": {
            "id": "abc123xyz",
            "name": "updated chat name",
            "user_ids": [
                "user1",
                "user2",
                "user3",
            ],
            "owner_id": "user2",
            "created_at": "2024-01-16T09:15:10"
        }
    }
    ```
    If the `id` provided does not correspond to an existing chat, the response
    has the HTTP status code `404` and the response adheres to the format:
    ```json
    {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": "abc123xyz"
        }
    }
    ```

4. `DELETE /chats/{chat_id}` deletes a chat for a given `id`.  If a chat with
    the `id` exists, the chat is removed from the database, and the response has
    the HTTP status code of 204 and has no content. If the `id` provided does not
    correspond to an existing chat, the response has the HTTP status code `404`
    and the response adheres to the format:
    ```json
    {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": "abc123xyz"
        }
    }
    ```

6. `GET /chats/{chat_id}/messages` returns a list of messages for a given chat
    `id` alongside some metadata. The metadata contains the count of messages
    (integer) and the list of messages is sorted by its `created_at` datetime.
    If a chat with the `id` exists, the response has the HTTP status code 200
    and adheres to the format:
    ```json
    {
        "meta": {
            "count": 1,
        },
        "messages": [
            {
                "id": "def456uvw",
                "user_id": "user1",
                "text": "the text of the message",
                "created_at": "2024-01-16T09:15:10"
            }
        ]
    }
    ```
    If the `id` provided does not correspond to an existing chat, the response
    has the HTTP status code `404` and the response adheres to the format:
    ```json
    {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": "abc123xyz"
        }
    }
    ```

7.  `GET /chats/{chat_id}/users` returns a list of users for a given chat `id`
    alongside some metadata. The list of users consists of only those users
    participating in the corresponding chat, sorted by `id`. The metadata
    contains the count of users (integer). If a chat with the `id` exists, the
    response has the HTTP status code 200 and adheres to the format:
    ```json
    {
        "meta": {
            "count": 1,
        },
        "users": [
            {
                "id": "user1",
                "created_at": "2024-01-16T09:15:10"
            }
        ]
    }
    ```
    If the `id` provided does not correspond to an existing chat, the response
    has the HTTP status code `404` and the response adheres to the format:
    ```json
    {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": "abc123xyz"
        }
    }
    ```
