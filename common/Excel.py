# encoding:utf-8
import os, xlrd,traceback
from xlutils.copy import copy


class Reader:
    # 用来读取excel文件内容，只支持xlsx
    def __init__(self):
        # 整个excel工作簿缓存
        self.workbook = None
        # 当前工作sheet
        self.sheet = None
        # 当前sheet的行数
        self.rows = 0
        # 当前读取到的行数
        self.r = 0

    # 打开excel，初始化参数
    def open_excel(self, srcfile):
        if not os.path.exists(srcfile):
            print("error: %s is not exist! " % (srcfile))
            return
        # 设置读取excel使用utf8编码
        xlrd.Book.encoding = "utf8"
        # 设置excel内容到缓存workbook
        self.workbook = xlrd.open_workbook(filename=srcfile)
        # 选取第一个sheet页面
        self.sheet = self.workbook.sheet_by_index(0)
        # 设置rows为当前sheet的行数
        self.rows = self.sheet.nrows
        # 设置当前读取行数为第一行
        self.r = 0

    # 获取sheet页面
    def get_sheets(self):
        # 获取所有sheet名字，并返回为一个列表
        sheets = self.workbook.sheet_names()
        return sheets

    # 切换sheet页面
    def set_sheet(self, name):
        self.sheet = self.workbook.sheet_by_name(name)
        self.rows = self.sheet.nrows
        self.r = 0

    # 逐行读取excel的文件
    def readline(self):
        row1 = None
        # 如果当前还没到最后一行，则往下读取一行
        if self.r < self.rows:
            row = self.sheet.row_values(self.r)
            self.r += 1
            i = 0
            row1 = row
            # 把读取的数据变为字符串
            for strs in row:
                row1[i] = str(strs)
                i = i + 1
        return row1


class Writer:
    def __int__(self):
        # 目标excel
        self.workbook = None
        # 拷贝的工作空间
        self.wb = None
        # 当前工作的sheet页面
        self.sheet = None
        # 记录生成的文件，用来保存
        self.df = None
        # 记录写入的行
        self.row = 0
        # 记录写入的列
        self.clo = 0

    def copy_open(self, srcfile, dstfile):
        if not os.path.exists(srcfile):
            print("error :%s is not exists!" % (srcfile))
            return
        if os.path.exists(dstfile):
            print("warn : the file %s is exists!" % (dstfile))

        # 记录要保存的目标文件
        self.df = dstfile
        # 读取excel到缓存
        self.workbook = xlrd.open_workbook(filename=srcfile, formatting_info=True)
        self.wb = copy(self.workbook)
        return

    def get_sheets(self):
        sheets = self.workbook.sheet_names()
        return sheets

    def set_sheet(self, name):
        self.sheet = self.wb.get_sheet(name)
        return

    def write(self,r,c,value):
        #获取要写入的单元格
        def _getCell(sheet,r,c):
            #获取行
            row = sheet._Worksheet__rows.get(r)
            if not row:
                return None
            #获取单元格
            cell = row._Row__cells.get(c)
            return cell
        cell = _getCell(self.sheet,r,c)
        self.sheet.write(r,c,value)
        if cell:
            ncell = _getCell(self.sheet,r,c)
            if ncell:
                ncell.xf_idx = cell.xf_idx
        return

    def save_close(self):
        try:
            self.wb.save(self.df)
        except Exception as e:
            print("error: 文件保存失败！")
            print(traceback.format_exc(e))
        return

if __name__ == '__main__':
    reader = Reader()
    reader.open_excel("../lib/cases/百度ip测试.xls")
    sheets = reader.get_sheets()
    for sheet in sheets:
        reader.set_sheet(sheet)
        for i in range(reader.rows):
            print(reader.readline())
    # writer = Writer()
    # writer.copy_open('../lib/cases/百度ip测试.xls','../lib/results/百度ip测试-result.xls')
    # sheetnames = writer.get_sheets()
    # writer.set_sheet(sheetnames[0])
    # writer.write(1,1,'william')
    # writer.save_close()


