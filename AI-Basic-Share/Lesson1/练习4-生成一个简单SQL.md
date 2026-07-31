# 练习 4：生成一个简单 SQL

---

## 练习目标

使用 GitHub Copilot 或公司内网模型，根据业务描述生成 SQL 查询语句，并理解 AI 生成的 SQL 逻辑。

---

## 练习步骤

1. 将下方业务需求描述复制到 AI 工具中
2. 使用类似以下的 Prompt 提问：
   > "我有以下数据库表结构和查询需求，请帮我生成对应的 SQL 查询语句"
3. 阅读 AI 生成的 SQL
4. 检查 SQL 语法和逻辑是否正确
5. 尝试在本地数据库或模拟环境中验证
6. 记录你的发现

---

## 练习用业务需求

```
数据库表结构：

-- 用户表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TINYINT DEFAULT 1  -- 1=启用, 0=禁用
);

-- 订单表
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',  -- pending, paid, shipped, delivered, cancelled
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    paid_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 订单明细表
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

查询需求：
1. 查询本月下单次数最多的前 10 名用户（显示用户名、邮箱、下单次数）
2. 查询每个用户的订单总额和平均订单金额
3. 查询已付款但超过 7 天仍未发货的订单
4. 查询每个商品的销售总量和销售总额，按销售总额降序排列
```

---

## 练习引导问题

请让 AI 生成 SQL 后，尝试回答以下问题：

| 问题 | 你的回答 |
|------|----------|
| AI 生成的 SQL 是否可以直接运行？ | |
| 第 1 条 SQL 中用了什么聚合函数？ | |
| 第 2 条 SQL 中用了什么分组条件？ | |
| 第 3 条 SQL 中日期比较的逻辑是否正确？ | |
| 你觉得 AI 生成的 SQL 有没有遗漏索引或性能考虑？ | |
| 如果数据量很大，你会怎么优化这些查询？ | |

---

## 参考：AI 可能生成的 SQL 示例

```sql
-- 查询1：本月下单次数最多的前10名用户
SELECT u.username, u.email, COUNT(o.id) AS order_count
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE MONTH(o.created_at) = MONTH(CURRENT_DATE)
  AND YEAR(o.created_at) = YEAR(CURRENT_DATE)
GROUP BY u.id, u.username, u.email
ORDER BY order_count DESC
LIMIT 10;
```

> ⚠️ 注意：AI 生成的 SQL 可能存在语法错误、逻辑漏洞或性能问题，请务必人工检查后再使用。

---

## 打卡记录模板

```markdown
## 练习 4 打卡

- 练习内容：生成一个简单 SQL
- 使用的工具：GitHub Copilot / 公司内网模型
- Prompt 内容：
- AI 生成的 SQL 是否可用：是 / 部分可用 / 不可用
- 我做了哪些修改：
- 我的收获：
- 疑问或想进一步学习的内容：
```
