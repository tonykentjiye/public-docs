# VSCode + GitHub Copilot 使用技巧大全

> 面向: 已经在用 VSCode Copilot, 想"用得更好 + 用得更省"的开发者
> 阅读方式: 速查表先看, 再按需跳到对应章节; 每条尽量给可直接抄改的示例
> v1.0 新规做成, 采用2026/05/29的Copilot最强模型-Claude Opus 4.7(15x)生成

**文档结构**:
- **第 1 部分**: 各种优秀的使用技巧与方法 (产出质量优先)
- **第 2 部分**: 省 Token 的技巧与方法 (成本/效率优先)
- **第 3 部分**: 邪修技巧 (有效但不一定推荐, 自己斟酌)

---

## 0. 总速查表

| 想做什么 | 怎么做 | 章节 |
|---|---|---|
| 单行/小段补全 | Inline 补全 + 写好注释 | 1.1 |
| 局部小改 | 选区 → `Ctrl+I` Inline Chat | 1.1 |
| 跨文件重构 | Edits 模式 + `#file` 圈定 | 1.1 |
| 多步骤自动跑完 | Agent 模式 + 验收标准 | 1.1 |
| 沉淀团队规约 | `.github/copilot-instructions.md` | 1.4 |
| 复用提示词 | `.github/prompts/*.prompt.md` | 1.4 |
| 精准引用上下文 | `#file` `#sym` `#selection` | 1.3 / 2.2 |
| 让 AI 用工具 | `@workspace` `@terminal` `@vscode` | 1.2 |
| 省钱 | 任务隔离 + 精准引用 + 模型分级 | 第 2 部分 |

---

---

# 第 1 部分 · 各种优秀的使用技巧与方法

## 1.1 选对模式 (4 种模式各司其职)

VSCode Copilot 主要有 4 种交互模式. **选错模式 = 既费 Token 又得不到好结果.**

### Inline 补全 (灰字 / Ghost Text)
- **场景**: 写代码时下一行/下几行的自动补全
- **最佳实践**:
  - **先写注释/函数签名, 再等补全**, 命中率高
  - 多行补全时按 `Alt+]` / `Alt+[` 翻看不同候选
  - 不需要时按 `Esc` 关掉

**示例 (推荐写法)**:
```ts
// 把 ISO8601 字符串转成 YYYY/MM/DD HH:mm (JST)
function formatJst(iso: string): string {
  // ← 在这里等 Copilot 补全, 命中率 >90%
}
```

### Inline Chat (`Ctrl+I`)
- **场景**: 选中一段代码做局部修改 / 解释 / 重命名
- **最佳实践**:
  - **先选区再呼出**, 否则会把整文件送上去
  - 用动词短指令: `加 null 检查`, `改成 async/await`, `抽成函数`

**示例**: 选中一段 `for` 循环 → `Ctrl+I` → 输入 `改成 reduce, 不要新建变量`

### Ask 模式 (Chat 侧栏)
- **场景**: 问问题, 不直接改代码; 调研, 解释, 学习
- **最佳实践**:
  - 用 `#` 精准引用上下文
  - 让它先给方案再让你选, 不要直接动手

**示例**:
```
我想给 #file:src/promotion/sender.ts 的 send() 增加重试.
请先给 2~3 种方案 (库 / 自实现 / 退避策略), 对比优缺点, 不要写代码.
```

### Edits 模式 (`Ctrl+Shift+I`)
- **场景**: 跨多个文件的结构化修改 (加字段, 改接口名贯穿前后端)
- **最佳实践**:
  - 一次性把所有相关文件加进 working set
  - 一句话讲清楚目标, 让它 diff 一次出全

**示例**:
```
working set: #file:dto/user.ts #file:service/user.ts #file:controller/user.ts

目标: 给 User 增加 phoneNumber 字段 (string, optional).
要求:
1. dto 加字段 + class-validator @IsOptional @IsPhoneNumber('JP')
2. service 透传
3. controller 不变
4. 保持现有命名风格, 不要新增依赖
```

### Agent 模式
- **场景**: 多步骤任务 (建项目, 跑测试直到全绿, 修 bug 闭环)
- **最佳实践**:
  - **必给验收标准**, 比如 "改完 `npm test` 全绿"
  - **限制范围**, 比如 "只改 `src/api/` 下"
  - **不要边跑边插嘴**, 让它跑完

**示例**:
```
任务: 修复 `users.spec.ts` 里 3 个红色用例.
范围: 只允许改 `src/users/` 下文件.
完成标准: `npm test -- users.spec.ts` 全绿, 且 `tsc --noEmit` 无报错.
约束: 不新增依赖; 保留现有方法签名.
```

---

## 1.2 善用 Participants (`@`) 和 Slash (`/`)

`@` 是 chat participant, 它能调用专门工具/知识源, **少打很多字**.

| 写法 | 作用 | 例子 |
|---|---|---|
| `@workspace` | 在整个工作区检索 | `@workspace 哪里调用了 sendPromotion` |
| `@terminal` | 拿当前终端输出做上下文 | `@terminal 这个报错怎么修` |
| `@vscode` | VSCode 本身的知识 | `@vscode 怎么改默认字体` |
| `@github` | 仓库/PR/Issue 信息 (需登录) | `@github 列出最近 5 个 PR` |

**Slash 命令** (常用):
- `/explain` — 解释选中代码
- `/fix` — 修复选中代码的问题
- `/tests` — 为选中代码生成测试
- `/doc` — 生成文档注释
- `/new` — 引导建项目

**示例**:
```
/tests
为 #sym:formatJst 生成 Jest 用例, 覆盖: 正常 / 夏令时 / 非法输入 / 空字符串.
```

---

## 1.3 上下文引用 (`#`) — 精准比"广撒网"强 10 倍

| 写法 | 含义 |
|---|---|
| `#file:src/foo.ts` | 引用整个文件 |
| `#selection` | 当前编辑器选中区 |
| `#sym:ClassName` | 引用某个符号 |
| `#codebase` | 触发工作区检索 (慎用) |
| `#terminalLastCommand` | 上一条终端命令 + 输出 |
| `#changes` | 当前 git 未提交变更 |
| 拖文件到 Chat 框 | 等价于 `#file:` |

**示例 (强烈推荐这种格式)**:
```
[上下文] #file:src/promotion/sender.ts (重点 send 方法) + #file:test/sender.spec.ts
[任务] 给 send 加超时重试 (最多 3 次, 指数退避 1s/2s/4s)
[约束] 不引入新依赖; 保持函数签名; 日志用现有 logger
[产出] 仅输出 diff, 测试要全绿
```

---

## 1.4 项目级定制 — 一次配置, 永久受益

### 1.4.1 `.github/copilot-instructions.md` (项目 instructions)
仓库根目录创建, **Copilot 自动注入到每次对话**, 你不再需要每次重复说"我们用什么栈/什么规约".

**模板** (照抄微调即可):
```markdown
# 项目背景
- 系统: 促销中间件 (POS 周边)
- 后端: Nest.js + TypeScript, 部署 AWS ECS
- 前端: Nuxt.js, 部署 AWS S3
- DB: PostgreSQL (Aurora)
- 客户: 日本, 文案/注释用日文

# 编码规约
- TypeScript strict, 不允许 any
- 缩进 2 空格, 单引号, 行尾分号
- 异步统一 async/await, 禁用 .then 链
- 日志用 `logger.{info|warn|error}({ traceId, ... }, msg)`
- 错误必须 throw `AppError(code, message)`, 不裸 throw

# 回答约定
- 用中文回答, 代码注释用日文
- 涉及新依赖必须先询问, 不要自作主张安装
- 优先给最小改动方案
```

> 越精炼越好. 详细规约 (几十页) 放别处, 用到时 `#file` 引用.

### 1.4.2 `.github/prompts/*.prompt.md` (可复用提示词)
团队高频任务 → 模板化 → Chat 输入 `/<文件名>` 调用.

**示例**: `.github/prompts/review-coding.prompt.md`
```markdown
---
mode: ask
description: 对当前选区做 Coding Review (业界标准)
---
请基于 #selection 做 Code Review, 按下表输出:

| 类别 | 项目 | 结果 | 行号 | 说明/建议 |
|---|---|---|---|---|

检查类别:
1. 命名 (变数/函数/类是否表意, 是否符合驼峰)
2. 异常处理 (是否覆盖网络/IO/空值)
3. 性能 (N+1, 循环内 await, 同步阻塞)
4. 安全 (注入/越权/敏感信息日志)
5. 可读性 (函数长度, 嵌套层数, magic number)
6. 测试 (是否需要补 / 是否容易测)

只输出表格, 不要总结性文字.
```

**示例**: `.github/prompts/gen-jest.prompt.md`
```markdown
---
mode: edit
description: 为指定函数生成 Jest 测试用例
---
为 ${selection} 生成 Jest 测试, 要求:
- 覆盖 正常 / 边界 / 异常 三类
- 用 describe + it 嵌套
- 不引入新依赖
- 测试文件放在源文件同目录, 后缀 .spec.ts
```

### 1.4.3 自定义 Chat Mode
在设置里可创建专门 Mode (如 `Review 专家` / `测试生成器`), 预置 instructions + 限定可用工具集, **避免每次重交代角色**.

---

## 1.5 提示词设计 — 一次到位的"CRISP" 结构

```
[C] Context  — 项目背景 / 在做什么 (能进 instructions 就别在这写)
[R] Role     — 你扮演的角色 (可选, "你是资深 TS 工程师")
[I] Input    — 输入: #file / #sym / #selection / 这段文本
[S] Steps    — 你要做的步骤 (有序, 越具体越好)
[P] Product  — 期望产出格式 (代码 / diff / 表格 / 仅说明)
```

**对比**:

差:
> 帮我看看这个代码有啥问题

好:
> [C] Nest.js 后端促销中间件 (其他在 instructions)
> [I] #file:src/promotion/sender.ts (重点 send())
> [S] 1) 异常处理是否覆盖超时 2) 日志是否带 traceId 3) 是否有重试
> [P] 表格: 问题 | 行号 | 严重度 | 建议. 不要直接改代码

### 5 个高 ROI 的提示词小技巧

1. **明确"不要做什么"** — "不要新增依赖", "不要修改其他文件", "只输出 diff"
2. **给完成定义** — "改完后 `tsc --noEmit` 无报错且原测试全绿"
3. **先计划后执行** — "先列出修改计划, 等我确认后再动手"
4. **指定输出格式** — 表格/JSON/diff, 不要让它自由发挥
5. **给反例** — "不要像 XXX 那样写", 比正面描述更有效

---

## 1.6 工作流模式 (从 0 到上线的高效流)

### 模式 A: TDD (测试驱动)
```
1. Ask: "请基于 #file:requirement.md 列出 formatJst 应有的测试用例"
2. Edits: "把这些用例写到 formatJst.spec.ts, 函数本体先用 throw 占位"
3. Agent: "现在让所有用例通过, 范围只限 formatJst.ts"
```
**收益**: 自动验证, AI 自己 debug 自己, 你只需 review.

### 模式 B: 探针 → 改造
```
1. Ask + #codebase: "sendPromotion 在哪些地方被调用, 列调用链"
2. Ask: "如果给它加一个 traceId 参数, 哪些地方要改"
3. Edits: 把上述文件加入 working set, 一次性改完
```

### 模式 C: 设计 → 评审 → 实现
```
1. Ask: 给 3 种方案对比 (不写代码)
2. 人决策选 1 种
3. Edits: 按方案 X 实现
4. /tests 补测试
5. 自定义 prompt /review-coding 自检
```

---

## 1.7 给代码 / 错误 / 终端的正确"喂法"

| 不推荐 | 推荐 |
|---|---|
| 描述代码长啥样 | `#sym:User` |
| 复制错误信息部分 | `@terminal` 或贴完整 stack |
| 复制整文件到 Chat 框 | `#file:xxx` |
| "前几天有个报错..." | `#terminalLastCommand` |
| "我刚改的那段" | `#changes` |

---

## 1.8 让 Copilot 帮你写 Copilot 配置 (套娃)
- 用 Ask: `请帮我写一个 .github/copilot-instructions.md, 基于 #file:package.json #file:tsconfig.json #file:README.md`
- 用 Ask: `请帮我写一个 /review-coding 提示词, 用途是: ...`
- 善用 `/new` 命令引导新建带模板的项目

---

## 1.9 调试 / 排错增效

**示例 1**: 单元测试红了
```
@terminal 这个测试为什么红? #file:src/foo.ts #file:test/foo.spec.ts
要求: 先解释原因, 再给最小修复 diff
```

**示例 2**: 性能问题
```
#sym:loadDashboard 在生产环境 P95 1.2s.
请: 1) 找出嫌疑点 2) 给 3 种优化方案 (按 ROI 排序) 3) 不要写代码
```

**示例 3**: 看不懂的代码
```
/explain
重点: 这段为什么用了 Symbol.iterator? 有没有更易读的写法?
```

---

## 1.10 多人协作 / Code Review

- **PR 描述**: Chat → `基于 #changes 写一份 PR 描述, 模板 = 背景 / 改动 / 影响 / 测试方式`
- **Review 自查**: 提交前跑 `/review-coding` 自检一遍
- **Commit 信息**: `基于 #changes 生成符合 Conventional Commits 的提交信息`

---

## 1.11 模型选择 — 不是越强越好

| 任务复杂度 | 推荐 |
|---|---|
| 补全/简单改 | 默认轻量模型 |
| 一般问答/解释 | GPT-4.1 / Claude Sonnet |
| 大型重构/长上下文 | Claude Sonnet (200k 上下文) |
| 真·难题 (架构, 复杂 bug) | Claude Opus / GPT-5 |

**实践**: 默认走中档, 不行再升级. 顶配模型留给真值得的问题.

---

## 1.12 常用快捷键

| 快捷键 | 功能 |
|---|---|
| `Tab` / `Esc` | 接受 / 拒绝补全 |
| `Alt+]` / `Alt+[` | 切换补全候选 |
| `Ctrl+I` | Inline Chat (选区) |
| `Ctrl+Alt+I` | Chat 侧栏 |
| `Ctrl+Shift+I` | Edits |
| `Ctrl+L` (Chat 内) | 新会话 |
| `@` `#` `/` | participant / context / command |

---

---

# 第 2 部分 · 省 Token 的技巧与方法

> 核心思路: **少给无用上下文, 多给精准上下文; 少来回, 多一次成型; 复用模板, 不重复打字.**

## 2.1 模式选错就是烧钱

| 模式 | 大致成本 | 适用 |
|---|---|---|
| Inline 补全 | 最低 | 小段补全 |
| Inline Chat (选区) | 低 | 局部改 |
| Ask + `#file` | 中 | 调研问答 |
| Edits | 中-高 | 多文件改 |
| Agent | 高 (循环调用) | 多步骤自动 |

**口诀**: 能 Inline 就别开 Chat; 能选区就别整文件; 能 Ask 就别 Agent.

---

## 2.2 上下文 — 精准引用代替"全量倾倒"

### ✅ 用 `#`, 别复制粘贴
- `#file:xxx.ts` 比把整个文件粘贴到 Chat 框, **省的 Token 一样, 但更稳**(Copilot 知道路径, 后续能定位)
- `#sym:UserService` 只带这个类的相关片段, 比 `#file` 还省

### ✅ `#codebase` 慎用
- 它会触发工作区检索, **可能拉很多块**进上下文
- **已知文件路径永远优先 `#file`**, 只在真要全局搜索时用 `#codebase`

### ✅ 排除噪音
仓库根创建 `.copilotignore` (或调整 `files.exclude`):
```
dist/
build/
out/
node_modules/
coverage/
*.min.js
*.map
*.lock
*.snap
__snapshots__/
```

---

## 2.3 会话隔离 — 最便宜的省 Token 操作

- **每个独立任务开新会话** (`Ctrl+L` 或 Chat 顶部 `+`)
- 长会话里之前所有问答 **都会作为历史发送**
- 切任务 = 新会话, 几乎是 0 成本的省钱大招

---

## 2.4 Working Set 精简 (Edits / Agent)

- 视图左上角能看到当前 working set
- **不相关文件手动 X 掉**
- 不要让它带着 20 个文件去思考只涉及 3 个文件的改动

---

## 2.5 让产出更省 Token

| 浪费 | 省钱 |
|---|---|
| "请帮我把整个文件改一下并打印出来" | "只输出 diff" |
| "请逐步解释每一行的作用" | "只指出有问题的行" |
| "请详细说说..." | "用 3 句话总结" |
| 让它边想边说 | "先列计划, 我确认后执行" |
| 一个问题一轮对话 | "请依次回答 1) 2) 3)" |

**实操示例 (省 Token 的 prompt)**:
```
基于 #file:foo.ts, 仅输出修改后的 send 函数 (不要整文件, 不要解释).
约束: 改动最小化; 不新增依赖.
```

---

## 2.6 用 instructions 替代重复打字

每次都要交代"我们项目用 Nest.js, TypeScript strict, 缩进 2 空格..." → **进 `.github/copilot-instructions.md`**.

每月省下的 Token = 字数 × 对话次数 × 团队人数, 量级很可观.

---

## 2.7 用 Prompts 文件替代重复指令

高频提示词 (review / 写测试 / 生成 commit) 全部 `.prompt.md` 化.

**示例**: `.github/prompts/diff-only-refactor.prompt.md`
```markdown
---
mode: edit
description: 只输出 diff 的小步重构
---
对 ${selection} 做最小重构, 目标: ${input:目标}
要求:
- 仅输出 unified diff
- 不修改其他文件
- 不新增依赖
- 行为完全保持
```

调用一次省好几十字.

---

## 2.8 模型分级 — 别拿大炮打蚊子

- 简单任务用默认/Mini 档
- 复杂任务才用 Opus / GPT-5
- 状态栏点模型名快速切换

**实操**: 团队约定"非难题不上顶配", 每月配额能多撑很久.

---

## 2.9 关掉用不到的功能

- 看代码/做 Review 时, 临时关 Inline 补全 (右下角 Copilot 图标)
- 大型生成文件 (打包产物) 直接排除
- 不需要 NES (Next Edit Suggestions) 时关掉

---

## 2.10 一次问完一组相关问题

差:
```
你: A 是什么?
AI: ...
你: 那 B 呢?
AI: ...
你: C 又是啥?
```

好:
```
请依次回答:
1) A 是什么?
2) B 是什么?
3) C 是什么?
每个答案不超过 3 句.
```
**省**: 重复加载历史的开销 × N 次.

---

## 2.11 反模式清单 (看到就改)

- ❌ 在一个 Chat 里聊一整天
- ❌ 每次都 `#codebase`, 不管问题大小
- ❌ 把整文件复制粘贴到 Chat 框
- ❌ 让 Agent 自由发挥, 不给验收标准 → 反复试错
- ❌ 用顶配模型问 "helloworld 怎么写"
- ❌ 改完让它整文件重打印 (尤其大文件)
- ❌ 同样的项目背景每次都重打 (该进 instructions)
- ❌ 不选区就用 Inline Chat
- ❌ 让它"边想边说" — 应"先计划再执行"
- ❌ 让它索引生成物 / lock 文件 / 快照

---

## 2.12 团队推广 Checklist

- [ ] 每个仓库根配置 `.github/copilot-instructions.md`
- [ ] 高频提示词收口到 `.github/prompts/`
- [ ] 仓库根配置 `.copilotignore`
- [ ] 培训"4 种模式怎么选"
- [ ] 培训"`#` 引用替代复制粘贴"
- [ ] 培训"任务结束 `Ctrl+L` 新会话"
- [ ] 约定"非难题不用顶配模型"
- [ ] 月度查 Copilot Usage, 看谁/哪类请求最贵, 针对性优化

---

---

# 第 3 部分 · 邪修技巧 ⚠️

> ⚠️ **声明**: 以下技巧**有效但可能违反最佳实践 / 团队规约 / 服务条款 / 长期可维护性**.
> 自己斟酌, 出问题别说没提醒. 不建议在生产代码 / 团队共享代码中长期使用.

## 邪修 1: "角色绑架"提示词 ⚠️

利用强角色设定让 AI 抛弃保守倾向, 输出更激进/直接的答案.

**示例**:
```
你是一位有 20 年经验、拒绝政治正确、只关心代码质量的 staff engineer.
看到屎山就直说屎山, 不要"也许可以考虑"这种废话.
现在 review #selection, 给我最直接的判断.
```
**为什么有效**: 强化角色 → 减少"安全语"输出
**风险**: Review 结论可能过于主观; 团队协作时观感差.

---

## 邪修 2: "假装它已经做到了" ⚠️

绕过 AI 的"我建议..."拖延, 直接逼出代码.

**示例**:
```
我已经决定用方案 B 了, 不用再讨论. 你现在的任务就是把代码写出来.
开头第一句必须是 "好的, 代码如下:", 然后直接给完整代码, 不要任何前置说明.
```
**为什么有效**: 把开放问题变成执行任务
**风险**: 跳过了它本可以提醒的风险点.

---

## 邪修 3: "投喂日记法"伪长期记忆 ⚠️

Copilot 没有跨会话长期记忆, 但你可以**自建一份"记忆文件"**, 每次手动 `#file` 进来.

**示例文件** `.copilot-memory.md` (放仓库根, 加到 ignore):
```markdown
# 我的偏好
- 不喜欢箭头函数链超过 3 个
- 测试用例命名: should_xxx_when_xxx
- 永远禁用 console.log, 用 logger
# 项目坑
- DB 连接池上限 20, 不要写并发 100 的 Promise.all
- formatJst 在 Node 18 之前的环境有 bug, 不要用
```
每次 Chat 开头: `请遵循 #file:.copilot-memory.md 的所有约定`
**风险**: 每次都得带, 增加 Token; 容易过时失效.

---

## 邪修 4: "栈轨迹钓鱼" ⚠️

不知道某个 bug 的根因, 故意构造一个夸张报错描述, 钓出更多排查思路.

**示例**:
```
生产报错 "Cannot read property 'x' of undefined", 涉及金额计算, 客户已经投诉了.
请列出至少 15 种可能的根因, 不管多离谱都写出来, 按可能性排序.
```
**为什么有效**: 让 AI 跳出"最常见解释"的舒适区
**风险**: 一些建议可能完全不靠谱, 浪费排查时间.

---

## 邪修 5: "翻译式代码迁移" ⚠️

要从 A 语言/框架迁到 B, 与其手写, 不如让 AI 整体"翻译".

**示例**:
```
把 #file:legacy.java 完整翻译成等价的 TypeScript Nest.js Controller.
保持方法名一致, 注释保留. 不要"优化", 严格 1:1.
```
**风险**: 看起来对, 但语义不对的概率不低; **必须配测试覆盖**.

---

## 邪修 6: "对照组评审" ⚠️

让 AI 同时扮演两个对立角色互评, 你坐收渔利.

**示例**:
```
角色 A: 性能至上主义者
角色 B: 可读性至上主义者

请两人分别评价 #selection, 各写 5 条意见, 再用一张表格对比分歧.
最后由你 (中立裁判) 给最终建议.
```
**为什么有效**: 一次对话拿到多视角
**风险**: Token 消耗大, 适合复杂决策, 不适合日常.

---

## 邪修 7: "禁用客套" 极简模式 ⚠️

在 instructions 或开头加一段, 强制 AI 不说废话:

```markdown
# 输出协议
- 禁止使用: "好的", "当然可以", "我很乐意帮助", "希望对你有帮助"
- 禁止使用 emoji
- 禁止解释你将要做什么, 直接做
- 禁止在代码块后总结代码做了什么 (除非我问)
- 一句话能说完的别用两句
```
**风险**: 跟某些 prompt-tuning 冲突; 偶尔会显得很"冷".

---

## 邪修 8: "假上下文" 投毒法 ⚠️

为了让 AI 严格遵守某个规则, 故意在上下文里塞个"反例 + 错误后果".

**示例**:
```
[警告] 上次有个同事写了下面这段, 导致生产宕机:
```ts
items.forEach(async i => await save(i))  // ❌ 并发失控
```

现在请帮我实现批量保存, 必须避免上述错误.
```
**为什么有效**: AI 对"避免重蹈覆辙"的指令响应度极高
**风险**: 误导团队新人; 别在团队共享 prompt 里乱编故事.

---

## 邪修 9: "二段式提交" 绕长输出限制 ⚠️

模型一次输出有限, 大型生成 (如完整模块) 容易截断.

**做法**:
```
第 1 轮: 请只输出文件结构 + 每个文件的函数签名 (TypeScript declaration 形式)
我确认后...
第 2 轮: 请只实现 #file:a.ts 的全部函数本体, 不要其他文件.
第 3 轮: 实现 #file:b.ts ...
```
**风险**: 多轮意味着多花 Token; 但对超大任务比"一次全出"更稳.

---

## 邪修 10: "AI 互怼"找 bug ⚠️

写完代码, 让 AI 自己挑刺自己, 再让另一个会话攻击它的修复.

**流程**:
1. 会话 A: "请找出 #file:x.ts 的所有 bug"
2. 会话 A: "把这些 bug 全修了"
3. **新会话 B** (开新会话, 不带历史): "请尝试攻击 #file:x.ts, 找出仍存在的问题"
4. 重复 2~3 次

**为什么有效**: 不同会话上下文不同, 视角更新
**风险**: 极费 Token; 适合关键模块.

---

## 邪修使用建议

| 场景 | 可以邪修 | 别邪修 |
|---|---|---|
| 自己一人 hack 项目 | ✅ | |
| 学习 / 实验 | ✅ | |
| 一次性脚本 | ✅ | |
| 公司生产代码 | | ❌ |
| 团队共享 prompt 库 | | ❌ |
| 客户交付物 | | ❌ |

---

---

# 附录: 30 秒上手 Checklist

新人想立刻"用得更好 + 用得更省", 按顺序做这 5 件事:

1. ✅ 在仓库根创建 `.github/copilot-instructions.md` (抄 1.4.1 的模板, 改技术栈即可)
2. ✅ 在仓库根创建 `.copilotignore` (抄 2.2 的内容)
3. ✅ 学会一个快捷键: `Ctrl+L` (新会话)
4. ✅ 学会一种引用: `#file:路径`
5. ✅ 学会一种约束: "只输出 diff, 不要解释"

做完这 5 件, 至少省 30% Token, 质量明显提升.
