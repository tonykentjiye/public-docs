# Lesson 7: AI 工具地图与选型分享

---

## 本期主题

AI 工具地图：从个人提效到团队资产建设，了解哪些工具值得开发中心试用、推广或持续观察。

---

## 本期目标

- 了解开发中心可关注的 AI 工具类型
- 知道不同工具适合解决什么问题
- 重点了解代码、知识库、Excel、自动化、文档交付物相关工具
- 建立工具选型判断标准
- 完成一次工具体验报告

---

## 本期目录

1. 为什么需要 AI 工具地图
2. 工具分类总览
3. 个人开发提效类工具
4. 团队知识库与 RAG 工具
5. Excel 与表格分析工具
6. 自动化工作流工具
7. 模型网关、观测与本地模型
8. 文档与交付物生成工具
9. 工具选型标准
10. 作业与打卡

---

## 为什么需要了解多种 AI 工具

- 单一工具无法覆盖所有工作场景
- 个人提效和团队标准化需要不同工具
- 工具生态变化很快，需要持续观察
- 选型错误会带来成本、权限和维护问题
- 好工具可以沉淀成团队资产

---

## 工具分类总览

| 分类 | 代表工具 | 主要用途 |
| --- | --- | --- |
| Chat 与聚合客户端 | Cherry Studio、Open WebUI | 统一聊天入口、多模型体验 |
| 开发提效 | Copilot、Cursor、Codex、Cline、OpenCode、Aider | 写代码、改代码、跑测试 |
| 知识库与 RAG | Dify、RAGFlow | 项目文档问答、需求知识库 |
| Excel 与表格 | Microsoft 365 Copilot、SpreadsheetAgent、TabClaw | 表格分析、公式、报表、数据清洗 |
| 自动化工作流 | n8n、Dify Workflow、browser-use | 跨系统自动化 |
| 模型治理 | LiteLLM、Langfuse、Ollama | 网关、成本、观测、本地模型 |
| 交付物生成 | ppt-master、Marp、Slidev、MarkItDown | PPT、文档、培训材料 |

---

## Chat 与聚合客户端

**代表工具**

- Cherry Studio
- Open WebUI
- ChatGPT / Claude / Gemini
- 公司内网模型

**适合场景**

- 日常问答
- Prompt 练习
- 多模型对比
- 文档总结
- 需求或方案初稿

---

## Cherry Studio

- 桌面端 AI 聚合客户端
- 适合管理多个模型和 API Key
- 适合日常问答、Prompt 模板管理、多模型对比
- 更偏个人效率工具

**适合开发中心的用法**

- 给骨干人员做多模型体验
- 对比公司内网模型和外部模型效果
- 沉淀常用 Prompt

---

## Open WebUI

- 自托管 AI Chat 界面
- 支持 Ollama 和 OpenAI-compatible API
- 适合做团队内部统一 AI Chat 入口
- 可配合本地模型或公司内网模型使用

**适合开发中心的用法**

- 搭建内部 AI 问答门户
- 统一接入内网模型
- 给非编码场景提供简单入口

---

## 个人开发提效类工具

**代表工具**

- GitHub Copilot
- Cursor
- Codex
- Claude Code
- Cline
- OpenCode
- Aider
- Gemini CLI

**适合场景**

- 代码解释
- 小功能开发
- Bug 修复
- 单元测试
- 重构建议
- 脚本和工具制作

---

## Copilot、Cursor、Codex

| 工具 | 适合场景 | 特点 |
| --- | --- | --- |
| GitHub Copilot | IDE 内日常开发 | 上手成本低，适合全员推广 |
| Cursor | AI 原生 IDE | 代码库理解、Agent、并行任务体验强 |
| Codex | Coding Agent | 可处理较完整任务，适合任务委托和验证 |

---

## Cline、OpenCode、Aider、Gemini CLI

| 工具 | 适合场景 | 特点 |
| --- | --- | --- |
| Cline | VS Code Agent | Plan/Act、MCP、多模型、适合演示 Agent 流程 |
| OpenCode | 终端 Agent | 开源、终端优先、支持多模型 |
| Aider | 终端 Pair Programming | Git 集成好，适合小步修改 |
| Gemini CLI | 终端 Agent | 长上下文、MCP、Google Search、脚本化 |

---

## 团队知识库与 RAG 工具

**代表工具**

- Dify
- RAGFlow
- Open WebUI
- MarkItDown

**适合场景**

- 项目文档问答
- 需求知识库
- 新人入门问答
- 测试规范查询
- 障害和历史问题检索

---

## Dify

- 开源 LLM 应用开发平台
- 支持 Workflow、RAG、Agent、模型管理
- 适合从原型走向团队应用
- 可以通过 API 接入内部系统

**适合开发中心的用法**

- 项目知识库问答
- 需求分析助手
- 测试用例生成助手
- 发布检查助手

---

## RAGFlow 与 MarkItDown

**RAGFlow**

- 偏 RAG 引擎和知识库问答
- 适合处理文档检索、问答和上下文层

**MarkItDown**

- 把 PDF、Word、PowerPoint、Excel 等转成 Markdown
- 适合作为知识库入库前的文档预处理工具

---

## Excel 与表格分析工具

**为什么单独讲 Excel**

- 开发中心很多管理、测试、统计工作仍然依赖 Excel
- Excel 中常见重复劳动多
- 公式、透视表、数据清洗容易出错
- 报表和分析结果经常需要反复整理

**常见需求**

- 生成公式
- 检查数据异常
- 汇总测试结果
- 清洗 CSV / Excel
- 生成统计图表
- 输出周报或分析报告

---

## Microsoft 365 Copilot / Excel Agent Mode

- 直接嵌入 Excel
- 可用自然语言生成公式、分析数据、修改表格
- 适合业务报表、统计分析、公式修正
- 对 Microsoft 365 环境依赖较强

**适合开发中心的用法**

- 测试结果统计
- 工数和任务统计
- 缺陷趋势分析
- 项目周报数据整理

---

## ChatGPT / Claude / Gemini 处理 Excel

- 上传或粘贴表格内容进行分析
- 生成 Excel 公式
- 解释复杂公式
- 生成 VBA、Office Script、Python 脚本
- 把表格结果整理成报告

**适合场景**

- 小规模数据分析
- 公式学习和排错
- 临时 CSV 处理
- 报表说明文字生成

---

## Excel 自动化脚本

**可用技术**

- Python：pandas、openpyxl
- JavaScript：Office Scripts、SheetJS
- VBA：适合已有 Excel 宏环境
- Power Query：适合数据清洗和转换

**适合开发中心的用法**

- 批量整理测试结果
- 多个 Excel 合并
- 缺陷数据统计
- 日志 CSV 转分析表
- 自动生成周报数据

---

## SpreadsheetAgent / TabClaw 等前沿工具

- SpreadsheetAgent：偏复杂表格理解和多格式推理
- TabClaw：偏交互式表格操作、计划可见、可复用技能
- Spreadsheet-RL：偏真实 Excel 环境中的 Agent 训练研究
- Pista：偏可审计、可控制的表格 Agent 操作

**适合定位**

- 先作为技术观察对象
- 不建议马上全员推广
- 可给高级层级或骨干人员研究

---

## Excel 场景推荐落地路径

1. 先用 AI 生成公式和解释公式
2. 再用 AI 生成 Python / Office Script 处理重复表格
3. 把高频 Excel 任务做成脚本或模板
4. 用 n8n / Dify 串接数据来源和输出
5. 对复杂报表再评估 Microsoft 365 Copilot 或专用 Agent

---

## 自动化工作流工具

**代表工具**

- n8n
- Dify Workflow
- browser-use
- OpenClaw 等 Agent 框架

**适合场景**

- 定时拉取数据
- 自动整理 Issue
- 生成日报周报
- 调用模型处理文本
- 将结果发送到邮件或聊天工具

---

## n8n

- 可视化工作流自动化平台
- 支持大量系统集成
- 可自托管或使用云服务
- 支持在流程中调用 AI

**适合开发中心的用法**

- Redmine/Jira 缺陷摘要
- GitLab MR 通知和总结
- 测试报告自动汇总
- 定时生成项目风险清单

---

## browser-use

- 让 AI 操作浏览器
- 适合网页表单、后台系统、信息收集类任务
- 可作为自动化 PoC 工具
- 使用时需要严格控制账号和权限

**适合开发中心的用法**

- 后台系统巡检 PoC
- 网页数据收集
- 重复表单操作验证
- 简单端到端流程探索

---

## 模型网关与治理工具

**代表工具**

- LiteLLM
- Langfuse
- Ollama
- cc-switch / claude-code-router

**适合场景**

- 统一模型 API
- 统计调用成本
- 记录 Prompt 效果
- 管理多模型切换
- 本地模型试验

---

## LiteLLM、Langfuse、Ollama

| 工具 | 主要作用 | 适合谁关注 |
| --- | --- | --- |
| LiteLLM | 模型网关，统一 OpenAI-compatible 调用 | 平台负责人、工具负责人 |
| Langfuse | LLM 调用观测、Prompt 管理、评估 | AI 应用建设人员 |
| Ollama | 本地模型运行 | 个人体验、PoC、内网探索 |

---

## 文档与交付物生成工具

**代表工具**

- ppt-master
- ResearchStudio
- Marp
- Slidev
- MarkItDown
- PptxGenJS
- python-pptx

**适合场景**

- 培训课件
- 项目汇报
- 测试报告
- 技术分享
- 论文或调研材料整理

---

## 工具选型标准

评估一个工具时，看这 8 个问题：

1. 解决的是否是真实高频问题
2. 是否容易上手
3. 是否能接入现有流程
4. 是否支持团队共享
5. 是否可控、可审计
6. 数据和权限是否可接受
7. 成本是否可控
8. 是否有人维护和推广

---

## 推荐试点组合

**个人提效**

- Copilot
- Cherry Studio
- Cline / OpenCode / Aider

**团队知识库**

- Dify 或 RAGFlow
- MarkItDown
- Open WebUI

**Excel 和报表**

- Microsoft 365 Copilot
- ChatGPT / Claude / Gemini
- Python + pandas / openpyxl
- n8n

**平台治理**

- LiteLLM
- Langfuse
- Ollama

---

## 小组讨论

请每组选择一个最想试点的方向：

- 代码开发提效
- 团队知识库
- Excel 自动化
- 测试报告生成
- 缺陷分析自动化
- 文档和 PPT 生成

讨论：

- 当前痛点是什么
- 适合哪个工具
- 预期节省什么时间
- 需要什么权限或环境
- 谁负责试点

---

## 本期作业与打卡

**作业**

- 从本节课提到的工具中选择 1 个进行体验
- 结合真实工作场景完成一次小试用
- 输出一份工具体验报告

**体验报告内容**

- 工具名称
- 试用场景
- 输入内容
- 输出结果
- 是否可用
- 优点
- 缺点
- 是否建议团队继续试点

**打卡内容**

- 你体验了哪个工具
- 解决了什么问题
- 结果是否节省时间
- 有什么风险或限制
- 后续希望深入了解什么工具
