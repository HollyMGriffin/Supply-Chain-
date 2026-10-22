let allOrders = [];
let selectedStatus = "All";
let searchTerm = "";

/**
 * Only the supply chain manager gets the Edit and Cancel buttons.
 * The server enforces this too; this just hides the controls.
 */
function canEditOrders() {
    return document.getElementById("ordersTable").dataset.canEdit === "true";
}

/**
 * Retrieves orders from db and calls function to display them
 */
async function loadOrders() {
    try {
        const response = await fetch("/api/orders");

        if (response.status === 401) {
            window.location.href = "/";
            return;
        }

        if (!response.ok) {
            throw new Error("Failed to load orders");
        }

        allOrders = await response.json();

        updateTabCounts();
        showSelectedOrders();

    } catch (error) {
        console.error("Error:", error);
        alert("Connection error. Unable to load orders.");
        allOrders = [];
        updateTabCounts();
        showSelectedOrders();
    }
}

/**
 * Cancels an order by sending a POST request to the server.
 * @param {number} orderId 
 * @returns 
 */
async function cancelOrder(orderId) {
    if (!confirm("Are you sure you want to cancel this order?")) {
        return;
    }

    try {
        const response = await fetch(`/api/orders/${orderId}/cancel`, {
            method: "POST"
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.error || "Unable to cancel order.");
            return;
        }

        alert("Order successfully canceled!");
        loadOrders();

    } catch (error) {
        alert("Connection error. Order was not canceled.");
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
 * Checks if an order's number, material, or supplier contains the
 * search text. An empty search matches every order.
 * @param {*} order
 * @returns {bool}
 */
function matchesSearch(order) {
    if (searchTerm === "") {
        return true;
    }

    return [order.id, order.material, order.supplier].some(value =>
        String(value).toLowerCase().includes(searchTerm)
    );
}

/**
 * Returns the orders that match the current search text.
 */
function getSearchedOrders() {
    return allOrders.filter(matchesSearch);
}

/**
 * Saves the search box text and refreshes the tab counts and table.
 */
function searchOrders() {
    searchTerm = document.getElementById("searchInput").value
        .trim()
        .toLowerCase();

    updateTabCounts();
    showSelectedOrders();
}

/**
 * Updates the count badge on each status tab.
 */
function updateTabCounts() {
    const orders = getSearchedOrders();

    document.querySelectorAll(".status-tab").forEach(tab => {
        const status = tab.dataset.status;
        const count = status === "All"
            ? orders.length
            : orders.filter(order => order.status === status).length;

        tab.querySelector(".tab-count").textContent = count;
    });
}

/**
 * Displays only the orders that match the selected status tab.
 */
function showSelectedOrders() {
    const searchedOrders = getSearchedOrders();
    const orders = selectedStatus === "All"
        ? searchedOrders
        : searchedOrders.filter(order => order.status === selectedStatus);

    displayOrders(orders);
}

/**
 * Marks the clicked tab as active and filters the table.
 * @param {HTMLElement} tab
 */
function selectTab(tab) {
    document.querySelectorAll(".status-tab").forEach(otherTab => {
        otherTab.classList.remove("active");
        otherTab.setAttribute("aria-selected", "false");
    });

    tab.classList.add("active");
    tab.setAttribute("aria-selected", "true");

    selectedStatus = tab.dataset.status;
    showSelectedOrders();
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

        cell.colSpan = canEditOrders() ? 8 : 7;
        cell.textContent = searchTerm === ""
            ? "No orders found."
            : "No orders match your search.";

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

        if (!canEditOrders()) {
            tableBody.appendChild(row);
            return;
        }

        const actionsCell = document.createElement("td");

        const expired = isOrderExpired(order.created_at);

        const editButton = document.createElement("button");
        editButton.textContent = "Edit";
        editButton.disabled = expired || order.status !== "Pending";

        editButton.addEventListener("click", () => {
            window.location.href = `/orders/${order.id}/edit`;
        });

        const cancelButton = document.createElement("button");
        cancelButton.textContent = "Cancel";

        cancelButton.disabled = expired || order.status !== "Pending";
        cancelButton.addEventListener("click", () => cancelOrder(order.id));
        actionsCell.appendChild(editButton);
        actionsCell.appendChild(cancelButton);

        row.appendChild(actionsCell);
        tableBody.appendChild(row);
    });
}


document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".status-tab").forEach(tab => {
        tab.addEventListener("click", () => selectTab(tab));
    });

    const searchInput = document.getElementById("searchInput");

    // Filter as the user types, and also on Enter or the Search button.
    searchInput.addEventListener("input", searchOrders);
    searchInput.addEventListener("keydown", event => {
        if (event.key === "Enter") {
            searchOrders();
        }
    });
    document.getElementById("searchButton")
        .addEventListener("click", searchOrders);

    loadOrders();
});