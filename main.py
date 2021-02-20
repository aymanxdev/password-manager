from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)
    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)



# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_to_file():
    website = website_input.get()
    email = username_input.get()
    password = password_input.get()
    new_data = {website :{
        "email": email ,
        "password": password,
    }}

    if len(password) == 0 or len(website) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")
    else:
        is_ok = messagebox.askokcancel(title=website,   message=f"These are the details entered: \nEmail: {email} " 
                                                               f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            try:
                with open("data.json","r") as passwords_data:
                     #Reading old data
                    data = json.load(passwords_data)
            except FileNotFoundError:
                with open('data.json', 'w') as passwords_data:
                    json.dump(new_data, passwords_data, indent=4)
            else:
                #Updating old data with new data
                data.update(new_data)
                with open('data.json', 'w') as passwords_data:
                    #saving updated
                    json.dump(data, passwords_data, indent=4)
            finally:
                website_input.delete(0, END)
                password_input.delete(0, END)

# ---------------------------- Search For Passwords ------------------------------- #
def search():
    website = website_input.get()
    try:
        with open('data.json') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found, please add data")
    else:
        if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(title=website, message=f"Your Details: \nEmail: {email} \nPassword: {password} ")
        else:
            messagebox.showinfo(title="Error", message=f"No Details for {website} exists ")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)


logo_img = PhotoImage(file="logo.gif")
canvas = Canvas(width= 200, height=200)
canvas.create_image(100,103, image= logo_img)
canvas.grid(column=1, row=0)

# --------------- website Label --------------- #
website_label = Label(text="Website: ")
website_label.grid(column= 0, row=1)
website_input = Entry(width=21)
website_input.focus()
website_input.grid(column= 1, row=1)
# --------------- Email/Username Label --------------- #
username_label = Label(text="Email/Username: ")
username_label.grid(column= 0, row=2)
username_input = Entry(width=38)
username_input.insert(END, "ayman@email.com")
username_input.grid(column= 1, row=2, columnspan=2)
# --------------- Password Label --------------- #
password_label = Label(text="Password: ")
password_label.grid(column= 0, row=3)
password_input = Entry(width=21)
password_input.grid(column= 1, row=3)
# --------------- Generate Button --------------- #
generate_button = Button(text="Generate Password", command= generate_password)
generate_button.grid(column= 2, row=3)
# --------------- Search Button --------------- #
search_button = Button(text="Search", command= search, width=13)
search_button.grid(column= 2, row=1)
# --------------- Add Button --------------- #
add_button = Button(text="Add", width=36, command= save_to_file)
add_button.grid(column= 1, row= 4, columnspan=2)



# img = Image.open("logo.png")
# logo_img = ImageTk.PhotoImage(img)
window.mainloop()