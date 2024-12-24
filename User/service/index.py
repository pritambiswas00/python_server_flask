from ToDo.schema.index import Todo
from typing import List, Union
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from Database.db import db
from utils.index import Result
from ToDo.validation.index import CreateToDoPayload, UpdateTodoPayload

    
##Post to create task
def add_todo_to_db(payload:CreateToDoPayload) -> Result[Todo, SQLAlchemyError] :
    try:
        new_task = Todo(            
            title=payload.title,
            description=payload.description,
            completed=payload.completed,
            )
        db.session.add(new_task)
        db.session.commit()
        return Result.Ok(new_task)
    except SQLAlchemyError as error:
        # Handle database errors
        db.session.rollback()
        return Result.Err(error=error)
 
 
 
##GET all tasks
def all_todos() -> Result[List[Todo], SQLAlchemyError]:
    try:
         todos = Todo.query.all()
         return Result.Ok(value=todos)
    except SQLAlchemyError as error:
         return Result.Err(error=error)  
     
     
##Edit todos
def update_todos(payload:UpdateTodoPayload)->Result[Todo, SQLAlchemyError]:
    try:
        is_todo_exist: Union[Todo, None] = Todo.query.filter_by(id=payload.id).first()
        if is_todo_exist is None:
            return Result.Err(error=SQLAlchemyError(f"Couldn't find todo"))
        db.session.query(Todo).\
        filter(Todo.id == is_todo_exist.id).\
        update(payload.to_dict())
        db.session.commit()
        return Result.Ok(is_todo_exist)
    except SQLAlchemyError as error:
        db.session.rollback()
        return Result.Err(error)


##Delete todos
def delete_todos(id:int)->Result[Todo, SQLAlchemyError]:
    try:
        is_todo_exist: Union[Todo, None] = Todo.query.filter_by(id=id).first()
        if is_todo_exist is None:
            return Result.Err(error=SQLAlchemyError(f"Couldn't find todo"))
        db.session.query(Todo).\
        filter(Todo.id == is_todo_exist.id).\
        delete()
        db.session.commit()
        return Result.Ok(is_todo_exist)
    except SQLAlchemyError as error:
        db.session.rollback()
        return Result.Err(error) 