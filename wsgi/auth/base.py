from wsgi.request import Request
import os

class BaseAuthentication:
    header_name : str = "authorization"
    token_prefix : str
    
    def __init__(self, request : Request):
        self.request = request

    async def get_header_name(self):
        return self.header_name

    async def get_token(self):
        token : str = await self.request.headers[await self.get_header_name()]
        return token

    async def authenticate(self):
        raise NotImplementedError

    @staticmethod
    def get_api_secret_key():
        return os.environ['API_SECRET_KEY']