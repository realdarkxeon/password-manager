from tkinter import *
from tkinter import messagebox

from simplejson import JSONDecodeError
import pyperclip, json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '*', '+']

def password_generator():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    password_list += [random.choice(letters) for char in range(nr_letters)]
    password_list += [random.choice(symbols) for char in range(nr_symbols)]
    password_list += [random.choice(numbers) for char in range(nr_numbers)]

    random.shuffle(password_list)

    password = ''.join([char for char in password_list])

    password_entry.delete(0, END)
    password_entry.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def find_data():
    website = website_entry.get()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            try:
                caught_username = data[website]["username"]
            except KeyError:
                messagebox.showinfo(title = "Warning", message = f"No details for the {website} exists!")
            else:
                caught_password = data[website]["password"]
                messagebox.showinfo(title = website, message = f"Username/Email: {caught_username}\nPassword: {caught_password}")
    except FileNotFoundError:
        messagebox.showinfo(title="Warning", message="No data file has found!")

def add():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "username": username,
            "password": password
        }
    }

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showinfo(title = "Invalid operation", message = f"Please, do not leave any fields empty!")
    else:
        try:
            with open(file="data.json", mode="r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open(file="data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open(file="data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            pyperclip.copy(password)
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx = 50, pady = 50)

canvas = Canvas(width = 200, height = 200)
filename = PhotoImage(file = "logo.png")
image = canvas.create_image(100, 100, image = filename)
canvas.grid(row = 0, column = 1)

# Labels
website_label = Label(text = "Website:")
website_label.grid(row = 1, column = 0)
username_label = Label(text = "Email/Username:")
username_label.grid(row = 2, column = 0)
password_label = Label(text = "Password:")
password_label.grid(row = 3, column = 0)

# Entries
website_entry = Entry(width = 21)
website_entry.grid(row = 1, column = 1)
website_entry.focus()
username_entry = Entry(width = 35)
username_entry.grid(row = 2, column = 1, columnspan = 2)
username_entry.insert(0, "realdarkxeon@gmail.com")
password_entry = Entry(width = 21)
password_entry.grid(row = 3, column = 1)

#Buttons
search_button = Button(width = 14, text = "Search", command = find_data)
search_button.grid(row = 1, column = 2)
generate_password = Button(width = 14, text = "Generate Password", command = password_generator)
generate_password.grid(row = 3, column = 2)
add_password = Button(width = 36, text = "Add", command = add)
add_password.grid(row = 4, column = 1, columnspan = 2)

window.mainloop()