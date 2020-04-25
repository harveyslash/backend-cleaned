from Sugar import Dictifiable
from extensions import db


class UserRoles(Dictifiable, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

    user = db.relationship('User', backref='user_roles')
    role = db.relationship('Role', backref='user_roles')
