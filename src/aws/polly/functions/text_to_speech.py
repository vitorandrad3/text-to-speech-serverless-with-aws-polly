from src.aws.polly.polly_client import polly
from src.utils.format_date import format_date
from src.utils.error_class.api_error_class import APIError


def get_audio_and_date(phrase):
    try:
        response = polly.synthesize_speech(
            Engine='neural', Text=phrase, OutputFormat='mp3', VoiceId='Vitoria')
        audio_data = response['AudioStream'].read()

        creation_date = response['ResponseMetadata']['HTTPHeaders']['date']
        creation_date = format_date(creation_date)

        return creation_date, audio_data

    except polly.exceptions.TextLengthExceededException:
        raise APIError(
            status_code=413, message='Polly: Very long sentence, must be less than 3000 characters')

    except polly.exceptions.ServiceFailureException:
        raise APIError(status_code=500, message='Polly: Service failure error')

    except Exception as err:
        raise APIError(status_code=500,
                       message=f'Polly: Unexpected error: {str(err)}')
