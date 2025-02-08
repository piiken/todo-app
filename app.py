from flask import Flask, request, jsonify, Response, render_template, redirect, url_for
import psycopg2
import os
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

# Konfiguracja bazy danych
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/todo_db")

def connect_db():
    return psycopg2.connect(DATABASE_URL)

# Tworzenie tabeli jeśli nie istnieje
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT FALSE
        )
    """)
    conn.commit()
    conn.close()

create_table()

# Prometheus - Metryki
REQUEST_COUNT = Counter("http_requests_total", "Total number of HTTP requests", ["method", "endpoint"])

@app.before_request
def before_request():
    REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype="text/plain")

# Dodanie zadania
@app.route("/add", methods=["POST"])
def add_task():
    task_text = request.form.get("task")
    if not task_text:
        return jsonify({"error": "Treść zadania jest wymagana"}), 400
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task, done) VALUES (%s, %s)", (task_text, False))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

# Pobranie listy zadań
@app.route("/")
def index():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, done FROM tasks ORDER BY id")
    tasks = cursor.fetchall()
    conn.close()
    
    return render_template("index.html", tasks=tasks)

# Oznaczenie zadania jako wykonane
@app.route("/done/<int:task_id>")
def mark_done(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET done = TRUE WHERE id = %s", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

# Usunięcie zadania
@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Pobiera port z ENV lub ustawia domyślnie 5000
    app.run(host="0.0.0.0", port=port)
