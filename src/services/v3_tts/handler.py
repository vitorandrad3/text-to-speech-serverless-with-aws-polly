from src.aws.polly.functions.text_to_speech import get_audio_and_date
from src.aws.s3.functions.save_audio_on_s3 import save_audio_on_s3_and_get_link
from src.utils.hash_generator import hash_generator
from src.aws.dynamo.functions.save_on_dynamo import save_data_on_dynamo
from src.aws.dynamo.functions.fetch_on_dynamo import fetch_data_on_dynamo
import json


def v3_tts_lambda(event, context):
    try:

        user_post = json.loads(event["body"])

        text = user_post['phrase']

        text_hash = hash_generator(text)

        dynamo_item = fetch_data_on_dynamo(text_hash)

        if 'Item' in dynamo_item:
            api_return = {
                'received_phrase': dynamo_item['Item']['audio_data']['M']['received_phrase']['S'],
                'url_to_audio': dynamo_item['Item']['audio_data']['M']['url_to_audio']['S'],
                'created_audio': dynamo_item['Item']['audio_data']['M']['created_audio']['S'],
                'unique_id': dynamo_item['Item']['hash']['S']
            }

        else:
            created_date, audio_file = get_audio_and_date(text)

            audio_link = save_audio_on_s3_and_get_link(
                key=text_hash, audio_file=audio_file)

            api_return = {
                'received_phrase': text,
                'url_to_audio': audio_link,
                'created_audio': created_date,
                'unique_id': text_hash
            }

            save_data_on_dynamo(api_return)

        return json.dumps(api_return)

    except Exception as err:

        api_return = {"statusCode": err.status_code,
                      "body": json.dumps({"error": err.message})}

        return api_return
