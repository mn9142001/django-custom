from wsgi.auth.base import BaseAuthentication
from wsgi.exception import Http401
from jwt import decode as jwt_decode, exceptions as jwt_exception, encode as jwt_encode
from .user import RequestUser

class JwtAuthentication(BaseAuthentication):
    token_prefix = "Bearer"

    async def get_token(self):
        token = await super().get_token()
        try:                
            return token.split()[-1]
        except AttributeError as e:
            raise Http401

    async def authenticate(self):
        
        token = await self.get_token()
        
        try:                
            decoded_data = jwt_decode(token, self.get_api_secret_key(), algorithms=["HS256"])
            return RequestUser(**decoded_data)
        except (jwt_exception.InvalidSignatureError, jwt_exception.InvalidTokenError) as e:
            raise Http401("Invalid token")

    @classmethod
    async def encode(cls, data):
        return jwt_encode(data, cls.get_api_secret_key())