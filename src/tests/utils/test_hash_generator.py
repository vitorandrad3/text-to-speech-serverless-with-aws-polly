from src.utils.hash_generator import hash_generator

def test_hash_generator():
    assert hash_generator('test') == '098f6bcd4621d373cade4e832627b4f6'
    assert hash_generator('test2') == 'ad0234829205b9033196ba818f7a872b'
    assert hash_generator('test3') == '8ad8757baa8564dc136c1e07507f4a98'