import re
import tkinter as tk
from tkinter import ttk, messagebox
import random

def check_password_strength(password):
    common_passwords = {"123456", "password", "123456789", "qwerty", "111111"}
    
    if password in common_passwords:
        return "🚨 Too Common!", "#FF0000", 10
    
    strength_criteria = {
        "length": len(password) >= 8,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "digit": bool(re.search(r"\d", password)),
        "special": bool(re.search(r"[@$!%*?&]", password))
    }
    
    score = sum(strength_criteria.values())
    
    if score == 5:
        return "💪 Very Strong", "#00FF00", 100
    elif score == 4:
        return "😎 Strong", "#1E90FF", 80
    elif score == 3:
        return "😬 Medium", "#FFA500", 50
    elif score == 2:
        return "😟 Weak", "#FF4500", 25
    else:
        return "😡 Very Weak", "#FF0000", 10

def evaluate_password(event=None):
    password = entry.get()
    strength, color, value = check_password_strength(password)
    strength_label.config(text=strength, fg=color)
    strength_meter['value'] = value
    update_checklist(password)

def update_checklist(password):
    checklist = [
        ("At least 8 characters", len(password) >= 8),
        ("Contains an uppercase letter", bool(re.search(r"[A-Z]", password))),
        ("Contains a lowercase letter", bool(re.search(r"[a-z]", password))),
        ("Contains a number", bool(re.search(r"\d", password))),
        ("Contains a special character", bool(re.search(r"[@$!%*?&]", password)))
    ]
    for i, (text, condition) in enumerate(checklist):
        checklist_labels[i].config(text=f"{'✔' if condition else '✖'} {text}", fg="#00FF00" if condition else "#FF0000", bg=container['bg'])

def toggle_password():
    if entry.cget('show') == '*':
        entry.config(show='')
    else:
        entry.config(show='*')

def generate_strong_password():
    while True:
        characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@$!%*?&"
        generated = "".join(random.choices(characters, k=12))
        if sum(bool(re.search(criterion, generated)) for criterion in [r"[A-Z]", r"[a-z]", r"\d", r"[@$!%*?&]"]) == 4:
            return generated

def generate_password():
    strong_password = generate_strong_password()
    entry.delete(0, tk.END)
    entry.insert(0, strong_password)
    evaluate_password()

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(entry.get())
    root.update()
    messagebox.showinfo("Copied", "Password copied to clipboard!")

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        bg_color = "#1C1F2A"  # Deep navy blue
        text_color = "#FFFFFF"  # White font for contrast in dark mode
        accent_color = "#4A90E2"  # Royal blue
    else:
        bg_color = "#FFFFFF"
        text_color = "#000000"  # Black font for contrast in light mode
        accent_color = "#00FFFF"
    
    container.config(bg=bg_color)
    root.config(bg=bg_color)
    for widget in container.winfo_children():
        widget.config(bg=bg_color, fg=text_color)
    theme_button.config(text="🌞 Light Mode" if dark_mode else "🌙 Dark Mode", bg=accent_color, fg="#FFFFFF")

root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("500x500")
root.configure(bg="#FFFFFF")

dark_mode = False

container = tk.Frame(root, bg="#FFFFFF", padx=20, pady=20, relief="ridge", bd=3)
container.pack(pady=20)

tk.Label(container, text="Password Strength Checker", font=("Montserrat", 16, "bold"), bg="#FFFFFF", fg="#000000").pack()
tk.Label(container, text="Check how strong your password is!", font=("Roboto", 10), bg="#FFFFFF", fg="#000000").pack(pady=5)

entry_frame = tk.Frame(container, bg="#FFFFFF")
entry_frame.pack(pady=5)
entry = tk.Entry(entry_frame, show="*", width=30, font=("Roboto", 12), bg="#F8F8F8", fg="#000000", relief="solid", borderwidth=1)
entry.pack(side="left", padx=5)
entry.bind("<KeyRelease>", evaluate_password)

show_btn = tk.Button(entry_frame, text="👁", command=toggle_password, bg="#CCCCCC", relief="flat")
show_btn.pack(side="right", padx=5)

strength_label = tk.Label(container, text="", font=("Montserrat", 12, "bold"), bg="#FFFFFF", fg="#000000")
strength_label.pack(pady=5)

style = ttk.Style()
style.configure("TProgressbar", thickness=8, troughcolor="#DDDDDD", background="#00FFFF", borderwidth=0, relief="flat")
strength_meter = ttk.Progressbar(container, length=300, mode='determinate', maximum=100, style="TProgressbar")
strength_meter.pack(pady=5)

checklist_labels = []
for _ in range(5):
    lbl = tk.Label(container, text="", font=("Roboto", 10), bg="#FFFFFF", fg="#000000")
    lbl.pack(anchor="w", padx=10)
    checklist_labels.append(lbl)

generate_btn = tk.Button(container, text="Generate Strong Password", command=generate_password, bg="#00FFFF", fg="#000000", font=("Montserrat", 10, "bold"), relief="flat", padx=10, pady=5)
generate_btn.pack(pady=5)

copy_btn = tk.Button(container, text="Copy Password", command=copy_to_clipboard, bg="#4CAF50", fg="#000000", font=("Montserrat", 10, "bold"), relief="flat", padx=10, pady=5)
copy_btn.pack(pady=5)

theme_button = tk.Button(container, text="🌙 Dark Mode", command=toggle_theme, bg="#4A90E2", fg="#FFFFFF", font=("Montserrat", 10, "bold"), relief="flat", padx=10, pady=5)
theme_button.pack(pady=5)

root.mainloop()
