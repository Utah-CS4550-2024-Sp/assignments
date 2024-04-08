# Deploy frontend to AWS Amplify

## Update your frontend code

The frontend code needs to be updated to support a cloud backend. We can use an
environment variable for this. By default, Vite makes environment variables accessible at
`import.meta.env`, but only those that begin with `VITE_`. We will be using an environment
variable `VITE_API_BASE_URL`. If we don't supply the environment variable, we can default
to using the localhost. So we might include in our frontend code something like the
following.

```javascript
const baseUrl = import.meta.env.VITE_API_BASE_URL || http://127.0.0.1:8000;
```

Then, for example, instead of making a request to `"http://127.0.0.1:8000/users/me"`, we
would make a request to `baseUrl + "/users/me"`.

After updates, push your code to github so we can deploy.

## Deploying via github

Navigate to the Amplify console in AWS. Click `New app > Host web app`. You can specify
your github repository or you can build a zip file. Github is the easiest way, because any
merge to the specified branch will cause the app to rebuild and redeploy.

Select your github repository and choose a branch. Then check the box `Connecting to a
monorepo? Pick a folder.` Enter `frontend` as the folder. Then choose a suitable name for
your application.

Under advanced settings, add an environment variable with key `VITE_API_BASE_URL` and
value the URL from your HTTP API resource in API Gateway.

Finally, click `Save and deploy`. Make note of the URL of the new application.

## Updating the CORS middleware

In our `backend/main.py` file, we need to update our CORS middleware. Add the URL for the
new application to the list of possible origins.

Once you have done that, you can update your backend zip file.

```bash
zip -ur build.zip ./backend
```

Then you can upload the updated zip file to your lambda application via the Lambda
console, or via the command line.

```bash
aws lambda update-function \
--function-name pony-express-lambda \
--zip-file build.zip
```

