from Database.db import db

# Define the CountryCode model
class CountryCode(db.Model):
    __tablename__ = "country_code"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(30), nullable=False, unique=True)

    def __repr__(self):
        return f"<{self.code} {self.name}>"


# Association table for the many-to-many relationship between users and groups
class UserGroup(db.Model):
    __tablename__ = "user_group"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True, index=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), primary_key=True, index=True)


# Define the Group model
class Group(db.Model):
    __tablename__ = "group"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    todos = db.relationship("Todo", backref="group", lazy=True)
    users = db.relationship("User", secondary="user_group")

    def __repr__(self):
        return f"<Group {self.name}>"