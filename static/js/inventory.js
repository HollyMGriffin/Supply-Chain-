
// Sprint 3: Warehouse Inventory

// Format cents as dollars
function formatMoney(cents) {
    return (cents / 100).toLocaleString("en-US", {
        style: "currency",
        currency: "USD"
    });
}


// Load inventory from the database
async function loadInventory() {
    const table = document.getElementById("inventory-table");

    try {
        const response = await fetch("/api/inventory");

        if (!response.ok) {
            throw new Error("Unable to load inventory.");
        }

        const items = await response.json();

        // Clear the table
        table.innerHTML = "";

        // No inventory has been added yet
        if (items.length === 0) {
            const row = document.createElement("tr");
            const cell = document.createElement("td");

            cell.colSpan = 8;
            cell.textContent = "No inventory items found.";

            row.appendChild(cell);
            table.appendChild(row);
            return;
        }

        // Display each inventory item
        items.forEach(item => {
            const row = document.createElement("tr");

            // Calculate total inventory value
            const totalValue = item.quantity * item.cost_cents;

            const values = [
                item.id,
                item.material,
                item.quantity,
                item.location,
                formatMoney(item.cost_cents),
                formatMoney(totalValue),
                item.updated_at
            ];

            values.forEach(value => {
                const cell = document.createElement("td");
                cell.textContent = value;
                row.appendChild(cell);
            });

            // Edit button
            const actions = document.createElement("td");

            const editButton = document.createElement("button");
            editButton.textContent = "Edit";
            editButton.addEventListener("click", () => {
                window.location.href = `/inventory/${item.id}/edit`;
            });

            // Delete button
            const deleteButton = document.createElement("button");
            deleteButton.textContent = "Delete";
            deleteButton.addEventListener("click", () => {
                deleteInventory(item.id);
            });

            actions.appendChild(editButton);
            actions.appendChild(deleteButton);
            row.appendChild(actions);

            table.appendChild(row);
        });

    } catch (error) {
        table.innerHTML = "";

        const row = document.createElement("tr");
        const cell = document.createElement("td");

        cell.colSpan = 8;
        cell.textContent = error.message;

        row.appendChild(cell);
        table.appendChild(row);
    }
}


// Delete an inventory item
async function deleteInventory(itemId) {
    const confirmed = confirm(
        "Are you sure you want to delete this inventory item?"
    );

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(`/api/inventory/${itemId}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || "Unable to delete inventory.");
        }

        // Refresh inventory after deletion
        await loadInventory();

    } catch (error) {
        alert(error.message);
    }
}


// Load inventory when the page opens
document.addEventListener("DOMContentLoaded", loadInventory);
