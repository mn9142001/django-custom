from typing import List
from wsgi.schema import BaseModel
from pydantic import validator
from .permission import PermissionSchema
from wsgi import exception
from django.contrib.auth.hashers import make_password
from user.models import User


class PasswordMixin:
    password : str

    
    @validator("password")
    def password_validator(cls, password : str):
        if len(password) < 6:
            raise exception.ValidationError("password is too short")
        return password


class UserSchema(PasswordMixin, BaseModel):
    username : str
        
    @classmethod
    async def create(cls, data : dict):
        data = await cls.validate_data(data)
        data['password'] = make_password(data['password'])
        return await User.objects.acreate(**data)
    
    @classmethod
    async def validate_data(cls, data):
        if await User.objects.filter(username=data['username']).aexists():
            raise exception.ValidationError("username already exists")
        return data
    
    
class UserReadSchema(BaseModel):
    id : int
    first_name : str
    last_name : str
    username : str
    permissions : List[PermissionSchema]
    
    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        obj.permissions = obj.user_permissions.all()
        return super().model_validate(obj, *args, **kwargs)