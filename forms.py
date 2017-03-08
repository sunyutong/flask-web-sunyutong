from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField,SubmitField,IntegerField,DateField
from wtforms.validators import Email, Length, EqualTo, DataRequired,Required,NumberRange



class NameForm(FlaskForm):					#创建一个继承Form表单的表单，Form是表单的始祖
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
    '''StringField类表示属性为type="text"的input元素。
       SubmitField类表示属性为type="submit"的input元素。（表单中StringField等类见书P35）
       第二个变量进行验证，required()函数确保字段中有数据'''	

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = StringField('password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(min=5, max=35), Email()])
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Submit')

class PaperCreateForm(FlaskForm):
    paper_title = StringField('问卷名称', validators=[Required()])
    question_num = IntegerField('问题数量',validators=[NumberRange(min=1,max=30)])
    # paper_description = StringField('问卷描述',validators=[DataRequired()])
    # paper_deadline = DateField('截止日期',validators=[DataRequired()])
    submit = SubmitField('Submit')