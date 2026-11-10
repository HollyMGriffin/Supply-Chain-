
from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, request
from auth import inventory_view_required, inventory_permission_required
from db.inventory_repository import (
    get_all_inventory,
    get_inventory_item,
    add_inventory,
    update_inventory,
    delete_inventory
)

inventory_bp = Blueprint("inventory", __name__)


# Check inventory information before saving
def validate_inventory(data):
    material = str(data.get("material") or "").strip()
    location = str(data.get("location") or "").strip()
    quantity = data.get("quantity")
    cost = data.get("cost")

    if not material:
        return None, "Material is required."

    if not location:
        return None, "Warehouse location is required."

    # Quantity must be a whole number
    if isinstance(quantity, bool):
        return None, "Quantity must be a whole number."

    if isinstance(quantity, int):
        pass
    elif isinstance(quantity, str) and quantity.strip().isdigit():
        quantity = int(quantity.strip())
    else:
        return None, "Quantity must be a whole number."

    if quantity < 0:
        return None, "Quantity cannot be negative."

    # Cost must be a valid dollar amount
    if cost is None or isinstance(cost, bool):
        return None, "Cost per unit is required."

    try:
        unit_cost = Decimal(str(cost))
    except (InvalidOperation, ValueError):
        return None, "Enter a valid cost per unit."

    if not unit_cost.is_finite():
        return None, "Enter a valid cost per unit."

    if unit_cost < 0:
        return None, "Cost cannot be negative."

    # Convert dollars into cents
    cost_cents = unit_cost * 100

    if cost_cents != cost_cents.to_integral_value():
        return None, "Cost can have at most 2 decimal places."

    return {
        "material": material,
        "quantity": quantity,
        "location": location,
        "cost_cents": int(cost_cents)
    }, None


# View all inventory items
@inventory_bp.route("/api/inventory", methods=["GET"])
@inventory_view_required
def list_inventory():
    return jsonify(get_all_inventory())


# View one inventory item
@inventory_bp.route("/api/inventory/<int:item_id>", methods=["GET"])
@inventory_view_required
def view_inventory(item_id):
    item = get_inventory_item(item_id)

    if item is None:
        return jsonify(error="Inventory item not found."), 404

    return jsonify(item)


# Add a new inventory item
@inventory_bp.route("/api/inventory", methods=["POST"])
@inventory_permission_required
def create_inventory():
    data = request.get_json(silent=True) or {}
    inventory_data, error = validate_inventory(data)

    if error:
        return jsonify(error=error), 400

    item_id = add_inventory(inventory_data)

    return jsonify(
        message="Inventory added successfully.",
        id=item_id
    ), 201


# Edit an existing inventory item
@inventory_bp.route("/api/inventory/<int:item_id>", methods=["PUT"])
@inventory_permission_required
def edit_inventory(item_id):
    data = request.get_json(silent=True) or {}
    inventory_data, error = validate_inventory(data)

    if error:
        return jsonify(error=error), 400

    updated = update_inventory(item_id, inventory_data)

    if not updated:
        return jsonify(error="Inventory item not found."), 404

    return jsonify(message="Inventory updated successfully.")


# Delete an inventory item
@inventory_bp.route("/api/inventory/<int:item_id>", methods=["DELETE"])
@inventory_permission_required
def remove_inventory(item_id):
    try:
        deleted = delete_inventory(item_id)
    except ValueError as error:
        return jsonify(error=str(error)), 409

    if not deleted:
        return jsonify(error="Inventory item not found."), 404

    return jsonify(message="Inventory deleted successfully.")
