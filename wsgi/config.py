import os

class Config:
    
    DEFAULT_AUTHENTICATION_CLASSE = []
    SECRET_KEY = "SDKOAFGDDOAWOQTEQORQK0-1I359R91-I$K35-9"
    DEFAULT_PERMISSIONS_CLASSES = []
    
    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

        os.environ.setdefault('API_SECRET_KEY', self.SECRET_KEY)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)