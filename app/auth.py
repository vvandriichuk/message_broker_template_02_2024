import os
import jwt

APP_SECRET_KEY = os.environ.get('APP_ACCESS_KEY')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')


async def create_token():
    payload = {
        "sub": "brokers_handler",
    }
    token = jwt.encode(payload, APP_SECRET_KEY, algorithm=JWT_ALGORITHM)

    return token
