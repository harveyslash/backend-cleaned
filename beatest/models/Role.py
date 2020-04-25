from Sugar import Dictifiable
from extensions import db


class Role(Dictifiable, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    users = db.relationship('User',
                            secondary='user_roles')

    def __str__(self):
        return self.name
