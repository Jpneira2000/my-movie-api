from jwt import encode, decode

def create_token(data: dict):
    tocken: str = encode(payload=data, key='my_secret_key', algorithm='HS256')
    return tocken

def validate_token(token: str) -> dict:
    data: str = decode(token, key='my_secret_key', algorithms=['HS256'])
    return data