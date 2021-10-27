from postgresql import driver

login_db = "postgres"
password_db = "159653"
host_db = "172.20.111.230"
name_db = "test"

conn = driver.connect(user=login_db,
                      password=password_db,
                      host=host_db,
                      database=name_db,
                      port='5432')


def max_id():
    conn = driver.connect(user=login_db,
                          password=password_db,
                          host=host_db,
                          database=name_db,
                          port='5432')
    max_num = conn.query(f'''SELECT MAX(id_num)+1 FROM inbox''')
    if max_num[0][0] == None:
        max_num = 1
    else:
        max_num = max_num[0][0]
    print(max_num)
    return max_num


def create_upload_jpg(id_num, name):
    conn = driver.connect(user=login_db,
                          password=password_db,
                          host=host_db,
                          database=name_db,
                          port='5432')
    conn.query("""INSERT INTO inbox(id_num, name_jpg) VALUES ({0}, '{1}')""".format(id_num, name))
    conn.close()


def select_jpg(id_num):
    conn = driver.connect(user=login_db,
                          password=password_db,
                          host=host_db,
                          database=name_db,
                          port='5432')
    res = conn.query(f'''SELECT name_jpg, date FROM inbox WHERE id_num = {id_num}''')
    conn.close()
    return res


def del_jpg(id_num):
    conn = driver.connect(user=login_db,
                          password=password_db,
                          host=host_db,
                          database=name_db,
                          port='5432')
    res = conn.query(f'''DELETE FROM inbox WHERE id_num={id_num}''')
    return res
