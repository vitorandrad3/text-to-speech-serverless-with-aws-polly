from src.aws.boto_session import boto_session

dynamo = boto_session.client(service_name='dynamodb')