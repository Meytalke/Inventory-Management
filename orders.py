import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
from tkcalendar import Calendar

class orders:
    def __init__(self, root):
        self.root = root
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.title("Orders Page")

        bg_img = Image.open(r"C:\Users\meyta\inventory_management_images\Product_bg4.jpg")
        bg_img = bg_img.resize((screen_width, screen_height), Image.BILINEAR)
        self.bg_img = ImageTk.PhotoImage(bg_img)

        bg_label = Label(self.root, image=self.bg_img)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title label
        title_lbl = Label(self.root, text="Orders",
                          font=("Great Vibes", 34, "bold"), bg="#733634", fg="white")
        title_lbl.place(x=0, y=-105, width=1500, relx=0.5, rely=0.19, anchor="center")

        main_frame = Frame(self.root, bd=2, bg="white", )
        main_frame.place(x=10, y=70, width=1260, height=600)

        self.var_customer_name = StringVar()
        self.var_customer_contact = StringVar()

        self.var_Serach = StringVar()

        Serach_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                  text="Filters",
                                  font=("Great Vibes", 12, "bold"))
        Serach_frame.place(x=0, y=0, width=800, height=120)

        order_id_label = tk.Label(Serach_frame, text="Order ID", font=("Great Vibes", 12, "bold"),
                                 bg="white")
        order_id_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        order_id_entry = ttk.Entry(Serach_frame, width=11, font=("Great Vibes", 12, "bold"))
        order_id_entry.grid(row=1, column=0, pady=7, padx=10, sticky=W)
        self.order_id_serach = order_id_entry

        customer_label = tk.Label(Serach_frame, text="Customer", font=("Great Vibes", 12, "bold"),
                                  bg="white")
        customer_label.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        customer_entry = ttk.Entry(Serach_frame, width=11, font=("Great Vibes", 12, "bold"))
        customer_entry.grid(row=1, column=1, pady=7, padx=10, sticky=W)
        self.customer_serach = customer_entry

        source_label = tk.Label(Serach_frame, text="Source", font=("Great Vibes", 12, "bold"),
                                  bg="white")
        source_label.grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)

        source_entry = ttk.Combobox(Serach_frame, width=11, font=("Great Vibes", 12, "bold"),state="readonly")
        source_entry["values"] = ("Select", "From The Store", "other")
        source_entry.current(0)
        source_entry.grid(row=1, column=2, pady=7, padx=10, sticky=W)
        self.source_serach = source_entry

        status_label = tk.Label(Serach_frame, text="Status", font=("Great Vibes", 12, "bold"),
                                bg="white")
        status_label.grid(row=0, column=4, padx=10, pady=5, sticky=tk.W)

        status_entry = ttk.Combobox(Serach_frame, width=11, font=("Great Vibes", 12, "bold"), state="readonly")
        status_entry["values"] = ("Select", "Close- Store", "New","Picked", "Packed","Staged","Loaded","Shipped","Cancelled")
        status_entry.current(0)
        status_entry.grid(row=1, column=4, pady=7, padx=10, sticky=W)
        self.status_serach = status_entry

        Serach_btn = Button(Serach_frame, text="Search", font=("Great Vibes", 12, "bold"), width=10, command=self.Serach,
                            bg="#733634",
                            fg="white")
        Serach_btn.place(x=550, y=40)
        showAll_btn = Button(Serach_frame, text="Reset", font=("Great Vibes", 12, "bold"), width=10,command=self.fetch_data_orders,
                             bg="#733634",
                             fg="white")
        showAll_btn.place(x=680, y=40)

        orders_frame = Frame(main_frame, bd=2, bg="white", relief=RIDGE)
        orders_frame.place(x=0, y=130, width=800, height=430)

        scroll_y = ttk.Scrollbar(orders_frame, orient=VERTICAL)
        self.orders_frame = ttk.Treeview(orders_frame, column=(
            "orderId","customer", "source", "date",  "status", "total"),  yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.orders_frame.yview)

        self.orders_frame.heading("orderId", text="Order ID")
        self.orders_frame.heading("customer", text="Customer")
        self.orders_frame.heading("source", text="Source")
        self.orders_frame.heading("date", text="Create Date")
        self.orders_frame.heading("status", text="Status")
        self.orders_frame.heading("total", text="Total")
        self.orders_frame["show"] = "headings"

        self.orders_frame.column("orderId",  width=100)
        self.orders_frame.column("customer", width=100)
        self.orders_frame.column("source", width=150)
        self.orders_frame.column("date", width=100)
        self.orders_frame.column("status", width=100)
        self.orders_frame.column("total", width=100)
        self.orders_frame.pack(fill=BOTH, expand=1)
        self.orders_frame.tag_configure('button', background='lightblue')
        self.orders_frame.bind("<ButtonRelease-1>", self.get_cursor)

        order_details_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                  text="Order Details",
                                  font=("Great Vibes", 12, "bold"))
        order_details_frame.place(x=810, y=0, width=445, height=560)

        customer_frame = Frame(order_details_frame, bd=2, bg="white", relief=RIDGE, )
        customer_frame.place(x=0, y=0, width=440, height=125)

        name_label = tk.Label(customer_frame, text="Name:", font=("Great Vibes", 12, "bold"),
                              bg="white")
        name_label.place(x=0, y=0)

        name_entry = ttk.Entry(customer_frame, width=15,
                               font=("Great Vibes", 12, "bold"), textvariable=self.var_customer_name,state='disabled')
        name_entry.place(x=50, y=0)

        contact_label = tk.Label(customer_frame, text="Contact No:", font=("Great Vibes", 12, "bold"),
                                 bg="white")
        contact_label.place(x=200, y=0)

        contact_entry = ttk.Entry(customer_frame, width=15,
                                  font=("Great Vibes", 12, "bold"), textvariable=self.var_customer_contact,state='disabled')
        contact_entry.place(x=300, y=0)

        address_label = tk.Label(customer_frame, text="Address:", font=("Great Vibes", 12, "bold"),
                                 bg="white")
        address_label.place(x=0, y=40)

        text_frame = LabelFrame(customer_frame, bd=2, bg="white", relief=RIDGE,
                                font=("Great Vibes", 12, "bold"))
        text_frame.place(x=0, y=65, width=435, height=50)

        scroolbar = Scrollbar(text_frame, orient=VERTICAL)
        scroolbar.pack(side=RIGHT, fill=Y)

        self.textarea = Text(text_frame, height=10, width=60, yscrollcommand=scroolbar.set, state='disabled')
        self.textarea.pack()
        scroolbar.config(command=self.textarea.yview)

        order_details_table_frame = Frame(order_details_frame, bd=2, bg="white", relief=RIDGE,)
        order_details_table_frame.place(x=0, y=130, width=445, height=300)

        scroll_y = ttk.Scrollbar(order_details_table_frame, orient=VERTICAL)
        self.order_details_frame = ttk.Treeview(order_details_table_frame, column=(
            "productId", "productName", "qty", "price","total"), yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.order_details_frame.yview)

        self.order_details_frame.heading("productId", text="Product ID")
        self.order_details_frame.heading("productName", text="Product Name")
        self.order_details_frame.heading("qty", text="Qty")
        self.order_details_frame.heading("price", text="Price")
        self.order_details_frame.heading("total", text="Total")
        self.order_details_frame["show"] = "headings"

        self.order_details_frame.column("productId", width=70)
        self.order_details_frame.column("productName", width=75)
        self.order_details_frame.column("qty", width=70)
        self.order_details_frame.column("price", width=70)
        self.order_details_frame.column("total", width=70)
        self.order_details_frame.pack(fill=BOTH, expand=1)
        self.order_details_frame.tag_configure('button', background='lightblue')
        self.order_details_frame.bind("<ButtonRelease-1>")

        Pick_btn = Button(order_details_frame, text="Pick Order", font=("Great Vibes", 12, "bold"), width=10,
                            bg="#733634",command=self.pick,
                            fg="white")
        Pick_btn.place(x=10, y=450)

        Pack_btn = Button(order_details_frame, text="Pack Order", font=("Great Vibes", 12, "bold"), width=10,
                          bg="#733634",command=self.pack,
                          fg="white")
        Pack_btn.place(x=150, y=450)

        Stage_btn = Button(order_details_frame, text="Stage Order", font=("Great Vibes", 12, "bold"), width=10,
                          bg="#733634",command=self.stage,
                          fg="white")
        Stage_btn.place(x=290, y=450)

        Load_btn = Button(order_details_frame, text="Load Order", font=("Great Vibes", 12, "bold"), width=10,
                           bg="#733634",command=self.load,
                           fg="white")
        Load_btn.place(x=10, y=490)

        Ship_btn = Button(order_details_frame, text="Ship Order", font=("Great Vibes", 12, "bold"), width=10,
                          bg="#733634",command=self.ship,
                          fg="white")
        Ship_btn.place(x=150, y=490)

        Cancel_btn = Button(order_details_frame, text="Cancel Order", font=("Great Vibes", 12, "bold"), width=10,
                          bg="#733634",command=self.cancel,
                          fg="white")
        Cancel_btn.place(x=290, y=490)


        self.fetch_data_orders()

    def send_gmail(self, status, order_id):
        try:
            ob = smtplib.SMTP("smtp.gmail.com", 587)
            ob.starttls()
            ob.login("enter_mail", "enter_password")
            conn = mysql.connector.connect(host="localhost",
                                           user="root",
                                           passwd="1234",
                                           database="inventory_management")
            my_cursor = conn.cursor()
            select_query = "SELECT email FROM customers WHERE orderId = %s"
            my_cursor.execute(select_query, (order_id,))
            customer_email = my_cursor.fetchone()[0]
            subject = "Order Status Update"
            body = f"Hello,\nYour Order (Order ID: {order_id}) has been changed to status: {status}"
            message = MIMEMultipart()
            message["From"] = "meytalpython@gmail.com"
            message["To"] = customer_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))
            ob.sendmail("meytalpython@gmail.com", customer_email, message.as_string())
            ob.quit()
            messagebox.showinfo("Success", "Gmail is successfully sent", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def pick(self):
        selected_item = self.orders_frame.selection()
        print(selected_item)
        if selected_item:
            item_values = self.orders_frame.item(selected_item, "values")
            order_id = item_values[0]
            print(order_id)
            status = item_values[4]
            print(status)
            if status == "New":
                conn = mysql.connector.connect(host="localhost",
                                               user="root",
                                               passwd="1234",
                                               database="inventory_management")
                my_cursor = conn.cursor()
                update_query = "UPDATE orders SET status = 'Picked' WHERE orderId = %s"
                my_cursor.execute(update_query, (order_id,))
                conn.commit()
                conn.close()
                self.send_gmail("Picked", order_id)
                self.fetch_data_orders()
            else:
                messagebox.showerror("Error", "Please Choose Order In New Status Only", parent=self.root)
        else:
            messagebox.showerror("Error", "Please Choose Order In New Status Only", parent=self.root)

    def pack(self):
        selected_item = self.orders_frame.selection()
        print(selected_item)
        if selected_item:
            item_values = self.orders_frame.item(selected_item, "values")
            order_id = item_values[0]
            print(order_id)
            status = item_values[4]
            print(status)
            if status == "Picked":
                conn = mysql.connector.connect(host="localhost",
                                               user="root",
                                               passwd="1234",
                                               database="inventory_management")
                my_cursor = conn.cursor()
                update_query = "UPDATE orders SET status = 'Packed' WHERE orderId = %s"
                my_cursor.execute(update_query, (order_id,))
                conn.commit()
                conn.close()
                self.send_gmail("Packed", order_id)
                self.fetch_data_orders()
            else:
                messagebox.showerror("Error", "Please Choose Order In Picked Status Only", parent=self.root)
        else:
            messagebox.showerror("Error", "Please Choose Order In Picked Status Only", parent=self.root)

    def stage(self):
        selected_item = self.orders_frame.selection()
        print(selected_item)
        if selected_item:
            item_values = self.orders_frame.item(selected_item, "values")
            order_id = item_values[0]
            print(order_id)
            status = item_values[4]
            print(status)
            if status == "Packed":
                conn = mysql.connector.connect(host="localhost",
                                               user="root",
                                               passwd="1234",
                                               database="inventory_management")
                my_cursor = conn.cursor()
                update_query = "UPDATE orders SET status = 'Staged' WHERE orderId = %s"
                my_cursor.execute(update_query, (order_id,))
                conn.commit()
                conn.close()
                self.send_gmail("Staged", order_id)
                self.fetch_data_orders()
            else:
                messagebox.showerror("Error", "Please Choose Order In Packed Status Only", parent=self.root)
        else:
            messagebox.showerror("Error", "Please Choose Order In Packed Status Only", parent=self.root)

    def load(self):
        selected_item = self.orders_frame.selection()
        print(selected_item)
        if selected_item:
            item_values = self.orders_frame.item(selected_item, "values")
            order_id = item_values[0]
            print(order_id)
            status = item_values[4]
            print(status)
            if status == "Staged":
                conn = mysql.connector.connect(host="localhost",
                                               user="root",
                                               passwd="1234",
                                               database="inventory_management")
                my_cursor = conn.cursor()
                update_query = "UPDATE orders SET status = 'Loaded' WHERE orderId = %s"
                my_cursor.execute(update_query, (order_id,))
                conn.commit()
                conn.close()
                self.send_gmail("Loaded", order_id)
                self.fetch_data_orders()
            else:
                messagebox.showerror("Error", "Please Choose Order In Staged Status Only", parent=self.root)
        else:
            messagebox.showerror("Error", "Please Choose Order In Staged Status Only", parent=self.root)

    def ship(self):
        selected_item = self.orders_frame.selection()
        print(selected_item)
        if selected_item:
            item_values = self.orders_frame.item(selected_item, "values")
            order_id = item_values[0]
            print(order_id)
            status = item_values[4]
            print(status)
            if status == "Loaded":
                conn = mysql.connector.connect(host="localhost",
                                               user="root",
                                               passwd="1234",
                                               database="inventory_management")
                my_cursor = conn.cursor()
                update_query = "UPDATE orders SET status = 'Shipped' WHERE orderId = %s"
                my_cursor.execute(update_query, (order_id,))
                conn.commit()
                conn.close()
                self.send_gmail("Shipped", order_id)
                self.fetch_data_orders()
            else:
                messagebox.showerror("Error", "Please Choose Order In Loaded Status Only", parent=self.root)
        else:
            messagebox.showerror("Error", "Please Choose Order In Loaded Status Only", parent=self.root)

    def cancel(self):
        selected_item = self.orders_frame.selection()
        print(selected_item)
        if selected_item:
            item_values = self.orders_frame.item(selected_item, "values")
            order_id = item_values[0]
            print(order_id)
            status = item_values[4]
            print(status)
            if status == "New" or status == "Picked" or status == "Packed":
                conn = mysql.connector.connect(host="localhost",
                                               user="root",
                                               passwd="1234",
                                               database="inventory_management")
                my_cursor = conn.cursor()
                update_query = "UPDATE orders SET status = 'Cancelled' WHERE orderId = %s"
                my_cursor.execute(update_query, (order_id,))
                conn.commit()
                conn.close()
                self.send_gmail("Cancelled", order_id)
                self.return_stock_after_cancel()
                self.fetch_data_orders()
            else:
                messagebox.showerror("Error", "Unable to cancel after packed status", parent=self.root)
        else:
            messagebox.showerror("Error", "Please Choose Order In Loaded Status Only", parent=self.root)

    def return_stock_after_cancel(self):
        # Assuming you have already created and populated self.order_details_frame

        conn = mysql.connector.connect(host="localhost",
                                       user="root",
                                       passwd="1234",
                                       database="inventory_management")
        my_cursor = conn.cursor()

        try:
            cart_items = self.order_details_frame.get_children()
            cart_quantities = {}  # Initialize a dictionary to keep track of quantities in the cart

            # Create a list of product IDs in the cart
            for item in cart_items:
                item_values = self.order_details_frame.item(item)['values']
                product_id = item_values[0]
                quantity = int(item_values[2])  # Convert quantity to integer

                # Store the quantity in the cart_quantities dictionary
                cart_quantities[product_id] = quantity

            for product_id, quantity in cart_quantities.items():
                # Get the current quantity of the product
                query = "SELECT qty FROM products WHERE productID = %s"
                my_cursor.execute(query, (product_id,))
                current_qty = int(my_cursor.fetchone()[0])

                new_qty = current_qty + quantity
                print(current_qty)
                print(quantity)
                print(new_qty)
                if new_qty < 0:
                    messagebox.showerror("Error", f"Not enough stock for product ID {product_id}.", parent=self.root)
                else:
                    # Update the quantity in the database
                    update_query = "UPDATE products SET qty = %s WHERE productID = %s"
                    my_cursor.execute(update_query, (new_qty, product_id))
                    print(f"Product ID {product_id}: New quantity = {new_qty}")
                    conn.commit()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"An error occurred: {e}", parent=self.root)
        finally:
            conn.close()


    def open_calendar_popup(self, event=None):
        self.calendar_window = Toplevel(self.root)
        self.calendar_window.title("Choose a Date")

        self.date_calendar = Calendar(self.calendar_window, selectmode="day", date_pattern="dd/MM/yyyy", showweeknumbers=False)
        self.date_calendar.pack()

        select_button = Button(self.calendar_window, text="Select Date", command=self.select_date)
        select_button.pack()

    def select_date(self):
        selected_date = self.date_calendar.get_date()
        self.calendar_window.destroy()
        self.date_entry.delete(0, END)
        self.date_entry.insert(0, selected_date)

    def fetch_data_orders(self):
        conn = mysql.connector.connect(host="localhost",
                                       user="root",
                                       passwd="1234",
                                       database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM orders")
        data = my_cursor.fetchall()
        if len(data) != 0:
            self.orders_frame.delete(*self.orders_frame.get_children())
            for i in data:
                # Add a button column to each row and insert the data along with the "View" button
                self.orders_frame.insert("", END, values=i)
            conn.commit()
        conn.close()

    def get_cursor(self, event=""):
        selected_item = self.orders_frame.selection()
        if selected_item:
            item_values = self.orders_frame.item(selected_item, "values")
            order_id = item_values[0]  # Get the selected order ID

            # Update customer details from the customers table
            conn = mysql.connector.connect(host="localhost", user="root", passwd="1234",
                                           database="inventory_management")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT name, contact, address FROM customers WHERE orderId = %s", (order_id,))
            customer_data = my_cursor.fetchone()
            conn.close()

            if customer_data:
                customer_name, customer_contact, customer_address = customer_data

                # Clear the Text widget before inserting the new data
                self.textarea.config(state="normal")
                self.textarea.delete("1.0", "end")

                self.var_customer_name.set(customer_name)
                self.var_customer_contact.set(customer_contact)
                if customer_address:
                    self.textarea.insert("1.0", customer_address)


                # Disable the Text widget again
                self.textarea.config(state="disabled")

            # Fetch and display order details based on the selected order ID
            conn = mysql.connector.connect(host="localhost", user="root", passwd="1234",
                                           database="inventory_management")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT productId, productName, qty, price, total FROM orders_details WHERE orderId = %s",
                              (order_id,))
            order_details_data = my_cursor.fetchall()
            conn.close()

            if order_details_data:
                self.order_details_frame.delete(*self.order_details_frame.get_children())
                for i in order_details_data:
                    self.order_details_frame.insert("", "end", values=i)

    def Serach(self):
        selected_order_id = self.order_id_serach.get()
        selected_customer = self.customer_serach.get()
        selected_source = self.source_serach.get()
        #selected_date = self.date_serach.get()
        selected_status = self.status_serach.get()

        query = "SELECT * FROM orders WHERE 1=1"

        if selected_order_id:
            query += f" AND orderId = '{selected_order_id}'"
        if selected_customer:
            query += f" AND customer = '{selected_customer}'"
        if selected_source != "Select":
            query += f" AND source = '{selected_source}'"
        #if selected_date:
        #    query += f" AND date = '{selected_date}'"
        if selected_status != "Select":
            query += f" AND status = '{selected_status}'"

        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute(query)
        data = my_cursor.fetchall()

        if len(data) != 0:
            self.orders_frame.delete(*self.orders_frame.get_children())
            for i in data:
                self.orders_frame.insert("", END, values=i)
            conn.commit()
        else:
            messagebox.showinfo("No Results", "No matching records found.", parent=self.root)

        conn.close()


if __name__ == "__main__":
    root = Tk()
    obj = orders(root)
    root.mainloop()



