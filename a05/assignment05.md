# Assignment #5

There are **3 options** for this assignment. You must **choose one** of the options to
complete for full credit.

You may choose an additional second option to complete for extra credit. The extra credit
will be applied in as a boost to either your lowest assignment score or your lowest exam
score.

The assignment is due on **Friday, 19 April, 2024**.

## Assignment #5a

The goal of assignment #5a is to deploy your application (both backend and frontend) to
the cloud. You are free to choose any deployment strategy, but support is only provided
for the two strategies covered in class. Your backend and frontend must be publicly
available on the internet for at least two weeks after the due date.

1. Package and deploy your backend application to AWS Lambda. Host your database in the
   cloud and seed it with initial data. Choose one of the following:

    a. [With database hosted in EFS](./lambda_with_efs.md)

    b. [With database hosted in RDS](./lambda_with_rds.md)

4. [Add an HTTP API](./api_gateway.md) that integrates with your lambda function
5. [Deploy your frontend application](./amplify.md) to AWS Amplify.

## Assignment #5b

The goal of assignment #5b is to add features to both the backend and frontend that
support managing chats, including
- creating a new chat
- editing a chat name
- adding/removing users from chats
- enforcing some limited permissions around chat management and visilibity.

The specification will be available soon.

## Assignment #5c

The goal of assignment #5c is to add features to both the backend and frontend that
support managing chat messages, including
- editing messages
- deleted messages
- enforcing some limited permissions around message management

The specification will be available soon.

