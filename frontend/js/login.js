const form = document.getElementById("form");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = emailInput.value;
  const password = passwordInput.value;

  const body = new URLSearchParams({
    username: email,
    password: password,
  });

  const response = await fetch("http://localhost:8000/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: body,
  });

  if (!response.ok) {
    console.log("Get an error message in the page");
    alert("Invalid email or password");
  }

  const data = await response.json();
  localStorage.setItem("token", data.token);

  window.location.href = "dashboard.html";
  console.log(localStorage.getItem("token"));
});
