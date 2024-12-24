from Database.db import db

# Define the Todo model inside the schema module
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)

    def __repr__(self):
        return f"<ToDo {self.title}>"

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
    }
        
    def to_dict(self):
        return {
        "id": self.id,
        "title": self.title,
        "description": self.description,
        "completed": self.completed
    }
        
    def to_edit(self, data):
        print(f"{data} What's up im data")
        if data.title is not None:
            self.title = data.title
        if data.description is not None:
            self.description = data.description
        if data.completed is not None:
            self.completed = data.completed