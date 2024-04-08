# Assignment #5a

The goal of assignment #5a is to deploy your application (both backend and frontend) to
the cloud. You are free to choose any deployment strategy, but support is only provided
for the two strategies covered in class. Your backend and frontend must be publicly
available on the internet for at least two weeks after the due date.

## Steps for deployment

1. Package and deploy your backend application to AWS Lambda, choosing to hose your
   database in either EFS or RDS. Seed your database with initial data. The files for
   seeding the database are [db_seeder.py](./db_seeder.py) and [initial.db](./initial.db).

   - [Package and deploy to AWS Lambda / EFS](./lambda_with_efs.md)

   - [Package and deploy to AWS Lambda / RDS](./lambda_with_rds.md)

2. [Add an HTTP API via API Gateway](./api_gateway.md) that integrates with your lambda
   function.

3. [Deploy your frontend application to AWS Amplify](./amplify.md)

