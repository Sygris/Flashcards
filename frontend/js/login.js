const form = document.getElementById("login-form");
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
    ErrorMessage();
    return;
  }

  const data = await response.json();
  localStorage.setItem("token", data.token);
  localStorage.setItem("refresh_token", data.refresh_token);

  window.location.href = "dashboard.html";
});

function ErrorMessage() {
  passwordInput.value = "";

  const errorMessage = document.getElementById("login-fail");
  errorMessage.style.display = "block";

  emailInput.classList.add("error-outline");
  passwordInput.classList.add("error-outline");
}
