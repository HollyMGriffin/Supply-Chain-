let inventoryItems = [];
let editingOrder = null;

async function loadInventoryOptions(selectId, selectedId = null) {
  const response = await fetch("/api/inventory");
  if (!response.ok) throw new Error("Could not load warehouse inventory.");
  inventoryItems = await response.json();
  const select = document.getElementById(selectId);
  select.replaceChildren(new Option("Select warehouse material", ""));
  for (const item of inventoryItems) {
    if (item.quantity > 0 || item.id === Number(selectedId)) {
      const current = editingOrder && editingOrder.inventory_id === item.id ? editingOrder.quantity : 0;
      select.add(new Option(`${item.material} — ${item.location} (${item.quantity + current} available)`, String(item.id)));
    }
  }
  if (selectedId != null) select.value = String(selectedId);
  const info = document.getElementById(selectId === "material" ? "stockInfo" : "editStockInfo");
  const showStock = () => {
    const item = inventoryItems.find(x => x.id === Number(select.value));
    const own = editingOrder && editingOrder.inventory_id === item?.id ? editingOrder.quantity : 0;
    info.textContent = item ? `${item.quantity + own} units available` : "";
  };
  select.addEventListener("change", showStock);
  showStock();
}


async function saveOrder() {
  const inventory_id = Number(document.getElementById("material").value);
  const material = inventoryItems.find(item => item.id === inventory_id)?.material || "";
  const quantity = document.getElementById("quantity").value;
  const arrival = document.getElementById("arrival").value;
  const required = document.getElementById("required").value;

  if (!material || quantity === "" || !arrival || !required) {
    alert("Please fill out all order information.");
    return;
  }

  if (Number(quantity) <= 0 || !Number.isInteger(Number(quantity))) {
    alert("Quantity must be a positive whole number.");
    return;
  }

  const data = {
    material: material,
    inventory_id: inventory_id,
    quantity: Number(quantity),
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

    editingOrder = order;
    await loadInventoryOptions("editMaterial", order.inventory_id);
    document.getElementById("editQuantity").value = order.quantity;
    document.getElementById("editArrival").value = order.expected_arrival;
    document.getElementById("editRequired").value = order.required_by_date;
  } catch (error) {
    alert("Connection error. Unable to load order.");
  }
}


async function saveChanges() {
  const form = document.getElementById("editOrderForm");
  const orderId = form.dataset.orderId;

  const inventory_id = Number(document.getElementById("editMaterial").value);
  const material = inventoryItems.find(item => item.id === inventory_id)?.material || "";
  const quantity = document.getElementById("editQuantity").value;
  const arrival = document.getElementById("editArrival").value;
  const required = document.getElementById("editRequired").value;

  if (!material || quantity === "" || !arrival || !required) {
    alert("Please fill out all order information.");
    return;
  }

  if (Number(quantity) <= 0 || !Number.isInteger(Number(quantity))) {
    alert("Quantity must be a positive whole number.");
    return;
  }

  const data = {
    material: material,
    inventory_id: inventory_id,
    quantity: Number(quantity),
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

// Buttons are wired up here instead of with onclick, because the
// Content-Security-Policy header blocks inline event handlers.
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("cancelOrderButton").addEventListener("click", () => {
    window.location.href = "/orders";
  });

  const saveOrderButton = document.getElementById("saveOrderButton");
  if (saveOrderButton) {
    saveOrderButton.addEventListener("click", saveOrder);
  }

  const saveChangesButton = document.getElementById("saveChangesButton");
  if (saveChangesButton) {
    saveChangesButton.addEventListener("click", saveChanges);
  }

  if (saveOrderButton) {
    loadInventoryOptions("material").catch(error => alert(error.message));
  }
  loadEditOrder();
});
