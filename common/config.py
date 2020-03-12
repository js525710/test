# encoding:utf-8
from common import  logger
from common.txt import  Txt
#全局变量，存储配置，字典格式
config = {}
def get_config(path):
    global  config
    config.clear()
    txt = Txt(path,'r')
    data = txt.read()
    for s in data:
        if s.startswith('#'):
            continue
        if  s.find('=') < 0:
            logger.warn('配置文件格式错误，请检查'+str(s))
            continue
        try:
            key = s[0:s.find('=')]
            value = s[s.find('=')+1:]
            config[key] =  value
        except Exception as e:
            logger.warn("配置文件格式错误，请检查"+str(s))
    return config

if __name__ == '__main__':
    config = get_config('../lib/conf/conf.properties')
    print(config)
