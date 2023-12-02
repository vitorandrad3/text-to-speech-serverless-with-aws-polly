from src.aws.s3.s3_client import s3
from src.utils.error_class.api_error_class import APIError
from dotenv import load_dotenv
from os import getenv as env

load_dotenv()


def save_audio_on_s3_and_get_link(audio_file, key):
    try:
        bucket = env('bucket_name')

        s3.put_object(Bucket=bucket, Key=key, Body=audio_file)

        location = s3.generate_presigned_url(
            'get_object', Params={'Bucket': bucket, 'Key': key})

        return location
    except Exception as err:
        raise APIError(status_code=500,
                       message=f'Polly: Unexpected error: {str(err)}')
