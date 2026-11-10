/**
 * Checks the current password and saves the new one.
 * @param {SubmitEvent} event
 */
async function changePassword(event) {
    event.preventDefault();

    const passwordError = document.getElementById("passwordError");
    const passwordMessage = document.getElementById("passwordMessage");

    passwordError.textContent = "";
    passwordMessage.textContent = "";

    const data = {
        current_password: document.getElementById("currentPassword").value,
        new_password: document.getElementById("newPassword").value,
        confirm_password: document.getElementById("confirmPassword").value
    };

    if (!data.current_password || !data.new_password || !data.confirm_password) {
        passwordError.textContent = "Please fill out all fields.";
        return;
    }

    if (data.new_password !== data.confirm_password) {
        passwordError.textContent = "New passwords do not match.";
        return;
    }

    try {
        const response = await fetch("/api/account/password", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            passwordError.textContent =
                result.error || "Unable to change password.";
            return;
        }

        passwordMessage.textContent = result.message;
        document.getElementById("passwordForm").reset();
    } catch (error) {
        passwordError.textContent =
            "Connection error. Password was not changed.";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("passwordForm")
        .addEventListener("submit", changePassword);

    document.getElementById("cancelPasswordButton")
        .addEventListener("click", () => {
            window.location.href = "/orders";
        });
});
