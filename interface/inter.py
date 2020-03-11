# encoding=utf-8
import json
import requests
from common import logger


class HTTP:

    # 构造函数
    def __init__(self,writer):
        # 建立一个session的会话管理
        self.session = requests.session()
        # 默认添加headers信息，可以对对应的key进行修改
        self.session.headers['content-type'] = "application/x-www-form-urlencoded"
        # self.session.headers['user-agent'] = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"

        # 执行结果
        self.result = ''
        # 存储result转为json格式后的结果
        self.jsonres = {}
        # 存储参数
        self.params = {}
        # url
        self.url = ''
        # 写excel
        self.writer = writer

    def seturl(self, u):
        """
        设置url
        :param u:
        :return:
        """
        if u.startswith("http") or u.startswith("https"):
            self.url = u
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, "设置url: " + self.url)
        else:
            logger.error("url格式错误")
            print("url格式错误")
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, 'url格式错误')
            return False

            # post方法

    def post(self, url, d=None, j=None):
        """
        发送post请求
        :param url:url路径，可以使单纯的路径+全局的host，也可以是http/https开头的绝对路径
        :param d:标准url data传参
        :param j:传递json字符串的参数
        :return:
        """
        if not (url.startswith("http") or url.startswith("https")):
            url = self.url + '/' + self.__get_param(url)

        if d is None or d == '':
            pass
        else:
            # 将传进来的参数{var}替换
            d = self.__get_param(d)
            # print("***"+str(d))
            # 传参格式为json字符串
            # d = self.__get_data(d)
            # 传参格式为key1=value1&key2=value2格式的字符串
            d = self.__get_data1(d)
            # print(d)

        if j is None or j == '':
            pass
        else:
            # 将传进来的参数{var}替换
            j = self.__get_param(j)
            # j = str(j).replace("+", "%2B")
            # j = j.encode("utf-8")

            # 传参格式为json字符串
            j = self.__get_data(j)
        # logger.info("客户端请求json报文数据为：" + str(j))

        # 执行post请求，如果请求https，报ssl错误，就添加verify=False
        res = self.session.post(url, d, j, verify=False)
        logger.info("请求" + url + "返回的状态码为：" + str(res.status_code))
        print("请求" + url + "返回的状态码为：" + str(res.status_code))
        if res.status_code == 200:
            self.result = res.content.decode('utf-8')
            logger.info("执行结果: " + self.result)
            print("执行结果: " + self.result)
            try:
                # 将result的string格式转为json格式
                self.jsonres = json.loads(self.result)
                self.writer.write(self.writer.row, 7, 'PASS')
                self.writer.write(self.writer.row, 8, str(self.jsonres))
            except Exception as e:
                # 如果解析失败了，jsonres存储的为上一次结果，需要清空
                self.jsonres = {}
                self.writer.write(self.writer.row, 7, 'PASS')
                self.writer.write(self.writer.row, 8, str(self.result))
            return True
        else:
            logger.error("post请求返回状态码为：" + str(res.status_code))
            print("post请求返回状态码为：" + str(res.status_code))
            return False

    def get(self, url, params=None):
        """
        get请求
        :param url:
        :param params:
        :return:
        """
        # 替换参数
        if params is None or params == '':
            pass
        else:
            params = self.__get_param(params)

        # 将url和参数拼接起来
        if not (url.startswith('http') or url.startswith('https')):
            url = self.url + '/' + url + "?" + params
        else:
            url = self.url + "?" + params

        # 执行get请求
        res = self.session.get(url, verify=False)
        self.result = res.content.decode('utf8')
        logger.info("执行结果: " + self.result)
        print("执行结果: " + self.result)
        try:
            # 将result的string格式转为json格式
            jsons = self.result
            jsons = jsons[jsons.find('{'):jsons.rfind('}') + 1]
            self.jsonres = json.loads(jsons)
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, str(jsons))
            return True
        except Exception as e:
            # 如果解析失败了，jsonres存储为上一次结果，需要清空
            self.jsonres = {}
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, str(self.result))
            return False

    def addheader(self, key, value):
        """
        向header中添加一组键值对
        :param key:要添加的键
        :param value:对应的值
        :return:
        """
        value = self.__get_param(value)
        self.session.headers[key] = value
        self.writer.write(self.writer.row, 7, 'PASS')
        self.writer.write(self.writer.row, 8, str(self.session.headers))
        logger.info("headers: " + str(self.session.headers))
        print("headers: " + str(self.session.headers))
        return True

    def removeheader(self, key):
        """
        从header中删除一个键值对
        :param key:要删除的键
        :return:
        """
        try:
            self.session.headers.pop(key)
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, str(self.session.headers))
            logger.info(str(self.session.headers))
            print(str(self.session.headers))
            return True
        except Exception as e:
            logger.error("没有 " + key + " 这个键在header存在！")
            print("没有 " + key + " 这个键在header存在！")
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, str(self.session.headers))
            return False

    def assertequals(self, key, value):
        """
        断言json结果里面某个键的值和value是否相等
        :param key:键
        :param value: value
        :return:
        """
        value = self.__get_param(value)
        res = str(self.result)
        try:
            res = str(jsonpath.jsonpath(self.jsonres, key)[0])
        except Exception as e:
            pass
        if res == str(value):
            logger.info("PASS")
            print("PASS")
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, res)
            return True
        else:
            logger.info("Fail")
            print("Fail")
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, "实际结果：" + res + " 预期结果：" + value)
            return False

    def assertcontains(self, key, value):
        value = self.__get_param(value)
        res = str(self.result)
        try:
            res = str(jsonpath.jsonpath(self.jsonres, key)[0])
        except Exception as e:
            pass
        if str(value) in res:
            logger.info("PASS")
            print("PASS")
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, res)
            return True
        else:
            logger.info("Fail")
            print("Fail")
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, "实际结果：" + res + " 预期结果：" + value)
            return False

    def savejson(self, jpath, p):
        """
        保存数据存进字典中：格式为key:value
        :param jpath:要保存的json里的键
        :param p: 保存后，调用参数的键
        :return:
        """
        try:
            self.params[p] = str(jsonpath.jsonpath(self.jsonres, jpath)[0])
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, str(self.params[p]))
            return True
        except Exception as e:
            logger.error("保存参数失败！找不到" + jpath + "对应的值")
            print("保存参数失败！找不到" + jpath + "对应的值")
            logger.exception(e)
            print(e)
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, str(self.jsonres))
            return False

    def __get_param(self, s):
        """
        按照一定的格式将字符串中{var}格式替换为变量var的值
        :param s: 要替换的字符串
        :return:
        """
        for key in self.params:
            s = s.replace('{' + key + '}', self.params[key])
        return s

    def __get_data(self, s):
        """
        参数以json格式传递进来
        :param s:
        :return:
        """
        # print(s)
        s = eval(s)
        return s

    def __get_data1(self, s):
        """
        默认标准参数s是以key=value&key1=value2的格式，如果不是，就原样返回
        :param s:
        :return:
        """
        flg = False
        param = {}
        p = s.split('&')
        try:
            for pp in p:
                ppp = pp.split("=")
                # if ppp[1].isdigit():
                #     param[ppp[0]] = int(ppp[1])
                # else:
                ppp_value = ''
                ppp_value = '='.join(ppp[1:])
                param[ppp[0]] = ppp_value
        except Exception as e:
            flg = True
            logger.warn("url参数格式不标准！")
            print("url参数格式不标准！")
            logger.exception(e)
            print(e)
        # print(param)
        # 如果符合标准格式返回处理后的param，否则，返回原样s
        if flg:
            s = s.encode('utf-8')
            return s
        else:
            return param

    def saveparams(self, key, value):
        """
        保存一些公共参数，以key:value的形式存储在字典params中
        :param key:
        :param value:
        :return:
        """
        try:
            self.params[key] = value
            logger.info(str(key) + ":" + str(self.params[key]))
            print(str(key) + ":" + str(self.params[key]))
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, "在params中存储key:value为 " + str(key) + ":" + str(self.params[key]))
            return True
        except Exception as e:
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, "key:value保存失败")
            return False

    def sleep(self, t):
        try:
            tt = int(t)
            time.sleep(tt)
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, "程序等待" + str(t) + "seconds")
            return True
        except Exception as e:
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, e)
            return False

