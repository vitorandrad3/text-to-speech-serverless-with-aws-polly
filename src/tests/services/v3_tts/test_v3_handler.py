from src.services.v3_tts.handler import v3_tts_lambda
from src.tests.mocks.mock_constants import mock_dynamo_item, mock_dynamo_without_item
from src.utils.error_class.api_error_class import APIError
import unittest.mock as mock
from unittest import TestCase
import json


class TestV3TTSHandler(TestCase):

    def test_v3_tts_lambda_success(self):
        user_post = {"body": json.dumps({"phrase": "frase de teste"})}

        response = v3_tts_lambda(user_post, '')
        response = json.loads(response)

        self.assertIsNotNone(response)

    @mock.patch('src.services.v3_tts.handler.fetch_data_on_dynamo', return_value=mock_dynamo_item)
    def test_v3_tts_lambda_with_dynamo_item(self, mock_fetch_data_on_dynamo):

        api_return = v3_tts_lambda(
            {'body': json.dumps({'phrase': 'hello, world'})}, None)

        assert api_return == '{"received_phrase": "hello, world", "url_to_audio": "https://s3.amazonaws.com/meu-bucket/meu-arquivo.mp3", "created_audio": "10/07/2023", "unique_id": "1234567890"}'

    @mock.patch('src.services.v3_tts.handler.fetch_data_on_dynamo', return_value=mock_dynamo_without_item)
    def test_v3_tts_lambda_without_dynamo_item(self, mock_fetch_data_on_dynamo):

        api_return = v3_tts_lambda(
            {'body': json.dumps({'phrase': 'hello, world'})}, None)

        self.assertIsNotNone(api_return)

    @mock.patch('src.services.v3_tts.handler.fetch_data_on_dynamo', side_effect=APIError(status_code=500, message='test'))
    def test_v3_tts_lambda_with_raise_error(self, mock_fetch_data_on_dynamo):

        api_return = v3_tts_lambda(
            {'body': json.dumps({'phrase': 'hello, world'})}, None)

        expected_result = {"statusCode": 500,
                           "body": json.dumps({"error": "test"})}

        assert api_return == expected_result
