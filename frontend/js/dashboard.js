async function refreshToken() {
  const response = await fetch("http://localhost:8000/auth/refresh", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      refresh_token: localStorage.getItem("refresh_token"),
    }),
  });

  if (!response.ok) {
    const data = await response.json();
    console.log(data);
    window.location.href = "../index.html";
    return;
  }

  const data = await response.json();
  console.log("New access token" + data["new_access_token"]);
  localStorage.setItem("token", data["new_access_token"]);
  location.reload();
}

async function loadDecks() {
  const response = await fetch("http://localhost:8000/decks/", {
    method: "GET",
    headers: { Authorization: "Bearer " + localStorage.getItem("token") },
  });

  if (response.status == 401) {
    refreshToken();
    console.log("Refresh Successful");
  }

  const decks = await response.json();

  const decksCountText = document.getElementById("decks-count");
  decksCountText.textContent = decks.length + " decks";

  console.log(decks);
}

loadDecks();
//

// async function loadDecks() {
//   try {
//     const response = await fetch("http://localhost:8000/decks/", {
//       method: "GET",
//       headers: { Authorization: "Bearer " + localStorage.getItem("token") },
//     });
//
//     if (!response.ok) {
//       throw new Error(`Response status: ${response.status}`);
//     }
//
//     const decks = await response.json();
//     const deccksCountText = document.getElementById("decks-count");
//     deccksCountText.textContent = decks.length + " decks";
//   } catch (error) {
//     console.error(error.message);
//   }
// }
//
// loadDecks();
