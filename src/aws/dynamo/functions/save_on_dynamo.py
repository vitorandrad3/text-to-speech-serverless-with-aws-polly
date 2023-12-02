from src.aws.dynamo.dynamo_client import dynamo
from src.utils.error_class.api_error_class import APIError
from dotenv import load_dotenv
from os import getenv as env

load_dotenv()


def save_data_on_dynamo(api_return):
    try:
        item = {
            "hash": {"S": api_return["unique_id"]},
            "audio_data": {
                "M": {
                    "received_phrase": {"S": api_return["received_phrase"]},
                    "url_to_audio": {"S": api_return["url_to_audio"]},
                    "created_audio": {"S": api_return["created_audio"]},
                }
            },
        }
        dynamo.put_item(TableName=env("dynamo_table"), Item=item)

    except dynamo.exceptions.ResourceNotFoundException:
        raise APIError(
            status_code=400, message='dynamoDB: Resource not found')
    except dynamo.exceptions.ItemCollectionSizeLimitExceededException:
        raise APIError(
            status_code=400, message='dynamoDB:Too large object')
    except dynamo.exceptions.RequestLimitExceeded:
        raise APIError(
            status_code=429, message='dynamoDB: Resquest limit exceeded')
    except Exception as err:
        raise APIError(status_code=500,
                       message=f'dynamoDB: Unexpected error: {str(err)}')
