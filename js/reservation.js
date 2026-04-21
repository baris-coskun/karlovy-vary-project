// reservation.js – Backend API'ye bağlı versiyon
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("reservation-form");

  // Kullanıcı giriş yapmışsa formu email ile doldur
  checkLoginStatus();

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
      fullName:  document.getElementById("fullName").value.trim(),
      email:     document.getElementById("email").value.trim(),
      arrival:   document.getElementById("arrival").value,
      departure: document.getElementById("departure").value,
      guests:    document.getElementById("guests").value,
      type:      document.getElementById("type").value,
      notes:     document.getElementById("notes").value.trim(),
    };

    if (!data.fullName || !data.email || !data.arrival || !data.departure || !data.guests || !data.type) {
      showMessage("Please fill in all required fields.", "error");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/api/reservations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (result.success) {
        showMessage(result.message, "success");
        form.reset();
      } else {
        showMessage(result.message || "An error occurred.", "error");
      }
    } catch (err) {
      showMessage("Could not connect to server. Please try again.", "error");
    }
  });

  async function checkLoginStatus() {
    try {
      const res = await fetch("http://localhost:5000/api/auth/me", { credentials: "include" });
      const data = await res.json();
      if (data.loggedIn) {
        const notice = document.createElement("div");
        notice.style.cssText = "padding:8px 12px; background:#e8f4f8; border-radius:5px; margin-bottom:12px; font-size:14px; color:#1a6a8a;";
        notice.textContent = `✅ Logged in as: ${data.username}`;
        document.querySelector(".reservation-right").prepend(notice);
      }
    } catch {}
  }

  function showMessage(msg, type) {
    const existing = document.querySelector(".form-feedback");
    if (existing) existing.remove();

    const div = document.createElement("div");
    div.className = "form-feedback";
    div.textContent = msg;
    div.style.cssText = `
      padding: 12px 16px;
      margin-top: 12px;
      border-radius: 6px;
      font-size: 14px;
      background: ${type === "success" ? "#d4edda" : "#f8d7da"};
      color: ${type === "success" ? "#155724" : "#721c24"};
      border: 1px solid ${type === "success" ? "#c3e6cb" : "#f5c6cb"};
    `;
    document.querySelector(".reservation-button").after(div);
  }
});
