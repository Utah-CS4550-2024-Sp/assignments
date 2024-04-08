# Assignment #5c

The goal of assignment #5c is to add features to both the backend and frontend that
support managing chat messages.

## Backend

We will use the terminology that a user is a `member` of a chat if there is a row in the
`user_chat_links` table that connects the user to the chat.

1. Add an API endpoint `PUT /chats/{chat_id}/messages/{message_id}` to edit a message. The
   request body will have the following format.
    ```json
    {
      "text": "new_message_text"
    }
    ```
   This endpoint requires an access token and enforces that the current user is the user
   that created the message. For a response to be successful, the access token must be
   valid, the chat with `chat_id` must exist, the message with `message_id` must exist,
   and the current user must be the message user. A successful request will update the
   message in the database and return it. The response will have an HTTP status code of
   200, and will have a body that adheres to the following format.
    ```json
    {
      "message": {
        "id": 1,
        "text": "new_message_text",
        "chat_id": 1,
        "user": {
          "id": 1,
          "username": "juniper",
          "email": "juniper@email.com",
          "created_at": "2024-01-05T09:10:11.123",
        },
        "created_at": "2024-04-07T12:13:14.156"
      }
    }
    ```
   If the access token is valid, but the current user is **not** the user of the message,
   the response has HTTP status code 403 and the body has the following format.
    ```json
    {
      "detail": {
        "error": "no_permission",
        "error_description": "requires permission to edit message"
      }
    }
    ```
   If the chat or message does not exist, the response has HTTP status code 404 and the body
   adheres to the `"entity_not_found"` format defined previously.

   If the access token is not provided or invalid, the response has HTTP status code 401
   and the body adheres to the following format.
    ```json
    {
      "detail": {
        "error": "invalid_client",
        "error_description": "invalid access token"
      }
    }
    ```

2. Add an API endpoint `DELETE /chats/{chat_id}/messages/{message_id}` to edit a message.
   The request will have no body. This endpoint requires an access token and enforces that
   the current user is the user that created the message. For a response to be successful,
   the access token must be valid, the chat with `chat_id` must exist, the message with
   `message_id` must exist, and the current user must be the message user. A successful
   request will remove the message from the database. The response will have an HTTP
   status code of 204 with no response body.

   If the access token is valid, but the current user is **not** the user of the message,
   the response has HTTP status code 403 and the body has the following format.
    ```json
    {
      "detail": {
        "error": "no_permission",
        "error_description": "requires permission to delete message"
      }
    }
    ```
   If the chat or message does not exist, the response has HTTP status code 404 and the body
   adheres to the `"entity_not_found"` format defined previously.

   If the access token is not provided or invalid, the response has HTTP status code 401
   and the body adheres to the following format.
    ```json
    {
      "detail": {
        "error": "invalid_client",
        "error_description": "invalid access token"
      }
    }
    ```

3. Enforce permissions on `GET /chats` so that only the chats that a user is a member of
   are visible. The route now requires an access token. If the access token is valid, the
   response is unchanged except that it **ONLY** includes the chats that the current user
   is a member of.

   If the access token is not provided or invalid, the response has HTTP status code 401
   and the body adheres to the following format.
    ```json
    {
      "detail": {
        "error": "invalid_client",
        "error_description": "invalid access token"
      }
    }
    ```

4. Enforce permissions on the following three routes so that chat data can only be
   accessed if the current user is a member of the chat.

   - `GET /chats/{chat_id}`

   - `GET /chats/{chat_id}/messages`

   - `GET /chats/{chat_id}/users`

   - `POST /chats/{chat_id}/messages`

   In other words, these routes now require an access token. If the access token is valid
   and the current user is a member of the chat, then the behavior and response will be
   unchanged from previous specifications.

   If the access token is valid, but the current user is **not** a member of the chat, the
   response has HTTP status code 403 and the body has the following format.
    ```json
    {
      "detail": {
        "error": "no_permission",
        "error_description": "requires permission to view chat"
      }
    }
    ```

   If the access token is not provided or invalid, the response has HTTP status code 401
   and the body adheres to the following format.
    ```json
    {
      "detail": {
        "error": "invalid_client",
        "error_description": "invalid access token"
      }
    }
    ```

## Frontend

The backend permissions will make it so the frontend only shows the chats for which the
current user is a member.

### Message modification

For each message in a chat, if the message user is the same as the current user, there
should be two buttons: an edit button and a delete button. The buttons could have text or
could have icons.

```
--------------------------------------------------------------------------
| juniper                      Thu 29 Feb, 2024 - 3:42pm | edit | delete |
|                                                        ----------------|
|   this is a cool message.                                              |
--------------------------------------------------------------------------
```

#### Editing messages

The edit button should allow the user to edit the message. To edit the message will
require a form that has an input text field, a save button, and a cancel button. The input
text field should load with the original message text and should be editable. The save
button should submit the form, which will update the message in the database and in the
frontend. The cancel button should not make any updates to the database or the frontend
and should return the user to the standard view of the messages.

Here are a couple of options of how to render the edit form. You may choose one of these
or you may choose something else that fits the aesthetic of your page.

1. The edit button replaces the message text with the form.

```
--------------------------------------------------------------------------
| juniper                      Thu 29 Feb, 2024 - 3:42pm                 |
|   ---------------------------------------------------- ----------------|
|   | this is a cool message that i edited.            | | save | cancel |
--------------------------------------------------------------------------
```

2. The edit button opens a dialog modal on the screen that has the form.

```
-------------------------------------------------
|   text                                        |
|   -----------------------------------------   |
|   | this is a cool message that i edited. |   |
|   -----------------------------------------   |
|                                               |
|   --------  ----------                        |
|   | save |  | cancel |                        |
|   --------  ----------                        |
-------------------------------------------------
```

#### Deleting messages

The delete button should allow the user to delete the message. When clicked, it should
remove the message from the database and from the frontend.

