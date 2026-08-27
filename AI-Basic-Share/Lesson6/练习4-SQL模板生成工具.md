# 练习 4：SQL 模板生成工具

---

## 练习目标

编写一份小工具需求说明，让 AI 生成一个 SQL 模板生成器，根据表结构和查询需求生成常用 SQL 语句。

---

## 练习步骤

1. 阅读下方的需求模板和表结构
2. 填写需求说明中的目标、输入、输出、规则
3. 将需求说明提交给 Copilot 或公司内网模型
4. 运行生成的工具，验证生成的 SQL 是否正确
5. 根据验证结果迭代修正

---

## 小工具需求模板

```markdown
## 目标

我要做一个 SQL 模板生成工具，用来……

## 输入

- 表结构：
- 查询需求：

## 输出

- 输出格式：
- 示例结果：

## 规则

- 规则 1：
- 规则 2：

## 技术要求

- 使用语言：
- 运行方式：
- 不需要图形界面
```

---

## 表结构参考

```sql
-- 用户表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    status TINYINT DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 订单表
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    paid_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 商品表
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    category_id INT,
    price DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0
);
```

---

## 常见 SQL 模板类型参考

| 模板类型 | 说明 |
|----------|------|
| **按 ID 查询** | `SELECT * FROM {table} WHERE id = ?` |
| **分页查询** | `SELECT * FROM {table} ORDER BY id LIMIT ? OFFSET ?` |
| **按状态统计** | `SELECT status, COUNT(*) FROM {table} GROUP BY status` |
| **日期范围查询** | `SELECT * FROM {table} WHERE created_at BETWEEN ? AND ?` |
| **关联查询** | `SELECT ... FROM A JOIN B ON A.id = B.a_id WHERE ...` |
| **插入** | `INSERT INTO {table} (...) VALUES (...)` |
| **更新** | `UPDATE {table} SET ... WHERE id = ?` |

---

## 练习引导问题

| 问题 | 你的回答 |
|------|----------|
| 你希望工具以什么方式运行？（命令行参数 / 交互式输入 / 配置文件） | |
| 生成的 SQL 应该直接输出到控制台还是保存到文件？ | |
| 是否需要支持多表关联查询的模板？ | |
| 生成后的 SQL 语法是否正确？ | |
| 你做了哪些迭代修改？ | |

---

## 打卡记录模板

```markdown
## 练习 4 打卡

- 练习内容：SQL 模板生成工具
- 需求说明（目标/输入/输出/规则）：
- 使用的 AI 工具：Copilot / 公司内网模型
- 第一次生成结果是否可用：是 / 部分可用 / 不可用
- 迭代了几轮：
- 最终工具能否运行：是 / 否
- 我的收获：
- 疑问或想进一步学习的内容：
```
