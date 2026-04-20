async function refreshToken() {
  const response = await fetch("http://localhost:8000/auth/refresh", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      refresh_token: localStorage.getItem("refresh_token"),
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    window.location.href = "../index.html";
    return;
  }

  localStorage.setItem("token", data["new_access_token"]);
  loadDecks(true);
}

async function loadDecks(retried = false) {
  try {
    const response = await fetch("http://localhost:8000/decks/", {
      method: "GET",
      headers: { Authorization: "Bearer " + localStorage.getItem("token") },
    });

    if (response.status == 401) {
      if (retried) {
        window.location.href = "../index.html";
        return;
      }

      return await refreshToken();
    }

    const decks = await response.json();
    const deccksCountText = document.getElementById("decks-count");
    deccksCountText.textContent = decks.length + " decks";
  } catch (error) {
    console.error(error.message);
  }
}

loadDecks();
