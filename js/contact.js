// contact.js – Backend API'ye bağlı versiyon
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("contact-form");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const name    = document.getElementById("name").value.trim();
    const subject = document.getElementById("subject").value.trim();
    const message = document.getElementById("message").value.trim();

    if (!name || !subject || !message) {
      showMessage("Please fill in all fields.", "error");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ name, subject, message }),
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

  function showMessage(msg, type) {
    // Mevcut mesajı kaldır
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
    document.querySelector(".contact-button").after(div);
  }
});
