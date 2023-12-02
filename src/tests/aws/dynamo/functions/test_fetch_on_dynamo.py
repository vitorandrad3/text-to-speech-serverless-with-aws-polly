from src.aws.dynamo.functions.fetch_on_dynamo import fetch_data_on_dynamo
from unittest import TestCase
from src.utils.error_class.api_error_class import APIError
import unittest.mock as mock
from src.aws.dynamo.dynamo_client import dynamo
import pytest
from dotenv import load_dotenv
from os import getenv as env

load_dotenv()

class TestFetchDataOnDynamo(TestCase):

    @mock.patch.object(dynamo, "get_item")
    def test_fetch_data_on_dynamo(self, mock_get_item):
        hash = '1234567890'
        fetch_data_on_dynamo(hash)

        mock_get_item.assert_called_once_with(
            TableName=env("dynamo_table"),
            Key={
                "hash": {"S": hash},
            }
        )

    @mock.patch.object(dynamo, "get_item")
    def test_fetch_data_on_dynamo_request_limit_exceeded(self, mock_get_item):
        hash = '1234567890'

        mock_get_item.side_effect = dynamo.exceptions.RequestLimitExceeded

        with pytest.raises(APIError):
            fetch_data_on_dynamo(hash)
