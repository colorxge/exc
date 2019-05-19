import bcrypt
import datetime


password = b'123456'

# 每次拿到的盐都不一样
print(1, bcrypt.gensalt())
print(2, bcrypt.gensalt())

salt = bcrypt.gensalt()

# 拿到相同的盐，计算得到的秘文相同
print('========= same salt ===========')
x = bcrypt.hashpw(password, salt)
print(3, x)
y = bcrypt.hashpw(password, salt)
print(4, y)

# 每次拿到的盐不同，计算生成的密文也不一样
print('=========diff salt ============')
x = bcrypt.hashpw(password, bcrypt.gensalt())
print(5, x)
y = bcrypt.hashpw(password, bcrypt.gensalt())
print(6, y)

print('===============================')
# 校验
print(bcrypt.checkpw(password, x), len(x))
print(bcrypt.checkpw(password + b' ', x), len(x))

print('===============================')
# 生成密码计算时长
start = datetime.datetime.now()
z = bcrypt.hashpw(password, bcrypt.gensalt())
delta = (datetime.datetime.now() - start).total_seconds()
print(delta)
print(7, z)

# 解析密码计算时长
print('==============================')
start = datetime.datetime.now()
z = bcrypt.checkpw(password, y)
delta = (datetime.datetime.now() - start).total_seconds()
print(delta)
print(8, z)

# 加解密非常耗时，不易暴力破解
