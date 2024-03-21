# Assignment #4

## Goal
The goals of assignment #4 are to style the frontend using tailwindcss, add frontend
functionality for authentication, and add frontend functionality for adding messages to
chats.

## Dependencies
We need some new dependencies for this work:

- tailwindcss (utility-first CSS framework)
- postcss (CSS tranforming tool - used by tailwindcss)
- autoprefixer (postcss plugin to add vendor prefixes - used by tailwindcss)

Add these as development dependencies using the following command.
**Ensure you are in the frontend folder!!**

```bash
npm install -D tailwindcss postcss autoprefixer
```

## Styling

We will be following the instructions at
[Install Tailwind CSS with Vite](https://tailwindcss.com/docs/guides/vite).

Initialize tailwind with the following command.
```bash
npx tailwindcss init -p
```

Open up `tailwind.config.js` and modify the value of the `content` key to be
```javascript
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ]
```

Open up `src/index.css` and add three lines to the top:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Now you are ready to use tailwind classes in your application. Take a look at the buddy
system project for some styling ideas and patterns.

**Note**: You must use tailwind to style at least three of your pages: the login page, the
registration page, and the profile page. Styling the rest of the application can either be
done use tailwind or your original CSS. If you style everything with tailwind, it's a good
idea to delete the rest of the styling in `src/index.css`, to stop importing all of
your CSS files except for `src/index.css`, and then to start building up from scratch. If
you are going to keep some CSS around, you still might consider deleting all of the
original CSS in `src/index.css` and applying tailwind classes to some of your high level
components and the `root div` in `index.html`.

## Authentication

1. Build an `AuthContext` and `AuthProvider` as we did in class that provides access to
    - `token` (String - the access token)
    - `isLoggedIn` (Boolean - whether an access token exists)
    - `login` (Function - takes the response body from `/auth/token` and saves the token to
      state and in `localStorage` or `sessionStorage`.
    - `logout` (Function - takes no arguments and clears the token from state and from
      `localStorage` or `sessionStorage`.

2. Build a `UserContext` and `UserProvider` as we did in class that provides access to
   `user`, the response body from `/users/me`. It should do the API request if
   `isLoggedIn` is true.

3. Build a hook `useAuth` as a shortcut for `useContext(AuthContext)`.

4. Build a hook `useUser` as a shortcut for `useContext(UserContext)`.

5. Wrap your application in the new providers.
    ```jsx
    <QueryClientProvider ...>
      <BrowserRouter>
        <AuthProvider>
          <UserProvider>
            // your components and routes here
          </UserProvider>
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
    ```

## Routes

If a user is logged in, the app must support the routes
- `/`
- `/chats`
- `/chats/:chatId`
- `/profile`

If a user is not logged in, the app must support the routes
- `/`
- `/login`
- `/register`

If a user is logged in, a wildcard route `"*"` should exist that either redirects the user to
a Not Found page or to the `/chats` page. If a user is not logged in, a wildcard route
`"*"` should exist that redirects the user to the `/login` page.

If a user is loggd in, the routes `/login` and `/register` should be inaccessible. If a user is not logged in, the routes `/chats`, `/chats/:chatId`, and `/profile` should be inaccessible.

## Top navigation

Your application should have a navigation at the top, regardless of whether a user is
logged in or not. In either case, the top navigation should have two `Link` or `NavLink`
elements.

If a user is logged in, the elements are
- a link with text `pony express` (capitalization is up to you) that routes to `/`
- a link with text `{user.username}` that routes to `/profile`

If a user is not logged in, the elements are
- a link with text `pony express` (capitalization is up to you) that routes to `/`
- a link with text `login` that routes to `/login`

## Pages

1. The login page. For ease of grading, you must use a component located at
   `src/components/Login.jsx`. Recall that it must be styled using tailwind. This page is
   located at the route `/login`. It should include a form for logging in, with fields
   `username` and `password`, and a submit button with the text `login`. Submitting the
   form should get an access token and store the token in `localStorage` or
   `sessionStorage` and then redirect the user to the `/chats` route. There should also be
   a link to the `/register` page with text about creating an account. It could look
   something like this.
    ```
    username
    ------------------
    |                |
    ------------------

    password
    ------------------
    |                |
    ------------------

    -----------
    |  login  |
    -----------

    click here to create an account
    ```

2. The registration page. For ease of grading, you must use a component located at
   `src/components/Registration.jsx`. Recall that it must be styled using tailwind. This
   page is located at the route `/register`. It should include a form for registering a
   new user, with fields `username`, `email`, and `password`, and a submit button with the
   text `register`. Submitting the form should create a new user in the database and
   redirect the user to the login page. There should also be a link to the `/login` page
   with text about logging in. It could look something like this.
    ```
    username
    ------------------
    |                |
    ------------------

    email
    ------------------
    |                |
    ------------------

    password
    ------------------
    |                |
    ------------------

    --------------
    |  register  |
    --------------

    click here to login
    ```

3. The profile page. For ease of grading, you must use a component located at
   `src/components/Profile.jsx`. Recall that it must be styled using tailwind. This page
   is located at the route `/profile`. It should include the user details: `username`,
   `email`, and `created_at`. It should also include a button with the text `logout` that
   logs the user out and redirects to the `/login` route when it is clicked. It could look
   something like this.
    ```
    username: juniper

    email: juniper@cool.email

    member since: Sat Oct 31 2020

    ------------
    |  logout  |
    ------------
    ```

4. The left navigation. This component is present at both the `/chats` and
   `/chats/:chatId` routes. It should contain a `Link` or `NavLink` for every chat with
   the text `{chat.name}`. Clicking on a link should redirect the user to the appropriate
   `/chats/:chatId` route. It could look something like this.
    ```
    newt
    nostromo
    phoenix asteroids
    sensory apparatus
    skynet
    terminators
    ```

5. The chat page. This page is located at the `/chats/:chatId`. It should have the left
   navigation, as discussed above. It should contain all of the messages in the chat. And
   it should contain a new form at the bottom with a `text` input field and a submit
   button with the text `send`. Submitting this form should add a new message to the
   appropriate chat authored by the logged-in user. It could look something like this.
   ```
   ...

   ------------------------------------------------
   | terminator     Thu Dec 16 2021 - 11:53:38 AM |
   | I must be destroyed.                         |
   ------------------------------------------------

   ------------------------------------------------
   | sarah          Thu Dec 16 2021 - 06:22:50 PM |
   | Can you get us in there, past security?      |
   ------------------------------------------------

   ...

   -------------------------------------   --------
   | new message                       |   | send |
   -------------------------------------   --------
   ```

6. The chats page. This page is located at `/chats`. It has the left navigation as
   described above and the text `select a chat` to the right.

7. The home page. If the user is logged in, this page redirects the user to the `/chats`
   route. If the user is not logged in, it should have a brief description of the pony
   express application and a link to the `/login` page with the text `get started`.

