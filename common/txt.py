# coding:utf8
from common import logger


class Txt:
    """
    读写txt文本
    """

    def __init__(self, path, t='r', coding='utf8'):
        self.data = []
        self.f = None
        if t == 'r':
            for line in open(file=path, encoding=coding):
                self.data.append(line)
            for i in range(len(self.data)):
                self.data[i] = self.data[i].encode('utf-8').decode('utf-8-sig')
                self.data[i] = self.data[i].replace('\n', '')
            return

        if t == 'w':
            self.f = open(path, 'a', encoding=coding)
            return
        if t == 'rw':
            for line in open(file=path, encoding=coding):
                self.data.append(line)
            for i in range(self.data.__len__()):
                self.data[i] = self.data[i].encode('utf-8').decode('utf-8-sig')
                self.data[i] = self.data[i].replace('\n', '')
            self.f = open(path, 'a', encoding=coding)
            return

    def read(self):
        return self.data

    def writeline(self, s):
        if self.f is None:
            logger.error("未打开可写入的txt文件")
            return
        self.f.write(str(s))

    def save_close(self):
        if self.f is None:
            logger.error('未打开可写入的txt文件')
            return
        self.f.close()


# 调试
if __name__ == '__main__':
    # writer = Txt('../lib/log/1.txt', 'w')
    # writer.writeline("hahaha")
    # writer.save_close()
    # reader = Txt('../lib/log/1.txt', 'r','utf8')
    # data = reader.read()
    # print(data)
    rw = Txt('../lib/log/1.txt','rw')
    rw.writeline("11111读写\n")
    rw.save_close()
    data = rw.read()
    print(data)
