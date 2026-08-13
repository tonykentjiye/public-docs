# 练习 1：改写 Bug 分析 Prompt

---

## 练习目标

将模糊的 Bug 分析需求改写成包含五要素的清晰 Prompt。

---

## 练习步骤

1. 阅读下方的原始模糊 Prompt 和提供的上下文素材
2. 运用五要素（角色、任务、上下文、约束、输出格式）改写 Prompt
3. 将改写后的 Prompt 输入 Copilot 或公司内网模型
4. 对比两次输出结果的质量差异

---

## 原始模糊 Prompt

> 帮我分析这个 Bug

---

## 提供的上下文素材

```
现象：用户修改个人信息后保存，页面显示"保存成功"，但刷新页面后数据恢复为修改前的值
复现步骤：
  1. 登录系统
  2. 进入个人信息页面
  3. 修改昵称和手机号
  4. 点击保存，页面提示"保存成功"
  5. 刷新页面，数据恢复为修改前的值

相关代码（Controller 层）：
@PostMapping("/api/user/profile")
public Result updateProfile(@RequestBody UserProfile profile) {
    userService.updateProfile(profile);
    return Result.success("保存成功");
}

相关代码（Service 层）：
public void updateProfile(UserProfile profile) {
    // 直接更新数据库
    userMapper.updateById(profile);
}

环境：开发环境，MySQL 数据库，MyBatis-Plus
```

---

## 改写引导

请按五要素结构改写：

| 要素 | 思考方向 |
|------|----------|
| **角色** | 让 AI 以什么身份分析？ |
| **任务** | 具体要 AI 做什么？ |
| **上下文** | 上面提供的素材中哪些信息需要包含进去？ |
| **约束** | 有什么限制？比如不要直接改代码、要给出验证方法 |
| **输出格式** | 希望 AI 按什么结构输出？ |

---

## 参考改写示例（练习后查看）

<details>
<summary>点击展开参考示例</summary>

```
请以资深 Java 开发人员的身份，分析以下 Bug 的可能原因。

现象：用户修改个人信息后保存，页面显示"保存成功"，但刷新页面后数据恢复为修改前的值
复现步骤：
  1. 登录系统
  2. 进入个人信息页面
  3. 修改昵称和手机号
  4. 点击保存，页面提示"保存成功"
  5. 刷新页面，数据恢复为修改前的值

Controller 代码：
@PostMapping("/api/user/profile")
public Result updateProfile(@RequestBody UserProfile profile) {
    userService.updateProfile(profile);
    return Result.success("保存成功");
}

Service 代码：
public void updateProfile(UserProfile profile) {
    userMapper.updateById(profile);
}

环境：开发环境，MySQL，MyBatis-Plus

要求：
- 只分析可能原因和验证方法，不要直接修改代码
- 按概率从高到低排序

输出格式：
- 可能原因（按概率排序）
- 每个原因的验证方法
- 还需要补充哪些信息
```
</details>

---

## 打卡记录模板

```markdown
## 练习 1 打卡

- 练习内容：改写 Bug 分析 Prompt
- 原始 Prompt：帮我分析这个 Bug
- 改写后的 Prompt：
- AI 输出质量对比：改写前（差 / 一般 / 好） 改写后（差 / 一般 / 好）
- 我的收获：
- 疑问或想进一步学习的内容：
```
