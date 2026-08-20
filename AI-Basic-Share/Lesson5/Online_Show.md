# Online_Show

## 业务背景

本文件统一使用 Python 业务场景：一个简单的订单提交流程与代码评审场景。配套示例代码文件 `Online_Show.py` 提供实际函数、数据和 Markdown / Instruction 素材，方便课堂中直接打开、选中、复制。

本课主题是 **Markdown 与 Instruction：让经验变成团队规范**，重点演示：
- 如何用 Markdown 把零散信息整理成 AI 更容易理解的上下文
- 如何把常见输出结构沉淀成 Prompt 模板
- 如何把长期有效的规则沉淀成 Instruction
- 如何把个人经验变成团队共享资产

> 课堂核心思路：**让 AI 好用，不只是会提问，还要会整理上下文、会沉淀模板、会固化规则。**

---

## 1. 场景一：Markdown 把零散问题变成结构化上下文

### 讲解目标
让学员直观看到，同一份问题信息，零散描述和结构化 Markdown 会带来完全不同的 AI 输出质量。

### 示例内容
请打开 `Online_Show.py`，查看 `RAW_BUG_NOTES`、`BUG_CONTEXT` 和 `build_bug_analysis_markdown`：

```python
RAW_BUG_NOTES = """
订单提交易报错。用户说点提交后一直转圈，有时提示库存不足。
测试环境，今天上午开始出现。大概是购物车里有两个商品的时候容易出。
后端日志里能看到 submit order failed。最近改过优惠券和库存。
""".strip()
```

### 模糊 Prompt（先演示）

```
帮我分析一下这个问题

订单提交易报错。用户说点提交后一直转圈，有时提示库存不足。
测试环境，今天上午开始出现。大概是购物车里有两个商品的时候容易出。
后端日志里能看到 submit order failed。最近改过优惠券和库存。
```

### 改写后 Prompt（使用 Markdown 结构）

```markdown
请分析以下订单提交流程中的问题，按概率排序给出可能原因、验证方法和建议排查顺序。

# Bug 分析

## 背景
电商系统的提交订单接口，负责校验库存、计算优惠、创建订单。

## 现象
用户点击提交订单后，前端一直转圈，偶发提示库存不足。

## 复现步骤
1. 登录测试账号
2. 购物车加入两个商品，其中一个使用优惠券
3. 点击提交订单
4. 接口等待较久，最终失败

## 期望结果
订单成功创建，库存正确扣减，前端跳转到支付页。

## 实际结果
接口返回失败，部分请求提示库存不足，部分请求超时。

## 最近变更
- 优惠券抵扣逻辑重构
- 库存预占逻辑增加了批量校验

## 希望输出
- 可能原因（按概率排序）
- 每个原因的验证方法
- 建议排查顺序
```

### 教学步骤
1. 先用零散描述提问，观察 AI 输出是否泛泛而谈。
2. 再用 Markdown 结构化版本提问，对比结果。
3. 讨论：为什么 Markdown 让 AI 更容易抓到重点。

### 讲解要点
- Markdown 的价值不只是好看，而是帮助 AI 理解结构。
- 对开发测试场景来说，标题、列表、代码块就是最实用的三件套。
- 把信息分成背景、现象、步骤、期望、实际结果，AI 更容易给出可落地分析。

---

## 2. 场景二：Markdown 模板让 Prompt 变得可复用

### 讲解目标
让学员理解 Prompt 模板不是一句万能提示词，而是一份带占位符的结构化输入模板。

### 示例内容
请打开 `Online_Show.py`，查看 `build_test_points_markdown(LOGIN_REQUIREMENT)` 生成的表格：

```python
def build_test_points_markdown(requirement: Dict) -> str:
    rows = [
        "# 测试点清单",
        "",
        f"## 功能\n{requirement['feature']}",
        "",
        "| 分类 | 测试点 | 预期结果 |",
        "| --- | --- | --- |",
        "| 正常场景 | 输入正确用户名、密码、验证码 | 登录成功并跳转首页 |",
        "| 异常场景 | 用户名为空 | 提示用户名不能为空 |",
    ]
```

### 现场演示 Prompt

```
请根据以下 Markdown 模板中的内容，补全一个后台登录功能的测试点清单。

# 测试点清单

## 功能
后台登录

## 输入字段
- 用户名
- 密码
- 验证码

## 已知规则
- 用户名不能为空
- 密码连续输错 5 次后锁定 10 分钟
- 验证码错误时不给出过多提示

## 输出要求
- 按正常场景、异常场景、安全场景分类
- 用 Markdown 表格输出
- 每条测试点写清预期结果
```

### 教学步骤
1. 先让学员看模板本身，理解哪些部分是固定结构，哪些部分是要填空的业务信息。
2. 用模板提问，让 AI 生成测试点清单。
3. 讨论：为什么团队沉淀模板后，大家的输出会更一致。

### 讲解要点
- 模板的核心价值是可复制、可填空、可复用。
- 模板要保留固定骨架，把经常变化的内容放成占位区。
- 一个好模板应该让同事“添点内容就能直接用”。

---

## 3. 场景三：Instruction 约束长期行为

### 讲解目标
让学员理解 Instruction 和单次 Prompt 的区别：Prompt 解决当前任务，Instruction 约束长期行为。

### 示例内容
请打开 `Online_Show.py`，查看 `CODE_REVIEW_INSTRUCTION`：

```python
CODE_REVIEW_INSTRUCTION = """
# 代码 Review Instruction

当用户要求 Review 代码时，请始终按以下规则输出：

## 输出顺序
1. 先列出高风险问题
2. 再列出中风险问题
3. 最后列出低风险问题和改进建议
```

### 示例 Prompt

```
请按当前代码 Review Instruction，对 submit_order 函数做一次审查。
```

### 教学步骤
1. 先让学员只给普通 Prompt 做 Review。
2. 再增加 Instruction，观察输出结构变化。
3. 讨论：哪些规则适合写进 Instruction，哪些仍然应该留在单次 Prompt 中。

### 讲解要点
- Instruction 适合长期有效的规则，如输出结构、Review 关注点、语言风格。
- 不要把一次性业务细节都塞进 Instruction。
- 团队共享的重点不是“神秘提示词”，而是稳定、可维护的规则。

---

## 4. 场景四：同一段代码，在不同规则下输出不同

### 讲解目标
让学员看到同一段代码，在“解释代码”和“代码 Review”两种 Instruction 下，会得到不同结果。

### 示例内容
请在 `Online_Show.py` 中选中 `submit_order` 函数：

```python
def submit_order(order_payload: Dict) -> Dict:
    if not order_payload:
        return {"code": 400, "message": "order payload is empty"}
    items = order_payload.get("items", [])
    if not items:
        return {"code": 400, "message": "items is empty"}
    ...
```

### 对比 Prompt

**解释代码版**

```
请按代码解释 Instruction 解释 submit_order 函数。
```

**Review 代码版**

```
请按代码 Review Instruction 审查 submit_order 函数。
```

### 教学步骤
1. 选中同一段代码，分别使用两种 Prompt。
2. 对比输出：一个更偏“说明”，一个更偏“找问题”。
3. 讨论：为什么团队要区分不同场景的 Instruction。

### 讲解要点
- AI 不是只能“看代码”，关键在于你让它以什么规则处理代码。
- 同一份上下文，不同 Instruction 会改变输出角度和重点。
- 这正是团队规范的价值所在。

---

## 5. 场景五：团队共享与维护

### 讲解目标
让学员理解模板和 Instruction 不是写完就结束，还要考虑目录、命名、示例和维护方式。

### 示例内容
请打开 `Online_Show.py`，查看 `TEAM_TEMPLATE_INDEX`：

```python
TEAM_TEMPLATE_INDEX = [
    {"name": "Bug 分析 Prompt 模板", "usage": "提交缺陷分析给 Copilot 或内网模型"},
    {"name": "代码 Review Instruction", "usage": "统一 Review 输出结构"},
    {"name": "测试用例 Prompt 模板", "usage": "快速整理测试点"},
]
```

### 课堂引导问题
- 团队模板应该按什么目录分类？
- 谁来维护？多久回顾一次？
- 如何判断一个模板已经过时？
- 模板中要不要放示例？

### 讲解要点
- 没有示例的模板，别人很难直接用。
- 没有维护规则的模板，很快会过时。
- 最好用统一命名和统一目录，让新同事一眼能找到。

---

## 课堂演练建议

| 场景 | 对应练习 | 建议时长 | 操作方式 |
|------|----------|----------|----------|
| Markdown 整理上下文 | [练习1](练习1-编写Bug分析模板.md) | 10min | 零散描述改写成 Markdown |
| Prompt 模板复用 | [练习3](练习3-编写测试用例生成模板.md) | 10min | 用模板生成测试点 |
| 日志分析模板 | [练习4](练习4-编写日志分析模板.md) | 10min | 套用结构化模板 |
| Review 模板 | [练习5](练习5-编写代码Review模板.md) | 10min | 选中代码后按模板提问 |
| Instruction 编写 | [练习6](练习6-编写Instruction.md) | 15min | 写长期有效规则 |

- 建议先演示“零散信息”与“Markdown 模板”的差异，再演示 Instruction 的作用。
- Prompt 模板强调“当前任务怎么说清楚”，Instruction 强调“以后都按什么规则做”。
- 上课时可直接配合本目录下的 `开发中心通用-Prompt模板.md` 和 `开发中心通用-Instruction模板.md` 使用。
