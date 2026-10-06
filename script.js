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


    /* CHECK FOR EMPTY INFORMATION */

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


    row.insertCell(0).innerHTML =
        "ORD-00" + (table.rows.length - 1);

    row.insertCell(1).innerHTML =
        material;

    row.insertCell(2).innerHTML =
        quantity;

    row.insertCell(3).innerHTML =
        supplier;

    row.insertCell(4).innerHTML =
        arrival;

    row.insertCell(5).innerHTML =
        required;

    row.insertCell(6).innerHTML =
        "Pending";

    row.insertCell(7).innerHTML =
        '<button onclick="editOrder(this)">Edit</button> ' +
        '<button onclick="cancelOrder(this)">Cancel</button>';


    alert("Order successfully added!");


    /* CLEAR FORM */

    document.getElementById("material").value = "";

    document.getElementById("quantity").value = "";

    document.getElementById("supplier").value = "";

    document.getElementById("cost").value = "";

    document.getElementById("arrival").value = "";

    document.getElementById("required").value = "";


    /* RETURN TO CURRENT ORDERS */

    showOrdersPage();
}


/* OPEN UPDATE ORDER PAGE */

function editOrder(button) {

    selectedRow =
        button.parentElement.parentElement;


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


    document.getElementById("ordersPage").style.display =
        "none";

    document.getElementById("addOrderPage").style.display =
        "none";

    document.getElementById("editOrderPage").style.display =
        "block";
}


/* SAVE UPDATED ORDER */

function saveChanges() {

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


    if (material === "" ||
        quantity === "" ||
        supplier === "" ||
        arrival === "" ||
        required === "") {

        alert("Please fill out all order information.");

        return;
    }


    selectedRow.cells[1].innerHTML =
        material;

    selectedRow.cells[2].innerHTML =
        quantity;

    selectedRow.cells[3].innerHTML =
        supplier;

    selectedRow.cells[4].innerHTML =
        arrival;

    selectedRow.cells[5].innerHTML =
        required;


    alert("Order successfully updated!");


    showOrdersPage();
}


/* CANCEL ORDER */

function cancelOrder(button) {

    let answer =
        confirm("Are you sure you want to cancel this order?");


    if (answer) {

        let row =
            button.parentElement.parentElement;


        row.cells[6].innerHTML =
            "Canceled";


        button.disabled =
            true;

        button.innerHTML =
            "Canceled";


        alert("Order successfully canceled!");
    }
}