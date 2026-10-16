from flask import Flask, render_template
from routes.orders import orders_bp

app = Flask(__name__)
app.register_blueprint(orders_bp)

@app.route("/")
def login_page():
    return render_template("login.html")


@app.route("/orders")
def orders_page():
    return render_template("orders.html")


@app.route("/orders/new")
def add_order_page():
    return render_template("add_order.html")


@app.route("/orders/<int:order_id>/edit")
def edit_order_page(order_id):
    return render_template(
        "edit_order.html",
        order_id=order_id
    )

if __name__ == "__main__":
    app.run(debug=True)