"""Online_Show.py

示例文件用于支撑 Lesson5 的课堂演示场景。
采用订单提交流程与代码评审场景，演示 Markdown 如何组织上下文，
以及 Instruction 如何固化团队对 AI 的输出要求。
"""

from datetime import datetime
from decimal import Decimal
from typing import Dict, List


# ============================================================
# 场景一：Markdown 结构化上下文 —— 订单提交 Bug 信息
# ============================================================

RAW_BUG_NOTES = """
订单提交易报错。用户说点提交后一直转圈，有时提示库存不足。
测试环境，今天上午开始出现。大概是购物车里有两个商品的时候容易出。
后端日志里能看到 submit order failed。最近改过优惠券和库存。
""".strip()


BUG_CONTEXT = {
    "background": "电商系统的提交订单接口，负责校验库存、计算优惠、创建订单。",
    "symptom": "用户点击提交订单后，前端一直转圈，偶发提示库存不足。",
    "steps": [
        "登录测试账号",
        "购物车加入两个商品，其中一个使用优惠券",
        "点击提交订单",
        "接口等待较久，最终失败",
    ],
    "expected": "订单成功创建，库存正确扣减，前端跳转到支付页。",
    "actual": "接口返回失败，部分请求提示库存不足，部分请求超时。",
    "recent_changes": ["优惠券抵扣逻辑重构", "库存预占逻辑增加了批量校验"],
}


def build_bug_analysis_markdown(context: Dict) -> str:
    """将零散问题信息整理为适合交给 AI 的 Markdown。"""
    lines = [
        "# Bug 分析",
        "",
        "## 背景",
        context["background"],
        "",
        "## 现象",
        context["symptom"],
        "",
        "## 复现步骤",
    ]
    for index, step in enumerate(context["steps"], start=1):
        lines.append(f"{index}. {step}")
    lines.extend(
        [
            "",
            "## 期望结果",
            context["expected"],
            "",
            "## 实际结果",
            context["actual"],
            "",
            "## 最近变更",
        ]
    )
    for item in context["recent_changes"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## 希望输出",
            "- 可能原因（按概率排序）",
            "- 每个原因的验证方法",
            "- 建议排查顺序",
        ]
    )
    return "\n".join(lines)


# ============================================================
# 场景二：代码解释 / Review 的演示代码
# ============================================================

PRICE_DB = {
    "SKU-1001": Decimal("199.00"),
    "SKU-1002": Decimal("59.90"),
    "SKU-1003": Decimal("9.90"),
}

INVENTORY_DB = {
    "SKU-1001": 5,
    "SKU-1002": 0,
    "SKU-1003": 20,
}


def submit_order(order_payload: Dict) -> Dict:
    """模拟订单提交，保留一些适合课堂演示的问题点。"""
    if not order_payload:
        return {"code": 400, "message": "order payload is empty"}

    items = order_payload.get("items", [])
    if not items:
        return {"code": 400, "message": "items is empty"}

    total_amount = Decimal("0.00")
    inventory_errors: List[str] = []

    for item in items:
        sku = item.get("sku")
        quantity = item.get("quantity", 0)

        if sku not in PRICE_DB:
            return {"code": 400, "message": f"unknown sku: {sku}"}

        if INVENTORY_DB.get(sku, 0) < quantity:
            inventory_errors.append(f"{sku} inventory not enough")
            continue

        total_amount += PRICE_DB[sku] * quantity

    coupon_code = order_payload.get("coupon_code")
    if coupon_code == "SAVE10":
        total_amount -= Decimal("10.00")
    elif coupon_code == "HALF":
        total_amount = total_amount * Decimal("0.5")

    if inventory_errors:
        return {
            "code": 409,
            "message": "inventory check failed",
            "errors": inventory_errors,
        }

    order_no = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    return {
        "code": 200,
        "order_no": order_no,
        "total_amount": str(total_amount),
        "message": "success",
    }


# ============================================================
# 场景三：Markdown 表格与测试点
# ============================================================

LOGIN_REQUIREMENT = {
    "feature": "后台登录",
    "fields": ["用户名", "密码", "验证码"],
    "rules": [
        "用户名不能为空",
        "密码连续输错 5 次后锁定 10 分钟",
        "验证码错误时不给出过多提示",
    ],
}


def build_test_points_markdown(requirement: Dict) -> str:
    """根据需求整理测试点 Markdown 表格。"""
    rows = [
        "# 测试点清单",
        "",
        f"## 功能\n{requirement['feature']}",
        "",
        "| 分类 | 测试点 | 预期结果 |",
        "| --- | --- | --- |",
        "| 正常场景 | 输入正确用户名、密码、验证码 | 登录成功并跳转首页 |",
        "| 异常场景 | 用户名为空 | 提示用户名不能为空 |",
        "| 异常场景 | 密码错误超过 5 次 | 账号锁定 10 分钟 |",
        "| 安全场景 | 验证码错误 | 提示验证码错误，不泄漏多余信息 |",
    ]
    return "\n".join(rows)


# ============================================================
# 场景四：Instruction 示例文本
# ============================================================

CODE_REVIEW_INSTRUCTION = """
# 代码 Review Instruction

当用户要求 Review 代码时，请始终按以下规则输出：

## 输出顺序
1. 先列出高风险问题
2. 再列出中风险问题
3. 最后列出低风险问题和改进建议

## 重点检查项
- 正确性
- 边界条件
- 异常处理
- 测试覆盖
- 可读性

## 输出要求
- 每个问题说明触发条件和风险
- 只指出问题，不直接大改代码
- 如果信息不足，明确说明缺少什么
""".strip()


CODE_EXPLAIN_INSTRUCTION = """
# 代码解释 Instruction

当用户要求解释代码时，请按以下结构输出：
1. 一句话总结功能
2. 输入参数说明
3. 核心处理流程
4. 返回值说明
5. 可能异常和边界条件
6. 需要人工确认的问题
""".strip()


# ============================================================
# 场景五：团队共享模板索引
# ============================================================

TEAM_TEMPLATE_INDEX = [
    {"name": "Bug 分析 Prompt 模板", "usage": "提交缺陷分析给 Copilot 或内网模型"},
    {"name": "代码 Review Instruction", "usage": "统一 Review 输出结构"},
    {"name": "测试用例 Prompt 模板", "usage": "快速整理测试点"},
]


if __name__ == "__main__":
    print("=" * 60)
    print("Lesson 5 Online Show — Markdown 与 Instruction 演示")
    print("=" * 60)

    print("\n--- 场景一：零散问题信息 vs Markdown 上下文 ---")
    print("原始零散描述：")
    print(RAW_BUG_NOTES)
    print("\n整理后的 Markdown：")
    print(build_bug_analysis_markdown(BUG_CONTEXT))

    print("\n--- 场景二：可供解释 / Review 的代码 ---")
    sample_result = submit_order(
        {
            "items": [
                {"sku": "SKU-1001", "quantity": 1},
                {"sku": "SKU-1002", "quantity": 1},
            ],
            "coupon_code": "HALF",
        }
    )
    print(sample_result)

    print("\n--- 场景三：Markdown 表格 ---")
    print(build_test_points_markdown(LOGIN_REQUIREMENT))

    print("\n--- 场景四：Instruction 示例 ---")
    print(CODE_REVIEW_INSTRUCTION)

    print("\n--- 场景五：团队模板索引 ---")
    for item in TEAM_TEMPLATE_INDEX:
        print(f"- {item['name']}: {item['usage']}")
