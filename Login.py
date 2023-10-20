import smtplib
from email.mime.text import MIMEText
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
from software_for_customers_ import for_customers
from main import Inventory_Management
from employee import employees
import random


def main():
    win = Tk()
    app = Login_Window(win)
    win.mainloop()
class Login_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")
        root.configure(bg="white")

        self.bg_image = Image.open(r"C:\Users\meyta\inventory_management_images\bg.png")
        self.bg_image = self.bg_image.resize((screen_width, screen_height), Image.BILINEAR)
        self.bg = ImageTk.PhotoImage(self.bg_image)

        img = Image.open(r"C:\Users\meyta\inventory_management_images\menu_im.png")
        img = img.resize((700, 600), Image.BILINEAR)
        self.photo = ImageTk.PhotoImage(img)
        lblimg = Label(image=self.photo, bg="white", borderwidth=0)
        lblimg.place(x=50, y=20, width=700, height=600)

        frame = Frame(self.root, bg="white")
        frame.place(x=800, y=0, width=400, height=650)

        get_str = Label(frame, text="Sign in", font=("Great Vibes", 40, "bold"), fg="#008296", bg="white")
        get_str.place(x=80, y=100)

        #label
        username = lbl = Label(frame, text="Email", font=("Great Vibes", 15, "bold"),fg="black", bg="white")
        username.place(x=60, y=200)
        self.txtuser= Entry(frame, font=("Great Vibes", 15, "bold"))
        self.txtuser.place(x=30, y=230, width=270)

        passwd = lbl = Label(frame, text="Password", font=("Great Vibes", 15, "bold"), fg="black", bg="white")
        passwd.place(x=60, y=270)
        self.txtpasswd = Entry(frame, font=("Great Vibes", 15, "bold"))
        self.txtpasswd.place(x=30, y=300, width=270)

        # icon image
        img2 = Image.open(r"C:\Users\meyta\inventory_management_images\icon1.jpg")
        img2 = img2.resize((25, 25), Image.BILINEAR)
        self.photo2 = ImageTk.PhotoImage(img2)
        lblimg2 = Label(image=self.photo2, bg="white", borderwidth=0)
        lblimg2.place(x=830, y=200, width=25, height=25)

        img3 = Image.open(r"C:\Users\meyta\inventory_management_images\icon2.jpg")
        img3 = img3.resize((25, 25), Image.BILINEAR)
        self.photo3 = ImageTk.PhotoImage(img3)
        lblimg3 = Label(image=self.photo3, bg="white", borderwidth=0)
        lblimg3.place(x=830, y=270, width=25, height=25)

        # login btn

        loginbtn = Button(frame,text="Login",command=self.login, font=("Great Vibes", 15, "bold"), bd=3,relief=RIDGE, fg="white", bg="#008296", activebackground="#008296", activeforeground="white")
        loginbtn.place(x=30, y=350, width=300, height=35)

        # register btn
        registerbtn = Button(frame, text="New User Register", command=self.register_window, font=("Great Vibes", 10, "bold"), borderwidth=0,bd=3, relief=RIDGE, fg="black",
                          bg="white")
        registerbtn.place(x=20, y=400, width=160)

        # forget password btn
        forget_password_btn = Button(frame, text="forget Password",command=self.forget_password, font=("Great Vibes", 10, "bold"), borderwidth=0, bd=3, relief=RIDGE,
                             fg="black",
                             bg="white")
        forget_password_btn.place(x=20, y=430, width=160)

        store_btn = Button(frame, text="Click to go to store (for customers)",
                                     font=("Great Vibes", 15, "bold"), borderwidth=0, bd=3, relief=RIDGE,
                                     fg="black",
                                     bg="white",command=self.store)
        store_btn.place(x=20, y=480, width=350 ,height=40)

    def store(self):
        self.new_window= Toplevel(self.root)
        self.app= for_customers(self.new_window)


    def register_window(self):
        if self.txtuser.get() == "" or self.txtpasswd.get() == "":
            messagebox.showerror("Error", "All fields required", parent=self.root)
        else:
            conn = mysql.connector.connect(host="localhost", user="root", passwd="1234",
                                           database="inventory_management")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM employees WHERE email=%s and password=%s",
                              (self.txtuser.get(), self.txtpasswd.get()))
            row = my_cursor.fetchone()
            conn.close()

            conn2 = mysql.connector.connect(host="localhost", user="root", passwd="1234",
                                           database="inventory_management")
            my_cursor = conn2.cursor()
            my_cursor.execute("SELECT type FROM employees WHERE email=%s and password=%s",
                              (self.txtuser.get(), self.txtpasswd.get()))
            type = my_cursor.fetchone()
            conn2.close()

            if row is None:
                messagebox.showerror("Error", "Invalid Username or Password", parent=self.root)
            else:
                if type[0] == "Manager":
                    self.root.destroy()
                    inventory_root = Tk()
                    app = employees(inventory_root)
                    inventory_root.mainloop()
                else:
                    print(row)
                    print(type[0])
                    messagebox.showerror("Error", "Option Relevant Only To The Manager", parent=self.root)
            conn.commit()
            conn.close()
    def login(self):
        if self.txtuser.get() == "" or self.txtpasswd.get() == "":
            messagebox.showerror("Error", "All fields required", parent=self.root)
        else:
            conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM employees WHERE email=%s and password=%s",
                              (self.txtuser.get(), self.txtpasswd.get()))
            row = my_cursor.fetchone()
            conn.close()

            if row is None:
                messagebox.showerror("Error", "Invalid Username or Password", parent=self.root)
            else:
                self.root.destroy()
                inventory_root = Tk()
                app = Inventory_Management(inventory_root)
                inventory_root.mainloop()
            conn.commit()
            conn.close()

    def reset_pass(self):
        if self.code.get() == "":
            messagebox.showerror("Error", "Please enter the code", parent= self.root2)
        elif self.txt_newpass.get() == "":
            messagebox.showerror("Error", "Please enter the new password", parent= self.root2)
        else:
            conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
            my_cursor = conn.cursor()
            query = ("SELECT * FROM employees where email=%s")
            value = (self.txtuser.get(),)
            my_cursor.execute(query, value)
            row = my_cursor.fetchone()
            if row is None:
                messagebox.showerror("Error", "employee not found", parent= self.root2)
            else:
                print(int(self.new_pass))
                print(int(self.code.get()))
                if int(self.new_pass) == int(self.code.get()):
                    query = ("UPDATE employees SET password=%s WHERE email=%s")
                    value = (self.txt_newpass.get(), self.txtuser.get())
                    my_cursor.execute(query, value)

                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Info", "Your password has been reset, please login with the new password",
                                        parent=self.root2)
                    self.root2.destroy()
                else:
                    messagebox.showerror("Error", "Invalid Code", parent=self.root2)


    def is_valid_email(email):
        if "@" in email and "." in email:
            return True
        return False

    def forget_password(self):
        if self.txtuser.get() == "":
            messagebox.showerror("Error", "Please enter the email address to reset password", parent=self.root)
        else:
            conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
            my_cursor = conn.cursor()
            query = ("SELECT * FROM employees WHERE email=%s")
            value = (self.txtuser.get(),)
            my_cursor.execute(query, value)
            row = my_cursor.fetchone()
            print(row)
            if row is None:
                messagebox.showerror("My Error", "Please enter the valid user name", parent=self.root)
            else:
                conn.close()
                try:
                    ob = smtplib.SMTP("smtp.gmail.com", 587)
                    ob.starttls()
                    ob.login("enter_mail", "enter_password")
                    self.new_pass = random.randint(1000, 999999)
                    message = MIMEText(f"Hello, Your Code is: {self.new_pass}")
                    message["Subject"] = "Password Reset Code"
                    message["From"] = "meytalpython@gmail.com"
                    message["To"] = self.txtuser.get()

                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    ob.login("enter_mail", "enter_password")
                    server.sendmail("meytalpython@gmail.com", self.txtuser.get(), message.as_string())
                    server.quit()
                    messagebox.showinfo("Success", "Code is successfully sent to your email", parent=self.root)
                    self.root2 = Toplevel()
                    self.root2.title("Forget Password")
                    self.root2.geometry("340x250+500+100")

                    l = Label(self.root2, text="Forget Password", font=("Great Vibes", 20, "bold"), fg="#008296",
                              bg="white")
                    l.place(x=0, y=10, relwidth=1)

                    code = Label(self.root2, text="Code", font=("Great Vibes", 15, "bold"),
                                         bg="white",
                                         fg="black")
                    code.place(x=50, y=50)

                    self.code = ttk.Entry(self.root2, font=("Great Vibes", 15, "bold"))
                    self.code.place(x=50, y=80, width=250)

                    new_password = Label(self.root2, text="New Password", font=("Great Vibes", 15, "bold"),
                                         bg="white",
                                         fg="black")
                    new_password.place(x=50, y=110)

                    self.txt_newpass = ttk.Entry(self.root2, font=("Great Vibes", 15, "bold"))
                    self.txt_newpass.place(x=50, y=140, width=250)

                    btn = Button(self.root2, text="Reset", command=self.reset_pass,
                                 font=("Great Vibes", 15, "bold"),
                                 bg="#008296",
                                 fg="white")
                    btn.place(x=100, y=170)
                except Exception as es:
                    messagebox.showerror("Error", "Invalid Email", parent=self.root)


if __name__ == "__main__":
    main()
