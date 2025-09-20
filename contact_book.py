import tkinter as tk
from tkinter import messagebox
import json, os

# Data Persistence 
FILE_NAME = "contacts.json"

def load_contacts():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []

def save_contacts():
    with open(FILE_NAME, "w") as f:
        json.dump(contacts, f, indent=4)

# Core Functions
def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()
    address = address_entry.get().strip()
   
    if not name or not phone:
        messagebox.showwarning("Error", "Name and Phone are required!")
        return
   
    contacts.append({"name": name, "phone": phone, "email": email, "address": address})
    save_contacts()
    refresh_list()
    clear_entries()
    messagebox.showinfo("Success", "Contact added successfully!")

def update_contact():
    try:
        index = contact_list.curselection()[0]
        contacts[index] = {
            "name": name_entry.get().strip(),
            "phone": phone_entry.get().strip(),
            "email": email_entry.get().strip(),
            "address": address_entry.get().strip()
        }
        save_contacts()
        refresh_list()
        messagebox.showinfo("Updated", "Contact updated successfully!")
    except:
        messagebox.showwarning("Error", "Select a contact to update")

def delete_contact():
    try:
        index = contact_list.curselection()[0]
        del contacts[index]
        save_contacts()
        refresh_list()
        clear_entries()
        messagebox.showinfo("Deleted", "Contact deleted successfully!")
    except:
        messagebox.showwarning("Error", "Select a contact to delete")

def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

def show_details(event):
    try:
        index = contact_list.curselection()[0]
        contact = contacts[index]
        name_entry.delete(0, tk.END); name_entry.insert(0, contact["name"])
        phone_entry.delete(0, tk.END); phone_entry.insert(0, contact["phone"])
        email_entry.delete(0, tk.END); email_entry.insert(0, contact["email"])
        address_entry.delete(0, tk.END); address_entry.insert(0, contact["address"])
    except:
        pass

def refresh_list(filter_text=""):
    contact_list.delete(0, tk.END)
    for contact in contacts:
        if filter_text.lower() in contact["name"].lower():
            contact_list.insert(tk.END, contact["name"])

def search_contacts(event):
    query = search_entry.get().strip()
    refresh_list(query)

# GUI
root = tk.Tk()
root.title("Codsoft Contact Book")
root.geometry("800x500")
root.config(bg="#f0f4f7")

# Title
title = tk.Label(root, text="Codsoft Contact Book", font=("Arial", 20, "bold"),
                 bg="#8C30E7", fg="white", pady=10)
title.pack(fill="x")

main_frame = tk.Frame(root, bg="#f0f4f7")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Left Panel (Contacts List + Search)
left_frame = tk.Frame(main_frame, bg="#dca4ff", width=250, relief="groove", bd=2)
left_frame.pack(side="left", fill="y")

tk.Label(left_frame, text="Search", font=("Arial", 12, "bold"), bg="#dca4ff").pack(pady=5)
search_entry = tk.Entry(left_frame, font=("Arial", 11), width=25)
search_entry.pack(pady=5, padx=10)
search_entry.bind("<KeyRelease>", search_contacts)

contact_list = tk.Listbox(left_frame, width=25, height=20, font=("Arial", 12))
contact_list.pack(pady=10, padx=10, fill="y")
contact_list.bind("<<ListboxSelect>>", show_details)

# Right Panel (Details & Buttons)
right_frame = tk.Frame(main_frame, bg="#f0f4f7")
right_frame.pack(side="right", fill="both", expand=True, padx=20)

tk.Label(right_frame, text="Contact Details", font=("Arial", 16, "bold"),
         bg="#f0f4f7", fg="#8C30E7").pack(anchor="w", pady=5)

# Entry fields
def make_label_entry(parent, text):
    tk.Label(parent, text=text, font=("Arial", 12), bg="#f0f4f7").pack(anchor="w")
    entry = tk.Entry(parent, width=50, font=("Arial", 12))
    entry.pack(pady=3, anchor="w")
    return entry

name_entry = make_label_entry(right_frame, "Name:")
phone_entry = make_label_entry(right_frame, "Phone:")
email_entry = make_label_entry(right_frame, "Email:")
address_entry = make_label_entry(right_frame, "Address:")

# Buttons
btn_frame = tk.Frame(right_frame, bg="#f0f4f7")
btn_frame.pack(pady=15)

btn_style = {"font": ("Arial", 11, "bold"), "bg": "#F642FF", "fg": "white", "width": 12, "relief": "raised"}

tk.Button(btn_frame, text="Add", command=add_contact, **btn_style).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Update", command=update_contact, **btn_style).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_contact, **btn_style).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Clear", command=clear_entries, **btn_style).grid(row=0, column=3, padx=5)

# Run
contacts = load_contacts()
refresh_list()
root.mainloop()