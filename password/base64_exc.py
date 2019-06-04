import base64


# 编码解码
s = 'adga大哥gadfly-2341，。/'

print(base64.b64encode(s.encode()))
# b'YWRnYeWkp+WTpWdhZGZseS0yMzQx77yM44CCLw=='

s1 = 'YWRnYeWkp+WTpWdhZGZseS0yMzQx77yM44CCLw=='
print(base64.b64decode(s1).decode())
# adga大哥gadfly-2341，。/


# urlsafe 编码解码
s2 = b'i\xb7\x1d\xfb\xef\xff'
print(base64.b64encode(s2))
# b'abcd++//'

print(base64.urlsafe_b64encode(s2))
# b'abcd--__'

# 有些Base64会把末尾的 = 去掉,如何加回来
# s1 = 'YWRnYeWkp+WTpWdhZGZseS0yMzQx77yM44CCLw=='
s3 = 'YWRnYeWkp+WTpWdhZGZseS0yMzQx77yM44CCLw'

def safe_base64_decode(s:str):
    length = len(s) % 4
    s = s + length * '='
    return base64.b64decode(s).decode()

print(safe_base64_decode(s3))
