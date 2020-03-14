#encoding:utf-8
from suds.client import Client
from suds.xsd.doctor import Import,ImportDoctor
import json

# # 通过wsdl解析出当前webservice服务提供的接口
# client = Client("http://112.74.191.10:8081/inter/SOAP?wsdl")
# #通过webservice服务的client对象调用服务
# #请求auth接口
# res = client.service.auth()
# jsonres = json.loads(res)
# print(jsonres)
# # 请求login接口
# client = Client("http://112.74.191.10:8081/inter/SOAP?wsdl",headers={"token":jsonres['token']})
# res = client.service.login('Will','123456')
# jsonres = json.loads(res)
# print(res)
# #查询
# res = client.service.getUserInfo(jsonres['userid'])
# print(res)
# #退出
# res = client.service.logout()
# print(res)

# 反射
# #请求auth
# client = Client("http://112.74.191.10:8081/inter/SOAP?wsdl")
# res = client.service.__getattr__('auth')()
# jsonres = json.loads(res)
# print(jsonres)
# #login
# client = Client("http://112.74.191.10:8081/inter/SOAP?wsdl",headers={"token":jsonres['token']})
#
# list1 = ['Will','123456']
# res = client.service.__getattr__('login')(*list1)
# jsonres = json.loads(res)
# print(jsonres)
# #查询
# res = client.service.__getattr__('getUserInfo')(jsonres['userid'])
# print(res)
# # 退出
# res = client.service.__getattr__('logout')()
# print(res)

#
imp = Import('http://www.w3.org/2001/XMLSchema',location='http://www.w3.org/2001/XMLSchema.xsd')
imp.filter.add('http://WebXml.com.cn/')
doctor = ImportDoctor(imp)
client = Client('http://www.webxml.com.cn/WebServices/WeatherWebService.asmx?wsdl',doctor=doctor)
res = client.service.__getattr__('getSupportCity')('江苏')
print(res)