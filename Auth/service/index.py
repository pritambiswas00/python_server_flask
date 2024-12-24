from User.validation.index import CreateUser
from DBSchema.User.index import User
from DBSchema.Auth.index import GoogleSession
from Database.db import db
from utils.index import Result
from sqlalchemy.exc import SQLAlchemyError
from typing import Union


def create_or_get_user(payload:CreateUser, session_id:Union[int, None]) -> Result[User, SQLAlchemyError]:
    try:
        user:Union[User, None] = User.query.filter_by(email=payload.email).first()
        if user is None:
            user = User(
                name = payload.name,
                email = payload.email,
                phone_number = payload.phone_number,
                country_code_id = payload.country_code_id,
                session_id = session_id,  
            )
            db.session.add(user)
            db.session.commit()
            return Result.Ok(user)
        return Result.Ok(user)
    except SQLAlchemyError as error:
        # Handle database errors
        db.session.rollback()
        return Result.Err(error=error)
    
    
def get_google_session(session_key:str)->Result[GoogleSession, SQLAlchemyError]:
    try:
        session:Union[GoogleSession, None] = GoogleSession.query.filter_by(session_key=session_key).first()
        if session is None:
            return Result.Err(SQLAlchemyError("Couldn't find the session"))
        return Result.Ok(session)
    except SQLAlchemyError as error:
        return Result.Err(error=error)
             
            
        