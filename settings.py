class Base(object):
    """共有环境变量"""
    SECRET_KEY='asaudsh632482hagydga823y'  # 有待优化
    UPLOAD_FOLDER = 'uploads/'
    ALLOWED_EXTENSIONS = set(['zip',])
    MAX_CONTENT_LENGTH = 60 * 1024 * 1024


import pymysql

class DevelopmentConfig(Base):
    """开发环境配置"""
    DEBUG = True
    DB = pymysql.connect(host='localhost',user='root', password='abc123',port=3306,db='codeup_db')
    CURSOR = DB.cursor()











