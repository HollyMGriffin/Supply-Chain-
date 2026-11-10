
from flask import Blueprint, jsonify, redirect, request, session
from auth import login_required
from db.user_repository import (
    get_user_by_username, get_user_by_id, update_password
)
from passwords import hash_password, verify_password, validate_new_password

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    username = str(data.get("username") or "").strip()
    password = str(data.get("password") or "")

    user = get_user_by_username(username)

    if user is None or not verify_password(password, user["password_hash"]):
        return jsonify(error="Invalid username or password."), 401

    session.clear()
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["display_name"] = user["display_name"]
    session["role"] = user["role"]

    return jsonify(message="Logged in.", role=user["role"])


@auth_bp.route("/api/account/password", methods=["POST"])
@login_required
def change_password():
    data = request.get_json(silent=True) or {}

    current_password = str(data.get("current_password") or "")
    new_password = str(data.get("new_password") or "")
    confirm_password = str(data.get("confirm_password") or "")

    user = get_user_by_id(session["user_id"])

    if user is None:
        session.clear()
        return jsonify(error="Please log in."), 401

    if not verify_password(current_password, user["password_hash"]):
        return jsonify(error="Current password is incorrect."), 400

    error = validate_new_password(new_password)
    if error:
        return jsonify(error=error), 400

    if new_password != confirm_password:
        return jsonify(error="New passwords do not match."), 400

    if new_password == current_password:
        return jsonify(
            error="New password must be different from the current one."
        ), 400

    update_password(user["id"], hash_password(new_password))

    return jsonify(message="Password changed successfully.")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
