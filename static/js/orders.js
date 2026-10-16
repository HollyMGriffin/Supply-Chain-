/**
 * Retrieves orders from db and calls function to display them
 */
async function loadOrders() {
    try {
        const response = await fetch("/api/orders");

        if (!response.ok) {
            throw new Error("Failed to load orders");
        }

        const orders = await response.json();

        displayOrders(orders)

    } catch (error) {
        console.error("Error:", error);
    }
}

/**
 * Checks if 24 hours have passed since order creation. Used
 * to decide if the edit and cancel buttons should be enabled.
 * @param {string} createdAt 
 * @returns {bool}
 */
function isOrderExpired(createdAt) {
    const createdDate = new Date(
        createdAt.replace(" ", "T") + "Z"
    );

    const now = new Date();

    const oneDayInMilliseconds = 24 * 60 * 60 * 1000;

    return now.getTime() - createdDate.getTime() >= oneDayInMilliseconds;
}

/**
 * Creates table rows for each order in the db.
 * @param {*} orders 
 * @returns 
 */
function displayOrders(orders) {
    const tableBody = document.getElementById("ordersTableBody");

    tableBody.replaceChildren();

    if (orders.length === 0) {
        const row = document.createElement("tr");
        const cell = document.createElement("td");

        cell.colSpan = 8;
        cell.textContent = "No orders found.";

        row.appendChild(cell);
        tableBody.appendChild(row);
        return;
    }

    orders.forEach(order => {
        const row = document.createElement("tr");

        const values = [
            order.id,
            order.material,
            order.quantity,
            order.supplier,
            order.expected_arrival,
            order.required_by_date,
            order.status
        ];

        values.forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });

        const actionsCell = document.createElement("td");

        const expired = isOrderExpired(order.created_at);

        const editButton = document.createElement("button");
        editButton.textContent = "Edit";
        editButton.disabled = expired;

        editButton.addEventListener("click", () => {
            window.location.href = `/orders/${order.id}/edit`;
        });

        const cancelButton = document.createElement("button");
        cancelButton.textContent = "Cancel";

        cancelButton.disabled = true;

        actionsCell.appendChild(editButton);
        actionsCell.appendChild(cancelButton);

        row.appendChild(actionsCell);
        tableBody.appendChild(row);
    });
}


document.addEventListener("DOMContentLoaded", loadOrders);