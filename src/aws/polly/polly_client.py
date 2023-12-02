from src.aws.boto_session import boto_session

polly = boto_session.client(service_name='polly')