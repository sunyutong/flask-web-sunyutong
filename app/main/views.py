from flask import render_template, session, redirect, url_for
from datetime import datetime
from flask import request                       #上下文
from flask import flash                         #提示用户表单输入有误
from flask import make_response
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField,SubmitField,IntegerField,DateField,TextAreaField
from wtforms.validators import Email, Length, EqualTo, DataRequired,Required,NumberRange

from ..func import sms

from . import main
from .forms import NameForm,LoginForm,SignupForm,PaperCreateForm,QuestionCreateForm
from .. import db
from ..models import User,Paper,Question,Select,Answer

@main.before_request                        #注册一个函数，在每次请求之前运行
def check_user_status():
    if 'user_num' not in session:
        session['user_num'] = None
        session['user_name'] = None



@main.route('/',methods=['GET', 'POST'])
def index():								#该视图函数要渲染表单，也要接收表单中的数据
    form = NameForm()
    if form.validate_on_submit():		#如果数据能被所有验证函数接受，即Required()通过验证，返回True
        user=User.query.filter_by(name=form.name.data).first()
        if user is None:
            flash('please signup first!')
            return redirect(url_for('main.signup'))
        else:
            flash('Hello,please login!')
            return redirect(url_for('main.login'))
    return render_template('index.html',current_time=datetime.utcnow(), form=form, user=session.get('user_name'))


@main.route('/login',methods=['GET', 'POST'])
def login():
    if session['user_num']:
        flash('you have been logged')
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(stu_num=form.stu_num.data).first()
        if user is not None and user.check_password(form.password.data):
            session['user_num'] = form.stu_num.data
            session['user_name'] = user.name
            flash('Thanks for logging in')
            return redirect(url_for('main.index'))
        else:
            flash('Sorry! no user exists with this student number and password')
            return render_template('login.html',form=form)
    return render_template('login.html',form=form)

@main.route('/signup', methods=('GET', 'POST'))
def signup():

    if session['user_num']:
        flash('you are already signed up')
        return redirect(url_for('main.index'))
        
    form = SignupForm()
    if request.method == 'GET':
    # 获取 GET 请求参数
        phone_number = request.args.get('mobile_phone_number')
        if phone_number is not None:
            if sms.send_message(phone_number):
                return render_template('signup.html',form=form)
            else:
                flash('获取验证码失败！')
    elif request.method == 'POST':
        if form.validate_on_submit():
            user_num = User.query.filter_by(stu_num=form.stu_num.data).first()
            if user_num is None:
                phone_number = form.phone_number.data
                code =form.code.data
                if code == '':
                    flash('请输入验证码！')
                elif sms.verify(phone_number, code):
                    name = form.name.data
                    stu_num = form.stu_num.data
                    password = form.password.data
                    user = User(name,stu_num,phone_number,password)
                    db.session.add(user)
                    db.session.commit()
                    session['user_num']=stu_num
                    session['user_name']=name
                    flash("注册成功！")
                    return redirect(url_for('main.index'))
                else:
                    flash('验证码有误，请重新输入！')
                    return render_template('signup.html', form=form)
            else:
                flash("该学号已经注册！", 'error')
                return render_template('signup.html', form=form)
        else:
            flash("请输入正确信息")
            return render_template('signup.html', form=form)
    return render_template('signup.html',form=form)
    
    

@main.route('/logout', methods=('GET', 'POST'))
def logout():
    session.pop('user_num', None)
    session.pop('user_name', None)
    flash("You were successfully logged out")
    return redirect(request.referrer or url_for('main.index'))


@main.route('/createpaper', methods=('GET', 'POST'))
def createpaper():
    if session['user_num'] is None:
        flash('please login')
        return redirect(url_for('main.login'))
    user=User.query.filter_by(stu_num=session.get('user_num')).first()
    form = PaperCreateForm()
    if form.validate_on_submit():
        paper_title = Paper.query.filter_by(paper_title=form.paper_title.data).first()
        if paper_title is None:
            paper = Paper(paper_title=form.paper_title.data,question_num=form.question_num.data,author=user)
            db.session.add(paper)
            db.session.commit()
            session['paper_title'] = form.paper_title.data			
            return redirect(url_for('main.createquestion'))
        else:
            flash("A paper already exists.")
            return render_template('create-paper.html',form=form)
    return render_template('create-paper.html',form=form)



@main.route('/createpaper/createquestion',methods=('GET','POST'))
def createquestion():
    if session['user_num'] is None:
        flash('please login')
        return redirect(url_for('main.login'))

    paper = Paper.query.filter_by(paper_title = session.get('paper_title')).first()
    
    
    class DynamicQuestionForm(FlaskForm):
        pass


    for i in range(0,paper.question_num):
        
        setattr(DynamicQuestionForm,'form'+str(i),TextAreaField('题干'+str(i+1),validators=[Required()]))
    setattr(DynamicQuestionForm,'submit',SubmitField('提交'))
    

    form = DynamicQuestionForm()


    question=[]
    form_data=[]
    # flash(attr[0])
    if form.validate_on_submit():
        for i in range(paper.question_num):

            
            form_data.append(form.form0.data)
            flash(form.form0.data)
            a=getattr(DynamicQuestionForm,'form'+str(i))
            flash(a)
            question.append(Question(paper_id=paper.id,question_content = form_data[i]))
            db.session.add(question[i])
            db.session.commit()
            flash("创建完成")
        flash("2")
    flash(form.validate_on_submit())
    flash(form.errors)

    return render_template('create-question.html',paper_title=paper.paper_title,question_num=paper.question_num,form=form)


