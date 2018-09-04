from settings import DevelopmentConfig


def sql_execute(sql, type='search'):
    conn = DevelopmentConfig.POOL.connection()
    cur = conn.cursor()
    cur.execute(sql)
    ret = cur.fetchall()
    if type=='insert':
        conn.commit()
    conn.close()
    return ret




