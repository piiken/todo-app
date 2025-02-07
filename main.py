import todo

# Tworzymy tabelę w SQLite (jeśli nie istnieje)
todo.create_table()

while True:
    try:
        choice = int(input("\nCo chcesz zrobić?\n"
                   "1. Wyświetl listę\n"
                   "2. Dodaj zadanie\n"
                   "3. Oznacz zadanie jako wykonane\n"
                   "4. Edytuj zadanie\n"
                   "5. Usuń zadanie\n"
                   "6. Zakończ\n"
                   "> "))

        if choice == 1:
            todo.show_list()
        elif choice == 2:
            todo.add_task()
        elif choice == 3:
            todo.mark_task_done()
        elif choice == 4:
            todo.edit_task()
        elif choice == 5:
            todo.delete_task()
        elif choice == 6:
            print("👋 Do zobaczenia!")
            break
        else:
            print("⚠ Niepoprawny wybór, spróbuj ponownie.")

    except ValueError:
        print("⚠ Błąd: Wpisz liczbę od 1 do 7.")
