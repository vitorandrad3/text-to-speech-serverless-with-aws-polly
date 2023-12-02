from src.aws.polly.functions.text_to_speech import get_audio_and_date
from src.utils.error_class.api_error_class import APIError
from src.tests.mocks.mock_constants import mock_long_text
import pytest

def test_text_to_speech_success():
    creation_date, audio_data = get_audio_and_date('test')
    assert creation_date != None
    assert audio_data != None

def test_text_to_speech_length_exception():
    with pytest.raises(APIError):
        get_audio_and_date(mock_long_text)
