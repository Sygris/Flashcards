const form = document.getElementById("form");
const emailInput = document.getElementById("email")
const passwordInput = document.getElementById("password")

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  
  const email = emailInput.value;
  const password = passwordInput.value;

  const response = await fetch("http://localhost:8000/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({email, password})
  });

  const data = await response.json();
  console.log(data);
});
