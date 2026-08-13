# 练习 2：改写单元测试 Prompt

---

## 练习目标

将模糊的单元测试生成需求改写成包含五要素的清晰 Prompt。

---

## 练习步骤

1. 阅读下方的原始模糊 Prompt 和提供的上下文素材
2. 运用五要素改写 Prompt
3. 将改写后的 Prompt 输入 Copilot
4. 对比两次输出结果的质量差异

---

## 原始模糊 Prompt

> 帮我写单元测试

---

## 提供的上下文素材

```python
# utils/price_calculator.py

def calculate_shipping_cost(weight: float, destination: str, express: bool = False) -> float:
    """
    计算运费。

    Args:
        weight: 包裹重量（kg）
        destination: 目的地（"domestic" 国内 / "international" 国际）
        express: 是否加急

    Returns:
        运费金额

    Raises:
        ValueError: weight <= 0 或 destination 不合法
    """
    if weight <= 0:
        raise ValueError("重量必须大于 0")

    if destination not in ("domestic", "international"):
        raise ValueError("目的地不合法，仅支持 domestic 和 international")

    if destination == "domestic":
        base = 10.0
        per_kg = 2.0
    else:
        base = 30.0
        per_kg = 5.0

    cost = base + weight * per_kg

    if express:
        cost *= 1.5

    return round(cost, 2)
```

---

## 改写引导

请按五要素结构改写：

| 要素 | 思考方向 |
|------|----------|
| **角色** | 让 AI 以什么身份写测试？ |
| **任务** | 具体要 AI 做什么？生成什么框架的测试？ |
| **上下文** | 上面提供的代码中哪些信息需要包含？函数签名、异常情况？ |
| **约束** | 测试框架、命名风格、覆盖范围？ |
| **输出格式** | 希望 AI 按什么结构输出？ |

---

## 参考改写示例（练习后查看）

<details>
<summary>点击展开参考示例</summary>

```
请以 Python 开发人员的身份，为以下函数生成 pytest 单元测试。

函数：calculate_shipping_cost(weight, destination, express=False)
功能：计算运费
代码见下方。

要求：
- 使用 pytest 框架
- 测试文件命名为 test_price_calculator.py
- 覆盖以下场景：
  1. 正常场景（国内普通、国际普通、国内加急、国际加急）
  2. 异常场景（weight <= 0、destination 不合法）
  3. 边界场景（weight 为 0 的边界、weight 为小数）
- 测试函数命名格式：test_计算运费_xx场景
- 不要 mock，直接调用函数

输出格式：
- 完整的测试代码
- 每个测试用例的说明注释
```
</details>

---

## 打卡记录模板

```markdown
## 练习 2 打卡

- 练习内容：改写单元测试 Prompt
- 原始 Prompt：帮我写单元测试
- 改写后的 Prompt：
- AI 输出质量对比：改写前（差 / 一般 / 好） 改写后（差 / 一般 / 好）
- 我的收获：
- 疑问或想进一步学习的内容：
```
