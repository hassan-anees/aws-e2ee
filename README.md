# AWS End-to-end encryption

This project will focus on implementing e2ee with dynamodb

## Needed dependencies

- environs, boto3, dynamodb_encryption_sdk

## Project Details

This project serves as a basic template to start off with end-to-end encryption implmentation. There are several prerequisites to get this running which is listed below:

- create an AWS account to in order to use resources like DynamnoDB, encryption library, AWS Key Management System
- create a local.env file that will hold AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_CMK_ID. The first three come directly from your AWS account settings or you can create an IAM profile that enables DynamoDB accesss
- Go to the KMS panel on AWS and create a symmetric encryption key then grab the ARN link of that KMS key. Place this as the value for your AWS_CMK_ID envrionement variable.

## Running the program

Once you have added your values to your enviornment variables, you can simpley go within the code and change the schema for the database. The default schema in place will create a table named 'Patients' with a primary key as 'pid'.

To execute the program now simply run

```
python3 aws-script.py
```

This will create a database and add a single data item within the database
