from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length

class CreateUserForm(FlaskForm): #give option to create groups - make a null value key pair if not 
    first_name = StringField('First Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired()])
    phone_number = StringField('Phone Number',
                            validators=[DataRequired()])
    channel_group = SelectMultipleField("Add user to existing groups (optional)")
    submit = SubmitField('Submit user')

class DeleteUserForm(FlaskForm): #corresponding route needs to remove user from db
    first_name = StringField('First Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Permanently delete user')

class AddUserForm(FlaskForm): 
    first_name = StringField('First Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Add user')

class RemoveUserForm(FlaskForm): 
    first_name = StringField('First Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Remove user')

class CreateGroup(FlaskForm):
    group_name = StringField('Group Name',
                            validators=[DataRequired(), Length(min=2, max=30)])
    group_desc = TextAreaField('Group Description',
                            validators=[DataRequired(), Length(min=2, max=250)])
    group_add_existing = SelectMultipleField('Add existing user/s', 
                            choices=[], validate_choice=False) #UGH FINISH THIS
    submit = SubmitField('Create group')


class EditGroup(FlaskForm):
    group_name = StringField('Group Name',
                            validators=[DataRequired(), Length(min=2, max=30)])
    group_desc = TextAreaField('Group Description',
                            validators=[DataRequired(), Length(min=2, max=250)])
    submit = SubmitField('Submit changes')
 
class SendMessage(FlaskForm): 
    message_body = TextAreaField('Message Body',
                            validators=[DataRequired()])
    message_name = StringField('Message Title')
    submit = SubmitField('Send message')