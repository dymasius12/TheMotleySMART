#!/opt/anaconda3/envs/motley_smart/bin/python
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

def start_program():
    landing_frame.pack_forget()
    menu_frame.pack(fill=tk.BOTH, expand=True)
    stock_code_entry.pack(pady=20)
    menu_listbox.pack(pady=20)
    confirm_button.pack(pady=20)

def confirm_choice():
    choice = menu_listbox.curselection()[0]
    if choice == 4:
        exit_program()
    # ... Implement other choices here ...

def exit_program():
    root.destroy()

def go_back():
    menu_frame.pack_forget()
    landing_frame.pack(fill=tk.BOTH, expand=True)

# Main window
root = tk.Tk()
root.title("Stock Application")
root.geometry("800x500")
root.resizable(False, False)

# Style for a rounded button
style = ttk.Style()
style.configure('TButton', font=('Arial', 23), borderwidth='4')
style.map('TButton', background=[('active', 'cyan')])
button_height = 50  # or any other value you prefer
style.configure('TButton', padding=(0, button_height // 2, 0, button_height // 2))

# Landing Frame
landing_frame = tk.Frame(root)
landing_frame.pack(fill=tk.BOTH, expand=True)
logo_image = tk.PhotoImage(file="logo_mid.png")
tk.Label(landing_frame, image=logo_image).pack(pady=20)
tk.Label(landing_frame, text="Stock Application", font=('Arial', 24)).pack(pady=20)
start_button = ttk.Button(landing_frame, text="Start", command=start_program, style='TButton', width=10) #Start Button
start_button.pack(pady=20)

# Menu Frame
menu_frame = tk.Frame(root)
back_button = tk.Button(menu_frame, text="←", command=go_back, fg="black", bg="blue", font=('Arial', 16), height=1, width=3)
back_button.pack(anchor="nw", padx=10, pady=10)
stock_code_entry = tk.Entry(menu_frame, font=('Arial', 16), width=30)
menu_listbox = tk.Listbox(menu_frame, font=('Arial', 16), width=30, height=5)
menu_listbox.insert(1, "1. Stock Dashboard")
menu_listbox.insert(2, "2. Display Stock Price vs Time Graph")
menu_listbox.insert(3, "3. Stock Analysis on Stock Parameters")
menu_listbox.insert(4, "4. Stock News")
menu_listbox.insert(5, "5. Exit Program")
confirm_button = ttk.Button(menu_frame, text="Confirm", command=confirm_choice, style='TButton', width=10)
confirm_button.pack(pady=20)

root.mainloop()

