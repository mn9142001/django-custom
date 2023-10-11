from functools import cached_property
from wsgi.structs import QueryParameter, Headers
from wsgi.mixins import SendResponseMixin, RequestBodyDecoder


class Request(RequestBodyDecoder, SendResponseMixin):
    kwargs : dict
    method : str
    
    def __init__(self, scope : dict, send = None, rec = None) -> None:
        self.kwargs = {}
        self.scope = scope
        self.set_scope()
        self.headers = Headers(headers=scope.get('headers', []))
        
        self.sender, self.rec = send, rec
        
    def set_scope(self):
        for key, value in self.scope.items():
            setattr(
                self, 
                key, 
                value.decode() if type(value) == bytes else value
            )
    
    @property
    def api_config(self):
        return self.scope['app'].config
    
    @cached_property
    def params(self) -> QueryParameter:
        return QueryParameter(self.query_string)
    
    @property
    def content_length(self):
        return int((self.headers, b'content-length', b'0'))

    @property
    def dest(self):
        return self.path
    
    async def authenticate(self, auth_class = None):
        
        if auth_class is None:
            auth_class = self.api_config.DEFAULT_AUTHENTICATION_CLASSE
        
        auth_class = auth_class(self)
        await auth_class.authenticate()        
