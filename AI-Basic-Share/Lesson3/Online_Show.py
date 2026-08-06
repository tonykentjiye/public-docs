"""Online_Show.py

示例文件用于支撑 Lesson3 的课堂演示场景。
采用线上订单管理系统（与 Lesson2 同一业务域），
新增工程实践场景：Bug 分析、异常日志分析、单元测试生成、
测试用例补充、重构建议、代码审查辅助。
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Dict, List, Optional, Tuple
import json
import math
import random

# ============================================================
# 场景一：Bug 分析 —— 折扣计算函数（含浮点数精度 Bug）
# ============================================================

def calculate_discount_v2(price: float, quantity: int, discount_rate: float) -> dict:
    """
    计算商品折扣信息。

    参数:
        price: 商品单价
        quantity: 购买数量
        discount_rate: 折扣率（0.0 ~ 1.0）

    返回:
        包含原价、折扣金额、折后价的字典
    """
    subtotal = price * quantity
    discount = subtotal * discount_rate
    final = subtotal - discount

    return {
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "final": round(final, 2),
    }


def batch_calculate_discount(items: List[dict]) -> List[dict]:
    """
    批量计算订单中每个商品的折扣。

    参数:
        items: 商品列表，每项包含 price, quantity, discount_rate

    返回:
        每个商品的折扣计算结果
    """
    results = []
    for item in items:
        result = calculate_discount_v2(
            item["price"],
            item["quantity"],
            item["discount_rate"],
        )
        result["name"] = item["name"]
        results.append(result)
    return results


# ============================================================
# 场景二：异常日志分析 —— 订单导入服务（模拟日志场景）
# ============================================================

# 模拟的订单号生成器（含 Bug：可能生成重复订单号）
_order_id_counter = 1000
_generated_order_nos: set = set()


def generate_order_no(date_str: str) -> str:
    """生成订单号：ORD-{日期}-{序号}"""
    global _order_id_counter
    _order_id_counter += 1
    return f"ORD-{date_str}-{_order_id_counter:04d}"


def batch_import_orders(orders: List[dict]) -> dict:
    """
    批量导入订单（模拟实现，用于演示异常日志分析）。

    参数:
        orders: 待导入的订单列表

    返回:
        导入结果统计
    """
    imported = 0
    failed = 0
    skipped = 0
    errors = []

    for idx, order in enumerate(orders, start=1):
        try:
            # 模拟校验
            if not order.get("order_no"):
                # 自动生成订单号（可能重复）
                order["order_no"] = generate_order_no(
                    datetime.now().strftime("%Y%m%d")
                )

            # 模拟唯一键冲突
            if order["order_no"] in _generated_order_nos:
                raise ValueError(
                    f"Duplicate entry '{order['order_no']}' for key 'orders.order_no'"
                )

            # 模拟其他校验
            if not order.get("user_id"):
                raise ValueError("user_id 不能为空")

            if not order.get("amount", 0) > 0:
                raise ValueError("订单金额必须大于0")

            # 模拟保存成功
            _generated_order_nos.add(order["order_no"])
            imported += 1

        except ValueError as e:
            failed += 1
            errors.append(f"第 {idx} 条记录导入失败: {e}")
        except Exception as e:
            failed += 1
            errors.append(f"第 {idx} 条记录发生未知错误: {e}")

    skipped = len(orders) - imported - failed

    return {
        "total": len(orders),
        "imported": imported,
        "failed": failed,
        "skipped": skipped,
        "errors": errors,
    }


# ============================================================
# 场景三：单元测试生成 —— 字符串与数据工具类
# ============================================================

class OrderUtils:
    """订单工具类，包含字符串处理和格式化方法。"""

    @staticmethod
    def format_order_id(raw_id: str) -> str:
        """
        格式化订单 ID：去除多余空格，统一为大写。

        示例:
            "  ord-1001  " -> "ORD-1001"
        """
        if not raw_id:
            return ""
        return raw_id.strip().upper()

    @staticmethod
    def mask_phone(phone: str) -> str:
        """
        隐藏手机号中间四位。

        示例:
            "13812345678" -> "138****5678"
        """
        if not phone or len(phone) != 11:
            return phone
        return phone[:3] + "****" + phone[7:]

    @staticmethod
    def parse_order_date(date_str: str) -> Optional[date]:
        """
        解析订单日期字符串，支持多种格式。

        支持格式: YYYY-MM-DD, YYYY/MM/DD, YYYYMMDD
        """
        if not date_str:
            return None

        date_str = date_str.strip()
        formats = ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue

        return None

    @staticmethod
    def validate_order_status(status: str) -> bool:
        """
        验证订单状态是否合法。

        合法状态: PENDING, PAID, SHIPPED, DELIVERED, CANCELLED, REFUNDED
        """
        valid_statuses = {
            "PENDING", "PAID", "SHIPPED",
            "DELIVERED", "CANCELLED", "REFUNDED",
        }
        return status.upper() in valid_statuses


# ============================================================
# 场景四：测试用例补充 —— 优惠券计算逻辑
# ============================================================

def calculate_coupon_discount(
    subtotal: Decimal,
    coupon_type: str,
    coupon_value: Decimal,
    user_level: str = "normal",
) -> Dict:
    """
    根据优惠券类型和用户等级计算折扣金额。

    优惠券类型:
        - "fixed": 固定金额减免，coupon_value 为减免金额
        - "percent": 百分比折扣，coupon_value 为折扣率（如 0.1 表示 10%）
        - "threshold": 满减，coupon_value 为减免金额，需满足最低消费

    用户等级影响:
        - "vip": 在计算结果上额外打 9 折
        - "normal": 无额外折扣

    规则:
        - 固定金额减免不能超过 subtotal
        - 百分比折扣最高 50%（coupon_value <= 0.5）
        - 满减最低消费为 100 元
        - 计算结果保留两位小数
    """
    if subtotal <= 0:
        return {"code": 400, "message": "订单金额必须大于0", "discount": Decimal("0.00")}

    if coupon_type == "fixed":
        if coupon_value < 0:
            return {"code": 400, "message": "优惠金额不能为负数", "discount": Decimal("0.00")}
        discount = min(coupon_value, subtotal)

    elif coupon_type == "percent":
        if coupon_value < 0 or coupon_value > 0.5:
            return {"code": 400, "message": "折扣率必须在0~50%之间", "discount": Decimal("0.00")}
        discount = subtotal * coupon_value

    elif coupon_type == "threshold":
        if subtotal < Decimal("100.00"):
            return {"code": 400, "message": "未达到最低消费100元", "discount": Decimal("0.00")}
        if coupon_value < 0:
            return {"code": 400, "message": "优惠金额不能为负数", "discount": Decimal("0.00")}
        discount = min(coupon_value, subtotal)

    else:
        return {"code": 400, "message": f"不支持的优惠券类型: {coupon_type}", "discount": Decimal("0.00")}

    # VIP 用户额外 9 折
    if user_level == "vip":
        discount = discount * Decimal("0.9")

    discount = discount.quantize(Decimal("0.01"))

    return {"code": 200, "message": "success", "discount": discount}


# ============================================================
# 场景五：重构建议 —— 遗留订单处理函数（可维护性差）
# ============================================================

def legacy_process_refund(refund_data: dict) -> dict:
    """
    处理退款申请（遗留代码，可维护性差）。

    这个函数做了太多事情：验证、计算、更新状态、发送通知。
    """
    # 验证退款数据
    if not refund_data:
        return {"code": 400, "msg": "退款数据不能为空"}
    if "order_id" not in refund_data:
        return {"code": 400, "msg": "缺少订单ID"}
    if "amount" not in refund_data:
        return {"code": 400, "msg": "缺少退款金额"}
    if "reason" not in refund_data:
        return {"code": 400, "msg": "缺少退款原因"}

    refund_amount = refund_data["amount"]
    if not isinstance(refund_amount, (int, float, Decimal)):
        return {"code": 400, "msg": "退款金额格式不正确"}
    if refund_amount <= 0:
        return {"code": 400, "msg": "退款金额必须大于0"}

    # 模拟查询原始订单
    original_order = {
        "order_id": refund_data["order_id"],
        "total_amount": 299.99,
        "paid_amount": 299.99,
        "status": "PAID",
        "items": [
            {"name": "商品A", "price": 99.99, "quantity": 2},
            {"name": "商品B", "price": 99.99, "quantity": 1},
        ],
    }

    # 检查订单状态
    if original_order["status"] not in ["PAID", "SHIPPED", "DELIVERED"]:
        return {"code": 400, "msg": "当前订单状态不支持退款"}
    if refund_amount > original_order["paid_amount"]:
        return {"code": 400, "msg": "退款金额不能超过已支付金额"}

    # 计算退款后金额
    remaining = original_order["paid_amount"] - refund_amount

    # 更新订单状态
    if remaining == 0:
        new_status = "REFUNDED"
    else:
        new_status = "PARTIALLY_REFUNDED"

    # 记录退款日志
    refund_log = {
        "refund_id": f"RF{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "order_id": refund_data["order_id"],
        "amount": refund_amount,
        "reason": refund_data["reason"],
        "status": "SUCCESS",
        "created_at": str(datetime.now()),
    }

    # 发送通知
    print(f"[通知] 订单 {refund_data['order_id']} 退款 {refund_amount} 元")
    print(f"[通知] 退款原因: {refund_data['reason']}")
    print(f"[通知] 退款后订单状态: {new_status}")

    # 发送邮件（模拟）
    email_content = f"""
    尊敬的客户，您的订单 {refund_data['order_id']} 已退款 {refund_amount} 元。
    退款原因：{refund_data['reason']}
    如有疑问请联系客服。
    """
    print(f"[邮件] {email_content}")

    return {
        "code": 200,
        "msg": "退款成功",
        "data": {
            "refund": refund_log,
            "remaining": remaining,
            "new_status": new_status,
        },
    }


# ============================================================
# 场景六：代码审查辅助 —— 用户 API 处理函数
# ============================================================

# 模拟内存数据库
_user_db: Dict[int, dict] = {}
_next_user_id = 1


def create_user_api(request_body: str) -> str:
    """
    创建用户 API 处理函数（含多个代码质量问题）。

    参数:
        request_body: JSON 格式的请求体字符串

    返回:
        JSON 格式的响应字符串
    """
    global _next_user_id

    try:
        data = json.loads(request_body)
    except json.JSONDecodeError:
        return json.dumps({"error": "请求格式错误"})

    username = data.get("username", "")
    email = data.get("email", "")
    age = data.get("age", 0)
    phone = data.get("phone", "")

    # 校验用户名
    if len(username) < 2:
        return json.dumps({"error": "用户名至少2个字符"})

    # 校验邮箱
    if "@" not in email:
        return json.dumps({"error": "邮箱格式不正确"})

    # 校验年龄
    if age < 0 or age > 150:
        return json.dumps({"error": "年龄必须在0~150之间"})

    # 检查用户名重复
    for uid, user in _user_db.items():
        if user["username"] == username:
            return json.dumps({"error": "用户名已存在"})

    # 创建用户
    user = {
        "id": _next_user_id,
        "username": username,
        "email": email,
        "age": age,
        "phone": phone,
        "status": "active",
        "created_at": str(datetime.now()),
    }
    _user_db[_next_user_id] = user
    _next_user_id += 1

    return json.dumps({"code": 201, "data": user})


def get_user_api(user_id: str) -> str:
    """
    查询用户 API 处理函数。

    参数:
        user_id: 用户 ID 字符串

    返回:
        JSON 格式的响应字符串
    """
    try:
        uid = int(user_id)
    except (ValueError, TypeError):
        return json.dumps({"error": "用户ID格式不正确"})

    user = _user_db.get(uid)
    if not user:
        return json.dumps({"error": "用户不存在"})

    return json.dumps({"code": 200, "data": user})


def update_user_api(user_id: str, request_body: str) -> str:
    """
    更新用户 API 处理函数。

    参数:
        user_id: 用户 ID 字符串
        request_body: JSON 格式的请求体字符串

    返回:
        JSON 格式的响应字符串
    """
    try:
        uid = int(user_id)
    except (ValueError, TypeError):
        return json.dumps({"error": "用户ID格式不正确"})

    if uid not in _user_db:
        return json.dumps({"error": "用户不存在"})

    try:
        data = json.loads(request_body)
    except json.JSONDecodeError:
        return json.dumps({"error": "请求格式错误"})

    user = _user_db[uid]

    # 逐字段更新（没有校验）
    if "username" in data:
        user["username"] = data["username"]
    if "email" in data:
        user["email"] = data["email"]
    if "age" in data:
        user["age"] = data["age"]
    if "phone" in data:
        user["phone"] = data["phone"]

    user["updated_at"] = str(datetime.now())
    _user_db[uid] = user

    return json.dumps({"code": 200, "data": user})


def list_users_api(page: int = 1, page_size: int = 10) -> str:
    """
    用户列表 API 处理函数。

    参数:
        page: 页码
        page_size: 每页条数

    返回:
        JSON 格式的响应字符串
    """
    all_users = list(_user_db.values())
    total = len(all_users)

    start = (page - 1) * page_size
    end = start + page_size
    paged_users = all_users[start:end]

    return json.dumps({
        "code": 200,
        "data": {
            "users": paged_users,
            "total": total,
            "page": page,
            "page_size": page_size,
        },
    })


# ============================================================
# 主程序：演示各场景
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Lesson 3 Online Show — 工程实践演示")
    print("=" * 60)

    print("\n--- 场景一：Bug 分析 ---")
    items = [
        {"name": "商品A", "price": 19.99, "quantity": 3, "discount_rate": 0.1},
        {"name": "商品B", "price": 29.99, "quantity": 2, "discount_rate": 0.15},
        {"name": "商品C", "price": 9.99, "quantity": 5, "discount_rate": 0.0},
        {"name": "商品D", "price": 1.05, "quantity": 1, "discount_rate": 0.1},
        {"name": "商品E", "price": 0.07, "quantity": 10, "discount_rate": 0.1},
    ]
    results = batch_calculate_discount(items)
    for r in results:
        print(f"{r['name']}: 小计={r['subtotal']}, 折扣={r['discount']}, 最终={r['final']}")

    # 验证：小计 - 折扣 是否等于 最终价（浮点数精度问题演示）
    print("\n--- 精度验证 ---")
    for r in results:
        expected = round(r["subtotal"] - r["discount"], 2)
        match = "✓" if expected == r["final"] else "✗ BUG!"
        print(f"{r['name']}: {r['subtotal']} - {r['discount']} = {expected}, 实际={r['final']} {match}")

    print("\n--- 场景二：异常日志分析 ---")
    test_orders = [
        {"order_no": "ORD-20260712-0001", "user_id": "U001", "amount": 299.99},
        {"order_no": "ORD-20260712-0001", "user_id": "U002", "amount": 199.99},
        {"user_id": "U003", "amount": -50},
    ]
    result = batch_import_orders(test_orders)
    print(f"导入结果: 成功={result['imported']}, 失败={result['failed']}, 跳过={result['skipped']}")
    for err in result["errors"]:
        print(f"  [错误] {err}")

    print("\n--- 场景三：单元测试生成 ---")
    utils = OrderUtils()
    print(f"format_order_id('  ord-1001  ') = {utils.format_order_id('  ord-1001  ')}")
    print(f"mask_phone('13812345678') = {utils.mask_phone('13812345678')}")
    print(f"parse_order_date('2026-07-15') = {utils.parse_order_date('2026-07-15')}")
    print(f"validate_order_status('paid') = {utils.validate_order_status('paid')}")

    print("\n--- 场景四：测试用例补充 ---")
    result = calculate_coupon_discount(
        subtotal=Decimal("200.00"),
        coupon_type="threshold",
        coupon_value=Decimal("30.00"),
        user_level="vip",
    )
    print(f"满减+VIP: {result}")

    print("\n--- 场景五：重构建议 ---")
    refund_result = legacy_process_refund({
        "order_id": "O1001",
        "amount": 99.99,
        "reason": "商品质量问题",
    })
    print(f"退款结果: {refund_result['code']}, {refund_result['msg']}")

    print("\n--- 场景六：代码审查辅助 ---")
    resp = create_user_api('{"username": "alice", "email": "alice@test.com", "age": 25}')
    print(f"创建用户: {resp}")
    resp = get_user_api("1")
    print(f"查询用户: {resp}")
