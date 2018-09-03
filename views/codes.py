from flask import Blueprint, render_template, session, redirect, request, flash, url_for
from settings import DevelopmentConfig
import functools
from utils import sql_execute


co = Blueprint('co', __name__)


def wrapper(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        if not session.get('is_login'):
            return redirect('/login')
        return func(*args, **kwargs)
    return inner


@co.route('/users', endpoint='user_list')
@wrapper
def user_list():
    # 进入数据库验证用户信息
    sql = "select id, name from user_profile"
    ret = sql_execute(sql)
    return render_template('codes/users.html',data=ret)



@co.route('/users/<int:nid>', endpoint='my_uploads')
@wrapper
def my_uploads(nid):
    """我的上传记录页面"""
    sql = "select id, lines_num,user,upload_time from codes_upload where user=%d" % nid
    ret = sql_execute(sql)
    # print(ret)

    sql1 = 'select id,nick_name from user_profile where id=%s' % nid
    ret1 = sql_execute(sql1)
    ret = {'user':ret1, 'data':ret}
    return render_template('codes/my_codes.html', data=ret)



def allowed_file(filename):
    """过滤上传文件的后缀"""
    ALLOWED_EXTENSIONS = DevelopmentConfig.ALLOWED_EXTENSIONS
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


import os
import datetime
import shutil
import uuid


@co.route('/upload',methods=['POST', 'GET'], endpoint='upload_code')
@wrapper
def upload_code():

    error = None
    if request.method == 'POST':
        # 1、上传的文件不能为空
        if 'file' not in request.files:
            error = '需要上传文件'
            return render_template('codes/upload.html', error=error)

        file = request.files['file']
        print(file.filename)  # 文件名称
        print(file.stream)  #　文件内容
        # 2、上传的文件格式必须符号要求
        if file and allowed_file(file.filename):
            # 3、判断当前用户是否是首次上传
            today_str = str(datetime.datetime.now())[:10]
            sql = 'select * from codes_upload where user=%s and upload_time=%s' % (int(session.get('id','')), "'"+today_str+"'")
            rets = sql_execute(sql)
            # print('查询结果:', rets)

            if not rets:
                # 4、接收用户上传文件并解压到指定的目录，生成随机文件夹名称，防止重名覆盖
                # 注意必须确保上传的文件是以zip方式压缩的，单纯的修改zip后缀仍然不算zip格式
                target_path = os.path.join(DevelopmentConfig.UPLOAD_FOLDER, str(uuid.uuid4()))
                shutil._unpack_zipfile(file.stream, target_path)

                # 6、遍历目录下的所有文件，并汇总出解压后的所有的文件的行数
                total_num = 0
                for root, dirs, files in os.walk(target_path):
                    # print(dirs)
                    # print(root)  # 文件夹的绝对路径
                    for filename in files:
                        line_count = 0
                        file_path = os.path.join(root, filename)
                        with open(file_path, 'rb') as f:
                            for line in f:
                                line = line.strip()
                                if not line or line.startswith(b'#'):
                                    continue
                                line_count += 1
                        total_num += line_count
                print(total_num)
                add_sql = 'insert into codes_upload (user,lines_num,upload_time) values (%s, %s, %s)' % (session.get('id',''), total_num, "'"+today_str+"'")
                rets = sql_execute(add_sql, type='insert')
                return redirect(url_for('co.my_uploads',nid=int(session.get('id'))))

            error = '今天代码已上传'

        else:error = '文件必须为zip格式'

    return render_template('codes/upload.html', error=error)



