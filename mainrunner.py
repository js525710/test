# encoding:utf-8
from common.Excel import Writer, Reader
from interface.inter import HTTP
import inspect


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
http = HTTP(writer)


for sheet in sheetnames:
    reader.set_sheet(sheet)
    writer.set_sheet(sheet)
    for i in range(reader.rows):
        writer.row = i
        line = reader.readline()
        runcase(line,http)
writer.save_close()
