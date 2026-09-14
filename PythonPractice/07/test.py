### 例子1：100以内的素数

### **说明**：素数指的是只能被 1 和自身整除的正整数（不包括 1），之前我们写过判断素数的代码，这里相当于是一个升级版本。

for num in range(2, 100):               # 限定范围：不包括1到100
    is_prime = True                     # 先设定质数状态为真

    for i in range(2, int (num ** 0.5) + 1):            # 限定范围：让 i 从 2 开始，一直取到 num 的平方根向下取整为止，用来逐个试除 num，判断它是不是素数。
        if num % i == 0:                                # 判定标准：无法整除
            is_prime = False
            break
    if is_prime:                                        # 如果是质数
        print(num)                                      # 打印出来