from src.aws.dynamo.functions.save_on_dynamo import save_data_on_dynamo
from unittest import TestCase
from src.utils.error_class.api_error_class import APIError
import unittest.mock as mock
from src.aws.dynamo.dynamo_client import dynamo
import pytest
from dotenv import load_dotenv
from os import getenv as env

load_dotenv()

class TestSaveDataOnDynamo(TestCase):

    @mock.patch.object(dynamo, "put_item")
    def test_save_data_on_dynamo_success(self, mock_put_item):
        api_return = {
            "unique_id": "1234567890",
            "received_phrase": "test",
            "url_to_audio": "https://example.com/audio.mp3",
            "created_audio": "2023-5-19"
        }

        save_data_on_dynamo(api_return)

        
        mock_put_item.assert_called_once_with(
            TableName=env("dynamo_table"),
            Item={
                "hash": {"S": api_return["unique_id"]},
                "audio_data": {
                    "M": {
                        "received_phrase": {"S": api_return["received_phrase"]},
                        "url_to_audio": {"S": api_return["url_to_audio"]},
                        "created_audio": {"S": api_return["created_audio"]},
                    }
                },
            }
        )

    @mock.patch.object(dynamo, "put_item")
    def test_save_data_on_dynamo_resource_not_found(self, mock_put_item):
        api_return = {
            "unique_id": "1234567890",
            "received_phrase": "Hello, world!",
            "url_to_audio": "https://example.com/audio.mp3",
            "created_audio": "2023-09-27T11:12:44Z"
        }

        mock_put_item.side_effect = dynamo.exceptions.ResourceNotFoundException

        with pytest.raises(APIError):
            save_data_on_dynamo(api_return)

       
