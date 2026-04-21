const logoutButton = document.getElementById("logout");

logoutButton.addEventListener("click", async (e) => {
  const response = await fetch("http://localhost:8000/auth/logout", {
    method: "POST",
    headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
  });

  if (!response.ok) {
  }

  localStorage.removeItem("token");
  localStorage.removeItem("refresh_token");
  window.location.href = "../index.html";
});
