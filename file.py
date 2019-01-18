import pymysql

def writeFile(path,idsList):
    with open(path,'w') as f:
        for str in idsList:
            f.write('\'' +str +'\'' + ',')

def readFile(path):
    with open(path, 'r') as f:
        lines = f.read(100000)  # 按行读取文件中的内容
        list = lines.strip().replace('\'', '').replace(' ','').replace('\n', '').split(',')
        if list.index('') != -1:
            print('执行了')
            list.remove('')
        return list

def appendFile(path,idsList):
    with open(path,'a') as f:
        for str in idsList:
            f.write('\'' +str +'\'' + ',')


#'./IDS'
def save_info_print(file_name, new_links):
    print('新爬取的链接在去重之前有' + str(len(new_links)) + '个')
    new_links = list(set(new_links))
    print('新爬取的链接在去重之后有' + str(len(new_links)) + '个')
    old_links = readFile(file_name)
    print('IDS池中链接有' + str(len(old_links)) + '个')
    new_links = list(set(new_links + old_links))
    print('新爬取的去重链接加上IDS池中链接有' + str(len(new_links)) + '个，将保存进IDS文件中')
    writeFile(file_name, new_links)


def save_ids_to_mysql(db_name , table_name , links , source):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "root", db_name)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    for x in links:
        try:
            sql = '';
            if source == '京东':
                sql = 'insert into ' + table_name + ' (id, skuid , url , source) values ( "%s", "%s", "%s" , "%s")' % (
                    'jd' + x, x, 'https://item.jd.com/' + x + '.html', '京东')
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except Exception as e:
            # 如果发生错误则回滚
            # print(e)
            db.rollback()
    # 关闭数据库连接
    db.close()


