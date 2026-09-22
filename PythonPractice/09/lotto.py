# 双色球是由中国福利彩票发行管理中心发售的乐透型彩票
# 每注投注号码由`6`个红色球和`1`个蓝色球组成。
# 红色球号码从`1`到`33`中选择，蓝色球号码从`1`到`16`中选择。
# 每注需要选择`6`个红色球号码和`1`个蓝色球号
import random

redNumbers = list(range(1,34))
blueNumber = list(range(1,17))

for _ in range(5):
    redBalls = random.sample(redNumbers, 6)
    blueBall = random.choice(blueNumber)
    print(f"红球: {sorted(redBalls)}, 蓝球: {blueBall}")