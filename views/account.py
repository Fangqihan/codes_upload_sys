from flask import Blueprint, render_template, request,session, redirect
from settings import DevelopmentConfig


ac = Blueprint('ac', __name__)


@ac.route('/login', methods=["POST", "GET"])
def login():
    # 拿到用户信息
    if request.method=='POST':
        username = request.form.get('username','')
        password = request.form.get('password','')
        print(username, password)

        # 进入数据库验证用户信息
        sql = 'select id, nick_name from user_profile where name = "%s" and password = "%s"' % (username,password)
        DevelopmentConfig.CURSOR.execute(sql)
        ret = DevelopmentConfig.CURSOR.fetchall()
        print(ret)
        ret = {'user':username, "data":ret}
        if ret:
            session['user'] = username
            session['id'] = ret['data'][0][0]
            session['is_login'] = True
            return redirect('/users')

    return render_template('account/login.html')


@ac.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/login')

