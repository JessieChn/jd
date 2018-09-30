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

def save_info_print(new_links):
    print('新爬取的链接在去重之前有' + str(len(new_links)) + '个')
    new_links = list(set(new_links))
    print('新爬取的链接在去重之后有' + str(len(new_links)) + '个')
    old_links = readFile('./IDS')
    print('IDS池中链接有' + str(len(old_links)) + '个')
    new_links = list(set(new_links + old_links))
    print('新爬取的去重链接加上IDS池中链接有' + str(len(new_links)) + '个，将保存进IDS文件中')
    writeFile('./IDS',new_links)
