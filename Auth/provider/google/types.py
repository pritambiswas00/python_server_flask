from dataclasses import dataclass, field, asdict
from typing import Optional
from marshmallow import Schema, fields, post_load, INCLUDE
from utils.index import Result


@dataclass
class UserInfo:
    at_hash: Optional[str] = None
    aud: Optional[str] = None
    azp: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    exp: Optional[int] = None
    family_name: Optional[str] = None
    given_name: Optional[str] = None
    iat: Optional[int] = None
    iss: Optional[str] = None
    name: Optional[str] = None
    nonce: Optional[str] = None
    picture: Optional[str] = None
    sub: Optional[str] = None


@dataclass
class GoogleUser:
    access_token: str
    expires_at: int
    expires_in: int
    id_token: str
    scope: str
    token_type: str
    userinfo: Optional[UserInfo] = field(default=None)

    def to_json(self) -> dict:
        return asdict(self)


class UserInfoSchema(Schema):
    at_hash = fields.Str(allow_none=True)
    aud = fields.Str(allow_none=True)
    azp = fields.Str(allow_none=True)
    email = fields.Str(allow_none=True)
    email_verified = fields.Bool(allow_none=True)
    exp = fields.Int(allow_none=True)
    family_name = fields.Str(allow_none=True)
    given_name = fields.Str(allow_none=True)
    iat = fields.Int(allow_none=True)
    iss = fields.Str(allow_none=True)
    name = fields.Str(allow_none=True)
    nonce = fields.Str(allow_none=True)
    picture = fields.Str(allow_none=True)
    sub = fields.Str(allow_none=True)

    @post_load
    def return_userinfo(self, data, **kwargs):
        return UserInfo(**data)


class GoogleUserSchema(Schema):
    access_token = fields.Str(required=True, allow_none=True)
    expires_at = fields.Int(required=True, allow_none=True)
    expires_in = fields.Int(required=True, allow_none=True)
    id_token = fields.Str(required=True, allow_none=True)
    scope = fields.Str(required=True, allow_none=True)
    token_type = fields.Str(required=True, allow_none=True)
    userinfo = fields.Nested(UserInfoSchema, allow_none=True)
    
    # Allow additional fields in the input
    class Meta:
        unknown = INCLUDE

    @post_load
    def return_google_user(self, data, **kwargs):
        return GoogleUser(**data)
    

