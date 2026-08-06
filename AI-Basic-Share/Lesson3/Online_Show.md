# Online_Show

## 业务背景

本文件统一使用 Python 业务场景：一个简单的线上订单管理系统。配套示例代码文件 `Online_Show.py` 提供实际函数、数据和业务上下文，方便课堂中直接打开、选中、操作。

场景主题：
- 折扣计算（含 Bug）
- 批量订单导入（异常日志）
- 订单工具方法（单元测试）
- 优惠券计算（测试用例补充）
- 退款处理（重构建议）
- 用户管理 API（代码审查）

---

## 1. 场景一：Bug 分析

### 讲解目标
让学员理解"提供完整上下文 → 让 AI 分析 → 人工验证"的 Bug 分析流程，并观察 Copilot 能否定位浮点数精度问题。

### 示例内容
请打开 `Online_Show.py`，定位到 `calculate_discount_v2` 函数：

```python
def calculate_discount_v2(price: float, quantity: int, discount_rate: float) -> dict:
    subtotal = price * quantity
    discount = subtotal * discount_rate
    final = subtotal - discount
    return {
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "final": round(final, 2),
    }
```

### 示例 Prompt
```
请根据以下信息分析 Bug 可能原因：

- 现象：调用 batch_calculate_discount 时，部分订单的折扣金额计算结果不正确，有时多扣有时少扣
- 复现步骤：创建包含多个商品的订单，每个商品有不同的折扣率，调用折扣计算接口
- 期望结果：每个商品按各自折扣率计算折扣金额，合计正确
- 实际结果：部分订单折扣金额与预期不符
- 相关代码：见 Online_Show.py 中 calculate_discount_v2 和 batch_calculate_discount
- 错误日志：无报错日志，计算结果不正确

请输出：可能原因、验证方法、建议修改点、还需要补充的信息。
```

### 教学步骤
1. 让学员确认业务意图：计算每个商品的折扣金额。
2. 在 Copilot Chat 中粘贴上述 Prompt。
3. 检查 Copilot 是否指出浮点数精度问题。
4. 运行 `Online_Show.py` 观察输出，验证 `subtotal - discount != final` 的问题。
5. 讨论修复方案：改用 `Decimal` 还是用 `round` 调整计算顺序。

### 讲解要点
- Bug 分析的关键是提供完整上下文：现象、步骤、代码、日志。
- 浮点数精度是经典问题，Copilot 通常能识别，但需要人工确认。
- AI 给的是排查线索，不是最终结论。

---

## 2. 场景二：异常日志分析

### 讲解目标
让学员学会用 Copilot 分析异常日志，区分直接原因和根因，并给出排查步骤。

### 示例内容
请在 `Online_Show.py` 中定位到 `batch_import_orders` 函数，了解其逻辑后，将以下日志复制到 Copilot Chat：

```
2026-07-12 10:15:23.456 ERROR [http-nio-8080-exec-5] c.e.s.OrderService - 批量导入订单失败
java.sql.BatchUpdateException: Batch entry 0: Duplicate entry 'ORD-20260712-0001' for key 'orders.order_no'
    at com.mysql.cj.jdbc.StatementImpl.executeBatch(StatementImpl.java:1026)
    at org.springframework.jdbc.core.JdbcTemplate.batchUpdate(JdbcTemplate.java:1524)
    at com.example.service.OrderService.batchImport(OrderService.java:87)

2026-07-12 10:15:23.458 WARN  [http-nio-8080-exec-5] c.e.s.OrderService - 批量导入第 1 条记录时发生唯一键冲突，订单号: ORD-20260712-0001
2026-07-12 10:15:23.459 INFO  [http-nio-8080-exec-5] c.e.s.OrderService - 已导入: 0 条，失败: 1 条，跳过: 99 条
```

### 示例 Prompt
```
请分析以下异常日志，按以下格式输出：

- 错误摘要
- 关键异常位置
- 可能原因排序（按概率从高到低）
- 建议检查项
- 需要补充的日志或配置

日志内容：
[粘贴上方日志]
```

### 教学步骤
1. 让学员先看日志，自己判断直接原因是什么。
2. 在 Copilot Chat 中粘贴 Prompt 和日志。
3. 对比 Copilot 的分析和自己的判断。
4. 讨论：为什么批量导入第 1 条就失败了？代码层面可以怎么改进？

### 讲解要点
- 日志分析最常见的问题是信息不完整，要保留异常堆栈和时间顺序。
- 要求 AI 区分"直接原因"和"根因猜测"。
- 固定输出格式可以减少废话，也方便团队交流。

---

## 3. 场景三：单元测试生成

### 讲解目标
让学员学会用 Copilot 为方法生成单元测试，覆盖正常、异常、边界场景。

### 示例内容
请在 `Online_Show.py` 中选中 `OrderUtils` 类的 `mask_phone` 方法：

```python
@staticmethod
def mask_phone(phone: str) -> str:
    if not phone or len(phone) != 11:
        return phone
    return phone[:3] + "****" + phone[7:]
```

### 示例 Prompt
```
请为选中的 mask_phone 方法生成 pytest 单元测试，覆盖以下场景：

- 正常输入（11 位手机号）
- 空字符串
- 不足 11 位
- 超过 11 位
- 包含非数字字符
- 带空格或特殊符号

测试文件命名为 test_online_show.py，使用 pytest 框架。
```

### 教学步骤
1. 选中 `mask_phone` 方法。
2. 在 Copilot Chat 中输入 Prompt。
3. 检查生成的测试用例是否覆盖了所有场景。
4. 将测试代码保存为 `test_online_show.py` 并运行。
5. 讨论：哪些边界条件 AI 遗漏了？

### 讲解要点
- Copilot 生成测试很有用，但最容易出错的是断言不准确。
- 生成后一定要运行测试并检查业务含义。
- 可以尝试对 `format_order_id`、`parse_order_date` 等不同方法重复练习。

---

## 4. 场景四：测试用例补充

### 讲解目标
让学员学会用 Copilot 从需求描述中拆解测试点，练习"AI 列清单，人做判断"。

### 示例内容
请在 `Online_Show.py` 中定位到 `calculate_coupon_discount` 函数，了解其业务规则：

```python
def calculate_coupon_discount(
    subtotal: Decimal,
    coupon_type: str,      # "fixed" / "percent" / "threshold"
    coupon_value: Decimal,
    user_level: str = "normal",  # "normal" / "vip"
) -> Dict:
```

### 示例 Prompt
```
请根据以下需求生成测试点：

- 功能说明：优惠券折扣计算
- 输入字段：订单金额(subtotal)、优惠券类型(coupon_type)、优惠值(coupon_value)、用户等级(user_level)
- 业务规则：
  1. fixed：固定金额减免，减免金额不能超过订单金额
  2. percent：百分比折扣，折扣率不能超过 50%
  3. threshold：满减，最低消费 100 元
  4. VIP 用户在计算结果上额外打 9 折
  5. 所有金额保留两位小数
- 异常处理：无效优惠券类型、负数金额、超出范围
- 权限要求：无

请按正常场景、异常场景、边界场景输出。
```

### 教学步骤
1. 让学员先自己思考有哪些测试点。
2. 在 Copilot Chat 中粘贴 Prompt。
3. 对比 AI 生成的测试点和自己的清单。
4. 讨论：AI 遗漏了什么？哪些测试点 AI 列得比你好？

### 讲解要点
- 测试人员可以把 AI 当成"补漏助手"。
- 关键是把业务规则写清楚，否则 AI 只能生成通用测试点。
- 人负责判断业务正确性，AI 负责从不同角度列清单。

---

## 5. 场景五：重构建议

### 讲解目标
让学员学会"先分析问题再决定改什么"的重构思路，而不是直接让 AI 改写代码。

### 示例内容
请在 `Online_Show.py` 中选中 `legacy_process_refund` 函数（全部代码）：

```python
def legacy_process_refund(refund_data: dict) -> dict:
    # 这个函数太长了，做了太多事情
    # 验证退款数据
    if not refund_data:
        return {"code": 400, "msg": "退款数据不能为空"}
    # ...（大量代码）
```

### 示例 Prompt
```
请分析选中代码的可维护性问题。

请输出：
- 主要问题
- 可以重构的点
- 每个重构点的收益
- 可能风险
- 建议的最小修改步骤

不要直接大幅改写代码。
```

### 教学步骤
1. 让学员先自己看代码，感受可维护性问题。
2. 在 Copilot Chat 中粘贴 Prompt。
3. 阅读 Copilot 的分析结果。
4. 讨论：最大的问题是什么？如果让你重构，你会先改哪一部分？
5. 可以尝试让 Copilot 只重构其中一个子问题（如提取验证逻辑）。

### 讲解要点
- 重构不能从"帮我重构这段代码"开始。
- 先让 AI 识别问题，再由人决定改哪一部分。
- 强调"小范围重构，逐步验证"的原则。

---

## 6. 场景六：代码审查辅助

### 讲解目标
让学员学会用 Copilot 做第一轮代码审查，按严重程度排序，辅助人工 Review。

### 示例内容
请在 `Online_Show.py` 中选中 `create_user_api` 和 `get_user_api` 函数：

```python
def create_user_api(request_body: str) -> str:
    # ...（含多个代码质量问题）
```

### 示例 Prompt
```
请从以下角度审查选中代码：

- 正确性
- 边界条件
- 异常处理
- 可读性
- 测试覆盖

请按严重程度排序，并说明每个问题为什么需要关注。
```

### 教学步骤
1. 让学员先自己看代码，尝试找出问题。
2. 在 Copilot Chat 中粘贴 Prompt。
3. 对比 Copilot 找出的问题和自己的发现。
4. 讨论：严重程度最高的问题是什么？有没有 Copilot 没发现的问题？
5. 讨论 AI 审查和人工审查各自的优势。

### 讲解要点
- AI 适合做第一轮扫查，但不能替代人工 Review。
- 让 AI 按严重程度排序，避免输出一堆风格建议。
- 重点关注可能导致 Bug 的问题，而不是代码风格。

---

## 课堂演练建议

| 场景 | 对应练习 | 建议时长 | 操作方式 |
|------|----------|----------|----------|
| Bug 分析 | [练习1](练习1-Bug分析.md) | 10min | Copilot Chat 粘贴 Prompt |
| 异常日志分析 | [练习2](练习2-异常日志分析.md) | 10min | Copilot Chat 粘贴日志 |
| 单元测试生成 | [练习3](练习3-单元测试生成.md) | 15min | 选中代码 → Copilot Chat |
| 测试用例补充 | [练习4](练习4-测试用例补充.md) | 10min | Copilot Chat 粘贴需求 |
| 重构建议 | [练习5](练习5-重构建议.md) | 15min | 选中代码 → Copilot Chat |
| 代码审查辅助 | [练习6](练习6-代码审查辅助.md) | 10min | 选中代码 → Copilot Chat |

- 所有场景均使用 `Online_Show.py` 中的同一业务域，帮助学员建立连续认知。
- 建议按顺序演示，每个场景 5~8 分钟，剩余时间让学员动手练习。
- 强调"工具辅助，人工负责"的理念：AI 负责提供线索和初稿，人负责判断和落地。
