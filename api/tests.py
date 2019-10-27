# # from django.test import TestCase
#
# # Create your tests here.
#
# #
# # a = {1: 2, 4: 5}.items()
# # b = {2: 3}.items()
# # c = {3: 3}.items()
# # # print(list(a.items()).extend(b.items()))
# #
# #
# # d = sum([list(a), list(b), list(c)], [])
#
# # print(d)
#
# import json
#
# a = {1: [1, 2]}
# b = {1: [1, 2]}
# c = {3: 3}
# # d = sum([a,b,c],{})
# # print(d)
#
# print(a == b)
#
# for i in {1, 2, 1}:
#     print(i)
#
#
# class A():
#     pass
#
#
# a = A()
# b = A()
# print(a == b)
#
# a = {1, 2}
# print(a)
# a = {'slot': '5', 'model': 'S1AXNSAFB00549A     Samsung SSD 840 PRO Series              DXM0', 'capacity': '476.939',
#      'pd_type': 'SATA'}
# b = {'slot': '5', 'pd_type': 'SATA', 'capacity': '476.939',
#      'model': 'S1AXNSAFB00549A     Samsung SSD 840 PRO Series              DXM06B0Q', 'server_obj_id': 1}
# print(a == b)
#
# print(json.loads('{"1":2}'))
#
# a = {'server_obj_id': 1, 'slot': 'DIMM #7', 'manufacturer': 'Not Specified', 'speed': '667 MHz', 'capacity': 0.0,
#      'model': 'DRAM', 'sn': 'Not Specified'}
# b = {'capacity': 0, 'slot': 'DIMM #7', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified',
#      'sn': 'Not Specified', 'server_obj_id': 1}
# print(a == b)
#
# print('a' in 'b')
# import json
# import re
# regx = re.compile('[^|]*\|[^|]*')
# print(regx.match('1234qwer|').group())
# from api.utils import AES
# a=AES.encrypt('123')
# print(a,type(str(a)))
# b=AES.decrypt(b'%s'%(a))
# print(b)

#
# from redis import Redis
#
# conn = Redis(host='172.16.181.133')
# print(conn.get('jhc'))
# print(True + False + True)
print(chr(64))
