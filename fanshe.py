#encoding:utf-8
from test import Http
import inspect

http = Http()
# 反射对象的函数
func = getattr(http,'post')
#直接传参即可
func(1,2)
# 获取反射关键字的描述
print(func.__doc__)

# 获取反射关键字的参数
args = inspect.getfullargspec(func).__str__()
print(args)
#截取args的含有参数的内容
args = args[args.find('['):args.rfind(', varargs')]
print(args)  #['self', 'a', 'b']
args = eval(args)
# 去掉self
args.remove('self')
print(args) #['a', 'b']

