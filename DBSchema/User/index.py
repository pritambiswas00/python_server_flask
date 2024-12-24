from Database.db import db


# Define the User model
class User(db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    phone_number = db.Column(db.String(10), nullable=True)
    country_code_id = db.Column(db.Integer, db.ForeignKey("country_code.id", ondelete="SET NULL"))
    session_id = db.Column(db.Integer, db.ForeignKey("google_sessions.id", ondelete="CASCADE"))
    todos = db.relationship("Todo", backref="user", lazy=True)
    sessions = db.relationship("GoogleSession", backref="user", lazy=True)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "country_code": self.country_code.name if self.country_code else None,
        }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "country_code": self.country_code.name if self.country_code else None,
        }

    def to_edit(self, data):
        if data.name is not None:
            self.name = data.name
        if data.email is not None:
            self.email = data.email
        if data.phone_number is not None:
            self.phone_number = data.phone_number