from functools import wraps
from flask import jsonify, redirect, request, session

SUPPLY_CHAIN_MANAGER = "Supply Chain Manager"
WAREHOUSE_MANAGER = "Warehouse Manager"
EMPLOYEE = "Employee"

# Order statuses each role is allowed to see. None means every status.
VISIBLE_STATUSES = {
    SUPPLY_CHAIN_MANAGER: None,
    WAREHOUSE_MANAGER: ("In Transit", "Delivered"),
    EMPLOYEE: ("Delivered",)
}


def current_user():
    if "user_id" not in session:
        return None

    return {
        "id": session["user_id"],
        "username": session["username"],
        "display_name": session["display_name"],
        "role": session["role"]
    }


def visible_statuses():
    return VISIBLE_STATUSES.get(session.get("role"), ())


def can_view_order(order):
    statuses = visible_statuses()
    return statuses is None or order["status"] in statuses


def can_edit_orders():
    return session.get("role") == SUPPLY_CHAIN_MANAGER


def _is_api_request():
    return request.path.startswith("/api/")


def login_required(view):
    """
    Sends users who aren't logged in back to the login page,
    or returns 401 for API calls.
    """
    @wraps(view)
    def wrapped(*args, **kwargs):
        if current_user() is None:
            if _is_api_request():
                return jsonify(error="Please log in."), 401
            return redirect("/")
        return view(*args, **kwargs)

    return wrapped


def edit_permission_required(view):
    """
    Only the supply chain manager can add, edit, or cancel orders.
    """
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not can_edit_orders():
            if _is_api_request():
                return jsonify(
                    error="You do not have permission to change orders."
                ), 403
            return redirect("/orders")
        return view(*args, **kwargs)

    return wrapped
