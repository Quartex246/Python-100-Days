# advanced counter by using lists
# 6 dices, throw 6000 times, count the number of times each number appears
import random

counters = [0] * 6  # 将0这个元素重复了6次，创建了一个长度为6的列表，用于记录每个点数出现的次数
                    # 结果为 [0, 0, 0, 0, 0, 0]
# 模拟掷色子记录每种点数出现的次数
for _ in range(6000):
    face = random.randrange(1, 7)   # 生成1到6之间的随机整数，表示掷色子的结果
    counters[face - 1] += 1         # 列表下标从 0 开始，但骰子的点数从 1 开始
                                    # 方括号为列表的第几个元素，face - 1表示将掷出的点数减去1，得到对应的列表下标
# 输出每种点数出现的次数
for face in range(1, 7):
    print(f'{face}点出现了{counters[face - 1]}次')