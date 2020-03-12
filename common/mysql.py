# encoding:utf-8
import pymysql
from common import logger
from common import config


class Mysql:
    def __init__(self):
        self.mysql_config = {
            'mysqluser': 'root',
            'mysqlpassword': "js123456",
            'mysqlport': 3306,
            'mysqlhost': '47.114.111.249',
            'mysqldb': 'test_project',
            'mysqlcharset': "utf8"
        }
        # 从配置文件读取配置
        for key in self.mysql_config:
            try:
                self.mysql_config[key] = config.config[key]
            except Exception as e:
                logger.exception(e)
        # 把端口处理为整数
        try:
            self.mysql_config['mysqlport'] = int(self.mysql_config['mysqlport'])
        except Exception as e:
            logger.exception(e)

    def __read_sql_file(self, file_path):
        sql_list = []
        with open(file_path, 'r', encoding='utf8') as f:
            for line in f.readlines():
                if line.startswith('SET'):
                    sql_list.append(line.replace('\n', ''))
                elif line.startswith('DROP'):
                    sql_list.append(line.replace('DROP', 'TRUNCATE').replace(' IF EXISTS', '').replace('\n', ''))
                elif line.startswith('INSERT'):
                    sql_list.append(line.replace('\n', ''))
                else:
                    pass
        return sql_list

    # 初始化mysql配置
    def init_mysql(self, path):
        connect = pymysql.connect(
            user=self.mysql_config['mysqluser'],
            password=self.mysql_config['mysqlpassword'],
            port=self.mysql_config['mysqlport'],
            host=self.mysql_config['mysqlhost'],
            db=self.mysql_config['mysqldb'],
            charset=self.mysql_config['mysqlcharset']
        )
        # 获取游标
        cursor = connect.cursor()
        logger.info("正在恢复%s数据库" % path)
        for sql in self.__read_sql_file(path):
            cursor.execute(sql)
            connect.commit()
        # 关闭游标和连接
        cursor.close()
        connect.close()


if __name__ == '__main__':
    config.get_config('../lib/conf/conf.properties')
    mysql = Mysql()
    mysql.init_mysql("../lib/conf/userinfo.sql")
