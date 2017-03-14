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
    stu_num = StringField('学号', validators=[DataRequired(), Length(min=7, max=12)])
    password = StringField('密码', validators=[DataRequired()])
    submit = SubmitField('提交')

class SignupForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(), Length(min=2, max=8)])
    stu_num = StringField('学号',validators=[DataRequired(), Length(min=7, max=12)])
    # email = StringField('邮箱', validators=[DataRequired(), Length(min=5, max=35), Email()])
    password = PasswordField('密码', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('确认密码')
    phone_number = StringField('手机号',validators=[DataRequired(), Length(min=8, max=11)])
    code = StringField('验证码',validators=[DataRequired(), Length(min=4, max=8)])
    # submit = SubmitField('提交')

class PaperCreateForm(FlaskForm):
    paper_title = StringField('问卷名称', validators=[Required()])
    question_num = IntegerField('问题数量',validators=[NumberRange(min=1,max=30)])
    # paper_description = StringField('问卷描述',validators=[DataRequired()])
    # paper_deadline = DateField('截止日期',validators=[DataRequired()])
    submit = SubmitField('提交')

class QuestionCreateForm(FlaskForm):
    question_content = StringField('题干',validators=[Required()])
