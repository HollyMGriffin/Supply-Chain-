
from flask import Blueprint, jsonify, redirect, request, session
from db.user_repository import get_user_by_username

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    username = str(data.get("username") or "").strip()
    password = str(data.get("password") or "")

    user = get_user_by_username(username)

    # Plaintext comparison for the prototype. Replace with hashed passwords.
    if user is None or user["password"] != password:
        return jsonify(error="Invalid username or password."), 401

    session.clear()
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["display_name"] = user["display_name"]
    session["role"] = user["role"]

    return jsonify(message="Logged in.", role=user["role"])


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
