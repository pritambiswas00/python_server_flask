from marshmallow import Schema, fields, post_load
from typing import TypedDict, Optional, Union
from dataclasses import dataclass, asdict
        
        
##User
@dataclass
class CreateUser:
    name:str
    email:str
    phone_number:str
    country_code_id:str
    session_id:Union[int, None]
    
    
    def to_dict(self) -> dict:
            return {key: value for key, value in asdict(self).items() if value is not None}

        
  
##Update todo validation schema     
# class UpdateTodoSchema(Schema):
#     title = fields.Str(required=False, validate=lambda x: len(x) > 0, allow_none=True, default=None)
#     description = fields.Str(required=False, allow_none=True, default=None)
#     completed = fields.Bool(required=False, allow_none=True, default=None)
#     id = fields.Int(strict=True, required=True)
    
#     @post_load
#     def make_payload(self, data, **kwargs):
#         # Ensure all fields have default values if not provided
#         data_with_defaults = {
#             "id": data.get("id"),  # ID is required, no default needed
#             "title": data.get("title", None),  # Default to None
#             "description": data.get("description", None),  # Default to None
#             "completed": data.get("completed", None),  # Default to None
#         }
#         print(f"{data_with_defaults} data after adding defaults")
#         return UpdateTodoPayload(**data_with_defaults)
