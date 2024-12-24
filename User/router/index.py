from flask import Blueprint, jsonify, request
from ToDo.service.index import add_todo_to_db , all_todos, update_todos, delete_todos
from ToDo.schema.index import Todo
from ToDo.validation.index import CreateToDoPayload, TodoSchema, UpdateTodoSchema, UpdateTodoPayload
from apiflask.validators import ValidationError

user_route_blueprint = Blueprint("routes", __name__)
todo_schema = Todo()

##Create new ToDo
@user_route_blueprint.post("/user/create")
def create_todo():
    
    ##Converting the Request to Body to Dictionary
    req_body = request.json
    try:
        
        ## Validating if the Request Body is Valid based on the Schema provided
        validated_req_body: CreateToDoPayload = TodoSchema().load(req_body)
        
        ##Passing the Parsed Data to the create task to create the task in the DB Return a Monad Result type
        result = add_todo_to_db(validated_req_body)
        
        if result.is_err():
            return jsonify({ "error": f"{result.unwrap_err()._message()}"})
        return jsonify({ "data": result.unwrap().to_json(), "message": "Successfully created the Task" }), 201
    except ValidationError as error:
        return jsonify({"error": f"Error- {error.messages}"}), 400
    
    
##Edit todo
@user_route_blueprint.patch("/user/update/<int:id>")
def edit_todo(id):
    req_body = request.json
    req_body["id"] = id
    print(f"{req_body} -->Request Body")
    try:
       validated_req_body: UpdateTodoPayload = UpdateTodoSchema().load(req_body)
       result = update_todos(validated_req_body)
       if result.is_err():
            return jsonify({ "error": f"{result.unwrap_err()._message()}"}), 404
       return jsonify({ "data": result.unwrap().to_json(), "message": "Successfully edited the Task" }), 200
    except ValidationError as error:
         return jsonify({"error": f"{error.messages}"}), 400   


##Delete Todo
@user_route_blueprint.delete("/user/delete/<int:id>")
def delete_todo(id):
     result = delete_todos(id)
     if result.is_err():
         return jsonify({ "error": f"Error : {result.unwrap_err()._message}" }), 400
     return jsonify({"data": result.unwrap().to_json(), "message": "Successfully deleted todo"}), 200