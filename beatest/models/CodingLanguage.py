from sqlalchemy.orm import validates

from Sugar import Dictifiable
from extensions import db


class CodingLanguage(Dictifiable, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(256), unique=True)

    def __str__(self):
        return self.name
