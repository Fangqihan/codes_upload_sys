from flask import Blueprint, render_template, request,session, redirect
from settings import DevelopmentConfig
from utils import sql_execute

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
        rets = sql_execute(sql)
        ret = {'user':username, "data":rets}
        if ret:
            session['user'] = username
            session['id'] = ret['data'][0][0]
            session['is_login'] = True
            # 取出当前用户的所有权限url列表
            sql = '''select url from permmision where id in (select permission_id from role_permission where role_id in 
                      (select role from user_profile_role u_r where u_r.user =%d))'''% ret['data'][0][0]
            ret = sql_execute(sql)
            ret = [item[0] for item in ret if item]
            print('urls>>>',ret)

            session['permission_urls'] = ret
            return redirect('/users')

    return render_template('account/login.html')


@ac.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/login')


@ac.route('/chart',methods=['GET'])
def test_page():
    return render_template('codes/block_chart.html')



from .forms import RegisterForm


@ac.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = RegisterForm()
        return render_template('account/register.html', form=form)

    else:
        form = RegisterForm(formdata=request.form)
        if form.validate():
            username = form.data.get('username','')
            password = form.data.get('pwd','')
            email = form.data.get('email','')
            # 查询用户是否中存在
            print('用户提交数据通过格式验证，提交的值为: ', form.data)

            return redirect('/login')

        else:
            print(form.errors)
        return render_template('account/register.html', form=form)



