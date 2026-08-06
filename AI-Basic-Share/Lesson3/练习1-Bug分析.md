# 练习 1：Bug 分析

---

## 练习目标

使用 Copilot 分析一个带有 Bug 的代码，练习"提供完整上下文 → 让 AI 分析 → 人工验证"的流程。

---

## 练习步骤

1. 将下方示例代码保存为 `example_discount_bug.py`
2. 在 VS Code 中打开该文件
3. 在 Copilot Chat 中使用 Bug 分析 Prompt 模板提问
4. 阅读 Copilot 的分析结果
5. 对照代码验证分析是否准确

---

## Bug 分析 Prompt 模板

```
请根据以下信息分析 Bug 可能原因：

- 现象：调用 calculate_discount 时，部分订单的折扣金额计算结果不正确，有时多扣有时少扣
- 复现步骤：创建包含多个商品的订单，每个商品有不同的折扣率，调用折扣计算接口
- 期望结果：每个商品按各自折扣率计算折扣金额，合计正确
- 实际结果：部分订单折扣金额与预期不符
- 相关代码：见下方 example_discount_bug.py
- 错误日志：无报错日志，计算结果不正确

请输出：可能原因、验证方法、建议修改点、还需要补充的信息。
```

---

## 示例代码（含 Bug）

```python
# example_discount_bug.py
from decimal import Decimal, ROUND_HALF_UP
from typing import List


class OrderItem:
    def __init__(self, name: str, price: float, quantity: int, discount_rate: float = 0.0):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.discount_rate = discount_rate  # 0.0 ~ 1.0

    def subtotal(self) -> float:
        return self.price * self.quantity

    def discount_amount(self) -> float:
        return self.subtotal() * self.discount_rate

    def final_price(self) -> float:
        return self.subtotal() - self.discount_amount()


def calculate_discount(items: List[OrderItem]) -> dict:
    """
    计算订单折扣信息。
    """
    total_before_discount = sum(item.subtotal() for item in items)
    total_discount = sum(item.discount_amount() for item in items)
    total_after_discount = total_before_discount - total_discount

    # 四舍五入到两位小数
    total_before_discount = round(total_before_discount, 2)
    total_discount = round(total_discount, 2)
    total_after_discount = round(total_after_discount, 2)

    return {
        "total_before_discount": total_before_discount,
        "total_discount": total_discount,
        "total_after_discount": total_after_discount,
        "items_detail": [
            {
                "name": item.name,
                "subtotal": round(item.subtotal(), 2),
                "discount": round(item.discount_amount(), 2),
                "final": round(item.final_price(), 2),
            }
            for item in items
        ],
    }


# 测试用例
if __name__ == "__main__":
    items = [
        OrderItem("商品A", 19.99, 3, 0.1),   # 3件，10%折扣
        OrderItem("商品B", 29.99, 2, 0.15),  # 2件，15%折扣
        OrderItem("商品C", 9.99, 5, 0.0),    # 5件，无折扣
    ]

    result = calculate_discount(items)
    print("=== 订单折扣计算结果 ===")
    for detail in result["items_detail"]:
        print(f"{detail['name']}: 小计={detail['subtotal']}, "
              f"折扣={detail['discount']}, 最终={detail['final']}")
    print(f"\n合计(折扣前): {result['total_before_discount']}")
    print(f"总折扣: {result['total_discount']}")
    print(f"合计(折扣后): {result['total_after_discount']}")

    # 验证：折扣前 - 总折扣 = 折扣后
    expected = round(result["total_before_discount"] - result["total_discount"], 2)
    actual = result["total_after_discount"]
    print(f"\n验证: {result['total_before_discount']} - {result['total_discount']} = {expected}")
    print(f"实际 total_after_discount = {actual}")
    print(f"结果一致: {expected == actual}")
```

> 💡 **提示**：这段代码有一个浮点数精度相关的 Bug，运行测试用例就能发现。让 Copilot 分析看看它能不能找到问题所在。

---

## 练习引导问题

| 问题 | 你的回答 |
|------|----------|
| Copilot 是否找到了 Bug？ | |
| Bug 的根本原因是什么？ | |
| 为什么运行测试用例时验证会失败？ | |
| 建议的修复方法是什么？ | |
| 如果不用 Decimal，还有什么修复方式？ | |

---

## 打卡记录模板

```markdown
## 练习 1 打卡

- 练习内容：Bug 分析
- 使用的 Copilot 功能：Copilot Chat
- 提供的上下文：
- Copilot 分析是否准确：是 / 部分准确 / 不准确
- 我是否同意 Copilot 的分析：
- 我的收获：
- 疑问或想进一步学习的内容：
```
