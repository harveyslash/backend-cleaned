from sqlalchemy.orm import validates

from Sugar import Dictifiable
from extensions import db


class Tag(Dictifiable, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(256), unique=True)

    questions = db.relationship('Question',
                                secondary='question_tags')

    @validates('name')
    def convert_upper(self, key, value):
        return value.lower()

    def __str__(self):
        return self.name
