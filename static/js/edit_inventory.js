
// Sprint 3: Edit Warehouse Inventory

const inventoryForm = document.getElementById("inventory-form");
const inventoryError = document.getElementById("inventory-error");

// Get inventory item ID from the URL
const pathParts = window.location.pathname.split("/");
const itemId = pathParts[2];


// Load the existing inventory information
async function loadInventoryItem() {
    try {
        const response = await fetch(`/api/inventory/${itemId}`);
        const item = await response.json();

        if (!response.ok) {
            throw new Error(item.error || "Unable to load inventory.");
        }

        // Fill the form with the current inventory information
        document.getElementById("material").value = item.material;
        document.getElementById("quantity").value = item.quantity;
        document.getElementById("location").value = item.location;
        document.getElementById("cost").value =
            (item.cost_cents / 100).toFixed(2);

    } catch (error) {
        inventoryError.textContent = error.message;
    }
}


// Save changes to the inventory item
inventoryForm.addEventListener("submit", async function(event) {
    event.preventDefault();

    // Get updated information from the form
    const material = document.getElementById("material").value.trim();
    const quantity = document.getElementById("quantity").value;
    const location = document.getElementById("location").value.trim();
    const cost = document.getElementById("cost").value;

    inventoryError.textContent = "";

    // Check required fields
    if (!material || !location || quantity === "" || cost === "") {
        inventoryError.textContent = "Please fill out all fields.";
        return;
    }

    // Check quantity
    if (!Number.isInteger(Number(quantity)) || Number(quantity) < 0) {
        inventoryError.textContent =
            "Quantity must be a whole number and cannot be negative.";
        return;
    }

    // Check cost
    if (!Number.isFinite(Number(cost)) || Number(cost) < 0) {
        inventoryError.textContent =
            "Cost must be a valid nonnegative amount.";
        return;
    }

    // Prepare updated inventory information
    const inventoryData = {
        material: material,
        quantity: Number(quantity),
        location: location,
        cost: cost
    };

    try {
        // Send updated inventory to Flask
        const response = await fetch(`/api/inventory/${itemId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(inventoryData)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Unable to update inventory.");
        }

        // Return to Inventory page after saving
        window.location.href = "/inventory";

    } catch (error) {
        inventoryError.textContent = error.message;
    }
});


// Load inventory information when the page opens
document.addEventListener("DOMContentLoaded", loadInventoryItem);
