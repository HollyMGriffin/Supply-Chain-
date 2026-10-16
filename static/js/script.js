
let selectedRow;

/* LOGIN */

function login() {

    let username =
        document.getElementById("username").value;

    let password =
        document.getElementById("password").value;

    if (username === "manager" &&
        password === "1234") {

        document.getElementById("loginPage").style.display =
            "none";

        document.getElementById("dashboard").style.display =
            "block";

        document.getElementById("loginError").style.display =
            "none";

        showOrdersPage();
    }

    else {

        document.getElementById("loginError").style.display =
            "block";
    }
}


/* LOG OUT */

function logout() {

    document.getElementById("dashboard").style.display =
        "none";

    document.getElementById("loginPage").style.display =
        "flex";

    document.getElementById("username").value = "";

    document.getElementById("password").value = "";

    document.getElementById("loginError").style.display =
        "none";
}


/* SHOW CURRENT ORDERS */

function showOrdersPage() {

    document.getElementById("ordersPage").style.display =
        "block";

    document.getElementById("addOrderPage").style.display =
        "none";

    document.getElementById("editOrderPage").style.display =
        "none";
}


/* SEARCH FOR ORDER */

function searchOrder() {

    let orderID =
        document.getElementById("searchOrder").value.trim();

    let table =
        document.getElementById("ordersTable");

    for (let i = 1; i < table.rows.length; i++) {

        if (table.rows[i].cells[0].textContent.trim() === orderID) {

            let button =
                table.rows[i].cells[7].querySelector("button");

            editOrder(button);

            return;
        }
    }

    alert("No such order exists.");
}


/* SHOW ADD ORDER PAGE */

function showAddOrderPage() {

    document.getElementById("ordersPage").style.display =
        "none";

    document.getElementById("editOrderPage").style.display =
        "none";

    document.getElementById("addOrderPage").style.display =
        "block";
}


/* SAVE NEW ORDER */

function saveOrder() {

    let material =
        document.getElementById("material").value;

    let quantity =
        document.getElementById("quantity").value;

    let supplier =
        document.getElementById("supplier").value;

    let cost =
        document.getElementById("cost").value;

    let arrival =
        document.getElementById("arrival").value;

    let required =
        document.getElementById("required").value;

    if (material === "" ||
        quantity === "" ||
        supplier === "" ||
        cost === "" ||
        arrival === "" ||
        required === "") {

        alert("Please fill out all order information.");

        return;
    }

    let table =
        document.getElementById("ordersTable");

    let row =
        table.insertRow();

    row.insertCell(0).textContent =
        "ORD-00" + (table.rows.length - 1);

    row.insertCell(1).textContent =
        material;

    row.insertCell(2).textContent =
        quantity;

    row.insertCell(3).textContent =
        supplier;

    row.insertCell(4).textContent =
        arrival;

    row.insertCell(5).textContent =
        required;

    row.insertCell(6).textContent =
        "Pending";

    row.insertCell(7).innerHTML =
        '<button onclick="editOrder(this)">Edit</button> ' +
        '<button onclick="cancelOrder(this)">Cancel</button>';

    alert("Order successfully added!");

    document.getElementById("material").value = "";
    document.getElementById("quantity").value = "";
    document.getElementById("supplier").value = "";
    document.getElementById("cost").value = "";
    document.getElementById("arrival").value = "";
    document.getElementById("required").value = "";

    showOrdersPage();
}


/* OPEN UPDATE ORDER PAGE */

function editOrder(button) {

    selectedRow =
        button.parentElement.parentElement;

    document.getElementById("editMaterial").value =
        selectedRow.cells[1].textContent;

    document.getElementById("editQuantity").value =
        selectedRow.cells[2].textContent;

    document.getElementById("editSupplier").value =
        selectedRow.cells[3].textContent;

    document.getElementById("editArrival").value =
        selectedRow.cells[4].textContent;

    document.getElementById("editRequired").value =
        selectedRow.cells[5].textContent;

    document.getElementById("ordersPage").style.display =
        "none";

    document.getElementById("addOrderPage").style.display =
        "none";

    document.getElementById("editOrderPage").style.display =
        "block";
}


/* SAVE UPDATED ORDER */

function saveChanges() {

    if (!selectedRow) {

        alert("No such order exists.");

        return;
    }

    let material =
        document.getElementById("editMaterial").value;

    let quantity =
        document.getElementById("editQuantity").value;

    let supplier =
        document.getElementById("editSupplier").value;

    let arrival =
        document.getElementById("editArrival").value;

    let required =
        document.getElementById("editRequired").value;

    if (material.trim() === "" ||
        quantity === "" ||
        supplier.trim() === "" ||
        arrival === "" ||
        required === "") {

        alert("Please fill out all order information.");

        return;
    }

    if (Number(quantity) <= 0) {

        alert("Quantity must be greater than zero.");

        return;
    }

    selectedRow.cells[1].textContent =
        material;

    selectedRow.cells[2].textContent =
        quantity;

    selectedRow.cells[3].textContent =
        supplier;

    selectedRow.cells[4].textContent =
        arrival;

    selectedRow.cells[5].textContent =
        required;

    alert("Order successfully updated!");

    showOrdersPage();
}


/* CANCEL ORDER */

function cancelOrder(button) {

    let row =
        button.parentElement.parentElement;

    if (row.cells[6].textContent === "In Transit" ||
        row.cells[6].textContent === "Shipped") {

        alert("This order cannot be canceled because it has already been shipped.");

        return;
    }

    let answer =
        confirm("Are you sure you want to cancel this order?");

    if (answer) {

        row.cells[6].textContent =
            "Canceled";

        button.disabled =
            true;

        button.textContent =
            "Canceled";

        alert("Order successfully canceled!");
    }
}
