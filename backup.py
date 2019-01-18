import os
def back_up(mongodump_path = 'E:\\mongo\\bin\\mongodump',
            ip_address = 'localhost',
            databases = 'jd',
            dest_address = 'F:\\backtest'):
    command = mongodump_path + ' -h ' + ip_address + ' -d ' + databases + ' -o ' + dest_address
    print(command)
    os.system(command)
back_up()