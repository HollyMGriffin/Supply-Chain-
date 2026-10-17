
async function saveOrder() {
  const material = document.getElementById("material").value.trim();
  const quantity = document.getElementById("quantity").value;
  const supplier = document.getElementById("supplier").value.trim();
  const cost = document.getElementById("cost").value;
  const arrival = document.getElementById("arrival").value;
  const required = document.getElementById("required").value;

  if (!material || !supplier || quantity === "" ||
      cost === "" || !arrival || !required) {
    alert("Please fill out all order information.");
    return;
  }

  if (Number(quantity) <= 0 || !Number.isInteger(Number(quantity))) {
    alert("Quantity must be a positive whole number.");
    return;
  }

  if (!Number.isFinite(Number(cost)) || Number(cost) < 0) {
    alert("Please enter a valid cost.");
    return;
  }

  const data = {
    material: material,
    quantity: Number(quantity),
    supplier: supplier,
    cost: cost,
    expected_arrival: arrival,
    required_by_date: required
  };

  try {
    const response = await fetch("/api/orders", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok) {
      alert(result.error || "Unable to save order.");
      return;
    }

    alert(result.message);
    window.location.href = "/orders";
  } catch (error) {
    alert("Connection error. Order was not saved.");
  }
}


async function loadEditOrder() {
  const form = document.getElementById("editOrderForm");
  if (!form) return;

  const orderId = form.dataset.orderId;

  try {
    const response = await fetch(`/api/orders/${orderId}`);
    const order = await response.json();

    if (!response.ok) {
      alert(order.error || "Unable to load order.");
      return;
    }

    document.getElementById("editMaterial").value = order.material;
    document.getElementById("editQuantity").value = order.quantity;
    document.getElementById("editSupplier").value = order.supplier;
    document.getElementById("editArrival").value = order.expected_arrival;
    document.getElementById("editRequired").value = order.required_by_date;
  } catch (error) {
    alert("Connection error. Unable to load order.");
  }
}


async function saveChanges() {
  const form = document.getElementById("editOrderForm");
  const orderId = form.dataset.orderId;

  const material = document.getElementById("editMaterial").value.trim();
  const quantity = document.getElementById("editQuantity").value;
  const supplier = document.getElementById("editSupplier").value.trim();
  const arrival = document.getElementById("editArrival").value;
  const required = document.getElementById("editRequired").value;

  if (!material || !supplier || quantity === "" ||
      !arrival || !required) {
    alert("Please fill out all order information.");
    return;
  }

  if (Number(quantity) <= 0 || !Number.isInteger(Number(quantity))) {
    alert("Quantity must be a positive whole number.");
    return;
  }

  const data = {
    material: material,
    quantity: Number(quantity),
    supplier: supplier,
    expected_arrival: arrival,
    required_by_date: required
  };

  try {
    const response = await fetch(`/api/orders/${orderId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok) {
      alert(result.error || "Unable to update order.");
      return;
    }

    alert(result.message);
    window.location.href = "/orders";
  } catch (error) {
    alert("Connection error. Order was not updated.");
  }
}

document.addEventListener("DOMContentLoaded", loadEditOrder);
