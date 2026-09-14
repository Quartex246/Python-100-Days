### 例子5：CRAPS赌博游戏

# > **说明**：CRAPS又称花旗骰，是美国拉斯维加斯非常受欢迎的一种的桌上赌博游戏。
# > 
# > 该游戏使用两粒骰子，玩家通过摇两粒骰子获得点数进行游戏。
# > 
# > 简化后的规则是：玩家第一次摇骰子如果摇出了 7 点或 11 点，玩家胜；
# > 
# > 玩家第一次如果摇出 2 点、3 点或 12 点，庄家胜；
# > 
# > 玩家如果摇出其他点数则游戏继续，玩家重新摇骰子，如果玩家摇出了 7 点，庄家胜；
# > 
# > 如果玩家摇出了第一次摇的点数，玩家胜；
# > 
# > 其他点数玩家继续摇骰子，直到分出胜负。

# > 为了增加代码的趣味性，我们设定游戏开始时玩家有 1000 元的赌注，

# > 每局游戏开始之前，玩家先下注，如果玩家获胜就可以获得对应下注金额的奖励，如果庄家获胜，玩家就会输掉自己下注的金额。游戏结束的条件是玩家破产（输光所有的赌注）。
import random

money = 1000  # 玩家初始资金
while money > 0:
    print(f"你当前的资金为：{money}元")
    if money <= 0:
        print("你已经破产，游戏结束！")
        break
    while True:
        bet = int(input("请输入你的下注金额（必须小于等于你当前的资金）(输入00获取帮助)："))

        if input == 00:
            help_code = int(input("请输入帮助选项（1-3）："))
            print("1 - 退出游戏")
            print("2 - 查询余额")
            print("3 - 继续游戏")
            match help_code:
                case 1:
                    print("退出游戏")
                    exit()
                case 2:
                    print(f"你当前的资金为：{money}元")
                case 3:
                    print("继续游戏")

                case _:
                    print("无效的帮助选项，请重新输入！")

        if 0 > bet or bet > money:
            print("下注金额无效，请重新输入！")
            break

        first_point = random.randint(1, 6) + random.randint(1, 6)  # 玩家第一次摇骰子
        print(f"你第一次摇出的点数是：{first_point}")
        if first_point == 7 or first_point == 11:
            print("恭喜你，你赢了！")
            money += bet
        elif first_point == 2 or first_point == 3 or first_point == 12:
            print("很遗憾，你输了！")
            money -= bet
        else:
            print("游戏继续，你需要再次摇骰子。")
            while True:
                next_point = random.randint(1, 6) + random.randint(1, 6)  # 玩家再次摇骰子
                print(f"你摇出的点数是：{next_point}")
                if next_point == 7:
                    print("很遗憾，你输了！")
                    money -= bet
                    break
                elif next_point == first_point:
                    print("恭喜你，你赢了！")
                    money += bet
                    break