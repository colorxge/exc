def change1(data, val):
    for i in range(len(data)):
        data[i] *= val
    return data

# print(change1(['q', 'a', 'f'], 5))

def range1(start, stop=None, step=1):
    if stop == None:
        stop = start
        start = 0

# print(max(1, -2, -3, key= lambda x:x**2)) # -3

# for i in range(5):
#     print(i, end='@@@@')

a = range(18)
print(a[2], a)

str.split()