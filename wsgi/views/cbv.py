from wsgi.request import Request
from wsgi.exception import Http405


class View:
    
    request : Request
    DEFAULT_AUTHENTICATION_CLASS = False
    DEFAULT_PERMISSIONS_CLASSES = None
    
    def __init__(self, request : Request) -> None:
        self.request = request
    
    @classmethod
    def as_view(cls):
        return cls.dispatch
    
    @classmethod
    async def dispatch(cls, request : Request):
        view = cls(request)
        return await view.call_method()
    
    async def call_method(self):
        await self.authenticate()
        
        method_name = self.request.method.lower()
        view = getattr(self, method_name, None)
        
        if view is None:
            raise Http405
        
        response = await view()
        return response

    async def authenticate(self):
        if self.DEFAULT_AUTHENTICATION_CLASS is False: return
        await self.request.authenticate(await self.get_authentication_classes())
    
    async def get_authentication_classes(self):
        if self.DEFAULT_AUTHENTICATION_CLASS is None:    
            return self.request.api_config.DEFAULT_AUTHENTICATION_CLASS
        return self.DEFAULT_AUTHENTICATION_CLASS

