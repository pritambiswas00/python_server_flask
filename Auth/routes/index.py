from flask import Blueprint, url_for, jsonify, session
from marshmallow import ValidationError
from Auth.provider.google.index import oauth
from Auth.provider.google.types import GoogleUser, GoogleUserSchema

auth_route_blueprint = Blueprint("routes", __name__)

##Google Login User
@auth_route_blueprint.get("/auth/google/login")
def login():
   return oauth.google.authorize_redirect(redirect_uri=url_for("routes.authorize", _external=True))
   
        
        
        
        
##Google Callback User
@auth_route_blueprint.get("/auth/google/callback")
def authorize():
   try:
    token = oauth.google.authorize_access_token()
    validated_google_user:GoogleUser = GoogleUserSchema().load(token)
    
    
    print(f"{validated_google_user.to_json()}")
    session['user'] = token['userinfo']
    return jsonify(token)
   except ValidationError as error:
        return jsonify({"error": error.messages}), 400
   except Exception as e:
        return jsonify({"error": str(e)}), 500
   
      