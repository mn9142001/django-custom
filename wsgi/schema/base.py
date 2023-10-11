from pydantic import BaseModel as pydantic_model


class BaseModel(pydantic_model):
    
    async def validate_data(data : dict):
        return data
    

BaseModel.model_config["from_attributes"]=True