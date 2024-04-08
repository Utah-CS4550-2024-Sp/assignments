# Deploying to AWS Lambda with database hosted in EFS

This deployment strategy (covered in class) consists of the following steps:

1. Update and package your backend application, then deploy to AWS Lambda.

2. Connect your lambda function to a file system (AWS Elastic File System) to host your
   database.

3. Deploy code to Lambda that can seed your EFS database with the initial data.

## Update your backend application

In order to run FastAPI in AWS Lambda, we need to use a connector to translate between
Lambda context and FastAPI requests and responses. The package we use is called `mangum`.
Firstly, we add the package to our dependencies.

```bash
poetry add mangum
```

Then we add two lines of code to our `backend/main.py`. One line at the top to import the
connector

```python
from mangum import Mangum
```

and one line at the bottom to define the lambda handler.

```python
lambda_handler = Mangum(app)
```

We also need to support multiple database engines. During development, we want to continue
to use the local database `backend/pony_express.db`, but in production we want to use a
SQLite database located in EFS at `/mnt/efs/pony_express.db`. In order to support both, we
will introduce an optional environment variable `DB_LOCATION` and check whether it is
equal to `"EFS"`. We will also decide whether to print the results of our database
operations to the console using the same environment variable. Update the appropriate code
in `backend/database.py` with functionality that may look something like this.

```python
if os.environ.get("DB_LOCATION") == "EFS":
    db_path = "/mnt/efs/pony_express.db"
    echo = False
else:
    db_path = "backend/pony_express.db"
    echo = True

engine = create_engine(
    f"sqlite:///{db_path}",
    echo=echo,
    connect_args={"check_same_thread": False},
)
```

## Package your backend application

We need to build a zip file that contains our backend code alongside its dependencies.
This zip file should contain dependencies that are compatible with `x86_64` architecture.

See [./package_backend.md](Package your backend application).

## Choose a VPC (Virtual Private Cloud)

Navigate to the VPC console in AWS and choose a VPC. For example, you may decide to choose
the default VPC that comes with your account. Make note of the `Subnet IDs`, for example
`subnet-{{hex1}` and `subnet-{{hex2}}`.

Navigate to the Security Groups page in the EC2 console in AWS and choose a security
group. For example, you may choose the default security group that comes with your
account. Make note of the `Security group ID`, for example `sg-{{hex3}}`.

## Create a file system in EFS (Elastic File System)

Navigate to the EFS console and create a file system. Make sure to create it in the VPC
that you chose above. In that file system, create an access point. Give your access point
a meaningful name, for example `pony-express-fs-ap`. The access point should have the
following: a root directory path of `/mnt/efs`; a POSIX user with User ID `1000` and Group
ID `1000`; and root directory creation permssions with Owner user ID `1000`, Owner group
ID `1000`, and Access point permissions `0777`. Make note of the access point ARN, of the
form `arn:aws:elasticfilesystem:{{region}}:{{account}}:access-point/{{access-point-id}}`.

## Create an execution role

Navigate to the Roles page in the IAM console and create a role. It will be an AWS Service
role with a Lambda use case. We need to attach four policies for our lambda function to
use: `AWSLambdaBasicExecutionRole`, `AWSLambdaVPCAccessExecutionRole`,
`AWSXRayDaemonWriteAccess`, and `AmazonElasticFileSystemClientFullAccess`. Give the role a
meaningful name, for example `pony-express-lambda-role`. Make note of the role ARN, of the
form `arn:aws:iam::{{account}}:role/pony-express-lambda-role`.

## Create a lambda function

We will create a lambda function using either the console or the command line.

### Console

Navigate to the Lambda console in AWS and create a function.
1. Choose a meaningful name, for example `pony-express-lambda`.
2. Select `Python 3.11` as the runtime.
3. Choose `x86_64` as the achitecture.
4. Choose `pony-express-lambda-role` for the execution role.
5. Under advanced settings, click on `Enable VPC`, select the VPC you chose above, the
   subnets you chose above, and the security group you chose above.
6. Click `Create function`.
7. Under `Code`, click `Upload from` and choose the zip file `build.zip`.
8. Under `Code`, edit the runtim settings and change the handler to
   `backend.main.lambda_handler`.
9. Under `Configuration > General configuration`, edit the timeout to be 10 seconds and
   the memory to be 1024 MB.
10. Under `Configuration > Environment variables`, add an environment variable with key
    `DB_LOCATION` and value `EFS`.
11. Under `Configuration > File systems`, add the file system and access point you created
    above with local mount path `/mnt/efs`.

### Command line

```bash
aws lambda create-function \
--function-name pony-express-lambda \
--runtime python3.11 \
--role {{pony-express-lambda-role-ARN}} \
--handler backend.main.lambda_handler \
--zip-file fileb://build.zip \
--memory-size 1024 \
--timeout 10 \
--environment "Variables={DB_LOCATION=EFS}" \
--vpc-config SubnetIds=subnet-{{hex1}},subnet-{{hex2}},SecurityGroupIds=sg-{{hex3}} \
--file-system-configs Arn={{pony-express-fs-ap-ARN}}
```

## Seed the database

Our last step is to seed the EFS database with the initial data. We will deploy a second
lambda function to seed the database.

1. Copy the two files [initial.db](./initial.db) and [db_seeder.py](./db_seeder.py) into
   `backend` in your project. The first file is the same as the `sample.db` from a
   previous assignment. The second file has code and a lambda handler to take the data
   from `initial.db` and insert it into the EFS database.

2. Update your `build.zip`.
    ```bash
    zip -ur build.zip ./backend
    ```

3. Create a lambda function with all of the exact same settings as the lambda you created
   in the previous section, with the following differences:

    - The function-name should be different, for example `pony-express-db-seeder`.

    - The timeout should be longer, say 60 seconds.

    - The handler must be `backend.db_seeder.lambda_handler`.

4. In the Lambda console in AWS, navigate to the newly created DB Seeder lambda function,
   and click `Test` to run the function. If everything works, you should see the result
   and it should look something like
    ```json
    {
        "statusCode": 200,
        "body": {
            user_count: {local: 10, prev: 0, additions: 10, final: 10},
            chat_count: {local: 6, prev: 0, additions: 6, final: 6},
            message_count: {local: 291, prev: 0, additions: 291, final: 291},
            link_count: {local: 13, prev: 0, additions: 13, final: 13}
        }
    }
    ```

