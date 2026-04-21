# Karlovy Vary – Semestral Project Backend
**Group 13:** Barış Coşkun · Doğa Acar · Hakan Öğretmen · Ali Efe Gülertekin

---

## 📁 Project Structure

```
karlovy-vary-backend/
│
├── app.py                  ← Flask backend (main server)
├── karlovy_vary.db         ← SQLite database (auto-created on first run)
├── README.md
│
└── karlovy-vary-full/      ← Complete frontend (original + new pages)
    ├── index.html
    ├── landmarks.html
    ├── culture.html
    ├── reservation.html
    ├── contact.html
    ├── login.html              ← NEW: Login / Register page
    ├── my-reservations.html    ← NEW: Logged-in user's reservations
    ├── admin.html              ← NEW: Admin panel
    ├── js/
    │   ├── contact.js          ← UPDATED: calls backend API
    │   ├── reservation.js      ← UPDATED: calls backend API
    │   └── landmarks.js
    ├── styles/
    └── img/
```

---

## ⚙️ Backend Setup

### Requirements
- Python 3.8+
- pip

### Install dependencies
```bash
pip install flask flask-cors
```

### Run the server
```bash
python app.py
```

Server will start at: **http://localhost:5000**

The SQLite database (`karlovy_vary.db`) is automatically created on first run.

---

## 🌐 Running the Frontend

Open the `karlovy-vary-full/` folder with a local server.

**Option 1 – VS Code Live Server** (recommended):
Right-click `index.html` → "Open with Live Server"

**Option 2 – Python built-in server:**
```bash
cd karlovy-vary-full
python -m http.server 5500
```
Then open: http://localhost:5500

---

## 🔌 API Endpoints

| Method | URL | Description | Auth Required |
|--------|-----|-------------|:---:|
| POST | `/api/auth/register` | Register new user | ❌ |
| POST | `/api/auth/login` | Login | ❌ |
| POST | `/api/auth/logout` | Logout | ❌ |
| GET  | `/api/auth/me` | Check login status | ❌ |
| POST | `/api/contact` | Submit contact message | ❌ |
| POST | `/api/reservations` | Submit reservation | ❌ |
| GET  | `/api/reservations/my` | My reservations | ✅ |
| GET  | `/api/landmarks?category=spa` | Get landmarks | ❌ |
| GET  | `/api/admin/reservations` | All reservations | ✅ |
| GET  | `/api/admin/messages` | All messages | ✅ |

---

## 🗄️ Database Tables

| Table | Description |
|-------|-------------|
| `users` | Registered users (username, email, hashed password) |
| `reservations` | Reservation requests from the form |
| `messages` | Contact form submissions |
| `landmarks` | Landmark content (pre-seeded) |

---

## 👥 User Roles

| Feature | Guest (not logged in) | Registered User |
|---------|:---------------------:|:---------------:|
| Browse pages | ✅ | ✅ |
| Submit contact form | ✅ | ✅ |
| Submit reservation | ✅ | ✅ |
| View own reservations | ❌ | ✅ |
| View admin panel | ❌ | ✅ |

---

## 📋 Hoca Gereksinimleri – Karşılanan Maddeler

- ✅ **Backend + veritabanı** – Flask + SQLite
- ✅ **Dinamik içerik üretimi** – Rezervasyonlar DB'den çekiliyor
- ✅ **API (client–server iletişim)** – REST API endpointleri
- ✅ **Kimlik doğrulama / kullanıcı yönetimi** – Session cookie tabanlı login/register
- ✅ **Form kullanımı** – Contact + Reservation formları backend'e bağlı
- ✅ **Kayıtlı ve kayıtsız kullanıcı için farklı fonksiyonlar**
- ✅ **Yönetim (admin) paneli** – admin.html
- ✅ **Erişilebilirlik / kullanılabilirlik** – Mevcut frontend'in üzerine inşa edildi
