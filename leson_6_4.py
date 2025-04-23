# import sqlite3

# # Підключення до бази даних
# conn = sqlite3.connect("my_database.db")

# # Створення курсора
# cursor = conn.cursor()

# # Створення таблиці (якщо її немає)
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS users (

# id INTEGER PRIMARY KEY AUTOINCREMENT,
# name TEXT,
# age INTEGER
               
# )               
# ''')

# # Вставка одного запису
# cursor.execute("INSERT INTO users (name, age) VALUES ('Nick', 37)")

# # Підтвердження змін 
# conn.commit()

# # Перевірка результату
# cursor.execute("SELECT * FROM users")
# print(cursor.fetchall()) #Вивести всі записи з таблиці
# cursor.execute("UPDATE users SET age =  30  WHERE age < 30")
# print(cursor.fetchall())
# cursor.execute("UPDATE users SET name =  'Ms.' || name  WHERE name LIKE 'A%'")
# cursor.execute("SELECT * FROM users")
# print(cursor.fetchall())
# cursor.execute("DELETE FROM users WHERE age > 30")
# cursor.execute("SELECT * FROM users")
# print(cursor.fetchall())
# cursor.execute("DELETE FROM users WHERE name = 'Ms.Adam'")
# cursor.execute("SELECT * FROM users")
# print(cursor.fetchall())
# cursor.execute("DELETE FROM users")
# cursor.execute("SELECT * FROM users")
# print(cursor.fetchall())

# # Закриття з'єднання
# conn.close()

import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
conn.commit()

# Функції для роботи з базою даних
def add_user():
    name = name_entry.get()
    age = age_entry.get()
    if name and age.isdigit():
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, int(age)))
        conn.commit()
        update_listbox()
    else:
        messagebox.showerror("Помилка", "Введіть коректні дані!")

def update_user():
    try:
        selected = user_listbox.curselection()[0]
        user_id = user_ids[selected]
        name = name_entry.get()
        age = age_entry.get()
        if name and age.isdigit():
            cursor.execute("UPDATE users SET name=?, age=? WHERE id=?", (name, int(age), user_id))
            conn.commit()
            update_listbox()
        else:
            messagebox.showerror("Помилка", "Введіть коректні дані!")
    except IndexError:
        messagebox.showerror("Помилка", "Виберіть користувача для оновлення!")

def delete_user():
    try:
        selected = user_listbox.curselection()[0]
        user_id = user_ids[selected]
        cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        update_listbox()
    except IndexError:
        messagebox.showerror("Помилка", "Виберіть користувача для видалення!")

def update_listbox():
    global user_ids
    user_listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    user_ids = [user[0] for user in users]
    for user in users:
        user_listbox.insert(tk.END, f"{user[1]} ({user[2]} років)")

# Створення графічного інтерфейсу
root = tk.Tk()
root.title("Керування користувачами")
root.configure(bg="#0D656F")

# Стилі
btn_style = {"bg": "#cce1e8", "fg": "#070c15", "font": ("Roboto", 12, "bold"), "padx": 10, "pady": 5}
entry_style = {"bg": "#ecf0f1", "font": ("Roboto", 12)}

tk.Label(root, text="Ім'я:", bg="#2c3e50", fg="white", font=("Roboto", 12)).grid(row=0, column=0)
name_entry = tk.Entry(root, **entry_style)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Вік:", bg="#2c3e50", fg="white", font=("Roboto", 12)).grid(row=1, column=0)
age_entry = tk.Entry(root, **entry_style)
age_entry.grid(row=1, column=1)

tk.Button(root, text="Додати", command=add_user, **btn_style).grid(row=2, column=0)
tk.Button(root, text="Оновити", command=update_user, **btn_style).grid(row=2, column=1)
tk.Button(root, text="Видалити", command=delete_user, **btn_style).grid(row=3, column=0, columnspan=2)

user_listbox = tk.Listbox(root, bg="#ecf0f1", font=("Roboto", 12))
user_listbox.grid(row=4, column=0, columnspan=2, sticky="ew")
update_listbox()

root.mainloop()



