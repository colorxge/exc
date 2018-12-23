# 使用线性递归计算序列元素的和

S = [1, 2, 3, 2, 4, 3, 5, 4, 6, 7, 8, 7, 6, 5]


def linear_sum(S, n):
    if n == 0:
        return 0
    else:
        return linear_sum(S, n-1) + S[n-1]


# print(linear_sum(S, len(S)))
