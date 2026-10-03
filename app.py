from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = "salon.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            telephone TEXT NOT NULL,
            email TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS rendez_vous (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            service TEXT NOT NULL,
            date_rdv TEXT NOT NULL,
            heure TEXT NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = get_db()
    clients = conn.execute("SELECT * FROM clients ORDER BY id DESC").fetchall()
    rendez_vous = conn.execute("""
        SELECT rendez_vous.*, clients.nom
        FROM rendez_vous
        JOIN clients ON clients.id = rendez_vous.client_id
        ORDER BY date_rdv, heure
    """).fetchall()
    conn.close()
    return render_template("index.html", clients=clients, rendez_vous=rendez_vous)

@app.route("/client/ajouter", methods=["POST"])
def ajouter_client():
    nom = request.form["nom"]
    telephone = request.form["telephone"]
    email = request.form.get("email", "")
    conn = get_db()
    conn.execute(
        "INSERT INTO clients (nom, telephone, email) VALUES (?, ?, ?)",
        (nom, telephone, email)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/rendez-vous/ajouter", methods=["POST"])
def ajouter_rendez_vous():
    client_id = request.form["client_id"]
    service = request.form["service"]
    date_rdv = request.form["date_rdv"]
    heure = request.form["heure"]

    conn = get_db()
    conn.execute("""
        INSERT INTO rendez_vous (client_id, service, date_rdv, heure)
        VALUES (?, ?, ?, ?)
    """, (client_id, service, date_rdv, heure))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
