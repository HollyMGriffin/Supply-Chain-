async function login() {
  const username = document.getElementById("username").value;

  const password = document.getElementById("password").value;

  const loginError = document.getElementById("loginError");

  try {
    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: username, password: password })
    });

    if (response.ok) {
      window.location.href = "/orders";
    } else {
      loginError.style.display = "block";
    }
  } catch (error) {
    alert("Connection error. Unable to log in.");
  }
}
