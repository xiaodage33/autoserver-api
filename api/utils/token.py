import time
import hashlib
from api.utils import AES
import re

key_record = {
    # "548aa8aeb09db415d168b1010016a38c" : [123123143.123,user_obj]
}
server_token = "vdgsavhdsbhafbsdbfhbdshfbsd"


def auth_token(token):
    response = {'flag': False, 'msg': None}
    server_time = time.time()
    # client_md5_header = AES.decrypt(request.META.get('X-Token'))
    client_md5_header = AES.decrypt(b'' % token)
    regx = re.compile('[^|]+|[^|]+')
    if not regx.match(client_md5_header):
        response['msg'] = '无效token'
        return response
    client_md5_token, client_time = client_md5_header.split('|')
    client_time = float(client_time)
    if server_time - client_time > 10:
        response['msg'] = 'token已过期'
        return response

    tmp = "%s|%s" % (server_token, client_time)
    m = hashlib.md5()
    m.update(bytes(tmp, encoding='utf-8'))
    server_md5_token = m.hexdigest()

    if server_md5_token != client_md5_token:
        response['msg'] = '无效token'
        return response

    for k in list(key_record.keys()):
        if server_time > key_record[k]:
            del key_record[k]

    if client_md5_token in key_record:
        response['msg'] = 'token已被占用'

        return response

    key_record[client_md5_token][0] = client_time + 10
    response['flag'] = True
    return response


def get_token(user_obj):
    server_time = time.time()
    token = '%s|%s' % (server_token, server_time)
    key_record[token] = [server_time, user_obj]
    return str(AES.encrypt(token))


def parse_token(token):
    return key_record[AES.decrypt(token)][1]
