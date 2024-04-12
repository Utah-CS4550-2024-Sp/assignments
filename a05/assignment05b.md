# Assignment #5b

The goal of assignment #5b is to add features to both the backend and frontend that
support managing chats.

## Backend

We will use the terminology that a user is a `member` of a chat if there is a row in the
`user_chat_links` table that connects the user to the chat.

1. Add an API endpoint `POST /chats` to create a new chat. The request body will have the
   following format.
    ```json
    {
      "name": "new_chat_name"
    }
    ```
   This endpoint requires an access token. If the token is valid, a new chat is created
   with the current user as owner and the current user is added as a member of the chat.
   The successful response has HTTP status code 201 and the response body adheres to the
   following format.
    ```json
    {
      "chat": {
        "id": 1,
        "name": "new_chat_name",
        "owner": {
          "id": 1,
          "username": "juniper",
          "email": "juniper@email.com",
          "created_at": "2024-01-05T09:10:11.123",
        },
        "created_at": "2024-04-07T12:13:14.156"
      }
    }
    ```
   If the token is not provided or is invalid, the response has HTTP status code 401 and
   the body adheres to the following format.
    ```json
    {
      "detail": {
        "error": "invalid_client",
        "error_description": "invalid access token"
      }
    }
    ```

2. Modify the API endpoint `PUT /chats/{chat_id}` so that an access token is required. In
   addition, enforce that the current user is the owner of the chat. Recall that the
   request body adheres to the format
    ```json
    {
      "name": "updated_chat_name"
    }
    ```
   If the token is valid and the current user is the owner of the chat, the chat name is
   updated and the successful response has status code 200 and body of the following
   format.
    ```json
    {
      "chat": {
        "id": 1,
        "name": "updated_chat_name",
        "owner": {
          "id": 1,
          "username": "juniper",
          "email": "juniper@email.com",
          "created_at": "2024-01-05T09:10:11.123",
        },
        "created_at": "2024-04-07T12:13:14.156"
      }
    }
    ```
   If the access token is valid, but the current user is **not** the owner of the chat,
   the response has HTTP status code 403 and the body has the following format.
    ```json
    {
      "detail": {
        "error": "no_permission",
        "error_description": "requires permission to edit chat"
      }
    }
    ```
   If the chat does not exist, the response has HTTP status code 404 and the body adheres
   to the `"entity_not_found"` format defined previously.

   If the access token is invalid, the response has HTTP status code
   401 and the body adheres to the following format.
    ```json
    {
      "detail": {
        "error": "invalid_client",
        "error_description": "invalid access token"
      }
    }
    ```

3. Add an API endpoint `PUT /chats/{chat_id}/users/{user_id}` to add a user as a member of
   a chat. This endpoint requires an access token and enforces that the current user is
   the owner of the specified chat. There is no body associated with the request. For a
   request to be successful, the access token must be valid, the chat with `chat_id` must
   exist, the current user must be the owner of the chat, and the user with `user_id` must
   exist. A successful request will add a row to the `user_chat_links` table with the
   given `user_id` and `chat_id` if such a row does not already exist. The response will
   have HTTP status code 201 and the response body will return all users that are members
   of the chat, adhering to the following format.
    ```json
    {
      "meta": {
        "count": 1
      },
      "users": [
        {
          "id": 1,
          "username": "juniper",
          "email": "juniper@email.com",
          "created_at": "2024-01-05T09:10:11.123"
        }
      ]
    }
    ```
   If the access token is valid, but the current user is **not** the owner of the chat,
   the response has HTTP status code 403 and the body has the following format.
    ```json
    {
      "detail": {
        "error": "no_permission",
        "error_description": "requires permission to edit chat members"
      }
    }
    ```
   If the chat or user does not exist, the response has HTTP status code 404 and the body
   adheres to the `"entity_not_found"` format defined previously.

   If the access token is invalid, the response has HTTP status code 401
   and the body adheres to the following format.
    ```json
    {
      "detail": {
        "error": "invalid_client",
        "error_description": "invalid access token"
      }
    }
    ```

4. Add an API endpoint `DELETE /chats/{chat_id}/users/{user_id}` to remove a user from a
   chat. This endpoint requires an access token and enforces that the current user is
   the owner of the specified chat. There is no body associated with the request. For a
   request to be successful, the access token must be valid, the chat with `chat_id` must
   exist, the current user must be the owner of the chat, the user with `user_id` must
   exist, and the user being removed must not be the owner of the chat. A successful
   request will remove a row to the `user_chat_links` table with the given `user_id` and
   `chat_id` if such a row exists. The response will have HTTP status code 200 and the
   response body will return all users that are still members of the chat, adhering to the
   following format.
    ```json
    {
      "users": [
        {
          "id": 1,
          "username": "juniper",
          "email": "juniper@email.com",
          "created_at": "2024-01-05T09:10:11.123"
        }
      ]
    }
    ```
   If the access token is valid, but the current user is **not** the owner of the chat,
   the response has HTTP status code 403 and the body has the following format.
    ```json
    {
      "detail": {
        "error": "no_permission",
        "error_description": "requires permission to edit chat members"
      }
    }
    ```
   If the access token is valid and the current user is the owner of the chat, but the
   `user_id` corresponds to the owner of the chat, the response has HTTP status code 422
   and the body has the following format.
    ```json
    {
      "detail": {
        "error": "invalid_state",
        "error_description": "owner of a chat cannot be removed"
      }
    }
    ```
   If the chat or user does not exist, the response has HTTP status code 404 and the body
   adheres to the `"entity_not_found"` format defined previously.

   If the access token is invalid, the response has HTTP status code 401
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

### Chat details link

Above the messages at the `/chats/:chatId` route, include a link with the text `settings`,
the text `details`, or a settings icon. The link should navigates the user to the
`/chats/:chatId/details` route.

### Chat details page

Add a frontend route `/chats/:chatId/details` and a component that shows the details for a
given chat.

It will include a form with an input field for the chat name and a button to update the
chat name. The input field should be disabled and the button should be disabled or hidden
unless the current user is the owner of the chat. Submitting the form should update the
chat name in the database and update the name in the list of chats.

It will also include the list of members. Mark the user that is the owner of the chat.
Next to each user (except the chat owner), include a button to remove the user from the
chat. If the button is clicked, it should remove the user from the chat and update the
list of users. This button should be disabled or hidden unless the current user is the
owner of the chat.

Below the list of members, include a form to add a user to the chat. It should include a
`<select>` dropdown that has the list of users **not** in the chat and a button to add the
user. When the form is submitted, the selected user should be added in the database and
the list of users should be updated in the frontend. This form should not be visible
unless the current user is the owner of the chat.

```
----------------------------------------------
| chat name                                  |
| -----------------------------   ---------- |
| | nostromo                  |   | update | |
| -----------------------------   ---------- |
----------------------------------------------

----------------------------------------------
| users                                      |
|                                 ---------- |
|   bishop                        | remove | |
|                                 ---------- |
|                                            |
|                                 ---------- |
|   burke                         | remove | |
|                                 ---------- |
|                                            |
|                                  --------- |
|   ripley                         | owner | |
|                                  --------- |
|                                            |
|   -----------------                ------- |
|   | select a user |                | add | |
|   -----------------                ------- |
----------------------------------------------
```

### New chat button

At the bottom of the chat list, include a link to create a new chat. It should navigate
the user to the route `/chats/new` page.

### New chat page

Add a frontend route `/chats/new` and a component to create a new chat. It should include
a form with an input field for the chat name and a button to create a new chat.

```
-------------------------------------
| chat name                         |
| --------------------------------- |
| |                               | |
| --------------------------------- |
| ----------                        |
| | create |                        |
| ----------                        |
-------------------------------------
```

Upon submitting the form,

- it should update the list of chats on the left to include the new chat.

- it should navigate the user to `/chats/:chatId/details` so that the user can add
  members.

