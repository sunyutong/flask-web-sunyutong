import os
from flask import Flask
from flask import session 						#用户会话
from flask import redirect						#重定向
from flask import url_for						#生成URL 使用URL映射生成URL，修改路由名字依然可用
from flask import flash 						#提示用户表单输入有误
from flask import render_template 				#渲染模板
from flask import request 						#上下文
from flask import make_response 				#
from flask_script import Manager	 			#解析指令行
from flask_script import Shell 					#让flask的shell命令自动导入特定的对象
from flask_bootstrap import Bootstrap 			#前端模板
from flask_moment import Moment 				#本地化日期和时间
from flask_wtf import Form 						#表单
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from datetime import datetime 	
from flask_sqlalchemy import SQLAlchemy 		#数据库

from werkzeug import generate_password_hash, check_password_hash
												#登陆密码的加解密

#让Script的Shell命令自动导入app,db,User对象												
def make_shell_context():
	return dict(app=app,db=db,User=User)
    


app = Flask(__name__)					#创建一个Python实例
manager=Manager(app)					#初始化主类的实例
bootstrap=Bootstrap(app)
moment=Moment(app)						#初始化Moment实例


app.config['SECRET_KEY'] = '123qwe'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    email = db.Column(db.String(60))
    password = db.Column(db.String(30))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):					#__repr__返回一个具有可读性的字符串表示模型，调试和测试中使用
        return '<User %r>' % self.name




class NameForm(Form):					#创建一个继承Form表单的表单，Form是表单的始祖
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
    '''StringField类表示属性为type="text"的input元素。
       SubmitField类表示属性为type="submit"的input元素。（表单中StringField等类见书P35）
    第二个变量进行验证，required()函数确保字段中有数据'''		

@app.route('/',methods=['GET', 'POST'])							
def index():								#该视图函数要渲染表单，也要接收表单中的数据
    # user_agent=request.headers.get('User-Agent')
    # response=make_response('<h1>This document carries a cookie</h1>')
    # response.set_cookie('answer','42')
    # return response

    form = NameForm()
    if form.validate_on_submit():		#如果数据能被所有验证函数接受，即Required()通过验证，返回True
        user=User.query.filter_by(name=form.name.data).first()
        if user is None:
        	user=User(name=form.name.data,email='',password='')
        	db.session.add(user)
        	db.session.commit()
        session['name'] = form.name.data			#表单输入的内容存入name后清空
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',current_time=datetime.utcnow(), form=form, name=session.get('name'),known=session.get('known',False))

@app.route('/account')
def accout():
	return render_template('account.html',name=name)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# @app.route('/user/<name>')				#设置路由 视图函数（/user/name）
# def user(name):
#     # return '<h1>hello,%s</h1>' % name
#     return render_template('user.html',name=name)

# @app.route('/test')
# def test():
# 	user = { 'nickname': 'Miguel' }
# 	return '''
# 	<html>
#  	<head>
#   	<title>Home Page</title>
#  	</head>
#  	<body>
#   	<h1>Hello, ''' + user['nickname'] + '''</h1>
#   	<h2></br>this is a web page</h2>
#  	</body>
# 	</html>
# 	'''

if __name__ == '__main__':				#执行这个脚本时启动web服务器
    # app.run(host='0.0.0.0',debug=True)					#启动服务器
    manager.add_command("shell",Shell(make_context=make_shell_context))
    manager.run()