"""
WTForms form definitions for Aursikho.
Handles validation and CSRF protection for all user-facing forms.
"""
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SelectField, TextAreaField,
                     IntegerField, BooleanField, SubmitField)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, NumberRange
from app.models import User


class LoginForm(FlaskForm):
    """User login form."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    """User registration form with role selection."""
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=128)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    role = SelectField('I am a', choices=[('student', 'Student'), ('instructor', 'Instructor')],
                       validators=[DataRequired()])
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('An account with this email already exists.')


class CourseForm(FlaskForm):
    """Form for creating and editing courses."""
    title = StringField('Course Title', validators=[DataRequired(), Length(max=200)])
    short_description = StringField('Short Description (shown on cards)',
                                    validators=[Optional(), Length(max=300)])
    description = TextAreaField('Full Description', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Programming', 'Programming'),
        ('Web Development', 'Web Development'),
        ('Data Science', 'Data Science'),
        ('Machine Learning', 'Machine Learning'),
        ('Mobile Development', 'Mobile Development'),
        ('Database', 'Database'),
        ('DevOps', 'DevOps'),
        ('Cyber Security', 'Cyber Security'),
        ('Design', 'Design'),
        ('Business', 'Business'),
        ('Other', 'Other'),
    ], validators=[DataRequired()])
    difficulty = SelectField('Difficulty', choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ], validators=[DataRequired()])
    submit = SubmitField('Save Course')


class LessonForm(FlaskForm):
    """Form for creating and editing lessons."""
    title = StringField('Lesson Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Lesson Content / Description', validators=[Optional()])
    video_url = StringField('YouTube Video URL', validators=[Optional(), Length(max=500)])
    lesson_type = SelectField('Lesson Type', choices=[
        ('video', 'Video Lesson'),
        ('text', 'Text Lesson'),
        ('hybrid', 'Hybrid Lesson (Video + Text)'),
    ], validators=[DataRequired()])
    duration_minutes = IntegerField('Duration (minutes)', validators=[Optional(), NumberRange(min=1, max=600)])
    submit = SubmitField('Save Lesson')


class QuizForm(FlaskForm):
    """Form for creating a quiz."""
    title = StringField('Quiz Title', validators=[DataRequired(), Length(max=200)])
    passing_score = IntegerField('Passing Score (%)',
                                 validators=[DataRequired(), NumberRange(min=1, max=100)],
                                 default=60)
    submit = SubmitField('Save Quiz')


class QuizQuestionForm(FlaskForm):
    """Form for adding a question to a quiz."""
    question_text = TextAreaField('Question', validators=[DataRequired()])
    option_a = StringField('Option A', validators=[DataRequired(), Length(max=300)])
    option_b = StringField('Option B', validators=[DataRequired(), Length(max=300)])
    option_c = StringField('Option C', validators=[DataRequired(), Length(max=300)])
    option_d = StringField('Option D', validators=[DataRequired(), Length(max=300)])
    correct_answer = SelectField('Correct Answer', choices=[
        ('a', 'Option A'),
        ('b', 'Option B'),
        ('c', 'Option C'),
        ('d', 'Option D'),
    ], validators=[DataRequired()])
    submit = SubmitField('Add Question')
