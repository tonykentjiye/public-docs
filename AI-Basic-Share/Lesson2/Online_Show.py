"""Online_Show.py

示例文件用于支撑 Lesson2 的课堂演示场景。
采用线上订单管理业务场景，包含订单校验、金额计算、统计和订单创建。
"""

from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional

ORDER_STATUS_PENDING = "PENDING"
ORDER_STATUS_PAID = "PAID"
ORDER_STATUS_CANCELLED = "CANCELLED"
ORDER_STATUS_REFUNDED = "REFUNDED"

sample_orders: List[Dict] = [
    {
        "order_id": "O1001",
        "user_id": "U001",
        "items": [
            {"sku": "A100", "price": Decimal("29.99"), "quantity": 2},
            {"sku": "B200", "price": Decimal("15.50"), "quantity": 1},
        ],
        "discount_rate": Decimal("0.10"),
        "status": ORDER_STATUS_PAID,
        "created_at": datetime(2026, 7, 1, 10, 15),
    },
    {
        "order_id": "O1002",
        "user_id": "U002",
        "items": [
            {"sku": "C300", "price": Decimal("49.00"), "quantity": 1},
        ],
        "discount_rate": Decimal("0.00"),
        "status": ORDER_STATUS_CANCELLED,
        "created_at": datetime(2026, 7, 2, 14, 30),
    },
    {
        "order_id": "O1003",
        "user_id": "U001",
        "items": [
            {"sku": "A100", "price": Decimal("29.99"), "quantity": 1},
            {"sku": "D400", "price": Decimal("9.99"), "quantity": 3},
        ],
        "discount_rate": Decimal("0.05"),
        "status": ORDER_STATUS_PAID,
        "created_at": datetime(2026, 7, 10, 9, 20),
    },
]


def parse_date(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d")


def calculate_order_total(items: List[Dict], discount_rate: Decimal = Decimal("0.0")) -> Dict[str, Decimal]:
    """注文金額の内訳を計算する。

    引数:
        items: 注文内の商品一覧。各要素には price と quantity が含まれる。
        discount_rate: 割引率。0 から 1 の範囲内で指定する。

    戻り値:
        subtotal、discount_rate、discounted、tax、total を含む辞書。

    例外:
        割引率が 0 から 1 の範囲外の場合、ValueError を送出する。
    """
    subtotal = sum(item["price"] * item["quantity"] for item in items)
    if discount_rate < 0 or discount_rate > 1:
        raise ValueError("折扣率必须在0到1之间")
    discounted = (subtotal * (Decimal("1.0") - discount_rate)).quantize(Decimal("0.01"))
    tax = (discounted * Decimal("0.08")).quantize(Decimal("0.01"))
    total = (discounted + tax).quantize(Decimal("0.01"))
    return {
        "subtotal": subtotal.quantize(Decimal("0.01")),
        "discount_rate": discount_rate,
        "discounted": discounted,
        "tax": tax,
        "total": total,
    }


def validate_order_payload(payload: Dict) -> List[str]:
    errors = []

    if not isinstance(payload, dict):
        return ["payload 必须是字典"]

    user_id = payload.get("user_id")
    if not isinstance(user_id, str) or not user_id.strip():
        errors.append("user_id 不能为空")

    items = payload.get("items")
    if not isinstance(items, list) or not items:
        errors.append("items 必须是非空列表")
    else:
        for index, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                errors.append(f"第 {index} 个商品必须是字典")
                continue

            sku = item.get("sku")
            if not isinstance(sku, str) or not sku.strip():
                errors.append(f"第 {index} 个商品 sku 不能为空")

            quantity = item.get("quantity")
            if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
                errors.append(f"第 {index} 个商品 quantity 必须是大于0的整数")

            price = item.get("price")
            if not isinstance(price, Decimal) or price <= 0:
                errors.append(f"第 {index} 个商品 price 必须是大于0的 Decimal")

    order_date = payload.get("order_date")
    if not isinstance(order_date, str) or not order_date.strip():
        errors.append("order_date 不能为空")
    else:
        try:
            parse_date(order_date)
        except ValueError:
            errors.append("order_date 格式必须是 YYYY-MM-DD")

    if "discount_rate" in payload:
        rate = payload["discount_rate"]
        if not isinstance(rate, Decimal) or rate < 0 or rate > 1:
            errors.append("discount_rate 必须是0到1之间的 Decimal")

    return errors


def create_order(payload: Dict) -> Dict:
    errors = validate_order_payload(payload)
    if errors:
        raise ValueError(f"订单数据无效: {errors}")
    return {
        "order_id": f"O{len(sample_orders) + 1001}",
        "user_id": payload["user_id"],
        "items": payload["items"],
        "discount_rate": payload.get("discount_rate", Decimal("0.0")),
        "status": ORDER_STATUS_PENDING,
        "created_at": parse_date(payload["order_date"]),
    }


def get_valid_order_count(user_id: str, start_date: str, end_date: str) -> int:
    """ユーザーIDと日付範囲に基づいて、支払い済み注文数を集計する。"""
    start = parse_date(start_date)
    end = parse_date(end_date)
    count = 0
    for order in sample_orders:
        if order["user_id"] != user_id:
            continue
        if order["status"] != ORDER_STATUS_PAID:
            continue
        if not (start <= order["created_at"] <= end):
            continue
        count += 1
    return count


def get_monthly_sales_by_user(user_id: str, orders: List[Dict], year: int, month: int) -> Decimal:
    total = Decimal("0.00")
    for order in orders:
        if order["user_id"] != user_id:
            continue
        if order["status"] != ORDER_STATUS_PAID:
            continue
        if order["created_at"].year != year or order["created_at"].month != month:
            continue
        total += calculate_order_total(order["items"], order["discount_rate"])["total"]
    return total


def build_monthly_paid_order_total_sql(year: int, month: int) -> str:
    """本月の支払い済み注文をユーザー別に集計するSQLを返す。"""
    return f"""
    SELECT
        u.user_id,
        u.name,
        COALESCE(SUM(o.order_amount), 0) AS total_amount
    FROM orders AS o
    JOIN users AS u ON o.user_id = u.user_id
    WHERE o.status = 'PAID'
      AND EXTRACT(YEAR FROM o.created_at) = {year}
      AND EXTRACT(MONTH FROM o.created_at) = {month}
    GROUP BY u.user_id, u.name
    ORDER BY total_amount DESC;
    """
