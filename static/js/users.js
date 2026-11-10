/**
 * Loads every account into the Existing Accounts table.
 */
async function loadUsers() {
    const tableBody = document.getElementById("usersTableBody");

    try {
        const response = await fetch("/api/users");
        const users = await response.json();

        if (!response.ok) {
            throw new Error(users.error || "Unable to load accounts.");
        }

        tableBody.replaceChildren();

        users.forEach(user => {
            const row = document.createElement("tr");

            [user.username, user.display_name, user.role].forEach(value => {
                const cell = document.createElement("td");
                cell.textContent = value;
                row.appendChild(cell);
            });

            tableBody.appendChild(row);
        });
    } catch (error) {
        const row = document.createElement("tr");
        const cell = document.createElement("td");

        cell.colSpan = 3;
        cell.textContent = error.message;

        row.appendChild(cell);
        tableBody.replaceChildren(row);
    }
}

/**
 * Sends the new account to the server. The server hashes the password
 * before it is stored.
 * @param {SubmitEvent} event
 */
async function createUser(event) {
    event.preventDefault();

    const userError = document.getElementById("userError");
    const userMessage = document.getElementById("userMessage");

    userError.textContent = "";
    userMessage.textContent = "";

    const data = {
        username: document.getElementById("newUsername").value.trim(),
        display_name: document.getElementById("newDisplayName").value.trim(),
        password: document.getElementById("newPassword").value,
        role: document.getElementById("newRole").value
    };

    if (!data.username || !data.password || !data.role) {
        userError.textContent = "Please enter a username, password, and role.";
        return;
    }

    try {
        const response = await fetch("/api/users", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            userError.textContent = result.error || "Unable to create account.";
            return;
        }

        userMessage.textContent = `Account "${data.username}" created.`;
        document.getElementById("userForm").reset();
        loadUsers();
    } catch (error) {
        userError.textContent = "Connection error. Account was not created.";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("userForm")
        .addEventListener("submit", createUser);

    loadUsers();
});
