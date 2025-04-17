from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import BooleanField, DateField, FileField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class EventForm(FlaskForm):
    name = StringField("Event Name", validators=[DataRequired(), Length(min=2, max=200)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=10)])
    date = DateField("Date", format="%Y-%m-%d", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired(), Length(min=2, max=100)])
    is_public = BooleanField("Make Event Public", default=False)
    image = FileField("Event Image (Optional)", validators=[FileAllowed(["jpg", "png"], "Images only!")])
    submit = SubmitField("Create Event")


class EventDeleteForm(FlaskForm):
    id = StringField("Event ID", validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    event_id = StringField("Event ID", validators=[DataRequired()])
    submit = SubmitField("Register")
