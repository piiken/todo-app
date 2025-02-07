import psycopg2
import os
import time

# Pobranie zmiennej środowiskowej DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres:5432/todo_db")

# Funkcja do połączenia z bazą danych PostgreSQL
def connect_db(retries=5, delay=5):
    for i in range(retries):
        try:
            conn = psycopg2.connect(DATABASE_URL)
            return conn
        except psycopg2.OperationalError:
            print(f"🔄 Próba {i+1}/{retries} - Baza danych nie jest gotowa. Czekam {delay} sekund...")
            time.sleep(delay)
    print("❌ Nie udało się połączyć z bazą danych. Sprawdź konfigurację.")
    exit(1)

# Tworzenie tabeli, jeśli nie istnieje
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

# Dodawanie zadania do bazy danych
def add_task(task_text):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task, done) VALUES (%s, FALSE)", (task_text,))
    conn.commit()
    conn.close()

# Pobieranie listy zadań
def get_tasks():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, done FROM tasks ORDER BY id ASC")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Oznaczanie zadania jako wykonane
def mark_task_done(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET done = NOT done WHERE id = %s", (task_id,))
    conn.commit()
    conn.close()

# Usuwanie zadania
def delete_task(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    conn.close()
