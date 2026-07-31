# Online_Show

## 业务背景

本文件统一使用 Python 业务场景：一个简单的线上订单管理系统。配套示例代码文件 `Online_Show.py` 提供实际函数、数据和业务上下文，方便课堂中直接打开、选中、补全。

场景主题：
- 订单校验
- 金额计算
- 已支付订单统计
- 订单创建
- 生成 SQL 报表

---

## 1. 场景一：代码补全

### 讲解目标
让学员理解“先写意图，再补全”的思路，并观察 Copilot 如何根据函数名、注释和文件上下文补全 Python 业务逻辑。

### 示例内容
请打开 `Online_Show.py`，定位到 `get_valid_order_count` 函数：

```python
def get_valid_order_count(user_id: str, start_date: str, end_date: str) -> int:
    """根据用户ID和日期范围统计已支付订单数量。"""
    # TODO: 根据 sample_orders 完成统计逻辑
    pass
```

### 教学步骤
1. 先让学员确认业务意图：统计已支付订单、按用户、按日期范围。
2. 让 Copilot 在 `Online_Show.py` 中补全 `get_valid_order_count` 函数体。
3. 检查生成结果是否包含：日期解析、状态过滤、用户过滤、统计逻辑。
4. 实际运行并验证：`get_valid_order_count("U001", "2026-07-01", "2026-07-31")` 应返回正确数量。

### 讲解要点
- 函数名要具体，`get_valid_order_count` 清晰表达了“已支付订单数量”。
- 注释和 TODO 是 Copilot 生成上下文的重要线索。
- 补全后要人工验证边界条件，比如日期格式、空结果、未付款订单。

---

## 2. 场景二：解释代码

### 讲解目标
教会学员用选中代码提问，让 Copilot 帮助快速建立代码结构理解。

### 示例内容
请在 `Online_Show.py` 中选中 `calculate_order_total` 函数：

```python
def calculate_order_total(items: List[Dict], discount_rate: Decimal = Decimal("0.0")) -> Dict[str, Decimal]:
    subtotal = sum(item["price"] * item["quantity"] for item in items)
    if discount_rate < 0 or discount_rate > 1:
        raise ValueError("折扣率必须在0到1之间")
    discounted = (subtotal * (Decimal("1.0") - discount_rate)).quantize(Decimal("0.01"))
    tax = (discounted * Decimal("0.08")).quantize(Decimal("0.01"))
    total = (discounted + tax).quantize(Decimal("0.01"))
    return {
        "subtotal": subtotal.quantize(Decimal("0.01")),
        "discount_rate": discount_rate,
        "discounted": discounted,
        "tax": tax,
        "total": total,
    }
```

### 示例 Prompt
请解释这段代码的处理流程，重点说明输入参数、主要分支、返回值和可能异常。

### 讲解要点
- 输出结构建议：一句话总结、分步骤说明、关键变量含义、可能异常。
- 让学员对照代码逐行确认生成的解释。
- 这种方式适合新人理解业务函数，也适合审查现有代码。

---

## 3. 场景三：生成样板代码

### 讲解目标
让学员学会用 Copilot 生成重复性结构代码，如订单请求校验、创建订单、DTO 结构。

### 示例内容
请在 `Online_Show.py` 中定位到 `validate_order_payload` 或 `create_order` 函数，使用现有业务字段作为提示：

```python
payload = {
    "user_id": "U003",
    "items": [
        {"sku": "A100", "price": Decimal("29.99"), "quantity": 1},
    ],
    "discount_rate": Decimal("0.05"),
    "order_date": "2026-07-15",
}
```

示例 prompt：
生成一个 `validate_order_payload(payload: Dict) -> List[str]` 的校验函数，检查 `user_id`、`items`、`sku`、`quantity`、`price`、`discount_rate`、`order_date`。

### 教学步骤
1. 给出订单请求字段说明。
2. 让 Copilot 生成校验函数或订单创建函数的起始代码。
3. 让学员补充业务规则，例如 `discount_rate` 范围、`items` 非空、`price` 必须大于 0。

### 讲解要点
- 样板代码适合由 Copilot 生成，业务规则必须由人来判断。
- 人负责设计校验项，AI 帮忙把重复条件写成代码。
- 对生成结果进行人工修正和补充，确保符合实际订单逻辑。

---

## 4. 场景四：生成注释和文档

### 讲解目标
让学员通过 Copilot 生成 Python 函数说明和文档初稿，提升代码可读性。

### 示例内容
请选中 `create_order` 或 `calculate_order_total` 的函数签名与注释位置：

```python
def create_order(payload: Dict) -> Dict:
    errors = validate_order_payload(payload)
    if errors:
        raise ValueError(f"订单数据无效: {errors}")
    return {
        "order_id": f"O{len(sample_orders) + 1001}",
        "user_id": payload["user_id"],
        "items": payload["items"],
        "discount_rate": payload.get("discount_rate", Decimal("0.0")),
        "status": ORDER_STATUS_PENDING,
        "created_at": parse_date(payload["order_date"]),
    }
```

### 示例 Prompt
根据选中代码生成函数说明，包含功能、参数说明、返回值、异常情况，语言保持简洁。

### 讲解要点
- 让 Copilot 生成注释后，再手动过滤掉“废话”和无意义描述。
- 注释适合公共接口、关键业务流程、复杂参数。
- 仍需人工校对，避免将 AI 生成内容直接当成最终文档。

---

## 5. 场景五：生成 SQL

### 讲解目标
让学员掌握“给出表结构和业务要求，再让 Copilot 生成 SQL”的正确方式。

### 示例内容
假设订单报表对应的表结构为：

```sql
orders(order_id, user_id, status, order_amount, discount_rate, created_at)
users(user_id, name, region)
```

### 示例 Prompt
根据上面的表结构，生成按用户统计本月已支付订单总金额的 SQL，要求统计结果按金额降序。

### 讲解要点
- 必须提供表名、字段名、字段含义。
- 只给业务需求容易生成“假字段”或错误关联。
- 生成后要人工确认字段是否准确、关联条件是否合理。

---

## 课堂演练建议
- 让学员实际在 VS Code 中打开 `Online_Show.py`，选中代码并使用 Copilot 补全、解释、改写。
- 场景一到场景四均使用同一个 Python 业务场景，帮助学员建立连续认知。
- 强调“工具辅助，人工负责”的理念：AI 负责出结构和建议，人负责判断边界、业务和正确性。
