# encoding:utf-8
from common.Excel import Reader
from common import logger


class Result:
    def __init__(self):
        self.sumarry = {}

    def get_res(self, result_path):
        self.sumarry.clear()
        status = 'Fail'
        # 标记是够有失败
        flag = True
        # 测试用例总条数目
        totalcount = 0
        # 统计通过用例数
        totalpass = 0

        reader = Reader()
        reader.open_excel(result_path)
        reader.readline()
        line = reader.readline()
        self.sumarry['runtype'] = line[1]
        self.sumarry['title'] = line[2]
        self.sumarry['starttime'] = line[3]
        self.sumarry['endtime'] = line[4]
        for n in reader.get_sheets():
            reader.set_sheet(n)
            row = reader.rows
            reader.r = 1

            for i in range(1, row):
                line = reader.readline()
                if not (line[0] == '' and line[1] == ''):
                    pass
                else:
                    if len(line) < 7 or line[7] == '':
                        flag = False
                    else:
                        totalcount = totalcount + 1
                        if line[7] == 'PASS':
                            totalpass += 1
                        else:
                            flag = False

        if flag:
            status = "Pass"
        try:
            p = int(totalpass * 10000 / totalcount)
            passrate = p / 100
        except Exception as e:
            passrate = 0.0
            logger.exception(e)

        self.sumarry["casecount"] = str(totalcount)
        # 通过率
        self.sumarry["passrate"] = str(passrate) + '%'
        self.sumarry['status'] = status
        return self.sumarry


if __name__ == '__main__':
    res = Result()
    r = res.get_res('../lib/results/百度ip测试-result.xls')
    print(r)
