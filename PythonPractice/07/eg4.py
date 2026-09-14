### 例子4：百钱百鸡问题

# 要求：用 100 块钱买 100 只鸡，问公鸡、母鸡、小鸡各有多少只？
# 公鸡5元/只，母鸡3元/只，小鸡1元/3只。

for cock in range(0, 21):  # 公鸡最多20只
    for hen in range(0, 34):  # 母鸡最多33只
        chick = 100 - cock - hen  # 小鸡数量，最多买100只
        if cock * 5 + hen * 3 + chick / 3 == 100:  # 满足花费100元
            print(f"公鸡：{cock}只，母鸡：{hen}只，小鸡：{chick}只")