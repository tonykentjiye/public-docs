"""Online_Show.py

示例文件用于支撑 Lesson4 的课堂演示场景。
采用线上订单管理系统（与 Lesson2/Lesson3 同一业务域），
用于演示 Prompt 五要素、模糊需求改写、输出格式控制、迭代式提问。

本文件同时提供"模糊上下文"和"完整上下文"两种素材，
方便课堂对比同一个任务在不同 Prompt 写法下的输出质量差异。
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Dict, List, Optional
import json


# ============================================================
# 场景一：五要素演示 —— 运费计算函数
# ============================================================

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
        base = 10.0
        per_kg = 2.0
    else:
        base = 30.0
        per_kg = 5.0

    cost = base + weight * per_kg

    if express:
        cost *= 1.5

    return round(cost, 2)


# ============================================================
# 场景二：模糊需求改写 —— 用户信息保存（含 Bug）
# ============================================================

# 模拟数据库
_user_profile_db: Dict[int, dict] = {
    1: {"nickname": "张三", "phone": "13800000000"},
}


def update_profile(user_id: int, profile: dict) -> dict:
    """
    更新用户个人信息（模拟实现，用于演示 Bug 分析 Prompt）。

    注意：这里故意省略了"写回数据库"的步骤，
    导致页面显示保存成功，但刷新后数据恢复原样。
    """
    # 校验
    if not profile:
        return {"code": 400, "msg": "资料不能为空"}

    nickname = profile.get("nickname")
    phone = profile.get("phone")

    if not nickname or not phone:
        return {"code": 400, "msg": "昵称和手机号不能为空"}

    # 模拟：只更新了内存中的临时对象，没有写回 _user_profile_db
    # 这就是"保存成功但刷新后恢复原样"的 Bug 来源
    temp = dict(_user_profile_db.get(user_id, {}))
    temp["nickname"] = nickname
    temp["phone"] = phone

    # 故意不执行 _user_profile_db[user_id] = temp
    return {"code": 200, "msg": "保存成功"}


def get_profile(user_id: int) -> dict:
    """查询用户信息。"""
    return _user_profile_db.get(user_id, {})


# ============================================================
# 场景三：输出格式控制 —— 订单状态统计
# ============================================================

ORDER_STATUS_PENDING = "PENDING"
ORDER_STATUS_PAID = "PAID"
ORDER_STATUS_SHIPPED = "SHIPPED"
ORDER_STATUS_DELIVERED = "DELIVERED"
ORDER_STATUS_CANCELLED = "CANCELLED"
ORDER_STATUS_REFUNDED = "REFUNDED"

sample_orders: List[Dict] = [
    {"order_id": "O1001", "user_id": "U001", "amount": Decimal("299.99"), "status": ORDER_STATUS_PAID, "created_at": datetime(2026, 7, 1)},
    {"order_id": "O1002", "user_id": "U002", "amount": Decimal("59.99"), "status": ORDER_STATUS_CANCELLED, "created_at": datetime(2026, 7, 2)},
    {"order_id": "O1003", "user_id": "U001", "amount": Decimal("129.50"), "status": ORDER_STATUS_SHIPPED, "created_at": datetime(2026, 7, 5)},
    {"order_id": "O1004", "user_id": "U003", "amount": Decimal("89.00"), "status": ORDER_STATUS_PAID, "created_at": datetime(2026, 7, 8)},
    {"order_id": "O1005", "user_id": "U002", "amount": Decimal("450.00"), "status": ORDER_STATUS_DELIVERED, "created_at": datetime(2026, 7, 10)},
    {"order_id": "O1006", "user_id": "U001", "amount": Decimal("19.99"), "status": ORDER_STATUS_REFUNDED, "created_at": datetime(2026, 7, 12)},
]


def get_order_status_summary(orders: List[Dict]) -> Dict[str, int]:
    """统计各订单状态的数量。"""
    summary: Dict[str, int] = {}
    for order in orders:
        status = order["status"]
        summary[status] = summary.get(status, 0) + 1
    return summary


def get_order_status_summary_markdown(orders: List[Dict]) -> str:
    """以 Markdown 表格形式输出订单状态统计。"""
    summary = get_order_status_summary(orders)
    lines = ["| 状态 | 数量 |", "|------|------|"]
    for status, count in sorted(summary.items()):
        lines.append(f"| {status} | {count} |")
    return "\n".join(lines)


def get_order_status_summary_json(orders: List[Dict]) -> str:
    """以 JSON 形式输出订单状态统计。"""
    return json.dumps(get_order_status_summary(orders), ensure_ascii=False, indent=2)


# ============================================================
# 场景四：迭代式提问 —— 订单搜索接口
# ============================================================

def search_orders(
    user_id: Optional[str] = None,
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = 1,
    size: int = 20,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> Dict:
    """
    搜索订单接口（模拟实现，用于演示迭代式提问）。

    参数:
        user_id: 按用户筛选
        status: 按状态筛选
        keyword: 按商品关键字搜索
        page: 页码（从 1 开始）
        size: 每页条数
        sort_by: 排序字段
        sort_order: 排序方向（asc / desc）

    返回:
        分页查询结果
    """
    # 模拟筛选
    results = sample_orders
    if user_id:
        results = [o for o in results if o["user_id"] == user_id]
    if status:
        results = [o for o in results if o["status"] == status]

    # 模拟分页
    start = (page - 1) * size
    end = start + size
    paged = results[start:end]

    return {
        "code": 200,
        "data": paged,
        "total": len(results),
        "page": page,
        "size": size,
    }


# ============================================================
# 场景五：开发测试常用模板 —— 分类销量 SQL
# ============================================================

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

CATEGORY_SALES_CONTEXT = """
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
"""


# ============================================================
# 场景六：需求分析素材 —— 购物车过期提醒
# ============================================================

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


# ============================================================
# 主程序：演示各场景
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Lesson 4 Online Show — Prompt 基础演示")
    print("=" * 60)

    print("\n--- 场景一：五要素演示（运费计算） ---")
    print(f"calculate_shipping_cost(2.5, 'domestic') = {calculate_shipping_cost(2.5, 'domestic')}")
    print(f"calculate_shipping_cost(2.5, 'domestic', True) = {calculate_shipping_cost(2.5, 'domestic', True)}")
    print(f"calculate_shipping_cost(1.0, 'international') = {calculate_shipping_cost(1.0, 'international')}")

    print("\n--- 场景二：模糊需求改写（用户信息保存 Bug） ---")
    print(f"更新前: {get_profile(1)}")
    result = update_profile(1, {"nickname": "李四", "phone": "13900000000"})
    print(f"保存结果: {result}")
    print(f"更新后: {get_profile(1)}  <- 注意：刷新后数据恢复原样（Bug）")

    print("\n--- 场景三：输出格式控制（订单状态统计） ---")
    print("Markdown 格式:")
    print(get_order_status_summary_markdown(sample_orders))
    print("\nJSON 格式:")
    print(get_order_status_summary_json(sample_orders))

    print("\n--- 场景四：迭代式提问（订单搜索接口） ---")
    result = search_orders(user_id="U001", page=1, size=10)
    print(f"搜索 U001 订单: total={result['total']}, 返回 {len(result['data'])} 条")

    print("\n--- 场景五：开发测试常用模板（分类销量 SQL） ---")
    print("SQL 素材已就绪，可在课堂中复制使用。")

    print("\n--- 场景六：需求分析素材（购物车过期提醒） ---")
    print("需求素材已就绪，可在课堂中复制使用。")
