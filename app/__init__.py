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
from flask_sqlalchemy import SQLAlchemy 		#数据库
from flask_debugtoolbar import DebugToolbarExtension   #Debug导航栏
from config import config

# manager=Manager()					#初始化主类的实例
bootstrap=Bootstrap()
moment=Moment()						#初始化Moment实例
toolbar=DebugToolbarExtension()      #初始化debugtoolbar实例
db = SQLAlchemy()

def create_app(config_name):
	app = Flask(__name__)					#创建一个Python实例
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	# manager.init_app(app)
	moment.init_app(app)
	toolbar.init_app(app)
	db.init_app(app)
	with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
		db.create_all()


	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	#附加路由和自定义的错误页面
	
	return app
	