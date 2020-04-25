from jsonschema.validators import validates

from Sugar import Dictifiable
from extensions import db


class QuestionTags(Dictifiable, db.Model):
    question_id = db.Column(db.Integer(),
                            db.ForeignKey('question.id', ondelete='CASCADE'),
                            primary_key=True)
    tag_id = db.Column(db.Integer(),
                       db.ForeignKey('tag.id', ondelete='CASCADE'),
                       primary_key=True)

    question = db.relationship('Question', backref='question_tags')
    tag = db.relationship('Tag', backref='question_tags')
