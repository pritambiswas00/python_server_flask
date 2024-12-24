from Database.db import db
from datetime import datetime

##User Google Session Data Model
class GoogleSession(db.Model):
    __tablename__ = "google_sessions"
    id = db.Column(db.Integer, primary_key=True)
    session_key = db.Column(db.String(255), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    access_token = db.Column(db.String(), nullable=False)
    expires_at = db.Column(db.Integer, nullable=False)
    expires_in = db.Column(db.Integer, nullable=False)
    id_token = db.Column(db.Text, nullable=False)
    scope = db.Column(db.Text, nullable=False)
    token_type = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<GoogleSession {self.id}>"
    
    def is_valid(self):
        """Check if the session is still valid."""
        current_time = datetime.utcnow().timestamp()  # Get current time as a UNIX timestamp
        return current_time < self.expires_at