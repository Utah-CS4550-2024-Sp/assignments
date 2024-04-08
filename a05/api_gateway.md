# Connecting an API which integrates with the FastAPI Lambda

We will use AWS ApiGateway to manage the web connection to the lambda function that holds
our FastAPI application.

Navigate to the API Gateway console in AWS and create a new API. Under `HTTP API`, click
`Build`. Add a Lambda integration to the function `pony-express-lambda` that you created
in the previous document. Give the API a meaningful name, for example `pony-express-api`
and click `Next`. Change the Resource path to be `/{proxy+}` and click `Next`. Leave the
default stage and click `Next` again. Finalize it by clicking `Create`.

If you click on the API itself, you can find an Invoke URL. Navigating to that URL
appended by `/docs`, you should be able to access the Swagger docs. Test out some of the
functionality using the Swagger docs or Postman.

