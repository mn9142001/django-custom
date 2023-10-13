from wsgi.exception import ApiException
from typing import Any, Optional
from wsgi.request import Request
from wsgi.router import Router
from wsgi.middleware import BaseMiddleWare
from wsgi.response import Response
import tempfile
from django.core.exceptions import RequestAborted
from django.conf import settings

class App:

    def __init__(self, middlewares : list[BaseMiddleWare]=[], urls = [], config = settings) -> None:
        self.router = Router()
        self.middlewares = middlewares
        self.include_urls(urls)
        self.config = config
    
    def include_urls(self, urls):
        self.router.include_urls(urls)
        
    def include_router(self, router : Router):
        self.router.include_urls(router.routes)
    
    async def __call__(self, scope: dict, rec, send, **kwargs: Any) -> Any:
        scope['app'] = self
        try:                
            self.request = Request(scope, send=send, rec=rec, body_file = await self.read_body(rec))
            response = self.router(self.request)
            await response
        except ApiException as e:
            await self.handle_Exception(e)
            
    async def handle_Exception(self, exception : ApiException):
        message = await self.get_exception_message(exception.message)
        status = exception.status_code
        await Response(message, request=self.request, status=status).send_body()

    async def get_exception_message(self, message : Optional[str | dict]):
        if type(message) == dict:
            return dict
        return {"detail" : message}

    async def read_body(self, receive):
        """Reads an HTTP body from an ASGI connection."""
        # Use the tempfile that auto rolls-over to a disk file as it fills up.
        body_file = tempfile.SpooledTemporaryFile(
            max_size=settings.FILE_UPLOAD_MAX_MEMORY_SIZE, mode="w+b"
        )
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                body_file.close()
                # Early client disconnect.
                raise RequestAborted()
            # Add a body chunk from the message, if provided.
            if "body" in message:
                body_file.write(message["body"])
            # Quit out if that's the end.
            if not message.get("more_body", False):
                break
        body_file.seek(0)
        return body_file