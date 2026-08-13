# 练习 3：改写 SQL 优化 Prompt

---

## 练习目标

将模糊的 SQL 优化需求改写成包含五要素的清晰 Prompt。

---

## 练习步骤

1. 阅读下方的原始模糊 Prompt 和提供的上下文素材
2. 运用五要素改写 Prompt
3. 将改写后的 Prompt 输入 Copilot 或公司内网模型
4. 对比两次输出结果的质量差异

---

## 原始模糊 Prompt

> 帮我优化这段 SQL

---

## 提供的上下文素材

```sql
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
```

```
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

执行耗时：约 45 秒
数据库：MySQL 8.0
```

---

## 改写引导

请按五要素结构改写：

| 要素 | 思考方向 |
|------|----------|
| **角色** | 让 AI 以什么身份优化？ |
| **任务** | 具体要 AI 做什么？优化 SQL 还是加索引？还是两者都要？ |
| **上下文** | 表结构、数据量、现有索引、执行时间，哪些需要包含？ |
| **约束** | 不能改什么？比如不能改表结构、不能改业务逻辑 |
| **输出格式** | 希望 AI 按什么结构输出？ |

---

## 参考改写示例（练习后查看）

<details>
<summary>点击展开参考示例</summary>

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
[粘贴 SQL]

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
</details>

---

## 打卡记录模板

```markdown
## 练习 3 打卡

- 练习内容：改写 SQL 优化 Prompt
- 原始 Prompt：帮我优化这段 SQL
- 改写后的 Prompt：
- AI 输出质量对比：改写前（差 / 一般 / 好） 改写后（差 / 一般 / 好）
- 我的收获：
- 疑问或想进一步学习的内容：
```
