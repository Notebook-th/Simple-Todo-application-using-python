import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
import os
import time

# File to store tasks
TASKS_FILE = 'tasks.json'

# Function to load tasks from a JSON file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    return {"pending": [], "completed": []}

# Function to save tasks to a JSON file
def save_tasks():
    tasks = {
        "pending": [],
        "completed": []
    }
    for item in pending_tasks.get_children():
        tasks["pending"].append(pending_tasks.item(item)["values"])
    for item in completed_tasks.get_children():
        tasks["completed"].append(completed_tasks.item(item)["values"])
    
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file)

# Function to update the progress bar
def update_progress():
    total_tasks = len(pending_tasks.get_children()) + len(completed_tasks.get_children())
    if total_tasks > 0:
        completed_tasks_count = len(completed_tasks.get_children())
        progress = (completed_tasks_count / total_tasks) * 100
        progress_bar['value'] = progress
        progress_label['text'] = f'Progress: {completed_tasks_count}/{total_tasks} tasks completed'
    else:
        progress_bar['value'] = 0
        progress_label['text'] = 'Progress: 0/0 tasks completed'

# Function to add tasks to the list
def add_task():
    task = task_entry.get()
    date = date_entry.get()
    time_input = time_entry.get()
    if task and date and time_input:
        pending_tasks.insert('', 'end', values=(task, date, time_input))
        task_entry.delete(0, tk.END)
        date_entry.set_date('')
        time_entry.delete(0, tk.END)
        save_tasks()
        update_progress()
        messagebox.showinfo("Success", "Task added successfully!")
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")

# Function to mark a task as completed
def mark_completed():
    selected_item = pending_tasks.selection()
    if selected_item:
        values = pending_tasks.item(selected_item)['values']
        completed_tasks.insert('', 'end', values=values)
        pending_tasks.delete(selected_item)
        save_tasks()
        update_progress()
        messagebox.showinfo("Success", "Task marked as completed!")
    else:
        messagebox.showwarning("Warning", "Please select a task to mark as completed.")

# Function to delete completed tasks
def delete_completed():
    selected_item = completed_tasks.selection()
    if selected_item:
        if messagebox.askyesno("Confirmation", "Are you sure you want to delete this completed task?"):
            completed_tasks.delete(selected_item)
            save_tasks()
            update_progress()
            messagebox.showinfo("Success", "Completed task deleted!")
    else:
        messagebox.showwarning("Warning", "Please select a completed task to delete.")

# Function to update the time and date
def update_time():
    current_time = time.strftime("%I:%M:%S %p")  # 12-hour format
    current_date = time.strftime("%Y-%m-%d")
    time_label['text'] = f'Time: {current_time}'
    date_label['text'] = f'Date: {current_date}'
    app.after(1000, update_time)  # Update every second

# Function to close the app
def close_app():
    app.quit()

# Function to minimize the app
def minimize_app():
    app.iconify()

# Function to maximize the app
def maximize_app():
    app.state('zoomed')

# Creating the main application window
app = tk.Tk()
app.title('Enhanced To-Do List App')
app.configure(bg='#e9ecef')

# Frame for title and control buttons
top_frame = tk.Frame(app, bg='#343a40')
top_frame.pack(side=tk.TOP, fill=tk.X)

# Close Button
close_button = tk.Button(top_frame, text='X', command=close_app, bg='red', fg='white', font=('Arial', 12), padx=5, pady=5)
close_button.pack(side=tk.RIGHT)

# Minimize Button
minimize_button = tk.Button(top_frame, text='–', command=minimize_app, bg='yellow', fg='black', font=('Arial', 12), padx=5, pady=5)
minimize_button.pack(side=tk.RIGHT)

# Maximize Button
maximize_button = tk.Button(top_frame, text='□', command=maximize_app, bg='lightgray', fg='black', font=('Arial', 12), padx=5, pady=5)
maximize_button.pack(side=tk.RIGHT)

# Frame for adding tasks
frame = tk.Frame(app, bg='#f8f9fa')
frame.pack(pady=10, padx=10, fill=tk.X)

# Task entry widget
task_label = tk.Label(frame, text="Task", bg='#f8f9fa', font=('Arial', 12))
task_label.grid(row=0, column=0, padx=5)
task_entry = tk.Entry(frame, width=30, font=('Arial', 12))
task_entry.grid(row=0, column=1, padx=5)

# Date entry widget
date_label = tk.Label(frame, text="Date", bg='#f8f9fa', font=('Arial', 12))
date_label.grid(row=1, column=0, padx=5)
date_entry = DateEntry(frame, width=28, font=('Arial', 12), background='darkblue', foreground='white', borderwidth=2)
date_entry.grid(row=1, column=1, padx=5)

# Time entry widget
time_label = tk.Label(frame, text="Time", bg='#f8f9fa', font=('Arial', 12))
time_label.grid(row=2, column=0, padx=5)
time_entry = tk.Entry(frame, width=30, font=('Arial', 12))
time_entry.grid(row=2, column=1, padx=5)

# Add Task button
add_button = tk.Button(frame, text="Add Task", command=add_task, bg='#28a745', fg='white', font=('Arial', 12))
add_button.grid(row=0, column=2, rowspan=3, padx=10)

# Frame for task lists
task_frame = tk.Frame(app, bg='#f8f9fa')
task_frame.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

# Pending tasks label and table
pending_label = tk.Label(task_frame, text="Pending Tasks", bg='#f8f9fa', font=('Arial', 14, 'bold'))
pending_label.grid(row=0, column=0, padx=20, pady=10)
columns = ('Task', 'Date', 'Time')
pending_tasks = ttk.Treeview(task_frame, columns=columns, show='headings', height=10)
for col in columns:
    pending_tasks.heading(col, text=col)
pending_tasks.grid(row=1, column=0, padx=20)

# Load tasks from file
tasks = load_tasks()
for task in tasks["pending"]:
    pending_tasks.insert('', 'end', values=task)

# Completed tasks label and table
completed_label = tk.Label(task_frame, text="Completed Tasks", bg='#f8f9fa', font=('Arial', 14, 'bold'))
completed_label.grid(row=0, column=1, padx=20, pady=10)
completed_tasks = ttk.Treeview(task_frame, columns=columns, show='headings', height=10)
for col in columns:
    completed_tasks.heading(col, text=col)
completed_tasks.grid(row=1, column=1, padx=20)

# Load completed tasks from file
for task in tasks["completed"]:
    completed_tasks.insert('', 'end', values=task)

# Progress Bar
progress_bar = ttk.Progressbar(app, orient='horizontal', length=400, mode='determinate')
progress_bar.pack(pady=10)

# Progress Label
progress_label = tk.Label(app, text='Progress: 0/0 tasks completed', bg='#f8f9fa', font=('Arial', 12))
progress_label.pack()

# Buttons for managing tasks
button_frame = tk.Frame(app, bg='#f8f9fa')
button_frame.pack(pady=10)

mark_complete_button = tk.Button(button_frame, text="Mark as Completed", command=mark_completed, bg='#007bff', fg='white', font=('Arial', 12))
mark_complete_button.grid(row=0, column=0, padx=10)

delete_button = tk.Button(button_frame, text="Delete Completed Task", command=delete_completed, bg='#dc3545', fg='white', font=('Arial', 12))
delete_button.grid(row=0, column=1, padx=10)

# Date and Time Labels
time_label = tk.Label(app, text='', bg='#e9ecef', font=('Arial', 12))
time_label.pack(side=tk.BOTTOM, pady=5)
date_label = tk.Label(app, text='', bg='#e9ecef', font=('Arial', 12))
date_label.pack(side=tk.BOTTOM, pady=5)

# Initialize and start time updates
update_time()
update_progress()

# Open app in fullscreen
app.attributes('-fullscreen', True)

# Run the application
app.mainloop()
