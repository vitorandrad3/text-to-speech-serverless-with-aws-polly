from src.services.v2_tts.handler import v2_tts_lambda
from src.utils.error_class.api_error_class import APIError
from unittest import TestCase
import unittest.mock as mock
import json


class TestV2TTSHandler(TestCase):

    def test_v2_tts_lambda_success(self):
        user_post = {"body": json.dumps({"phrase": "frase de teste"})}

        response = v2_tts_lambda(user_post, '')
        response = json.loads(response)

        self.assertIsNotNone(response)

    @mock.patch('src.services.v2_tts.handler.get_audio_and_date', side_effect=APIError(status_code=500, message='test'))
    def test_v2_tts_lambda_with_get_audio_raise_error(self, mock_fetch_data_on_dynamo):

        api_return = v2_tts_lambda(
            {'body': json.dumps({'phrase': 'hello, world'})}, None)

        expected_result = {"statusCode": 500,
                           "body": json.dumps({"error": "test"})}

        assert api_return == expected_result

    @mock.patch('src.services.v2_tts.handler.save_audio_on_s3_and_get_link', side_effect=APIError(status_code=500, message='test'))
    def test_v2_tts_lambda_with_save_audio_raise_error(self, mock_fetch_data_on_dynamo):

        api_return = v2_tts_lambda(
            {'body': json.dumps({'phrase': 'hello, world'})}, None)

        expected_result = {"statusCode": 500,
                           "body": json.dumps({"error": "test"})}

        assert api_return == expected_result
