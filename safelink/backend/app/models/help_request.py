from app import db

class HelpRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(128))
    description = db.Column(db.Text)
    status = db.Column(db.String(32), default='open')
    created_at = db.Column(db.DateTime) 