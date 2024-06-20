import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox, ttk

DB_PATH = 'todo.db'

def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    priority INTEGER NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('pending', 'completed')),
                    category TEXT,
                    due_date TEXT
                )''')
    conn.commit()
    conn.close()

def add_task(description, priority, category, due_date):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO tasks (description, priority, status, category, due_date)
                 VALUES (?, ?, 'pending', ?, ?)''', (description, priority, category, due_date))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def update_task(task_id, description=None, priority=None, status=None, category=None, due_date=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if description:
        c.execute('UPDATE tasks SET description = ? WHERE id = ?', (description, task_id))
    if priority:
        c.execute('UPDATE tasks SET priority = ? WHERE id = ?', (priority, task_id))
    if status:
        c.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, task_id))
    if category:
        c.execute('UPDATE tasks SET category = ? WHERE id = ?', (category, task_id))
    if due_date:
        c.execute('UPDATE tasks SET due_date = ? WHERE id = ?', (due_date, task_id))
    conn.commit()
    conn.close()

def view_tasks(filter_by=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    query = 'SELECT id, description, priority, status, category, due_date FROM tasks'
    if filter_by:
        query += ' WHERE ' + filter_by
    c.execute(query)
    rows = c.fetchall()
    conn.close()
    return rows

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("800x600")
        
        self.create_widgets()
        self.load_tasks()

    def create_widgets(self):
        # Add task frame
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Task Description").grid(row=0, column=0, padx=5)
        self.description_entry = tk.Entry(frame, width=40)
        self.description_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Priority (1-5)").grid(row=1, column=0, padx=5)
        self.priority_entry = tk.Entry(frame, width=10)
        self.priority_entry.grid(row=1, column=1, padx=5)

        tk.Label(frame, text="Category").grid(row=2, column=0, padx=5)
        self.category_entry = tk.Entry(frame, width=20)
        self.category_entry.grid(row=2, column=1, padx=5)

        tk.Label(frame, text="Due Date (YYYY-MM-DD)").grid(row=3, column=0, padx=5)
        self.due_date_entry = tk.Entry(frame, width=20)
        self.due_date_entry.grid(row=3, column=1, padx=5)

        tk.Button(frame, text="Add Task", command=self.add_task).grid(row=4, column=0, columnspan=2, pady=10)

        # Task list
        self.tree = ttk.Treeview(self.root, columns=("ID", "Description", "Priority", "Status", "Category", "Due Date"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.column("ID", width=30)
        self.tree.column("Description", width=200)
        self.tree.column("Priority", width=60)
        self.tree.column("Status", width=80)
        self.tree.column("Category", width=100)
        self.tree.column("Due Date", width=100)
        self.tree.pack(pady=20)

        # Task operations
        self.operation_frame = tk.Frame(self.root)
        self.operation_frame.pack()

        tk.Button(self.operation_frame, text="Delete Task", command=self.delete_task).grid(row=0, column=0, padx=10)
        tk.Button(self.operation_frame, text="Mark as Completed", command=self.mark_as_completed).grid(row=0, column=1, padx=10)
        tk.Button(self.operation_frame, text="Filter Tasks", command=self.filter_tasks).grid(row=0, column=2, padx=10)

    def load_tasks(self, filter_by=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        tasks = view_tasks(filter_by)
        for task in tasks:
            self.tree.insert("", tk.END, values=task)

    def add_task(self):
        description = self.description_entry.get()
        priority = self.priority_entry.get()
        category = self.category_entry.get()
        due_date = self.due_date_entry.get()

        if description and priority.isdigit() and 1 <= int(priority) <= 5 and self.validate_date(due_date):
            add_task(description, int(priority), category, due_date)
            self.load_tasks()
        else:
            messagebox.showerror("Error", "Invalid input. Please check the data entered.")

    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            task_id = self.tree.item(selected_item)["values"][0]
            delete_task(task_id)
            self.load_tasks()
        else:
            messagebox.showerror("Error", "No task selected.")

    def mark_as_completed(self):
        selected_item = self.tree.selection()
        if selected_item:
            task_id = self.tree.item(selected_item)["values"][0]
            update_task(task_id, status='completed')
            self.load_tasks()
        else:
            messagebox.showerror("Error", "No task selected.")

    def filter_tasks(self):
        filter_window = tk.Toplevel(self.root)
        filter_window.title("Filter Tasks")

        tk.Label(filter_window, text="Filter by (status/category/due_date)").pack(pady=10)
        filter_by = tk.StringVar()
        filter_by.set("none")

        tk.Radiobutton(filter_window, text="Status", variable=filter_by, value="status").pack()
        tk.Radiobutton(filter_window, text="Category", variable=filter_by, value="category").pack()
        tk.Radiobutton(filter_window, text="Due Date", variable=filter_by, value="due_date").pack()

        tk.Button(filter_window, text="Apply Filter", command=lambda: self.apply_filter(filter_by.get(), filter_window)).pack(pady=10)

    def apply_filter(self, filter_by, window):
        if filter_by == "status":
            status = tk.simpledialog.askstring("Status", "Enter status ('pending' or 'completed'):")
            if status:
                self.load_tasks(f"status = '{status}'")
        elif filter_by == "category":
            category = tk.simpledialog.askstring("Category", "Enter category:")
            if category:
                self.load_tasks(f"category = '{category}'")
        elif filter_by == "due_date":
            due_date = tk.simpledialog.askstring("Due Date", "Enter due date (YYYY-MM-DD):")
            if due_date and self.validate_date(due_date):
                self.load_tasks(f"due_date = '{due_date}'")
        window.destroy()

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

if __name__ == "__main__":
    initialize_db()
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
