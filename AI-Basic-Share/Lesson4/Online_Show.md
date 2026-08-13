# Online_Show

## 业务背景

本文件统一使用 Python 业务场景：一个简单的线上订单管理系统。配套示例代码文件 `Online_Show.py` 提供实际函数、数据和业务上下文，方便课堂中直接打开、选中、操作。

本课主题是 **Prompt 基础**，重点演示：
- 好 Prompt 的五要素（角色、任务、上下文、约束、输出格式）
- 模糊需求改写
- 输出格式控制
- 迭代式提问
- 开发测试常用模板

> 课堂核心思路：**同一个任务，写法不同，AI 输出质量会差很多。** 每个场景都提供"模糊 Prompt"和"改写后 Prompt"两种写法，现场对比演示。

---

## 1. 场景一：好 Prompt 的五要素

### 讲解目标
让学员理解五要素（角色、任务、上下文、约束、输出格式），并观察不同写法对结果的影响。

### 示例内容
请打开 `Online_Show.py`，定位到 `calculate_shipping_cost` 函数：

```python
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
        base, per_kg = 10.0, 2.0
    else:
        base, per_kg = 30.0, 5.0
    cost = base + weight * per_kg
    if express:
        cost *= 1.5
    return round(cost, 2)
```

### 模糊 Prompt（先演示，效果差）

```
帮我写单元测试
```

### 改写后 Prompt（五要素完整，效果好）

```
请以 Python 开发人员的身份，为以下函数生成 pytest 单元测试。

函数：calculate_shipping_cost(weight, destination, express=False)
功能：计算运费
代码见 Online_Show.py。

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

### 教学步骤
1. 先让学员看"模糊 Prompt"，预测 AI 会输出什么。
2. 现场用模糊 Prompt 提问，观察输出质量。
3. 再展示"改写后 Prompt"，对比两次输出差异。
4. 逐条对应五要素：角色、任务、上下文、约束、输出格式。

### 讲解要点
- 五要素不一定每次都写全，但任务越复杂越需要结构化。
- 上下文和输出格式对结果影响最大。
- 角色要服务于任务，不要堆头衔。

---

## 2. 场景二：模糊需求改写

### 讲解目标
让学员掌握把模糊需求改写成清晰 Prompt 的方法，体验"改写前 vs 改写后"的质量差异。

### 示例内容
请打开 `Online_Show.py`，定位到 `update_profile` 函数。

**现象**：用户修改个人信息后保存，页面显示"保存成功"，但刷新页面后数据恢复为修改前的值。

```python
def update_profile(user_id: int, profile: dict) -> dict:
    # 校验
    if not profile:
        return {"code": 400, "msg": "资料不能为空"}
    nickname = profile.get("nickname")
    phone = profile.get("phone")
    if not nickname or not phone:
        return {"code": 400, "msg": "昵称和手机号不能为空"}
    # 模拟：只更新了内存中的临时对象，没有写回 _user_profile_db
    temp = dict(_user_profile_db.get(user_id, {}))
    temp["nickname"] = nickname
    temp["phone"] = phone
    # 故意不执行 _user_profile_db[user_id] = temp
    return {"code": 200, "msg": "保存成功"}
```

### 模糊 Prompt（先演示）

用户只是隐约觉得代码可能有问题，但说不清楚，只贴了代码：

```
帮我看看这段代码有没有问题
```

### 改写后 Prompt（五要素完整）

```
请以 Python 开发人员的身份，分析以下 Bug 的可能原因。

现象：用户修改个人信息后保存，页面显示"保存成功"，但刷新页面后数据恢复为修改前的值
复现步骤：
  1. 登录系统
  2. 进入个人信息页面
  3. 修改昵称和手机号
  4. 点击保存，页面提示"保存成功"
  5. 刷新页面，数据恢复为修改前的值

相关代码（见 Online_Show.py 的 update_profile 函数）：
- 只更新了内存中的临时对象，没有写回 _user_profile_db
- 返回"保存成功"但数据未持久化

环境：开发环境，模拟内存数据库

要求：
- 只分析可能原因和验证方法，不要直接修改代码
- 按概率从高到低排序

输出格式：
- 可能原因（按概率排序）
- 每个原因的验证方法
- 还需要补充哪些信息
```

### 教学步骤
1. 让学员先看模糊 Prompt，预测输出。
2. 现场用模糊 Prompt 提问，观察结果。
3. 展示改写后 Prompt，对比差异。
4. 讨论：改写后多了哪些信息？这些信息如何影响结果？

### 讲解要点
- 模糊 Prompt 让 AI 只能猜测，改写后 AI 知道该做什么。
- 上下文是 Prompt 的核心，很多时候不是 AI 能力不够，而是信息不足。
- 约束（只分析不改代码）能避免 AI 自作主张。

---

## 3. 场景三：输出格式控制

### 讲解目标
让学员理解输出格式对结果可用性的影响，学会用"输出格式"约束 AI。

### 示例内容
请打开 `Online_Show.py`，定位到 `get_order_status_summary` 相关函数：

```python
def get_order_status_summary(orders: List[Dict]) -> Dict[str, int]:
    summary: Dict[str, int] = {}
    for order in orders:
        status = order["status"]
        summary[status] = summary.get(status, 0) + 1
    return summary
```

### 模糊 Prompt（先演示）

```
帮我统计一下订单状态
```

### 改写后 Prompt（指定输出格式）

```
请统计以下订单列表中各状态的数量，并按以下格式输出：

1. 先用一句话总结
2. 再用 Markdown 表格列出：状态 | 数量
3. 最后用 JSON 格式输出一份完整结果

订单列表：
[粘贴 Online_Show.py 中的 sample_orders]
```

### 教学步骤
1. 让学员看模糊 Prompt，预测输出。
2. 现场用模糊 Prompt 提问，观察输出（可能是自由文本）。
3. 展示改写后 Prompt，对比输出（表格 + JSON）。
4. 讨论：哪种格式更适合复制到文档、Issue 或测试用例？

### 讲解要点
- 输出格式决定结果是否好用。
- 常见格式：表格、分步骤列表、JSON、Markdown、按严重程度排序。
- 我们不是只要一段回答，而是要能直接使用的结构化结果。

---

## 4. 场景四：迭代式提问

### 讲解目标
让学员体验"初稿 → 指出问题 → 补充上下文 → 重写"的多轮迭代过程。

### 示例内容
请打开 `Online_Show.py`，定位到 `search_orders` 函数：

```python
def search_orders(
    user_id: Optional[str] = None,
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = 1,
    size: int = 20,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> Dict:
```

### 初版 Prompt

```
帮我生成这个接口的文档
```

### 迭代方向（现场演示 2~3 轮）

| 轮次 | 追问方向 |
|------|----------|
| 第 2 轮 | "请按 OpenAPI 3.0 格式输出" |
| 第 3 轮 | "请补充每个参数的校验规则和默认值" |
| 第 4 轮 | "请补充每个响应状态码的含义和返回示例" |

### 教学步骤
1. 用初版 Prompt 提问，观察输出。
2. 指出不满意的地方，用第 2 轮追问。
3. 继续补充上下文，用第 3 轮追问。
4. 讨论：哪一轮改进最大？为什么？

### 讲解要点
- 不要期待一次 Prompt 就完美，好的结果往往来自两三轮迭代。
- 常用追问方向：风险、边界、验证步骤、排序、改表格、只保留可执行项。
- 迭代本身也是使用 AI 的能力。

---

## 5. 场景五：开发测试常用模板

### 讲解目标
让学员了解团队可沉淀的高频 Prompt 模板，并现场演示 SQL 优化模板。

### 示例内容
请打开 `Online_Show.py`，定位到 `CATEGORY_SALES_SQL` 和 `CATEGORY_SALES_CONTEXT` 常量：

```python
CATEGORY_SALES_SQL = """
-- 当前 SQL：查询每个分类下销量前 10 的商品
SELECT
    c.category_name,
    p.product_name,
    p.price,
    SUM(oi.quantity) AS total_sold
FROM
    categories c
    JOIN products p ON c.id = p.category_id
    JOIN order_items oi ON p.id = oi.product_id
    JOIN orders o ON oi.order_id = o.id
WHERE
    o.status = 'completed'
    AND o.paid_at >= '2026-01-01'
GROUP BY
    c.id, c.category_name, p.id, p.product_name, p.price
ORDER BY
    c.category_name, total_sold DESC;
"""
```

### 模糊 Prompt（先演示）

```
帮我优化这段 SQL
```

### 改写后 Prompt（SQL 优化模板）

```
请以 DBA 或资深后端开发的身份，优化以下 SQL 查询。

业务场景：查询每个分类下销量前 10 的商品
当前执行耗时：约 45 秒
数据库：MySQL 8.0

表结构和数据量：
- categories：约 500 条
- products：约 50 万条
- order_items：约 2000 万条
- orders：约 500 万条

当前索引：
- categories.id（主键）
- products.id（主键），products.category_id
- order_items.id（主键），order_items.order_id，order_items.product_id
- orders.id（主键），orders.status

SQL：
[粘贴 CATEGORY_SALES_SQL]

要求：
- 不能改变业务逻辑和查询结果
- 优先考虑加索引，其次考虑改写 SQL
- 给出每个优化方案的预期收益和风险

输出格式：
- 问题分析（当前慢的原因）
- 优化方案（按推荐优先级排序）
- 每个方案的预期提升幅度
- 风险提示
```

### 教学步骤
1. 让学员看模糊 Prompt，预测输出。
2. 现场用模糊 Prompt 提问，观察结果（可能只有泛泛建议）。
3. 展示改写后 Prompt，对比差异。
4. 讨论：为什么必须提供表结构、数据量、索引？

### 讲解要点
- 让 AI 写 SQL 时必须给表结构、字段含义和筛选条件，否则会生成不存在的字段。
- 约束（不能改业务逻辑）能避免 AI 破坏查询结果。
- 团队应把高频场景沉淀成模板，让新人也能直接使用。

---

## 6. 场景六：需求分析素材

### 讲解目标
让学员练习把需求分析需求改写成清晰 Prompt，体验"找需求漏洞"的用法。

### 示例内容
请打开 `Online_Show.py`，定位到 `CART_EXPIRY_REQUIREMENT` 常量：

```python
CART_EXPIRY_REQUIREMENT = """
功能名称：购物车商品过期提醒

需求描述：
用户在购物车中添加商品后，如果超过 24 小时未下单，该商品自动从购物车中移除，
并在用户下次打开购物车时提示"以下商品已超过保留时间，已自动移除"。

业务规则：
1. 商品加入购物车后保留 24 小时
2. 超过 24 小时未下单，标记为"已过期"
3. 用户打开购物车时，自动清除已过期的商品
4. 如果有商品被清除，在购物车页面顶部显示提示信息
5. 提示信息中列出被移除的商品名称
6. 用户关闭提示后不再显示

技术约束：
- 购物车数据存储在 Redis 中，key 为 cart:user:{userId}
- 每个商品项包含：productId, productName, quantity, addedAt（时间戳）
- 不需要定时任务，在用户打开购物车时实时判断
"""
```

### 模糊 Prompt（先演示）

```
帮我看看需求有没有问题
```

### 改写后 Prompt（需求分析模板）

```
请以测试负责人的身份，分析以下购物车商品过期提醒需求中可能存在的问题和遗漏场景。

需求描述：
[粘贴 CART_EXPIRY_REQUIREMENT]

技术约束：
- 购物车数据存储在 Redis 中，key 为 cart:user:{userId}
- 每个商品项包含：productId, productName, quantity, addedAt（时间戳）
- 不需要定时任务，在用户打开购物车时实时判断

要求：
- 只分析问题，不写代码
- 关注功能遗漏、边界条件、异常情况、用户体验问题

输出格式：
- 功能遗漏（哪些场景需求没有覆盖）
- 边界条件（时间临界点、并发等）
- 异常情况（Redis 宕机、数据不一致等）
- 用户体验问题
- 每个问题标注严重程度（高/中/低）
```

### 教学步骤
1. 让学员看模糊 Prompt，预测输出。
2. 现场用模糊 Prompt 提问，观察结果。
3. 展示改写后 Prompt，对比差异。
4. 讨论：改写后 AI 能发现哪些需求漏洞？

### 讲解要点
- 需求分析 Prompt 要明确"找什么"：功能遗漏、边界、异常、体验。
- 输出格式（按严重程度标注）让结果更可落地。
- 测试人员可以把 AI 当成"补漏助手"。

---

## 课堂演练建议

| 场景 | 对应练习 | 建议时长 | 操作方式 |
|------|----------|----------|----------|
| 五要素 | [练习2](练习2-改写单元测试Prompt.md) | 10min | 模糊 vs 改写对比 |
| 模糊改写 | [练习1](练习1-改写Bug分析Prompt.md) | 10min | 模糊 vs 改写对比 |
| 输出格式 | — | 5min | 指定表格/JSON 输出 |
| 迭代提问 | [练习5](练习5-迭代式提问.md) | 15min | 多轮追问 |
| 常用模板 | [练习3](练习3-改写SQL优化Prompt.md) | 10min | SQL 优化模板 |
| 需求分析 | [练习4](练习4-改写需求分析Prompt.md) | 10min | 需求漏洞分析 |

- 所有场景均使用 `Online_Show.py` 中的同一业务域，帮助学员建立连续认知。
- 每个场景都先演示"模糊 Prompt"，再演示"改写后 Prompt"，现场对比输出质量。
- 强调"Prompt 是清晰表达"的理念：把需求说清楚，AI 才能给出可用结果。
