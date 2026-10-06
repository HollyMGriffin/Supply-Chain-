let selectedRow;
function showAddOrder() {
    document.getElementById("addOrderForm").style.display = "block";
}

function hideAddOrder() {
    document.getElementById("addOrderForm").style.display = "none";
}

function saveOrder() {
    alert("Order successfully added!");
    hideAddOrder();
}
function saveOrder() {
    let material = document.getElementById("material").value;
    let quantity = document.getElementById("quantity").value;
    let supplier = document.getElementById("supplier").value;
    let cost = document.getElementById("cost").value;
    let arrival = document.getElementById("arrival").value;
    let required = document.getElementById("required").value;

    if (material === "" || quantity === "" || supplier === "" ||
        cost === "" || arrival === "" || required === "") {

        alert("Please fill out all order information.");
        return;
    }

    let table = document.getElementById("ordersTable");

    let row = table.insertRow();

    row.insertCell(0).innerHTML = "ORD-003";
    row.insertCell(1).innerHTML = material;
    row.insertCell(2).innerHTML = quantity;
    row.insertCell(3).innerHTML = supplier;
    row.insertCell(4).innerHTML = arrival;
    row.insertCell(5).innerHTML = required;
    row.insertCell(6).innerHTML = "Pending";

    row.insertCell(7).innerHTML =
        '<button onclick="editOrder(this)">Edit</button> ' +
        '<button onclick="cancelOrder(this)">Cancel</button>';

    alert("Order successfully added!");

    hideAddOrder();
}
function editOrder(button) {
    selectedRow = button.parentElement.parentElement;

    document.getElementById("editMaterial").value =
        selectedRow.cells[1].innerHTML;

    document.getElementById("editQuantity").value =
        selectedRow.cells[2].innerHTML;

    document.getElementById("editSupplier").value =
        selectedRow.cells[3].innerHTML;

    document.getElementById("editArrival").value =
        selectedRow.cells[4].innerHTML;

    document.getElementById("editRequired").value =
        selectedRow.cells[5].innerHTML;

    document.getElementById("editOrderForm").style.display = "block";
}

function hideEditOrder() {
    document.getElementById("editOrderForm").style.display = "none";
}

function saveChanges() {
    selectedRow.cells[1].innerHTML =
        document.getElementById("editMaterial").value;

    selectedRow.cells[2].innerHTML =
        document.getElementById("editQuantity").value;

    selectedRow.cells[3].innerHTML =
        document.getElementById("editSupplier").value;

    selectedRow.cells[4].innerHTML =
        document.getElementById("editArrival").value;

    selectedRow.cells[5].innerHTML =
        document.getElementById("editRequired").value;

    alert("Order successfully updated!");

    hideEditOrder();
}
function cancelOrder(button) {
    let answer = confirm("Are you sure you want to cancel this order?");

    if (answer) {
        let row = button.parentElement.parentElement;

        row.cells[6].innerHTML = "Canceled";

        button.disabled = true;
        button.innerHTML = "Canceled";

        alert("Order successfully canceled!");
    }
}