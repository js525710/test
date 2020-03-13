# encoding:utf-8
from common import config
from common.excelResult import Result
from common.Excel import Writer, Reader
from common.mail import Mail
from interface.inter import HTTP
import inspect
import json,jsonpath
import  datetime

def runcase(line, f):

    if len(line[0]) > 0 or len(line[1]) > 0:
        return
    func = getattr(f, line[3])
    # 获取反射关键字的参数个数
    args = inspect.getfullargspec(func).__str__()
    args = args[args.find('args=') + 5:args.rfind(', varargs')]
    args = eval(args)
    args.remove('self')

    if len(args) == 0:
        func()
        return
    if len(args) == 1:
        func(line[4])
        return
    if len(args) == 2:
        func(line[4], line[5])
        return
    if len(args) == 3:
        func(line[4], line[5], line[6])
        return
    print("warning: 目前仅支持三个以内的参数")


reader = Reader()
reader.open_excel("./lib/cases/百度ip测试.xls")

# sheets = reader.get_sheets()
# for s in sheets:
#     reader.set_sheet(s)
#     for i in range(reader.rows):
#         line = reader.readline()
#         runcase(line, http)

writer = Writer()
writer.copy_open('./lib/cases/百度ip测试.xls','./lib/results/百度ip测试-result.xls')
sheetnames = writer.get_sheets()

writer.set_sheet(sheetnames[0])
writer.write(1,3,str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

http = HTTP(writer)
for sheet in sheetnames:
    reader.set_sheet(sheet)
    writer.set_sheet(sheet)
    for i in range(reader.rows):
        writer.row = i
        line = reader.readline()
        runcase(line,http)

writer.set_sheet(sheetnames[0])
writer.write(1,4,str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
writer.save_close()

res = Result()
res.get_res('./lib/results/百度ip测试-result.xls')

config.get_config('./lib/conf/conf.properties')  # 返回的是一个字典
# logger.debug(config.config)


# 发送邮件

html = config.config['mailtxt']
html = html.replace('runtype', res.sumarry['runtype'])
html = html.replace('title', res.sumarry['title'])
html = html.replace('starttime', res.sumarry['starttime'])
html = html.replace('endtime', res.sumarry['endtime'])
html = html.replace('casecount', res.sumarry['casecount'])
html = html.replace('passrate', res.sumarry['passrate'])
html = html.replace('status', res.sumarry['status'])
if res.sumarry['status'] == 'Fail':
    html = html.replace('#00d800', 'red')

mail = Mail()
# mail.mail_info['filepaths'] = ['./lib/log/1.txt', './lib/log/all.log']
# mail.mail_info['filenames'] = ['1.txt', 'all.log']
mail.send(html)
