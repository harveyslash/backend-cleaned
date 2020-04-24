from jsonschema.validators import validates

from Sugar import Dictifiable
from extensions import db


class QuestionAllowedLanguages(Dictifiable, db.Model):
    language_id = db.Column(db.Integer(),
                            db.ForeignKey('coding_language.id'),
                            primary_key=True)

    question_id = db.Column(db.Integer(),
                            db.ForeignKey('question.id'),
                            primary_key=True)

    question = db.relationship('Question',
                               backref='question_allowed_languages')
