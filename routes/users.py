
import sqlite3

from flask import Blueprint, jsonify, request
from auth import (
    admin_required, ADMIN, SUPPLY_CHAIN_MANAGER, WAREHOUSE_MANAGER, EMPLOYEE
)
from db.user_repository import get_all_users, add_user
from passwords import hash_password, validate_new_password

users_bp = Blueprint("users", __name__, url_prefix="/api/users")

ROLES = (ADMIN, SUPPLY_CHAIN_MANAGER, WAREHOUSE_MANAGER, EMPLOYEE)


@users_bp.route("", methods=["GET"])
@admin_required
def list_users():
    return jsonify(get_all_users())


@users_bp.route("", methods=["POST"])
@admin_required
def create_user():
    data = request.get_json(silent=True) or {}

    username = str(data.get("username") or "").strip()
    display_name = str(data.get("display_name") or "").strip() or username
    password = str(data.get("password") or "")
    role = str(data.get("role") or "")

    if not username:
        return jsonify(error="Username is required."), 400

    if role not in ROLES:
        return jsonify(error="Please choose a valid role."), 400

    error = validate_new_password(password)
    if error:
        return jsonify(error=error), 400

    try:
        user_id = add_user(username, hash_password(password), display_name, role)
    except sqlite3.IntegrityError:
        return jsonify(error="That username is already taken."), 409

    return jsonify(message="Account created successfully.", id=user_id), 201
