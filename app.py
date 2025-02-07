from flask import Flask, render_template, request, redirect
import todo

app = Flask(__name__)

# Strona główna - wyświetlanie listy zadań
@app.route("/")
def index():
    conn = todo.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, done FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

# Dodawanie zadania
@app.route("/add", methods=["POST"])
def add_task():
    task_text = request.form.get("task")  # Pobieramy wartość z formularza
    if not task_text:
        return "Błąd: Nie podano treści zadania", 400

    todo.add_task(task_text)  # Przekazujemy task_text do funkcji
    return redirect("/")

# Usuwanie zadania
@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    todo.delete_task(task_id)
    return redirect("/")

# Oznaczanie jako wykonane
@app.route("/done/<int:task_id>")
def mark_done(task_id):
    todo.mark_task_done(task_id)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)