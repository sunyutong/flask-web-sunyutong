from werkzeug import generate_password_hash, check_password_hash		#登陆密码的加解密
from sqlalchemy import Column,Integer,String,ForeignKey
from . import db                                            
 
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    stu_num = db.Column(db.String(12))
    phone_num = db.Column(db.String(11))
    password = db.Column(db.String(30))
    papers = db.relationship('Paper',backref='author', lazy='dynamic')

    def __init__(self, name, stu_num,phone_num, password):
        self.name = name
        self.stu_num = stu_num
        self.phone_num = phone_num
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):                 #__repr__返回一个具有可读性的字符串表示模型，调试和测试中使用
        return '<User %r>' % self.name


class Paper(db.Model):
    __tablename__ = 'paper'
    id = db.Column(db.Integer, primary_key=True)
    paper_title = db.Column(db.String(30))
    question_num = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    questions = db.relationship('Question',backref='survey',lazy='dynamic')

    # paper_description = db.Column(db.String(120))
    # paper_deadline = db.Column(db.String(60))       #有待调整

    # def __init__(self, paper_title,question_num,user_id):
    #     self.paper_title = paper_title
    #     # self.question_num = question_num
    #     self.user_id = User.id

    def __repr__(self):                 #__repr__返回一个具有可读性的字符串表示模型，调试和测试中使用
        return '<Paper %r>' % self.paper_title


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    question_content = db.Column(db.String(240), default='none')
    paper_id = db.Column(db.Integer,db.ForeignKey('paper.id'))
    selects = db.relationship('Select',backref='stem', lazy='dynamic')

    def __init__(self, paper_id,question_content):
        self.question_content = question_content
        self.paper_id = paper_id



    def __repr__(self):                 #__repr__返回一个具有可读性的字符串表示模型，调试和测试中使用
        return '<Question %r>' % self.question_content


class Select(db.Model):
    __tablename__ = 'select'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer,ForeignKey('question.id'))
    select_content = db.Column(db.String(60))
    def __repr__(self):                 #__repr__返回一个具有可读性的字符串表示模型，调试和测试中使用
        return '<Select %r>' % self.id


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,ForeignKey('user.id'))
    question_id = db.Column(db.Integer,ForeignKey('question.id'))
    #user.id 外键 用户编号
    #question.id 外键 问题编号
    answer_content = db.Column(db.String(4))

    def __repr__(self):                 #__repr__返回一个具有可读性的字符串表示模型，调试和测试中使用
        return '<Answer %r>' % self.id                                              
                                               