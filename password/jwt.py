import jwt
import base64
import json
from jwt import algorithms


key = 'select'
token = jwt.encode({'payload': 'abc123'}, key, 'HS256')
print(token)
print(jwt.decode(token, key, algorithms=['HS256']))

header, payload, signature = token.split(b'.')
print(header)
print(payload)
print(signature)
print('+++++++++++++')

def addeq(b: bytes):
    """ 为Base64编码补齐等号"""
    rem = len(b) % 4
    return b + b'=' * rem

print('haader= ', base64.urlsafe_b64decode(addeq(header)))
print('payload=', base64.urlsafe_b64decode(addeq(payload)))
print('signature=', base64.urlsafe_b64decode(addeq(signature)))


# 根据jwt算法，重新生成签名
# 1 获取算法对象
alg = algorithms.get_default_algorithms()['HS256']
newkey = alg.prepare_key(key)
print(key)
print(newkey)

# 2 获取前两部分 header.payload
signing_input, _, _ = token.rpartition(b'.')
print(signing_input)

# 3 使用key签名
signature = alg.sign(signing_input, newkey)
print('++++++++++++')
print(signature)
print(base64.urlsafe_b64encode(signature))

print('++++++++++++')
print(base64.urlsafe_b64encode(json.dumps({'payload': 'abc123'}).encode()))
