
// Sprint 3: Add Inventory Form

const inventoryForm = document.getElementById("inventory-form");
const inventoryError = document.getElementById("inventory-error");

inventoryForm.addEventListener("submit", async function(event) {
    event.preventDefault();

    // Get the information entered by the Warehouse Manager
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

    // Prepare inventory information
    const inventoryData = {
        material: material,
        quantity: Number(quantity),
        location: location,
        cost: cost
    };

    try {
        // Send inventory to Flask
        const response = await fetch("/api/inventory", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(inventoryData)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Unable to save inventory.");
        }

        // Return to Inventory page after saving
        window.location.href = "/inventory";

    } catch (error) {
        inventoryError.textContent = error.message;
    }
});
