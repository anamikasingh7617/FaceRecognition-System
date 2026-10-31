import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def register_face():
    subprocess.Popen(
        [sys.executable, os.path.join(BASE_DIR, "register.py")],
        cwd=BASE_DIR
    )


def recognize_face():
    dataset_path = os.path.join(BASE_DIR, "dataset")

    if not os.path.isdir(dataset_path):
        messagebox.showwarning("Warning", "Register a face first!")
        return

    if not any(os.path.isdir(os.path.join(dataset_path, name))
               for name in os.listdir(dataset_path)):
        messagebox.showwarning("Warning", "Register a face first!")
        return

    subprocess.Popen(
        [sys.executable, os.path.join(BASE_DIR, "recognize.py")],
        cwd=BASE_DIR
    )


root = tk.Tk()
root.title("Face Recognition System")
root.geometry("600x450")
root.configure(bg="#172554")
root.resizable(False, False)

title = tk.Label(
    root,
    text="FACE RECOGNITION SYSTEM",
    font=("Arial", 22, "bold"),
    bg="#172554",
    fg="white"
)
title.pack(pady=45)

subtitle = tk.Label(
    root,
    text="Welcome to Face Recognition Application",
    font=("Arial", 12),
    bg="#172554",
    fg="#bfdbfe"
)
subtitle.pack(pady=5)

tk.Button(
    root,
    text="REGISTER NEW FACE",
    font=("Arial", 13, "bold"),
    bg="#16a34a",
    fg="white",
    width=25,
    height=2,
    command=register_face
).pack(pady=25)

tk.Button(
    root,
    text="RECOGNIZE FACE",
    font=("Arial", 13, "bold"),
    bg="#2563eb",
    fg="white",
    width=25,
    height=2,
    command=recognize_face
).pack(pady=10)

tk.Button(
    root,
    text="EXIT",
    font=("Arial", 12, "bold"),
    bg="#dc2626",
    fg="white",
    width=15,
    command=root.destroy
).pack(pady=25)

root.mainloop()