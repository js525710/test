# encoding:utf-8
import requests,json
session = requests.session()
requests.packages.urllib3.disable_warnings()
session.headers['content-type'] = 'application/x-www-form-urlencoded'
session.headers['user-agent']= "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
session.headers['x-zse-83'] = '3_2.0'
# session.headers['cookie'] = '_zap=dd8c44b8-081d-4833-9ac5-51e85946bf31; _xsrf=d93f3b70-01e1-4426-ad51-c3223daca9df; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1584083865,1584086535,1584088014,1584088126; _ga=GA1.2.591981928.1584088166; _gid=GA1.2.1599103079.1584088166; d_c0="ADDYj3bU9BCPTtJKL_c-NBusyQP04A5oV-o=|1584088165"; tst=r; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1584091821; capsion_ticket="2|1:0|10:1584091826|14:capsion_ticket|44:OTRlMDNjMzg1NmNlNGRmZGIyY2VjZWE3NDkwMTc4ZDc=|b38182f272595a053c8cf4a6d4a68755e8607e64823774fffc655beaf25ea7e3"; KLBRSID=ca494ee5d16b14b649673c122ff27291|1584091840|1584088165'
# session.headers['accept'] = '*/*'
# session.headers['x-xsrftoken']= 'd93f3b70-01e1-4426-ad51-c3223daca9df'
print(session.headers)

res = session.post("https://www.zhihu.com/udid")
# print(session.cookies)
print(res.text)

res = session.get("https://www.zhihu.com/api/v3/oauth/captcha?lang=cn")
print(res.text)
# print(session.cookies)

res = session.post("https://www.zhihu.com/api/v3/oauth/sign_in",data='AhYqk4U0g_LxcTYhKUVBErS0cT2tEgNmqgSMxU9qkLk9-qNZsUO1iugZoGVVxhYq8Ln9k4U0gXLxcTYhBupGeheVkCN_evx9BLfBFUCG-qVGNCNMMTYhXg9hgqxOcvSMccxGcrU0g6SYXqYhqbO8ArU0g02VShx9BLf8igXGQwOfSTYh1X2qS09yr0p_XqYhyhomogcMUuppkLPqfRtqo6r0o0FXr8tyihYqk4R92LkYJwNm8CSMcrU0gLNxS_S8MTxq6Tr82T2fr_N01Mt0Uhr0nCtYHBxq8XO8Q4H02XSxgut9BLfBkvwGUbOYDq3q8Ln8gcgZcUS_iD3ZpvS8Xg9hgqxOcvSMMTYhceuyo8Fp67t0K7Yqr6S0gRo9U9oMzcO1erU0g_xO-GoMBwxMXg9hguoLevwGXwNM3rU0gRtxguFqm0YBrAHqgg2f2Txy0qtq6A98S8Yfo8OBhq28Xg9hHgOGebOBtrS8')
# print(res.text.encode("utf-8").decode("unicode_escape"))
print("*********")
print(res.content.decode('utf-8'))