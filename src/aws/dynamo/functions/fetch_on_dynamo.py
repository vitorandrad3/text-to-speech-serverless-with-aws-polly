from src.aws.dynamo.dynamo_client import dynamo
from src.utils.error_class.api_error_class import APIError
from dotenv import load_dotenv
from os import getenv as env

load_dotenv()


def fetch_data_on_dynamo(hash):
    try:
        key = {
            "hash": {"S": hash}
        }

        item = dynamo.get_item(TableName=env('dynamo_table'), Key=key)

        return item
    except dynamo.exceptions.RequestLimitExceeded:
        raise APIError(
            status_code=429, message='dynamoDB: Request limit exceeded')
    except dynamo.exceptions.InternalServerError:
        raise APIError(
            status_code=500, message='dynamoDB: Internal server error')
    except Exception as err:
        raise APIError(status_code=500,
                       message=f'dynamoDB: Unexpected error: {str(err)}')
