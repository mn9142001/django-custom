from wsgi.schema import BaseModel


class PermissionSchema(BaseModel):
    name : str
    code_name : str
    
    