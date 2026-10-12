function login() {
  const username = document.getElementById("username").value;

  const password = document.getElementById("password").value;

  if (username === "manager" && password === "1234") {
    window.location.href = "/orders";
  } else {
    document.getElementById("loginError").style.display = "block";
  }
}
