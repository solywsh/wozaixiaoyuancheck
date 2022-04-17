from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,SelectField,BooleanField
from wtforms.validators import DataRequired
from collections import defaultdict, OrderedDict #缩进控制
from pathlib import Path
from gevent import pywsgi
import json
import os
import ast#json转换


app = Flask(__name__)
app.config['SECRET_KEY'] = 'xsyu-wsh'

bootstrap = Bootstrap(app)
moment = Moment(app)


class dataForm_reg(FlaskForm):
    name = StringField('请输入你的姓名：', validators=[DataRequired()])
    StuId = StringField('请输入你的学号：', validators=[DataRequired()])
    pwd = PasswordField('请输入你的密码：', validators=[DataRequired()])
    WoZaiStudent_Token = StringField('请输入你的“我在校园”token：', validators=[DataRequired()])
    PushPlus_token = StringField('请输入你的“PushPlus”token：', validators=[DataRequired()])
    #morning_check_self = BooleanField('给自己晨检打卡')
    #afternoon_check_self = BooleanField('给自己午检打卡')
    night_check_self = BooleanField('给自己晚检打卡')
    #health_check_self = BooleanField('给自己健康打卡')
    #morning_check_class = BooleanField('给班里的同学晨检查打卡')
    #afternoon_check_class = BooleanField('给班里的同学午检查打卡')
    #health_check_class = BooleanField('给班里的同学健康查打卡')
    night_check_class = BooleanField('给班里的同学晚检打卡')
    receive_message =  BooleanField('接收班级未打卡名单')

    submit = SubmitField(u'提交')

class dataForm_index(FlaskForm):
    StuId = StringField('请输入你的学号：', validators=[DataRequired()])
    pwd = PasswordField('请输入你的密码：', validators=[DataRequired()])
    WoZaiStudent_Token = StringField('请输入你的“我在校园”token：', validators=[DataRequired()])
    #morning_check_self = BooleanField('给自己晨检打卡')
    #afternoon_check_self = BooleanField('给自己午检打卡')
    night_check_self = BooleanField('给自己晚检打卡')
    #health_check_self = BooleanField('给自己健康打卡')
    #morning_check_class = BooleanField('给班里的同学晨检查打卡')
    #afternoon_check_class = BooleanField('给班里的同学午检查打卡')
    night_check_class = BooleanField('给班里的同学晚检打卡')
    receive_message =  BooleanField('接收班级未打卡名单')
    #health_check_class = BooleanField('给班里的同学健康查打卡')

    submit = SubmitField(u'提交')
  
def file_add(new_stu_info):
    path = r"config/id_" + new_stu_info['StuId']
    my_file = Path(path)
    if my_file.is_file():
        # 指定的文件存在
        return 0
    else:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(new_stu_info, indent=4, ensure_ascii=False))
        f.close()
        return 1

def file_change(new_stu_info):
    path = r"config/id_" + new_stu_info['StuId']
    my_file = Path(path)
    if my_file.is_file():
        # 指定的文件存在
        old_stu_info = file_read(new_stu_info['StuId'])
        if old_stu_info != 0:
            #给session赋值，避免在不同设备识别不了姓名的情况
            session['name'] = old_stu_info['name']

            old_stu_info['WoZaiStudent_Token'] = new_stu_info['WoZaiStudent_Token']
            old_stu_info['night_check_self'] = new_stu_info['night_check_self']
            #old_stu_info['morning_check_self'] = new_stu_info['morning_check_self']
            #old_stu_info['afternoon_check_self'] = new_stu_info['afternoon_check_self']
            #old_stu_info['health_check_self'] = new_stu_info['health_check_self']
            #old_stu_info['morning_check_class'] = new_stu_info['morning_check_class']
            #old_stu_info['afternoon_check_class'] = new_stu_info['afternoon_check_class']
            #old_stu_info['afternoon_check_class'] = new_stu_info['afternoon_check_class']
            old_stu_info['night_check_class'] = new_stu_info['night_check_class']
            old_stu_info['receive_message'] = new_stu_info['receive_message']
            with open(path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(old_stu_info, indent=4, ensure_ascii=False))
            f.close()
            return 1
        else:
            return 0
    else:
        return 0


def file_read(StuId):
    path = r"config/id_" + StuId
    my_file = Path(path)
    if my_file.is_file():
        # 指定的文件存在
        with open(path, 'r', encoding='utf-8') as f:
            info_dict = json.load(f)
        f.close()
        return info_dict
    else:
        return 0


#获取当前目录下的所有文件
def listdir(path,list_name):  #传入存储的list
    for file in os.listdir(path):  
        file_path = os.path.join(path, file)  
        if os.path.isdir(file_path):  
            listdir(file_path, list_name)  
        else:  
            list_name.append(file_path)

    return list_name

def find(Id):
    #获得config目录下的所有文件名格式为'id_20190707XXXX'
    #如果有相同班级的，返回0
    #如果没有返回1
    #这是为了防止一个班多个人注册
    path = r"config"
    all_flie_path = []
    listdir(path, all_flie_path)
    for flie_path in all_flie_path:
        print(flie_path[10:20])
        #config\id_201907071004
        if str(flie_path[10:20]) == str(Id[0:10]):
            return 0

    return 1
    
        
    


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    form = dataForm_index()
    if form.validate_on_submit():


        #判断是否存在对应学号的信息，如果有就返回学号对应身份的字典，如果没有，就返回0
        dir_stu_info  = file_read(form.StuId.data)
        if dir_stu_info == 0:
            flash('用户未注册！')
            return redirect(url_for('index'))

        if dir_stu_info['pwd'] != form.pwd.data:
            flash('密码错误！请重新输入！')
            return redirect(url_for('index'))



        old_WoZaiStudent_Token = dir_stu_info['WoZaiStudent_Token']
        if old_WoZaiStudent_Token is not None and old_WoZaiStudent_Token != form.WoZaiStudent_Token.data:
            #进行赋值
            session['StuId'] = form.StuId.data
            session['pwd'] = form.pwd.data
            session['WoZaiStudent_Token'] = form.WoZaiStudent_Token.data
            #session['morning_check_self'] = form.morning_check_self.data
            #session['afternoon_check_self'] = form.afternoon_check_self.data
            #session['health_check_self'] = form.health_check_self.data

            #session['morning_check_class'] = form.morning_check_class.data
            #session['afternoon_check_class'] = form.afternoon_check_class.data
            session['night_check_self'] = form.night_check_self.data
            session['night_check_class'] = form.night_check_class.data

            session['receive_message'] = form.receive_message.data
            #session['health_check_class'] = form.health_check_class.data
            
            user_dict = ast.literal_eval(str(session).replace('<','').replace('>','').replace('SecureCookieSession ',''))
            flag = file_change(user_dict)
            if flag:
                flash('成功更换“我在校园”token!!!')
                return redirect(url_for('index'))
            else:
                flash('更换失败！')
                return redirect(url_for('index'))

        else:
            flash('token为空或者相同！')
            return redirect(url_for('index'))
        
    

    return render_template('index.html', form=form, name = session.get('name'))


@app.route('/registered', methods=['GET', 'POST'])
def registered():
    form = dataForm_reg()
    
    if form.validate_on_submit():
        #对学号进行检查
        if str(form.StuId.data[0:8]) != '20190707':
            flash('该网站暂不对计算机学院2019级以外的人开放注册！')
            return redirect(url_for('registered'))

        #查找已经注册过的学号
        flag = find(form.StuId.data)
        if flag == 0:
            flash('你们班已经有人注册！请联系管理员')
            return redirect(url_for('registered'))

        session['name'] = form.name.data
        session['StuId'] = form.StuId.data
        session['pwd'] = form.pwd.data
        session['WoZaiStudent_Token'] = form.WoZaiStudent_Token.data
        session['PushPlus_token'] = form.PushPlus_token.data
        #session['morning_check_self'] = form.morning_check_self.data
        #session['afternoon_check_self'] = form.afternoon_check_self.data
        #session['health_check_self'] = form.health_check_self.data
        #session['morning_check_class'] = form.morning_check_class.data
        #session['afternoon_check_class'] = form.afternoon_check_class.data
        session['night_check_self'] = form.night_check_self.data
        session['night_check_class'] = form.night_check_class.data

        session['receive_message'] = form.receive_message.data
        #session['health_check_class'] = form.health_check_class.data
        user_dict = ast.literal_eval(str(session).replace('<','').replace('>','').replace('SecureCookieSession ',''))
        
        #检查完成
        flag = file_add(user_dict)
        if flag:
            flash('注册成功！！！')
            return redirect(url_for('index'))
        else:
            flash('注册失败，已经有相同的人注册了你的信息。')
            return redirect(url_for('registered'))
        

    return render_template('reg.html', form=form, name = session.get('name'))


@app.route('/foryb', methods=['GET', 'POST'])
def foryb():
    form = dataForm_reg()
    
    if form.validate_on_submit():
        # #对学号进行检查
        # if str(form.StuId.data[0:8]) != '20190707':
        #     flash('该网站暂不对计算机学院2019级以外的人开放注册！')
        #     return redirect(url_for('registered'))

        # #查找已经注册过的学号
        # flag = find(form.StuId.data)
        # if flag == 0:
        #     flash('你们班已经有人注册！请联系管理员')
        #     return redirect(url_for('registered'))

        session['name'] = form.name.data
        session['StuId'] = form.StuId.data
        session['pwd'] = form.pwd.data
        session['WoZaiStudent_Token'] = form.WoZaiStudent_Token.data
        session['PushPlus_token'] = form.PushPlus_token.data
        
        #session['morning_check_self'] = form.morning_check_self.data
        #session['afternoon_check_self'] = form.afternoon_check_self.data
        #session['health_check_self'] = form.health_check_self.data
        #session['morning_check_class'] = form.morning_check_class.data
        #session['afternoon_check_class'] = form.afternoon_check_class.data
        session['night_check_self'] = form.night_check_self.data
        session['night_check_class'] = form.night_check_class.data
        session['receive_message'] = form.receive_message.data
        #session['health_check_class'] = form.health_check_class.data
        user_dict = ast.literal_eval(str(session).replace('<','').replace('>','').replace('SecureCookieSession ',''))
        
        #检查完成
        flag = file_add(user_dict)
        if flag:
            flash('注册成功！！！')
            return redirect(url_for('index'))
        else:
            flash('注册失败，已经有相同的人注册了你的信息。')
            return redirect(url_for('foryb'))
        

    return render_template('foryb.html', form=form, name = session.get('name'))





if __name__ == '__main__':
    app.run(debug=True)
# if __name__ == '__main__':
#     server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
#     server.serve_forever()