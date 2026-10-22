import os
from flask import Flask, redirect, render_template
from auth import (
    current_user, login_required, edit_permission_required,
    can_edit_orders, visible_statuses
)
from database import initialize_database
from routes.auth import auth_bp
from routes.orders import orders_bp

app = Flask(__name__)
# Set SECRET_KEY in the environment for anything beyond local testing.
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")
app.register_blueprint(auth_bp)
app.register_blueprint(orders_bp)

initialize_database()


@app.context_processor
def inject_user():
    statuses = visible_statuses()
    return {
        "user": current_user(),
        "can_edit": can_edit_orders(),
        "visible_statuses": list(statuses) if statuses is not None else None
    }


@app.route("/")
def login_page():
    if current_user() is not None:
        return redirect("/orders")
    return render_template("login.html")


@app.route("/orders")
@login_required
def orders_page():
    return render_template("orders.html")


@app.route("/orders/new")
@edit_permission_required
def add_order_page():
    return render_template("add_order.html")


@app.route("/orders/<int:order_id>/edit")
@edit_permission_required
def edit_order_page(order_id):
    return render_template(
        "edit_order.html",
        order_id=order_id
    )

if __name__ == "__main__":
    app.run(debug=True)