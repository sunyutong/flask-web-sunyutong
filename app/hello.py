# import os
# from func import sms
# from flask import Flask
# from flask import session 						#用户会话
# from flask import redirect						#重定向
# from flask import url_for						#生成URL 使用URL映射生成URL，修改路由名字依然可用
# from flask import flash 						#提示用户表单输入有误
# from flask import render_template 				#渲染模板
# from flask import request 						#上下文
# from flask import make_response 				#
# from flask_script import Manager	 			#解析指令行
# from flask_script import Shell 					#让flask的shell命令自动导入特定的对象
# from flask_bootstrap import Bootstrap 			#前端模板
# from flask_moment import Moment 				#本地化日期和时间

# from werkzeug import generate_password_hash, check_password_hash
#                                                 #登陆密码的加解密

# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy 		#数据库
# from sqlalchemy import Column,Integer,String,ForeignKey


# from flask_debugtoolbar import DebugToolbarExtension   #Debug导航栏
# from forms import SignupForm, LoginForm,NameForm,PaperCreateForm       #从forms.py中导入所有表单

# from flask_wtf import FlaskForm
# from wtforms import PasswordField, StringField,SubmitField,IntegerField,DateField,TextAreaField
# from wtforms.validators import Email, Length, EqualTo, DataRequired,Required,NumberRange



#让Script的Shell命令自动导入app,db,User对象
# def make_shell_context():
# 	return dict(app=app,db=db,User=User,Paper=Paper,Question=Question)



# app = Flask(__name__)					#创建一个Python实例
# manager=Manager(app)					#初始化主类的实例
# bootstrap=Bootstrap(app)
# moment=Moment(app)						#初始化Moment实例
# toolbar=DebugToolbarExtension(app)      #初始化debugtoolbar实例

# app.config['SECRET_KEY'] = '123qwe'
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
# db = SQLAlchemy(app)





# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30))
#     stu_num = db.Column(db.String(12))
#     phone_num = db.Column(db.String(11))
#     password = db.Column(db.String(30))
#     papers = db.relationship('Paper',backref='author', lazy='dynamic')

#     def __init__(self, name, stu_num,phone_num, password):
#         self.name = name
#         self.stu_num = stu_num
#         self.phone_num = phone_num
#         self.set_password(password)

#     def set_password(self, password):
#         self.password = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password, password)

#     def __repr__(self):                 #__repr__返回一个具有可读性的字符串表示模型，调试和测试中使用
#         return '<User %r>' % self.name


# class Paper(db.Model):
#     __tablename__ = 'paper'
#     id = db.Column(db.Integer, primary_key=True)
#     paper_title = db.Column(db.String(30))
#     question_num = db.Column(db.Integer)
#     user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
#     questions = db.relationship('Question',backref='survey',lazy='dynamic')

#     # paper_description = db.Column(db.String(120))
#     # paper_deadline = db.Column(db.String(60))       #有待调整

#     # def __init__(self, paper_title,question_num,user_id):
#     #     self.paper_title = paper_title
#     #     # self.question_num = question_num
#     #     self.user_id = User.id

#     def __repr__(self):                 #__repr__返回一个具有可读性的字符串表示模型，调试和测试中使用
#         return '<Paper %r>' % self.paper_title


# class Question(db.Model):
#     __tablename__ = 'question'
#     id = db.Column(db.Integer, primary_key=True)
#     question_content = db.Column(db.String(240), default='none')
#     paper_id = db.Column(db.Integer,db.ForeignKey('paper.id'))
#     selects = db.relationship('Select',backref='stem', lazy='dynamic')

#     def __init__(self, paper_id,question_content):
#         self.question_content = question_content
#         self.paper_id = paper_id



#     def __repr__(self):                 #__repr__返回一个具有可读性的字符串表示模型，调试和测试中使用
#         return '<Question %r>' % self.question_content


# class Select(db.Model):
#     __tablename__ = 'select'
#     id = db.Column(db.Integer, primary_key=True)
#     question_id = db.Column(db.Integer,ForeignKey('question.id'))
#     select_content = db.Column(db.String(60))
#     def __repr__(self):                 #__repr__返回一个具有可读性的字符串表示模型，调试和测试中使用
#         return '<Select %r>' % self.id


# class Answer(db.Model):
#     __tablename__ = 'answer'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer,ForeignKey('user.id'))
#     question_id = db.Column(db.Integer,ForeignKey('question.id'))
#     #user.id 外键 用户编号
#     #question.id 外键 问题编号
#     answer_content = db.Column(db.String(4))

#     def __repr__(self):                 #__repr__返回一个具有可读性的字符串表示模型，调试和测试中使用
#         return '<Answer %r>' % self.id



# @app.before_request                        #注册一个函数，在每次请求之前运行
# def check_user_status():
#     if 'user_num' not in session:
#         session['user_num'] = None
#         session['user_name'] = None



# @app.route('/',methods=['GET', 'POST'])
# def index():								#该视图函数要渲染表单，也要接收表单中的数据
#     form = NameForm()
#     if form.validate_on_submit():		#如果数据能被所有验证函数接受，即Required()通过验证，返回True
#         user=User.query.filter_by(name=form.name.data).first()
#         if user is None:
#             flash('please signup first!')
#             return redirect(url_for('signup'))
#         else:
#             flash('Hello,please login!')
#             return redirect(url_for('login'))
#     return render_template('index.html',current_time=datetime.utcnow(), form=form, user=session.get('user_name'))


# @app.route('/login',methods=['GET', 'POST'])
# def login():
#     if session['user_num']:
#         flash('you have been logged')
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user=User.query.filter_by(stu_num=form.stu_num.data).first()
#         if user is not None and user.check_password(form.password.data):
#             session['user_num'] = form.stu_num.data
#             session['user_name'] = user.name
#             flash('Thanks for logging in')
#             return redirect(url_for('index'))
#         else:
#             flash('Sorry! no user exists with this student number and password')
#             return render_template('login.html',form=form)
#     return render_template('login.html',form=form)

# @app.route('/signup', methods=('GET', 'POST'))
# def signup():

#     if session['user_num']:
#         flash('you are already signed up')
#         return redirect(url_for('index'))
        
#     form = SignupForm()
#     if request.method == 'GET':
#     # 获取 GET 请求参数
#         phone_number = request.args.get('mobile_phone_number')
#         if phone_number is not None:
#             if sms.send_message(phone_number):
#                 return render_template('signup.html',form=form)
#             else:
#                 flash('获取验证码失败！')
#     elif request.method == 'POST':
#         if form.validate_on_submit():
#             user_num = User.query.filter_by(stu_num=form.stu_num.data).first()
#             if user_num is None:
#                 phone_number = form.phone_number.data
#                 code =form.code.data
#                 if code == '':
#                     flash('请输入验证码！')
#                 elif sms.verify(phone_number, code):
#                     name = form.name.data
#                     stu_num = form.stu_num.data
#                     password = form.password.data
#                     user = User(name,stu_num,phone_number,password)
#                     db.session.add(user)
#                     db.session.commit()
#                     session['user_num']=stu_num
#                     session['user_name']=name
#                     flash("注册成功！")
#                     return redirect(url_for('index'))
#                 else:
#                     flash('验证码有误，请重新输入！')
#                     return render_template('signup.html', form=form)
#             else:
#                 flash("该学号已经注册！", 'error')
#                 return render_template('signup.html', form=form)
#         else:
#             flash("请输入正确信息")
#             return render_template('signup.html', form=form)
#     return render_template('signup.html',form=form)
    
    

# @app.route('/logout', methods=('GET', 'POST'))
# def logout():
#     session.pop('user_num', None)
#     session.pop('user_name', None)
#     flash("You were successfully logged out")
#     return redirect(request.referrer or url_for('index'))


# @app.route('/createpaper', methods=('GET', 'POST'))
# def createpaper():
#     if session['user_num'] is None:
#         flash('please login')
#         return redirect(url_for('login'))
#     user=User.query.filter_by(stu_num=session.get('user_num')).first()
#     form = PaperCreateForm()
#     if form.validate_on_submit():
#         paper_title = Paper.query.filter_by(paper_title=form.paper_title.data).first()
#         if paper_title is None:
#             paper = Paper(paper_title=form.paper_title.data,question_num=form.question_num.data,author=user)
#             db.session.add(paper)
#             db.session.commit()
#             session['paper_title'] = form.paper_title.data			
#             return redirect(url_for('createquestion'))
#         else:
#             flash("A paper already exists.")
#             return render_template('create-paper.html',form=form)
#     return render_template('create-paper.html',form=form)



# @app.route('/createpaper/createquestion',methods=('GET','POST'))
# def createquestion():
#     if session['user_num'] is None:
#         flash('please login')
#         return redirect(url_for('login'))

#     paper = Paper.query.filter_by(paper_title = session.get('paper_title')).first()
    
    
#     class DynamicQuestionForm(FlaskForm):
#         pass


#     for i in range(0,paper.question_num):
        
#         setattr(DynamicQuestionForm,'form'+str(i),TextAreaField('题干'+str(i+1),validators=[Required()]))
#     setattr(DynamicQuestionForm,'submit',SubmitField('提交'))
    

#     form = DynamicQuestionForm()


#     question=[]
#     form_data=[]
#     # flash(attr[0])
#     if form.validate_on_submit():
#         for i in range(paper.question_num):

            
#             form_data.append(form.form0.data)
#             flash(form.form0.data)
#             a=getattr(DynamicQuestionForm,'form'+str(i))
#             flash(a)
#             question.append(Question(paper_id=paper.id,question_content = form_data[i]))
#             db.session.add(question[i])
#             db.session.commit()
#             flash("创建完成")
#         flash("2")
#     flash(form.validate_on_submit())
#     flash(form.errors)

#     return render_template('create-question.html',paper_title=paper.paper_title,question_num=paper.question_num,form=form)




# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404


# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500


# if __name__ == '__main__':				#执行这个脚本时启动web服务器
#     app.run(host='0.0.0.0',debug=True)					#启动服务器
#     db.create_all()

    # manager.add_command("shell",Shell(make_context=make_shell_context))
    # manager.run()
