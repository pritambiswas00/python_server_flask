from dotenv import load_dotenv
from marshmallow import Schema, fields, validate
from apiflask.validators import ValidationError
from dataclasses import dataclass, asdict
from utils.index import Result
import os

# Load environment variables from the .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Define the Configuration data class
@dataclass
class Configuration:
    PORT: int
    SQLALCHEMY_DATABASE_URI: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_SCOPE: str
    APP_SECRET_KEY: str


# Schema to validate and load configuration values
class ConfigurationSchema(Schema):
    PORT = fields.Integer(required=True, validate=validate.Range(min=1024, max=65535))
    SQLALCHEMY_DATABASE_URI = fields.String(required=True)
    GOOGLE_CLIENT=fields.Boolean(required=False, Default=False)
    GOOGLE_CLIENT_ID = fields.String(required=True)
    GOOGLE_CLIENT_SECRET = fields.String(required=True)
    GOOGLE_SCOPE = fields.String(required=True)
    APP_SECRET_KEY=fields.String(required=True)
    
    
    def to_dict(self) -> dict:
        return {key: value for key, value in asdict(self).items() if value is not None}

# Function to load configuration from environment variables using the schema
def load_configuration()->Result[Configuration, ValidationError]:
    # Retrieve environment variables
    try: 
        config_data = {
            "PORT": int(os.getenv("PORT", None)),
            "SQLALCHEMY_DATABASE_URI": os.getenv("SQLALCHEMY_DATABASE_URI", None),
            "GOOGLE_CLIENT_ID": os.getenv("GOOGLE_CLIENT_ID", None),
            "GOOGLE_CLIENT_SECRET": os.getenv("GOOGLE_CLIENT_SECRET", None),
            "GOOGLE_SCOPE": os.getenv("GOOGLE_SCOPE",None),
            "APP_SECRET_KEY": os.getenv('APP_SECRET_KEY', "")
        }
        print(f"{config_data}")
        # Validate and load the configuration using the schema
        schema = ConfigurationSchema()
        result = schema.load(config_data)

        # Return the valid configuration as a Configuration object
        return Result.Ok(value=Configuration(**result))
    except ValidationError as error:
        return Result.Err(error=error)
