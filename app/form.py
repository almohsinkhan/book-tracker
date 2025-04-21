from flask_wtf import FlaskForm # type: ignore
from wtforms import StringField, IntegerField, SelectField, TextAreaField, HiddenField # type: ignore
from wtforms.validators import DataRequired, NumberRange # type: ignore

# WTForms
class BookForm(FlaskForm):
    user_id      = HiddenField('User ID', validators=[DataRequired()])
    title        = StringField('Title', validators=[DataRequired()])
    author       = StringField('Author', validators=[DataRequired()])
    current_page = IntegerField('Current Page', validators=[DataRequired(), NumberRange(min=0)])
    status       = SelectField('Status', choices=[('want to read', 'Want To Read'),('reading','Reading'),('completed','Completed')], validators=[DataRequired()])
    notes        = TextAreaField('Notes')

class UpdateBookForm(FlaskForm):
    current_page = IntegerField('Current Page', validators=[NumberRange(min=0)])
    status       = SelectField('Status', choices=[('reading','Reading'),('completed','Completed')])
    notes        = TextAreaField('Notes')
