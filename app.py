"""
Karlovy Vary Tourism Website - Backend Server
Group 13: Barış Coşkun, Doğa Acar, Hakan Öğretmen, Ali Efe Gülertekin
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
import sqlite3
import hashlib
import os
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = "karlovy_vary_secret_key_2025"  # Production'da env variable kullan
CORS(app, supports_credentials=True, origins=["http://localhost:3000", "http://127.0.0.1:5500", "*"])

DB_PATH = "karlovy_vary.db"

# ─────────────────────────────────────────────
#  DATABASE SETUP
# ─────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT    UNIQUE NOT NULL,
            email       TEXT    UNIQUE NOT NULL,
            password    TEXT    NOT NULL,
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    """)

    # Reservations table
    c.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name       TEXT    NOT NULL,
            email           TEXT    NOT NULL,
            arrival         TEXT    NOT NULL,
            departure       TEXT    NOT NULL,
            guests          INTEGER NOT NULL,
            type            TEXT    NOT NULL,
            notes           TEXT,
            user_id         INTEGER REFERENCES users(id),
            submitted_at    TEXT    DEFAULT (datetime('now'))
        )
    """)

    # Contact messages table
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT    NOT NULL,
            subject         TEXT    NOT NULL,
            message         TEXT    NOT NULL,
            submitted_at    TEXT    DEFAULT (datetime('now'))
        )
    """)

    # Landmarks table (admin can manage)
    c.execute("""
        CREATE TABLE IF NOT EXISTS landmarks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            category    TEXT    NOT NULL,
            title       TEXT    NOT NULL,
            description TEXT    NOT NULL,
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    """)

    # Seed landmarks data
    c.execute("SELECT COUNT(*) FROM landmarks")
    if c.fetchone()[0] == 0:
        landmarks_data = [
            ("spa",       "Hot Springs",       "The hot springs of Karlovy Vary are the most important natural phenomenon of the city. Thermal water rises from deep underground and is traditionally used for drinking treatments and spa therapies."),
            ("spa",       "Colonnades",        "The colonnades serve as elegant shelters for the mineral springs. They are characteristic architectural structures that combine functionality with artistic design."),
            ("spa",       "Spa Architecture",  "Many spa buildings were constructed in the 18th and 19th centuries, reflecting classical and neo-renaissance styles."),
            ("church",    "Historic Churches", "Several churches in the city date back to the 18th century, featuring rich decorations, sculptures, and paintings."),
            ("church",    "Sacral Architecture","Church buildings demonstrate Baroque and neo-Gothic elements, emphasizing vertical structures and decorative facades."),
            ("church",    "Cultural Importance","Church monuments play an important role in local traditions, concerts, and cultural events."),
            ("towers",    "Observation Towers", "Observation towers allow visitors to view the city from elevated positions and remain popular sightseeing spots."),
            ("towers",    "Scenic Viewpoints",  "Natural viewpoints are located along forest paths and hills, providing peaceful places to admire the spa town landscape."),
            ("towers",    "Tourist Routes",     "Many towers and viewpoints are connected by walking and hiking routes combining physical activity with sightseeing."),
            ("protected", "Historical Villas",  "Many villas were originally built as residences for wealthy spa guests, showcasing elegant designs and decorative facades."),
            ("protected", "Preservation Efforts","Strict regulations ensure that protected buildings are properly maintained through restoration projects."),
            ("protected", "Cultural Heritage",  "Protected buildings help tell the story of the city's past, connecting architectural beauty with historical significance."),
        ]
        c.executemany("INSERT INTO landmarks (category, title, description) VALUES (?,?,?)", landmarks_data)

    conn.commit()
    conn.close()
    print("✅ Database initialized.")

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    return re.match(r'^[^@]+@[^@]+\.[^@]+$', email)

def current_user():
    return session.get("user_id")

# ─────────────────────────────────────────────
#  AUTH ROUTES
# ─────────────────────────────────────────────

@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    username = (data.get("username") or "").strip()
    email    = (data.get("email")    or "").strip()
    password = (data.get("password") or "").strip()

    if not username or not email or not password:
        return jsonify({"success": False, "message": "All fields are required."}), 400
    if len(username) < 3:
        return jsonify({"success": False, "message": "Username must be at least 3 characters."}), 400
    if not validate_email(email):
        return jsonify({"success": False, "message": "Invalid email address."}), 400
    if len(password) < 6:
        return jsonify({"success": False, "message": "Password must be at least 6 characters."}), 400

    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO users (username, email, password) VALUES (?,?,?)",
            (username, email, hash_password(password))
        )
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Registration successful! You can now log in."}), 201
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "Username or email already exists."}), 409


@app.route("/api/auth/login", methods=["POST"])
def login():
    data     = request.get_json()
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password are required."}), 400

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    ).fetchone()
    conn.close()

    if user:
        session["user_id"]  = user["id"]
        session["username"] = user["username"]
        return jsonify({"success": True, "message": f"Welcome, {user['username']}!", "username": user["username"]})
    else:
        return jsonify({"success": False, "message": "Invalid username or password."}), 401


@app.route("/api/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully."})


@app.route("/api/auth/me", methods=["GET"])
def me():
    if current_user():
        return jsonify({"loggedIn": True, "username": session.get("username")})
    return jsonify({"loggedIn": False})

# ─────────────────────────────────────────────
#  RESERVATION ROUTES
# ─────────────────────────────────────────────

@app.route("/api/reservations", methods=["POST"])
def create_reservation():
    data      = request.get_json()
    full_name = (data.get("fullName")   or "").strip()
    email     = (data.get("email")      or "").strip()
    arrival   = (data.get("arrival")    or "").strip()
    departure = (data.get("departure")  or "").strip()
    guests    = data.get("guests")
    acc_type  = (data.get("type")       or "").strip()
    notes     = (data.get("notes")      or "").strip()

    # Validation
    if not all([full_name, email, arrival, departure, guests, acc_type]):
        return jsonify({"success": False, "message": "All required fields must be filled."}), 400
    if not validate_email(email):
        return jsonify({"success": False, "message": "Invalid email address."}), 400
    try:
        guests = int(guests)
        if guests < 1 or guests > 20:
            raise ValueError()
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Number of guests must be between 1 and 20."}), 400

    # Date validation
    try:
        arr_date = datetime.strptime(arrival, "%Y-%m-%d")
        dep_date = datetime.strptime(departure, "%Y-%m-%d")
        if dep_date <= arr_date:
            return jsonify({"success": False, "message": "Departure must be after arrival."}), 400
        if arr_date < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
            return jsonify({"success": False, "message": "Arrival date cannot be in the past."}), 400
    except ValueError:
        return jsonify({"success": False, "message": "Invalid date format."}), 400

    conn = get_db()
    conn.execute(
        """INSERT INTO reservations
           (full_name, email, arrival, departure, guests, type, notes, user_id)
           VALUES (?,?,?,?,?,?,?,?)""",
        (full_name, email, arrival, departure, guests, acc_type, notes, current_user())
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Your reservation request has been submitted! We will contact you soon."}), 201


@app.route("/api/reservations/my", methods=["GET"])
def my_reservations():
    if not current_user():
        return jsonify({"success": False, "message": "Login required."}), 401

    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM reservations WHERE user_id=? ORDER BY submitted_at DESC",
        (current_user(),)
    ).fetchall()
    conn.close()

    result = [dict(r) for r in rows]
    return jsonify({"success": True, "reservations": result})

# ─────────────────────────────────────────────
#  CONTACT ROUTE
# ─────────────────────────────────────────────

@app.route("/api/contact", methods=["POST"])
def contact():
    data    = request.get_json()
    name    = (data.get("name")    or "").strip()
    subject = (data.get("subject") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not subject or not message:
        return jsonify({"success": False, "message": "All fields are required."}), 400
    if len(message) < 10:
        return jsonify({"success": False, "message": "Message is too short (min 10 characters)."}), 400

    conn = get_db()
    conn.execute(
        "INSERT INTO messages (name, subject, message) VALUES (?,?,?)",
        (name, subject, message)
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Your message has been sent successfully!"}), 201

# ─────────────────────────────────────────────
#  LANDMARKS ROUTE (public)
# ─────────────────────────────────────────────

@app.route("/api/landmarks", methods=["GET"])
def get_landmarks():
    category = request.args.get("category")
    conn = get_db()
    if category:
        rows = conn.execute(
            "SELECT * FROM landmarks WHERE category=? ORDER BY id",
            (category,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM landmarks ORDER BY category, id").fetchall()
    conn.close()
    return jsonify({"success": True, "landmarks": [dict(r) for r in rows]})

# ─────────────────────────────────────────────
#  ADMIN ROUTES (registered users only)
# ─────────────────────────────────────────────

@app.route("/api/admin/reservations", methods=["GET"])
def admin_reservations():
    if not current_user():
        return jsonify({"success": False, "message": "Login required."}), 401

    conn = get_db()
    rows = conn.execute(
        """SELECT r.*, u.username FROM reservations r
           LEFT JOIN users u ON r.user_id = u.id
           ORDER BY r.submitted_at DESC"""
    ).fetchall()
    conn.close()

    return jsonify({"success": True, "reservations": [dict(r) for r in rows]})


@app.route("/api/admin/messages", methods=["GET"])
def admin_messages():
    if not current_user():
        return jsonify({"success": False, "message": "Login required."}), 401

    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM messages ORDER BY submitted_at DESC"
    ).fetchall()
    conn.close()

    return jsonify({"success": True, "messages": [dict(r) for r in rows]})

# ─────────────────────────────────────────────
#  HEALTH CHECK
# ─────────────────────────────────────────────

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "project": "Karlovy Vary – Group 13"})

# ─────────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    print("🚀 Karlovy Vary Backend running on http://localhost:5000")
    app.run(debug=True, port=5000)
