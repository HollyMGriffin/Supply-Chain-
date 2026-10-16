from flask import Blueprint, jsonify
from db.order_repository import get_all_orders

orders_bp = Blueprint(
    "orders_api",
    __name__,
    url_prefix="/api/orders"
)


@orders_bp.route("", methods=["GET"])
def list_orders():
    orders = get_all_orders()
    return jsonify(orders)