from src.aws.s3.functions.save_audio_on_s3 import save_audio_on_s3_and_get_link
from unittest import TestCase
from src.utils.error_class.api_error_class import APIError
import unittest.mock as mock
from src.aws.s3.s3_client import s3
from dotenv import load_dotenv
from os import getenv as env

load_dotenv()

class TestSaveAudioOnS3AndGetLink(TestCase):

    @mock.patch.object(s3, "put_object")
    def test_save_audio_on_s3_and_get_link(self, mock_put_object):
        key = 'audio'
        audio_file = 'audio.mp3'
        save_audio_on_s3_and_get_link(audio_file, key)

        mock_put_object.assert_called_once_with(
            Bucket=env("bucket_name"),
            Key=key,
            Body=audio_file
        )
