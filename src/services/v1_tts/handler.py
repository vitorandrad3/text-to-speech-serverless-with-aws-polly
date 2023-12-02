from src.aws.polly.functions.text_to_speech import get_audio_and_date
from src.aws.s3.functions.save_audio_on_s3 import save_audio_on_s3_and_get_link
from src.utils.hash_generator import hash_generator
import json


def v1_tts_lambda(event, context):
    try:

        user_post = json.loads(event["body"])

        text = user_post['phrase']

        text_hash = hash_generator(text)
        created_date, audio_file = get_audio_and_date(text)
        audio_link = save_audio_on_s3_and_get_link(
            key=text_hash, audio_file=audio_file)

        api_return = {
            'received_phrase': text,
            'url_to_audio': audio_link,
            'created_audio': created_date
        }

        return json.dumps(api_return)

    except Exception as err:

        api_return = {"statusCode": err.status_code,
                      "body": json.dumps({"error": err.message})}

        return api_return
