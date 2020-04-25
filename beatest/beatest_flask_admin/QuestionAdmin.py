from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_admin.model.form import InlineFormAdmin
from wtforms.fields import DecimalField, TextAreaField
from wtforms.validators import AnyOf, InputRequired, NumberRange

from extensions import db
from models import Choice, CodingCase, Section, Tag
from .helpers import BaseAdminView, CKTextAreaField


class ChoicesInlineForm(InlineFormAdmin):
    form_columns = ('id', 'html', 'is_correct')
    form_overrides = dict(html=CKTextAreaField)
    form_rules = ('html', 'is_correct')

    create_template = 'edit.html'
    edit_template = 'edit.html'


class CodingCasesInlineForm(InlineFormAdmin):
    form_columns = ('id',
    'input',
    'right_output',
    'points_correct',
    'points_wrong',
    'viewable_with_solution',
    'viewable_with_question')

    form_overrides = dict(input=TextAreaField, right_output=TextAreaField)
    form_rules = ('input', 'right_output', "points_correct", 'points_wrong',
    'viewable_with_question', 'viewable_with_solution')

    create_template = 'edit.html'
    edit_template = 'edit.html'

    form_args = {
        'points_wrong': {
            'validators': [NumberRange(min=0)]
        },
    }


class QuestionAdmin(BaseAdminView):
    # def is_visible(self):
    #     return False

    column_list = ['id', 'type', 'lod', 'topic', 'tags']

    column_searchable_list = ['type', 'lod', 'topic']
    column_filters = ['type', 'lod', 'topic', 'tags']
    column_editable_list = ['type']

    form_edit_rules = [
        'type', 'lod', 'topic', 'tags', 'points_correct', 'points_wrong',
        'sections',
        'tita_answer', 'html',
        'rc_passage',
        'choices',
        'coding_cases',
        'allowed_languages',
        'logic'
    ]

    form_ajax_refs = {
        'sections': QueryAjaxModelLoader('sections', db.session, Section,
                                         fields=['name'], page_size=10),

        'tags': QueryAjaxModelLoader('tags', db.session, Tag,
                                     fields=['name'], page_size=10)
    }

    form_create_rules = form_edit_rules

    form_overrides = dict(html=CKTextAreaField, rc_passage=CKTextAreaField,
                          logic=CKTextAreaField)
    inline_models = (
        ChoicesInlineForm(Choice), CodingCasesInlineForm(CodingCase))

    form_choices = {
        'type': [
            ('RC', 'RC'),
            ('MCQ', 'MCQ'),
            ('TITA', 'TITA'),
            ('CODING', 'CODING'),
            ('SUBJECTIVE', 'SUBJECTIVE')
        ],

        'lod': [
            ('Easy', 'Easy'),
            ('Medium', 'Medium'),
            ('Difficult', 'Difficult')
        ],

        'topic': [
            ("Simplifications", "Simplifications"),
            ("Compound & Simple Interest", "Compound & Simple Interest"),
            ("Ratio and Proportion", "Ratio and Proportion"),
            ("Probability", "Probability"),
            ("Time,Speed,Distance & Work", "Time,Speed,Distance & Work"),
            ("Number System", "Number System"),
            ("Algebra", "Algebra"),
            ("Geometry", "Geometry"),
            ("Mensuration", "Mensuration"),
            ("Percentage", "Percentage"),
            ("Quadratic Equation", "Quadratic Equation"),
            ("Profit/Loss/Discount", "Profit/Loss/Discount"),
            ("Mixtures and Alligation", "Mixtures and Alligation"),
            ("Inequalities", "Inequalities"),
            ("Permutation & Combination", "Permutation & Combination"),
            ("Logarithms", "Logarithms"),
            ("Ages", "Ages"),
            ("Investments andShares", "Investments andShares"),
            ("Bar Graph", "Bar Graph"),
            ("Line Graph", "Line Graph"),
            ("Tables", "Tables"),
            ("PieChart", "PieChart"),
            ("Number Series", "Number Series"),
            ("Seating Arrangement", "Seating Arrangement"),
            ("Puzzles", "Puzzles"),
            ("Input Output", "Input Output"),
            (" Coding Decoding", " Coding Decoding"),
            ("Visual Puzzle", "Visual Puzzle"),
            ("Reading Comprehension", "Reading Comprehension"),
            ("Parajumbles", "Parajumbles"),
            ("Para  Completion", "Para  Completion"),
            ("Summary Based Question", "Summary Based Question"),
            ("Sentence error correction", "Sentence error correction"),
            ("Verbal Ability", "Verbal Ability"),
            ("Cloze Test", "Cloze Test"),
            ("Syllogisms", "Syllogisms"),
            ("Fill in the blanks", "Fill in the blanks"),
            ("Odd one out", "Odd one out"),
            ("Verbal Reasoning", "Verbal Reasoning"),
            ("Synoyms", "Synoyms"),
            ("Antonyms", "Antonyms"),
            ("Operating Systems", "Operating Systems"),
            ("C Programming", "C Programming"),
            ("Array", "Array"),
            ("Linkedlist", "Linkedlist"),
            ("Data Structures", "Data Structures"),
            ("DBMS", "DBMS"),
            ("Output", "Output")

        ]
    }
    form_args = {
        'type': {
            'validators': [InputRequired(),
                AnyOf(['RC', 'MCQ', 'TITA', "CODING", "SUBJECTIVE"])]
        },
        'points_correct': {
            'validators': [InputRequired(), DecimalField]
        },
        'points_wrong': {
            'validators': [InputRequired(), DecimalField]
        },
        'lod': {
            'validators': [InputRequired(),
                AnyOf(["Easy", "Medium", "Difficult"])]

        }
    }
