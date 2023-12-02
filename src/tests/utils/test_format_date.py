from src.utils.format_date import format_date

def test_format_date():
    assert format_date('Wed, 27 Sep 2023 16:29:38 GMT') == '27-09-2023 13:29:38'
    assert format_date('Thu, 28 Sep 2023 01:29:38 GMT') == '27-09-2023 22:29:38'
    assert format_date('Sat, 30 Sep 2023 13:29:38 GMT') == '30-09-2023 10:29:38'