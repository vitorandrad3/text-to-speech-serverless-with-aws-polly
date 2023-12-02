import hashlib

def hash_generator(phrase):
    formated_phrase = phrase.lower()
    hash = hashlib.md5(formated_phrase.encode()).hexdigest()
    return hash