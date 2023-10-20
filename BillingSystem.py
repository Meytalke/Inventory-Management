from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
import smtplib
import os
import tempfile
from tkinter import messagebox
from tkinter.ttk import Combobox
import mysql.connector
from datetime import datetime
import random
from tkinter import simpledialog
from prettytable import PrettyTable

class BillingSystem:
    def __init__(self, root):
        self.root = root
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.iconbitmap(r"C:\Users\meyta\inventory_management_images\bill.png")
        self.root.title("Billing System")


        bg_img = Image.open(r"C:\Users\meyta\inventory_management_images\Product_bg4.jpg")
        bg_img = bg_img.resize((screen_width, screen_height), Image.BILINEAR)
        self.bg_img = ImageTk.PhotoImage(bg_img)

        bg_label = Label(self.root, image=self.bg_img)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title label
        title_lbl = Label(self.root, text="Billing System",
                          font=("Great Vibes", 34, "bold"), bg="#2f3030", fg="white")
        title_lbl.place(x=0, y=-105, width=1500, relx=0.5, rely=0.19, anchor="center")

        main_frame = Frame(self.root, bd=2, bg="white", )
        main_frame.place(x=0, y=70, width=1270, height=600)

        self.var_customer_name = StringVar()
        self.var_customer_contact = StringVar()
        self.var_total = StringVar()

        self.var_product_name = StringVar()
        self.var_product_id = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()

        self.var_bill_number = StringVar()

        self.var_Serach = StringVar()

        Left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                font=("Great Vibes", 12, "bold"))
        Left_frame.place(x=0, y=10, width=450, height=550)

        title_all_products = Label(Left_frame, text="All Products",
                          font=("Great Vibes", 20, "bold"), bg="#2f3030", fg="white")
        title_all_products.place(x=0, y=-120, width=450, relx=0.5, rely=0.25, anchor="center")

        Serach_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE,
                                  text="Serach Product | By Name",
                                  font=("Great Vibes", 12, "bold"))
        Serach_frame.place(x=5, y=40, width=440, height=110)

        proName_label = tk.Label(Serach_frame, text="Product Name:", font=("Great Vibes", 12, "bold"),
                                 bg="white")
        proName_label.grid(row=0, column=0, padx=7, pady=5, sticky=tk.W)

        Serach_entry = ttk.Entry(Serach_frame, width=11, font=("Great Vibes", 12, "bold"))
        Serach_entry.grid(row=0, column=1, pady=7, padx=7, sticky=W)

        self.Serach_entry = Serach_entry
        Serach_btn = Button(Serach_frame, text="Search", font=("Great Vibes", 12, "bold"), width=10,
                            command=self.Serach,
                            bg="#2f3030",
                            fg="white")
        Serach_btn.grid(row=0, column=2, padx=3)
        showAll_btn = Button(Serach_frame, text="Reset", font=("Great Vibes", 12, "bold"), width=10,
                             command=self.fetch_data,
                             bg="#2f3030",
                             fg="white")
        showAll_btn.grid(row=1, column=2, padx=3)

        table_products_frame = Frame(Left_frame, bd=2, bg="white", relief=RIDGE)
        table_products_frame.place(x=5, y=150, width=440, height=390)

        scroll_y = ttk.Scrollbar(table_products_frame, orient=VERTICAL)
        self.products_table = ttk.Treeview(table_products_frame, column=(
            "productId", "name", "price",  "qty"),  yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.products_table.yview)

        self.products_table.heading("productId", text="Product ID")
        self.products_table.heading("name", text="Name")
        self.products_table.heading("price", text="Price")
        self.products_table.heading("qty", text="Quantity")
        self.products_table["show"] = "headings"

        self.products_table.column("productId",  width=100)
        self.products_table.column("name", width=100)
        self.products_table.column("price", width=100)
        self.products_table.column("qty", width=100)
        self.products_table.pack(fill=BOTH, expand=1)
        self.products_table.bind("<ButtonRelease>", self.get_cursor)

        Right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                 font=("Great Vibes", 12, "bold"))
        Right_frame.place(x=450, y=10, width=815, height=550)

        customer_details_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE,
                                 font=("Great Vibes", 12, "bold"))
        customer_details_frame.place(x=0, y=0, width=450, height=100)

        title_customer_details = Label(customer_details_frame, text="Customer Details",
                                   font=("Great Vibes", 20, "bold"), bg="#2f3030", fg="white")
        title_customer_details.place(x=0, y=-10, width=450, relx=0.5, rely=0.25, anchor="center")

        name_label = tk.Label(customer_details_frame, text="Name:", font=("Great Vibes", 12, "bold"),
                              bg="white")
        name_label.place(x=0, y=50)

        name_entry = ttk.Entry(customer_details_frame, width=15,
                               font=("Great Vibes", 12, "bold"), textvariable=self.var_customer_name)
        name_entry.place(x=50, y=50)

        contact_label = tk.Label(customer_details_frame, text="Contact No:", font=("Great Vibes", 12, "bold"),
                              bg="white")
        contact_label.place(x=200, y=50)

        contact_entry = ttk.Entry(customer_details_frame, width=15,
                               font=("Great Vibes", 12, "bold"),textvariable=self.var_customer_contact)
        contact_entry.place(x=300, y=50)

        product_details_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE,
                                            font=("Great Vibes", 12, "bold"))
        product_details_frame.place(x=0, y=100, width=450, height=100)

        ProName_label = tk.Label(product_details_frame, text="Product Name", font=("Great Vibes", 12, "bold"),
                              bg="white")
        ProName_label.place(x=0, y=0)

        ProName_entry = ttk.Entry(product_details_frame, width=15, textvariable=self.var_product_name,
                               font=("Great Vibes", 12, "bold"),state='disabled')
        ProName_entry.place(x=0, y=30)


        price_unit_label = tk.Label(product_details_frame, text="Price", font=("Great Vibes", 12, "bold"),
                                 bg="white")
        price_unit_label.place(x=150, y=0)

        price_unit_entry = ttk.Entry(product_details_frame, width=15, textvariable=self.var_price,
                                  font=("Great Vibes", 12, "bold"), state='disabled')
        price_unit_entry.place(x=150, y=30)

        qty_label = tk.Label(product_details_frame, text="Quantity:", font=("Great Vibes", 12, "bold"),
                                 bg="white")
        qty_label.place(x=300, y=0)

        qty_entry = ttk.Entry(product_details_frame, width=15, textvariable= self.var_qty,
                                  font=("Great Vibes", 12, "bold"))
        qty_entry.place(x=300, y=30)

        add_btn = Button(product_details_frame, text="Add To Cart", font=("Great Vibes", 12, "bold"),
                         width=14, bg="#2f3030", fg="white", command=self.add_to_cart)

        add_btn.place(x=300, y=58)

        clear_btn = Button(product_details_frame, text="Clear Cart", font=("Great Vibes", 12, "bold"),
                         width=14, bg="#2f3030", fg="white", command=self.clear_cart)

        clear_btn.place(x=140, y=58)

        title_cart = Label(Right_frame, text="Cart",
                                       font=("Great Vibes", 20, "bold"), bg="#2f3030", fg="white")
        title_cart.place(x=-180, y=85, width=450, relx=0.5, rely=0.25, anchor="center")

        cart_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        cart_frame.place(x=0, y=243, width=450, height=250)

        scroll_y = ttk.Scrollbar(cart_frame, orient=VERTICAL)
        self.cart_frame = ttk.Treeview(cart_frame, column=(
            "productId", "name", "price", "qty"), yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.cart_frame.yview)

        self.cart_frame.heading("productId", text="Product ID")
        self.cart_frame.heading("name", text="Name")
        self.cart_frame.heading("price", text="Price")
        self.cart_frame.heading("qty", text="Quantity")
        self.cart_frame["show"] = "headings"

        self.cart_frame.column("productId", width=100)
        self.cart_frame.column("name", width=100)
        self.cart_frame.column("price", width=100)
        self.cart_frame.column("qty", width=100)
        self.cart_frame.pack(fill=BOTH, expand=1)
        self.cart_frame.bind("<ButtonRelease>")
        self.cart_frame.tag_bind('button', '<Button-1>')
        self.cart_frame.tag_configure('button', background='lightblue')

        customer_bill_area_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE,
                                            font=("Great Vibes", 12, "bold"))
        customer_bill_area_frame.place(x=450, y=0, width=360, height=490)

        title_bill_area = Label(customer_bill_area_frame, text="Customer Bill Area",
                                       font=("Great Vibes", 20, "bold"), bg="#2f3030", fg="white")
        title_bill_area.place(x=0, y=-105, width=420, relx=0.5, rely=0.25, anchor="center")

        text_frame=LabelFrame(customer_bill_area_frame, bd=2, bg="white", relief=RIDGE,
                                            font=("Great Vibes", 12, "bold"))
        text_frame.place(x=0, y=40, width=355, height=445)

        scroolbar= Scrollbar(text_frame,orient=VERTICAL)
        scroolbar.pack(side=RIGHT,fill=Y)

        self.textarea = Text(text_frame, height=40,width=55,yscrollcommand=scroolbar.set)
        self.textarea.pack()
        scroolbar.config(command=self.textarea.yview)

        btn_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE,
                                 font=("Great Vibes", 12, "bold"))
        btn_frame.place(x=0, y=500, width=800, height=50)

        bill_btn = Button(btn_frame, text="Generate Bill", font=("Great Vibes", 12, "bold"),
                           width=15,height=2, bg="#2f3030", fg="white", command=self.bill_area)

        bill_btn.grid(row=0,column=0)

        clear_btn = Button(btn_frame, text="Clear", font=("Great Vibes", 12, "bold"),
                           width=15,height=2, bg="#2f3030", fg="white", command=self.clear_bill)

        clear_btn.grid(row=0, column=2)

        email_btn = Button(btn_frame, text="Gmail", font=("Great Vibes", 12, "bold"),
                          width=15,height=2, bg="#2f3030", fg="white" , command=self.send_gmail)

        email_btn.grid(row=0, column=3)

        print_btn = Button(btn_frame, text="Print", font=("Great Vibes", 12, "bold"),
                           width=15,height=2, bg="#2f3030", fg="white", command=self.print_bill)

        print_btn.grid(row=0, column=4)
        search_bill_btn = Button(btn_frame, text="Search Bill", font=("Great Vibes", 12, "bold"),
                           width=15, height=2, bg="#2f3030", fg="white", command=self.search_bill)
        search_bill_btn.grid(row=0, column=5)
        self.fetch_data()

    def connect_to_database(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="1234",
            database="inventory_management"
        )
        return conn

    def get_cursor(self,event=""):
        cursor_focus = self.products_table.focus()
        content = self.products_table.item(cursor_focus)
        data = content["values"]
        self.var_product_name.set(data[1])
        self.var_price.set(data[2])
        self.var_product_id = data[0]

    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost",
                                       user="root",
                                       passwd="1234",
                                       database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT productID,name,price,qty  FROM products WHERE status = 'Active'")
        data = my_cursor.fetchall()
        if len(data) != 0:
            self.products_table.delete(*self.products_table.get_children())
            for i in data:
                self.products_table.insert("", END, values=i)
            conn.commit()
        conn.close()

    def Serach(self):
        search_text = self.var_Serach.get()
        search_value = self.Serach_entry.get()

        if search_value != "":
            self.search_by_name(search_value)
        else:
            messagebox.showwarning("Invalid Selection", "Please select a valid search option.", parent=self.root)

    def search_by_name(self, search_value):
        query = "SELECT productID,name,price,qty  FROM products WHERE name = %s"
        params = (search_value,)
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute(query, params)
        data = my_cursor.fetchall()
        if len(data) != 0:
            self.products_table.delete(*self.products_table.get_children())
            for i in data:
                self.products_table.insert("", END, values=i)
            conn.commit()
        conn.close()

    def add_to_cart(self):
        product_id = self.var_product_id
        product_name = self.var_product_name.get()
        price = self.var_price.get()
        quantity = self.var_qty.get()

        if product_id == "" or product_name == "" or price == "" or quantity == "":
            messagebox.showerror("Error", "Please select a product and enter quantity.", parent=self.root)
        else:
            try:
                quantity = int(quantity)
                if quantity < 0:
                    messagebox.showerror("Error", "Please enter valid quantity.", parent=self.root)
                else:
                    available_qty = 0
                    selected_product = self.products_table.selection()
                    if selected_product:
                        item_values = self.products_table.item(selected_product)['values']
                        available_qty = int(item_values[3])

                    # Check if the product is already in the cart
                    cart_items = self.cart_frame.get_children()
                    for item in cart_items:
                        item_values = self.cart_frame.item(item)['values']
                        if item_values[0] == product_id:
                            total_quantity = quantity + int(item_values[3])
                            if total_quantity > available_qty:
                                messagebox.showerror("Error", "Total quantity exceeds available stock.",
                                                     parent=self.root)
                                return
                            else:
                                self.cart_frame.item(item, values=(
                                    product_id, product_name, price, total_quantity))
                                self.var_product_name.set("")
                                self.var_price.set("")
                                self.var_qty.set("")
                                return

                    if quantity > available_qty:
                        messagebox.showerror("Error", "Selected quantity is more than available stock.",
                                             parent=self.root)
                    else:
                        item_id = len(self.cart_frame.get_children()) + 1
                        self.cart_frame.insert("", END,
                                               values=(product_id, product_name, price, quantity))
                        self.var_product_name.set("")
                        self.var_price.set("")
                        self.var_qty.set("")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid integer for quantity.", parent=self.root)

    def clear_cart(self):
        self.cart_frame.delete(*self.cart_frame.get_children())

    def calculate_total(self):
        total = 0
        cart_items = self.cart_frame.get_children()
        for item in cart_items:
            item_values = self.cart_frame.item(item)['values']
            quantity = int(item_values[3])
            price = float(item_values[2])
            total += quantity * price
        print(total)
        self.var_total = total
        return total

    def is_valid_cvv(self, cvv):
        if len(cvv) != 3 or not cvv.isdigit():
            return False
        return True

    def is_valid_expiration_date(self, expiration_month, expiration_year):
        if expiration_month == "" or expiration_year == "":
            return False
        try:
            expiration_month = int(expiration_month)
            expiration_year = int(expiration_year)
            if not (1 <= expiration_month <= 12) or not (2023 <= expiration_year <= 2200):
                return False

            current_year = datetime.now().year
            current_month = datetime.now().month

            if expiration_year < current_year or (expiration_year == current_year and expiration_month < current_month):
                return False

            return True
        except ValueError:
            return False

    def is_valid_card_number(self, card_number):
        if len(card_number) != 16 or not card_number.isdigit():
            return False
        return True

    def process_credit_card_payment(self, credit_window, card_number, expiration_month, expiration_year, cvv):
        if not self.is_valid_card_number(card_number):
            messagebox.showerror("Error", "Invalid card number", parent=credit_window)
        elif not self.is_valid_expiration_date(expiration_month, expiration_year):
            messagebox.showerror("Error", "Invalid expiration date", parent=credit_window)
        elif not self.is_valid_cvv(cvv):
            messagebox.showerror("Error", "Invalid CVV", parent=credit_window)
        else:
            self.textarea.insert(END, "\nPayment Method: Credit")
            self.textarea.insert(END, "\nCard Number: " + card_number)
            self.textarea.insert(END, "\nExpiration Date: {}/{}".format(expiration_month, expiration_year))
            self.textarea.insert(END, "\nCVV: " + cvv)
            self.save_bill()
            self.release_stock()
            self.add_data_to_orders()
            self.add_data_to_orders_details()
            self.add_data_to_customers()
            self.clear_bill()
            self.fetch_data()
    def bill_area(self):
        self.textarea.delete("1.0", END)
        total_bill = self.calculate_total()
        print(str(self.var_customer_name.get()))
        print(str(self.var_customer_contact.get()))
        if self.var_customer_name.get() == "" or self.var_customer_contact.get() == "":
            messagebox.showerror("Error", "Customer Details Are Requires", parent=self.root)
        elif total_bill == 0:
            messagebox.showerror("Error", "No Product Are Selected", parent=self.root)
        else:
            self.textarea.insert(END, "\t\tMeytal Store")
            self.textarea.insert(END, "\n\tBrenner 1, Bat Yam, Israel")
            self.textarea.insert(END, "\n\t\t+972558852202")
            self.textarea.insert(END, "\n\tDate: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.textarea.insert(END, "\n*****************************************")
            self.var_bill_number = random.randint(1000, 999999)
            self.textarea.insert(END, "\n\tBill Number: " + str(self.var_bill_number))
            self.textarea.insert(END,
                                 "\n\tCustomer Name: " + str(self.var_customer_name.get()) + "\n\tCustomer Contact: " +
                                 str(self.var_customer_contact.get()))
            self.textarea.insert(END, "\n*****************************************")

            table = PrettyTable()
            table.field_names = ["Product", "Qty", "Price", "Total"]

            cart_items = self.cart_frame.get_children()
            for item in cart_items:
                item_values = self.cart_frame.item(item)['values']
                product = str(item_values[1])
                quantity = int(item_values[3])
                price = float(item_values[2])
                total = quantity * price
                table.add_row([product, quantity, price, total])
            self.textarea.insert(END, "\n" + str(table))
            self.textarea.insert(END, "\n\nTotal Bill:" + str(total_bill))
            self.textarea.insert(END, "\n-----------------------------------------")

            payment_method = simpledialog.askstring("Payment Method", "Choose payment method (Cash/Credit):",
                                                    parent=self.root)
            if payment_method == "Cash":
                while True:
                    cash_method = simpledialog.askstring("Payment Method - Cash", "Please enter the cash amount:",
                                                         parent=self.root)
                    if cash_method is None:
                        break  # Exit the loop if the user cancels
                    cash_method_float = float(cash_method)
                    if cash_method_float >= total_bill:
                        self.textarea.insert(END, "\nPayment Method: Cash")
                        self.textarea.insert(END, "\nCash Amount: " + str(cash_method_float))
                        self.textarea.insert(END, "\nChange: " + str(cash_method_float - total_bill))
                        self.save_bill()
                        self.release_stock()
                        self.add_data_to_orders()
                        self.add_data_to_orders_details()
                        self.add_data_to_customers()
                        self.clear_bill()
                        self.fetch_data()
                        break  # Exit the loop if the payment is sufficient
                    else:
                        messagebox.showerror("Error", "Not enough cash. Please enter a valid amount.", parent=self.root)
            elif payment_method == "Credit":
                credit_window = Toplevel(self.root)
                credit_window.title("Credit Card Payment")
                credit_window.geometry("300x200")
                number_label = Label(credit_window, text="Card Number:")
                number_label.pack()
                number_entry = Entry(credit_window)
                number_entry.pack()
                expiration_label_month = Label(credit_window, text="Expiration Month:")
                expiration_label_month.pack()
                expiration_entry_month = Combobox(credit_window, values=list(range(1, 13)))
                expiration_entry_month.pack()

                expiration_label_year = Label(credit_window, text="Expiration Year:")
                expiration_label_year.pack()
                expiration_entry_year = Combobox(credit_window, values=list(range(datetime.now().year, 2201)))
                expiration_entry_year.pack()
                cvv_label = Label(credit_window, text="CVV:")
                cvv_label.pack()
                cvv_entry = Entry(credit_window)
                cvv_entry.pack()
                confirm_button = Button(credit_window, text="Confirm",
                                        command=lambda: self.process_credit_card_payment(
                                            credit_window,number_entry.get(), expiration_entry_month.get(),expiration_entry_year.get(),cvv_entry.get()))
                confirm_button.pack()
            else:
                messagebox.showerror("Error", "Invalid Payment Method", parent=self.root)

    def release_stock(self):
        conn = mysql.connector.connect(host="localhost",
                                       user="root",
                                       passwd="1234",
                                       database="inventory_management")
        my_cursor = conn.cursor()

        try:
            cart_items = self.cart_frame.get_children()
            list_of_product_ids_in_cart = []  # Initialize an empty list

            # Create a list of product IDs in the cart
            for item in cart_items:
                item_values = self.cart_frame.item(item)['values']
                product_id = item_values[0]
                list_of_product_ids_in_cart.append(product_id)

            for item in cart_items:
                item_values = self.cart_frame.item(item)['values']
                product_id = item_values[0]
                quantity = int(item_values[3])  # Convert quantity to integer

                # Check if the product_id exists in the cart before releasing stock
                if product_id in list_of_product_ids_in_cart:
                    # Get the current quantity of the product
                    query = "SELECT qty FROM products WHERE productID = %s"
                    my_cursor.execute(query, (product_id,))
                    current_qty = int(my_cursor.fetchone()[0])  # Convert current_qty to integer

                    # Calculate the new quantity after releasing stock
                    new_qty = current_qty - quantity

                    if new_qty < 0:
                        messagebox.showerror("Error", f"Not enough stock for product ID {product_id}.", parent=self.root)
                    else:
                        # Update the quantity in the database
                        update_query = "UPDATE products SET qty = %s WHERE productID = %s"
                        my_cursor.execute(update_query, (new_qty, product_id))
                        conn.commit()
                        messagebox.showinfo("Success", f"Stock released for product ID {product_id} successfully.", parent=self.root)
                else:
                    messagebox.showerror("Error", f"Product ID {product_id} is not in the cart.", parent=self.root)
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"An error occurred: {e}", parent=self.root)
        finally:
            conn.close()

    def save_bill(self):
        res = messagebox.askyesno("Confirm","Do you want to save the bill?", parent=self.root)
        if res:
            bill_content = self.textarea.get(1.0,END)
            file = open(f'bills/{self.var_bill_number}.txt', 'w')
            file.write(bill_content)
            file.close()
            messagebox.showinfo("Success", f'{self.var_bill_number} is saved successfully', parent=self.root)

    def clear_bill(self):
        self.textarea.delete("1.0", END)
        self.clear_cart()
        self.var_customer_contact.set("")
        self.var_customer_name.set("")

    def search_bill(self):
        bill_to_search = simpledialog.askstring("Search Bill", "Please Enter Bill Number:", parent=self.root)
        for i in os.listdir('bills/'):
            if i.split('.')[0] == bill_to_search:
                file = open(f'bills/{i}', 'r')  # Corrected line using f-string
                self.textarea.delete(1.0, END)
                for data in file:
                    self.textarea.insert(END, data)
                file.close()
                break
        else:
            messagebox.showerror("Error", "Invalid Bill Number", parent=self.root)

    def print_bill(self):
        if self.textarea.get(1.0,END) == '\n':
            messagebox.showerror("Error", "Bill Is Empty", parent=self.root)
        else:
            file = tempfile.mktemp('.txt')
            open(file, "w").write(self.textarea.get(1.0,END))
            os.startfile(file, 'print')

    def send_gmail2(self):
        try:
            ob = smtplib.SMTP("smtp.gmail.com", 587)
            ob.starttls()
            ob.login(self.sender_Entry.get(), self.password_Entry.get())
            message = self.email_textarea.get(1.0, END)
            ob.sendmail(self.sender_Entry.get(), self.reciever_Entry.get(), message)
            ob.quit()
            messagebox.showinfo("Success", "Bill is successfully sent", parent=self.root)
        except:
            messagebox.showerror("Error", "Somthing went wrong, Please try again", parent=self.root)


    def send_gmail(self):
        if self.textarea.get(1.0, END) == '\n':
            messagebox.showerror("Error", "Bill Is Empty", parent=self.root)
        else:
            send_gmail = Toplevel()
            send_gmail.title("Sent Gmail")
            send_gmail.config(bg="#2f3030")
            send_gmail.resizable(0, 0)
            senderFrame = LabelFrame(send_gmail, text="Sender", font=("Great Vibes", 12, "bold"), bd=6, bg="#2f3030", fg="white")
            senderFrame.grid(row=0, column=0, padx=10, pady=8)
            gmailIdLabel = Label(senderFrame, text="Sender's Gmail",font=("Great Vibes", 12, "bold"), bg="#2f3030", fg="white")
            gmailIdLabel.grid(row=0, column=0, padx=10, pady=8)
            self.sender_Entry = Entry(senderFrame, font=("Great Vibes", 12, "bold"),bd=2, width=20,bg="white")
            self.sender_Entry.grid(row=0,column=1, padx=10, pady=8)

            passwordLabel = Label(senderFrame, text="Password", font=("Great Vibes", 12, "bold"), bg="#2f3030",
                                 fg="white")
            passwordLabel.grid(row=1, column=0, padx=10, pady=8)
            self.password_Entry = Entry(senderFrame, font=("Great Vibes", 12, "bold"), bd=2, width=20, bg="white", show='*')
            self.password_Entry.grid(row=1, column=1, padx=10, pady=8)

            recipient_Frame = LabelFrame(send_gmail, text="Recipient", font=("Great Vibes", 12, "bold"), bd=6,
                                     bg="#2f3030", fg="white")
            recipient_Frame.grid(row=1, column=0, padx=10, pady=8)
            reciever_Label = Label(recipient_Frame, text="Gmail Address", font=("Great Vibes", 12, "bold"), bg="#2f3030",
                                 fg="white")
            reciever_Label.grid(row=0, column=0, padx=10, pady=8)
            self.reciever_Entry = Entry(recipient_Frame, font=("Great Vibes", 12, "bold"), bd=2, width=20, bg="white")
            self.reciever_Entry.grid(row=0, column=1, padx=10, pady=8)

            message_Label = Label(recipient_Frame, text="Message", font=("Great Vibes", 12, "bold"),
                                   bg="#2f3030",
                                   fg="white")
            message_Label.grid(row=1, column=0, padx=10, pady=8)

            self.email_textarea = Text(recipient_Frame, font=("Great Vibes", 12, "bold"),bd=2, relief=SUNKEN, width=40,height=11)
            self.email_textarea.grid(row=2, column=0,columnspan=2)
            self.email_textarea.delete(1.0, END)
            self.email_textarea.insert(END, self.textarea.get(1.0, END))

            send_btn= Button(send_gmail, text="Send", font=("Great Vibes", 12, "bold"),command=self.send_gmail2)
            send_btn.grid(row=3, column=0)

    def add_data_to_orders(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="1234",
                database="inventory_management",
            )
            my_cursor = conn.cursor()

            order_id = self.var_bill_number
            customer_name = str(self.var_customer_name.get())
            total = self.var_total

            my_cursor.execute(
                "INSERT INTO orders (orderId, customer, source, date, status, total) VALUES (%s,%s,%s,%s,%s,%s)",
                (
                    order_id,
                    customer_name,
                    "From The Store",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Close- Store",
                    total,
                ),
            )
            conn.commit()
            self.fetch_data()
            conn.close()
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def add_data_to_orders_details(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="1234",
                database="inventory_management",
            )
            my_cursor = conn.cursor()

            for row in self.cart_frame.get_children():
                product_id = self.cart_frame.item(row, "values")[0]
                product_name = self.cart_frame.item(row, "values")[1]
                qty = float(self.cart_frame.item(row, "values")[3])
                price = float(self.cart_frame.item(row, "values")[2])
                total = float(qty * price)

                # Insert the data into the orders_details table
                my_cursor.execute(
                    "INSERT INTO orders_details (orderId, productId, productName, qty, price, total) VALUES (%s, %s, %s, %s, %s, %s)",
                    (
                        self.var_bill_number,  # You may need to define the order ID
                        product_id,
                        product_name,
                        qty,
                        price,
                        total,
                    ),
                )

            conn.commit()
            self.fetch_data()  # Update the displayed data, if needed
            conn.close()
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def add_data_to_customers(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="1234",
                database="inventory_management",
            )
            my_cursor = conn.cursor()

            order_id = self.var_bill_number
            customer_name = self.var_customer_name.get()
            customer_contact = self.var_customer_contact.get()

            my_cursor.execute(
                "INSERT INTO customers (orderId, name, contact) VALUES (%s,%s,%s)",
                (
                    order_id,
                    customer_name,
                    customer_contact,
                ),
            )
            conn.commit()
            self.fetch_data()
            conn.close()
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = BillingSystem(root)
    root.mainloop()



