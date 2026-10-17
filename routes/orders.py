
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from flask import Blueprint, jsonify, request
from db.order_repository import (
    get_all_orders, get_order, add_order,
    update_order, cancel_order
)

orders_bp = Blueprint(
    "orders_api",
    __name__,
    url_prefix="/api/orders"
)
def is_order_expired(order):
    created = datetime.fromisoformat(
        order["created_at"]
    ).replace(tzinfo=timezone.utc)

    return (
        datetime.now(timezone.utc) - created
    ).total_seconds() >= 24 * 60 * 60

def validate_order(data, include_cost=False):
    if not isinstance(data, dict):
        raise ValueError("Invalid order information.")

    material = str(data.get("material") or "").strip()
    supplier = str(data.get("supplier") or "").strip()

    if not material or not supplier:
        raise ValueError("Please enter a material and supplier.")

    try:
        quantity = int(data.get("quantity"))
        if str(data.get("quantity")) != str(quantity) or quantity <= 0:
            raise ValueError()
    except (ValueError, TypeError):
        raise ValueError("Quantity must be a positive whole number.")

    arrival = str(data.get("expected_arrival") or "")
    required = str(data.get("required_by_date") or "")

    try:
        arrival_date = date.fromisoformat(arrival)
        date.fromisoformat(required)

        if arrival_date < date.today():
            raise ValueError("Arrival date cannot be in the past.")

    except ValueError as error:
        if str(error) == "Arrival date cannot be in the past.":
            raise
        raise ValueError("Please enter valid dates.")

    result = {
        "material": material,
        "quantity": quantity,
        "supplier": supplier,
        "expected_arrival": arrival,
        "required_by_date": required
    }

    if include_cost:
        try:
            cost = Decimal(str(data.get("cost")))
            if not cost.is_finite() or cost < 0:
                raise ValueError()
            cents = cost * 100
            if cents != cents.to_integral_value():
                raise ValueError()
            result["cost_cents"] = int(cents)
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError("Please enter a valid cost.")

    return result


@orders_bp.route("", methods=["GET"])
def list_orders():
    return jsonify(get_all_orders())


@orders_bp.route("/<int:order_id>", methods=["GET"])
def read_order(order_id):
    order = get_order(order_id)
    if order is None:
        return jsonify(error="Order not found."), 404
    return jsonify(order)


@orders_bp.route("", methods=["POST"])
def create_order():
    try:
        data = validate_order(request.get_json(silent=True), True)
        order_id = add_order(data)
        return jsonify(
            message="Order successfully added!",
            id=order_id
        ), 201
    except ValueError as error:
        return jsonify(error=str(error)), 400
    except Exception:
        return jsonify(error="Unable to save order."), 500



@orders_bp.route("/<int:order_id>", methods=["PUT"])
def edit_order(order_id):
    order = get_order(order_id)

    if order is None:
        return jsonify(error="Order not found."), 404

    if is_order_expired(order):
        return jsonify(
            error="This order can no longer be edited after 24 hours."
        ), 409

    if order["status"] != "Pending":
        return jsonify(error="This order cannot be updated."), 409

    try:
        data = validate_order(request.get_json(silent=True))

        if not update_order(order_id, data):
            return jsonify(error="Order can no longer be updated."), 409

        return jsonify(message="Order successfully updated!")

    except ValueError as error:
        return jsonify(error=str(error)), 400

    except Exception:
        return jsonify(error="Unable to update order."), 500


@orders_bp.route("/<int:order_id>/cancel", methods=["POST"])
def cancel_existing_order(order_id):
    order = get_order(order_id)

    if order is None:
        return jsonify(error="Order not found."), 404

    if is_order_expired(order):
        return jsonify(
            error="This order can no longer be canceled after 24 hours."
        ), 409

    if order["status"] != "Pending":
        return jsonify(
            error="This order cannot be canceled because it is already delivered or canceled."
        ), 409

    try:
        if not cancel_order(order_id):
            return jsonify(error="Order can no longer be canceled."), 409

        return jsonify(message="Order successfully canceled!")

    except Exception:
        return jsonify(error="Unable to cancel order."), 500


