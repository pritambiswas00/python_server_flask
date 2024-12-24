from flask import Flask
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth, LocalProxy
from Config.index import load_configuration
from Auth.provider.google.index import oauth
from Database.db import db
from Auth.routes.index import auth_route_blueprint

def create_app():
    app = Flask(__name__)
    CORS(app)
    result = load_configuration()
    if result.is_err():
        raise ValueError(f"Configuration error: {result.unwrap_err().messages}")

    ##Validated Configuration
    config = result.unwrap()

    # Configuring the database
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = config.APP_SECRET_KEY

    
    ## Initialize SQLAlchemy
    db.init_app(app)
    oauth.init_app(app)
    oauth.register(
        'google',
        client_id=config.GOOGLE_CLIENT_ID,
        client_secret=config.GOOGLE_CLIENT_SECRET,
        server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    
    # Ensure the database tables are created
    with app.app_context():
        db.create_all()
        
        

    # Register routes
    
    app.register_blueprint(auth_route_blueprint, url_prefix="/api")
    

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
