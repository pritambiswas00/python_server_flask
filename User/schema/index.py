from Database.db import db

# Define the CountryCode model
class CountryCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(30), nullable=False, unique=True)
    users = db.relationship('User', backref='country', lazy=True)

    def __repr__(self):
        return f"<{self.code} {self.name}>"
    
# Association table for the many-to-many relationship between users and groups
class UserGroup(db.Model):
    __tablename__ = 'user_group'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True) 
    
# Define the Group model
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    tasks = db.relationship("Task", backref="group", lazy=True)
    users = db.relationship("User", secondary="user_group")

    def __repr__(self):
        return f"<Group {self.name}>"

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    phone_number = db.Column(db.String(10), nullable=True)
    country_code_id = db.Column(db.Integer, db.ForeignKey('country_code.id'), nullable=True)  # Foreign key
    completed = db.Column(db.Boolean, default=False)

    # Relationship with CountryCode
    country_code = db.relationship('CountryCode', backref='users', lazy=True)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "country_code": self.country_code.name if self.country_code else None,
            "completed": self.completed
        }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "country_code": self.country_code.name if self.country_code else None,
            "completed": self.completed
        }

    def to_edit(self, data):
        if data.name is not None:
            self.name = data.name
        if data.email is not None:
            self.email = data.email
        if data.phone_number is not None:
            self.phone_number = data.phone_number
        if data.completed is not None:
            self.completed = data.completed
