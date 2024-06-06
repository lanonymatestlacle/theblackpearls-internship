import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# Database setup
conn = sqlite3.connect('todo_list.db')
c = conn.cursor()

# Drop the table if it exists to ensure a clean start
c.execute('DROP TABLE IF EXISTS tasks')

# Create the table with the correct schema
c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                task TEXT NOT NULL,
                priority TEXT NOT NULL,
                due_date TEXT,
                category TEXT,
                completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
            )''')
conn.commit()

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("800x500")
        self.root.configure(bg='#f0f0f0')

        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Helvetica', 12))
        self.style.configure('TButton', font=('Helvetica', 12), padding=6)
        self.style.configure('TEntry', font=('Helvetica', 12))
        self.style.configure('TCombobox', font=('Helvetica', 12))
        self.style.configure('Treeview.Heading', font=('Helvetica', 14, 'bold'))
        self.style.configure('Treeview', font=('Helvetica', 12), rowheight=25)

        self.create_widgets()
        self.refresh_tasks()

    def create_widgets(self):
        self.header_frame = ttk.Frame(self.root)
        self.header_frame.pack(pady=10)

        self.task_label = ttk.Label(self.header_frame, text="Task")
        self.task_label.grid(row=0, column=0, padx=10, pady=10)
        self.task_entry = ttk.Entry(self.header_frame, width=30)
        self.task_entry.grid(row=0, column=1, padx=10, pady=10)

        self.priority_label = ttk.Label(self.header_frame, text="Priority")
        self.priority_label.grid(row=1, column=0, padx=10, pady=10)
        self.priority_combo = ttk.Combobox(self.header_frame, values=["Low", "Medium", "High"])
        self.priority_combo.grid(row=1, column=1, padx=10, pady=10)
        self.priority_combo.current(0)

        self.due_date_label = ttk.Label(self.header_frame, text="Due Date (YYYY-MM-DD)")
        self.due_date_label.grid(row=2, column=0, padx=10, pady=10)
        self.due_date_entry = ttk.Entry(self.header_frame, width=30)
        self.due_date_entry.grid(row=2, column=1, padx=10, pady=10)

        self.category_label = ttk.Label(self.header_frame, text="Category")
        self.category_label.grid(row=3, column=0, padx=10, pady=10)
        self.category_entry = ttk.Entry(self.header_frame, width=30)
        self.category_entry.grid(row=3, column=1, padx=10, pady=10)

        self.add_button = ttk.Button(self.header_frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=4, column=1, padx=10, pady=10)

        self.tasks_frame = ttk.Frame(self.root)
        self.tasks_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.tasks_tree = ttk.Treeview(self.tasks_frame, columns=("Task", "Priority", "Due Date", "Category", "Completed"), show='headings')
        self.tasks_tree.heading("Task", text="Task")
        self.tasks_tree.heading("Priority", text="Priority")
        self.tasks_tree.heading("Due Date", text="Due Date")
        self.tasks_tree.heading("Category", text="Category")
        self.tasks_tree.heading("Completed", text="Completed")
        self.tasks_tree.column("Task", width=200)
        self.tasks_tree.column("Priority", width=100)
        self.tasks_tree.column("Due Date", width=100)
        self.tasks_tree.column("Category", width=100)
        self.tasks_tree.column("Completed", width=100)
        self.tasks_tree.pack(fill=tk.BOTH, expand=True)

        self.tasks_tree.bind('<Double-1>', self.on_item_double_click)

        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.update_button = ttk.Button(self.button_frame, text="Update Task", command=self.update_task)
        self.update_button.grid(row=0, column=0, padx=10, pady=10)

        self.delete_button = ttk.Button(self.button_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=0, column=1, padx=10, pady=10)

        self.complete_button = ttk.Button(self.button_frame, text="Mark as Complete", command=self.complete_task)
        self.complete_button.grid(row=0, column=2, padx=10, pady=10)

    def refresh_tasks(self):
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)
        for row in c.execute("SELECT * FROM tasks"):
            self.tasks_tree.insert("", "end", values=(row[1], row[2], row[3], row[4], "Yes" if row[5] else "No"))

    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_combo.get()
        due_date = self.due_date_entry.get()
        category = self.category_entry.get()
        if task:
            c.execute("INSERT INTO tasks (task, priority, due_date, category, completed) VALUES (?, ?, ?, ?, 0)",
                      (task, priority, due_date, category))
            conn.commit()
            self.refresh_tasks()
            self.task_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty!")

    def update_task(self):
        selected_item = self.tasks_tree.selection()
        if selected_item:
            item = self.tasks_tree.item(selected_item)
            task = item['values'][0]
            task_id = c.execute("SELECT id FROM tasks WHERE task=?", (task,)).fetchone()[0]
            new_task = self.task_entry.get()
            new_priority = self.priority_combo.get()
            new_due_date = self.due_date_entry.get()
            new_category = self.category_entry.get()
            c.execute("UPDATE tasks SET task=?, priority=?, due_date=?, category=? WHERE id=?",
                      (new_task, new_priority, new_due_date, new_category, task_id))
            conn.commit()
            self.refresh_tasks()
        else:
            messagebox.showwarning("Selection Error", "No task selected!")

    def delete_task(self):
        selected_item = self.tasks_tree.selection()
        if selected_item:
            item = self.tasks_tree.item(selected_item)
            task = item['values'][0]
            task_id = c.execute("SELECT id FROM tasks WHERE task=?", (task,)).fetchone()[0]
            c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
            conn.commit()
            self.refresh_tasks()
        else:
            messagebox.showwarning("Selection Error", "No task selected!")

    def complete_task(self):
        selected_item = self.tasks_tree.selection()
        if selected_item:
            item = self.tasks_tree.item(selected_item)
            task = item['values'][0]
            task_id = c.execute("SELECT id FROM tasks WHERE task=?", (task,)).fetchone()[0]
            c.execute("UPDATE tasks SET completed=1 WHERE id=?", (task_id,))
            conn.commit()
            self.refresh_tasks()
        else:
            messagebox.showwarning("Selection Error", "No task selected!")

    def on_item_double_click(self, event):
        selected_item = self.tasks_tree.selection()
        if selected_item:
            item = self.tasks_tree.item(selected_item)
            task = item['values'][0]
            priority = item['values'][1]
            due_date = item['values'][2]
            category = item['values'][3]
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, task)
            self.priority_combo.set(priority)
            self.due_date_entry.delete(0, tk.END)
            self.due_date_entry.insert(0, due_date)
            self.category_entry.delete(0, tk.END)
            self.category_entry.insert(0, category)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
