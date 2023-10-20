from tkinter import *
from tkinter import ttk, scrolledtext
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

class for_customers:
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
        title_lbl = Label(self.root, text="Customers Software",
                          font=("Great Vibes", 34, "bold"), bg="#008296", fg="white")
        title_lbl.place(x=0, y=-105, width=1500, relx=0.5, rely=0.19, anchor="center")

        main_frame = Frame(self.root, bd=2, bg="white", )
        main_frame.place(x=0, y=70, width=1270, height=600)

        self.var_customer_name = StringVar()
        self.var_customer_contact = StringVar()
        self.var_address = StringVar()
        self.var_email  = StringVar()
        self.var_total = StringVar()

        self.var_product_name = StringVar()
        self.var_product_id = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()

        self.var_num_card = StringVar()
        self.var_expirationM = StringVar()
        self.var_expirationY = StringVar()
        self.var_CVV = StringVar()

        self.var_bill_number = StringVar()

        self.var_Serach = StringVar()

        text_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                font=("Great Vibes", 12, "bold"))
        text_frame.place(x=1900, y=40, width=355, height=400)

        scroolbar = Scrollbar(text_frame, orient=VERTICAL)
        scroolbar.pack(side=RIGHT, fill=Y)

        self.textarea = Text(text_frame, height=20, width=55, yscrollcommand=scroolbar.set)
        self.textarea.pack()
        scroolbar.config(command=self.textarea.yview)

        Left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                font=("Great Vibes", 12, "bold"))
        Left_frame.place(x=0, y=10, width=450, height=550)

        title_all_products = Label(Left_frame, text="All Products",
                          font=("Great Vibes", 20, "bold"), bg="#008296", fg="white")
        title_all_products.place(x=0, y=-120, width=450, relx=0.5, rely=0.25, anchor="center")

        Serach_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE,
                                  text="Serach Product | By Name",
                                  font=("Great Vibes", 12, "bold"))
        Serach_frame.place(x=5, y=40, width=440, height=100)

        proName_label = tk.Label(Serach_frame, text="Product Name:", font=("Great Vibes", 12, "bold"),
                                 bg="white")
        proName_label.grid(row=0, column=0, padx=7, pady=5, sticky=tk.W)

        Serach_entry = ttk.Entry(Serach_frame, width=11, font=("Great Vibes", 12, "bold"))
        Serach_entry.grid(row=0, column=1, pady=7, padx=7, sticky=W)

        self.Serach_entry = Serach_entry
        Serach_btn = Button(Serach_frame, text="Search", font=("Great Vibes", 12, "bold"), width=10,
                            command=self.Serach,
                            bg="#008296",
                            fg="white")
        Serach_btn.grid(row=0, column=2, padx=3)
        showAll_btn = Button(Serach_frame, text="Reset", font=("Great Vibes", 12, "bold"), width=10,
                             command=self.fetch_data,
                             bg="#008296",
                             fg="white")
        showAll_btn.grid(row=1, column=2, padx=3)

        table_products_frame = Frame(Left_frame, bd=2, bg="white", relief=RIDGE)
        table_products_frame.place(x=0, y=150, width=440, height=395)

        scroll_y = ttk.Scrollbar(table_products_frame, orient=VERTICAL)
        self.products_table = ttk.Treeview(table_products_frame, column=(
            "productId", "name", "price",  "image"),  yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.products_table.yview)

        self.products_table.heading("productId", text="Product ID")
        self.products_table.heading("name", text="Name")
        self.products_table.heading("price", text="Price")
        self.products_table.heading("image", text="Image")
        self.products_table["show"] = "headings"

        self.products_table.column("productId",  width=100)
        self.products_table.column("name", width=100)
        self.products_table.column("price", width=100)
        self.products_table.column("image", width=100)
        self.products_table.pack(fill=BOTH, expand=1)
        self.products_table.bind("<ButtonRelease>", self.get_cursor)

        Right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                 font=("Great Vibes", 12, "bold"))
        Right_frame.place(x=450, y=10, width=815, height=570)

        customer_details_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE,
                                 font=("Great Vibes", 12, "bold"))
        customer_details_frame.place(x=450, y=0, width=360, height=500)

        title_customer_details = Label(customer_details_frame, text="Customer Details",
                                   font=("Great Vibes", 20, "bold"), bg="#008296", fg="white")
        title_customer_details.place(x=0, y=-110, width=455, relx=0.5, rely=0.25, anchor="center")

        name_label = tk.Label(customer_details_frame, text="Name:", font=("Great Vibes", 12, "bold"),
                              bg="white")
        name_label.place(x=0, y=50)

        name_entry = ttk.Entry(customer_details_frame, width=15,
                               font=("Great Vibes", 12, "bold"), textvariable=self.var_customer_name)
        name_entry.place(x=150, y=50)

        contact_label = tk.Label(customer_details_frame, text="Contact No:", font=("Great Vibes", 12, "bold"),
                              bg="white")
        contact_label.place(x=0, y=100)

        contact_entry = ttk.Entry(customer_details_frame, width=15,
                               font=("Great Vibes", 12, "bold"),textvariable=self.var_customer_contact)
        contact_entry.place(x=150, y=100)

        email_label = tk.Label(customer_details_frame, text="Email:", font=("Great Vibes", 12, "bold"),
                                 bg="white")
        email_label.place(x=0, y=150)

        email_entry = ttk.Entry(customer_details_frame, width=15,
                                  font=("Great Vibes", 12, "bold"), textvariable=self.var_email)
        email_entry.place(x=150, y=150)


        address_label = tk.Label(customer_details_frame, text="Address:", font=("Great Vibes", 12, "bold"),
                                     bg="white")
        address_label.place(x=0, y=200)

        self.address_text = scrolledtext.ScrolledText(customer_details_frame, wrap='word',
                                                      font=("Great Vibes", 12, "bold"),
                                                      width=40, height=2)
        self.address_text.place(x=0, y=230)

        self.address_text.bind("<KeyRelease>", self.update_address_value)

        self.number_label = Label(customer_details_frame, text="Card Number:", font=("Great Vibes", 12, "bold"),
                                     bg="white")
        self.number_label.place(x=0, y=300)
        self.number_entry = Entry(customer_details_frame, width=15,
                                  font=("Great Vibes", 12, "bold"),textvariable=self.var_num_card)
        self.number_entry.place(x=150, y=300)
        self.expiration_label_month = Label(customer_details_frame, text="Expiration Month:", font=("Great Vibes", 12, "bold"),
                                     bg="white")
        self.expiration_label_month.place(x=0, y=350)
        self.expiration_entry_month = Combobox(customer_details_frame, values=list(range(1, 13)),width=15,
                                  font=("Great Vibes", 12, "bold"),textvariable=self.var_expirationM)
        self.expiration_entry_month.place(x=150, y=350)

        self.expiration_label_year = Label(customer_details_frame, text="Expiration Year:", font=("Great Vibes", 12, "bold"),
                                     bg="white")
        self.expiration_label_year.place(x=0, y=400)
        self.expiration_entry_year = Combobox(customer_details_frame, values=list(range(datetime.now().year, 2201)),width=15,
                                  font=("Great Vibes", 12, "bold"),textvariable=self.var_expirationY)
        self.expiration_entry_year.place(x=150, y=400)
        self.cvv_label = Label(customer_details_frame, text="CVV:", font=("Great Vibes", 12, "bold"),
                                     bg="white")
        self.cvv_label.place(x=0, y=450)
        self.cvv_entry = Entry(customer_details_frame,width=15,
                                  font=("Great Vibes", 12, "bold"),textvariable=self.var_CVV)
        self.cvv_entry.place(x=150, y=450)



        product_details_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE,
                                            font=("Great Vibes", 12, "bold"))
        product_details_frame.place(x=0, y=50, width=450, height=450)

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
                         width=14, bg="#008296", fg="white", command=self.add_to_cart)

        add_btn.place(x=290, y=58)

        clear_btn = Button(product_details_frame, text="Clear Cart", font=("Great Vibes", 12, "bold"),
                         width=14, bg="#008296", fg="white", command=self.clear_cart)

        clear_btn.place(x=130, y=58)

        View_Image_btn = Button(product_details_frame, text="View Image", font=("Great Vibes", 12, "bold"),
                           width=14, bg="#008296", fg="white", command=self.view_image)

        View_Image_btn.place(x=130, y=100)

        View_Details_btn = Button(product_details_frame, text="View Details", font=("Great Vibes", 12, "bold"),command=self.view_details,
                                width=14, bg="#008296", fg="white")

        View_Details_btn.place(x=290, y=100)

        title_cart = Label(Right_frame, text="Cart",
                                       font=("Great Vibes", 20, "bold"), bg="#008296", fg="white")
        title_cart.place(x=-180, y=-125, width=460, relx=0.5, rely=0.25, anchor="center")

        cart_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        cart_frame.place(x=0, y=200, width=450, height=300)

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

        Send_order_btn = Button(main_frame, text="Send order", font=("Great Vibes", 18, "bold"),height=1,
                                  width=57, bg="#008296", fg="white",command=lambda: self.process_credit_card_payment(self.number_entry.get(), self.expiration_entry_month.get(),self.expiration_entry_year.get(),self.cvv_entry.get()))
        Send_order_btn.place(x=455,y=512)

        self.fetch_data()

    def get_cursor2(self,event=""):
        cursor_focus = self.products_table.focus()
        content = self.products_table.item(cursor_focus)
        conn = mysql.connector.connect(host="localhost",
                                       user="root",
                                       passwd="1234",
                                       database="inventory_management")
        my_cursor = conn.cursor()
        select_query = "SELECT * FROM products WHERE productID=%s"
        my_cursor.execute(select_query, ( self.var_product_id,))
        data = my_cursor.fetchone()
        print(data)
        self.var_productID1.set(data[0])
        self.var_barcode1.set(data[1])
        self.var_category1.set(data[2])
        self.var_name1.set(data[3])
        self.var_price1.set(data[4])
        self.var_shelf_life1.set(data[5])
        self.var_weight1.set(data[6])
        self.var_manufacturer1.set(data[7])
        self.var_product_status1.set(data[8])
        if isinstance(data[10], str):
            self.var_description1.set(data[10])
            self.description_text.delete("1.0", "end")
            self.description_text.insert("1.0", data[10])
        else:
            self.var_description1.set(str(data[10]))
            self.description_text.delete("1.0", "end")
            self.description_text.insert("1.0", str(data[10]))

        self.description_text.config(state='disabled')

    def view_details(self):
        self.var_productID1 = StringVar()
        self.var_barcode1 = StringVar()
        self.var_category1 = StringVar()
        self.var_name1 = StringVar()
        self.var_price1 = StringVar()
        self.var_shelf_life1 = StringVar()
        self.var_weight1 = StringVar()
        self.var_manufacturer1 = StringVar()
        self.var_product_status1 = StringVar()
        self.var_qty1 = StringVar()
        self.var_description1 = StringVar()
        selected_item = self.products_table.focus()
        if selected_item:
            credit_window = Toplevel(self.root)
            credit_window.title("Product Details")
            credit_window.geometry("650x350")
            productID_label = tk.Label(credit_window, text="Product ID:", font=("Great Vibes", 12, "bold"),
                                       bg="white")
            productID_label.grid(row=0, column=0, padx=7, pady=5, sticky=tk.W)

            productID_entry = ttk.Entry(credit_window, textvariable=self.var_productID1, width=19,
                                        font=("Great Vibes", 12, "bold"), state='disabled')
            productID_entry.grid(row=0, column=1, padx=7, pady=5, sticky=tk.W)

            barcode_label = tk.Label(credit_window, text="Barcode:", font=("Great Vibes", 12, "bold"),
                                     bg="white")
            barcode_label.grid(row=0, column=2, padx=7, pady=5, sticky=tk.W)

            barcode_entry = ttk.Entry(credit_window, textvariable=self.var_barcode1, width=19,
                                      font=("Great Vibes", 12, "bold"), state='disabled')
            barcode_entry.grid(row=0, column=3, padx=7, pady=5, sticky=tk.W)

            category_label = Label(credit_window, text="Category", font=("Great Vibes", 12, "bold"), bg="white")
            category_label.grid(row=1, column=0, padx=7, sticky=W)
            self.category_combo = ttk.Entry(credit_window, textvariable=self.var_category1,
                                               font=("Great Vibes", 12, "bold"),
                                               width=17, state='disabled')
            self.category_combo.grid(row=1, column=1, padx=8, pady=10, sticky=W)

            name_label = tk.Label(credit_window, text="Name:", font=("Great Vibes", 12, "bold"),
                                  bg="white")
            name_label.grid(row=1, column=2, padx=7, pady=5, sticky=tk.W)

            name_entry = ttk.Entry(credit_window, textvariable=self.var_name1, width=19,
                                   font=("Great Vibes", 12, "bold"), state='disabled')
            name_entry.grid(row=1, column=3, padx=7, pady=5, sticky=tk.W)

            price_label = tk.Label(credit_window, text="Price:", font=("Great Vibes", 12, "bold"),
                                   bg="white")
            price_label.grid(row=2, column=0, padx=7, pady=5, sticky=tk.W)

            price_entry = ttk.Entry(credit_window, textvariable=self.var_price1, width=19,
                                    font=("Great Vibes", 12, "bold"), state='disabled')
            price_entry.grid(row=2, column=1, padx=7, pady=5, sticky=tk.W)

            shelf_life_label = tk.Label(credit_window, text="Shelf Life:", font=("Great Vibes", 12, "bold"),
                                        bg="white")
            shelf_life_label.grid(row=2, column=2, padx=7, pady=5, sticky=tk.W)

            shelf_life_entry = ttk.Entry(credit_window, textvariable=self.var_shelf_life1, width=19,
                                         font=("Great Vibes", 12, "bold"), state='disabled')
            shelf_life_entry.grid(row=2, column=3, padx=7, pady=5, sticky=tk.W)

            weight_label = tk.Label(credit_window, text="Weight:", font=("Great Vibes", 12, "bold"),
                                    bg="white")
            weight_label.grid(row=3, column=0, padx=7, pady=5, sticky=tk.W)

            weight_entry = ttk.Entry(credit_window, textvariable=self.var_weight1, width=19,
                                     font=("Great Vibes", 12, "bold"), state='disabled')
            weight_entry.grid(row=3, column=1, padx=7, pady=5, sticky=tk.W)

            manufacturer_label = tk.Label(credit_window, text="Manufacturer:", font=("Great Vibes", 12, "bold"),
                                          bg="white")
            manufacturer_label.grid(row=3, column=2, padx=7, pady=5, sticky=tk.W)

            manufacturer_entry = ttk.Entry(credit_window, textvariable=self.var_manufacturer1, width=19,
                                           font=("Great Vibes", 12, "bold"), state='disabled')
            manufacturer_entry.grid(row=3, column=3, padx=7, pady=5, sticky=tk.W)

            product_status_label = Label(credit_window, text="Product Status", font=("Great Vibes", 12, "bold"),
                                         bg="white")
            product_status_label.grid(row=4, column=0, padx=7, sticky=W)
            product_status_combo = ttk.Entry(credit_window, textvariable=self.var_product_status1,
                                                font=("Great Vibes", 12, "bold"),
                                                width=17, state='disabled')
            product_status_combo.grid(row=4, column=1, padx=8, pady=10, sticky=W)


            description_label = tk.Label(credit_window, text="Description:", font=("Great Vibes", 12, "bold"),
                                         bg="white")
            description_label.grid(row=5, column=0, padx=7, pady=5, sticky=tk.W)

            self.description_text = scrolledtext.ScrolledText(credit_window, wrap='word',
                                                              font=("Great Vibes", 12, "bold"),
                                                              width=50, height=4)
            self.description_text.grid(row=5, column=1, columnspan=3, padx=8, pady=5, sticky=tk.W)

            self.description_text.bind("<KeyRelease>", self.update_description_value)
            self.get_cursor2()

        else:
            messagebox.showwarning("No Product Selected", "Please select a product to view its image.",
                                   parent=self.root)

    def update_description_value(self, event):
        self.var_description.set(event.widget.get("1.0", tk.END).replace("\n", "\n"))

    def update_address_value(self, event):
        self.var_address.set(event.widget.get("1.0", tk.END).replace("\n", "\n"))

    def view_image(self):
        selected_item = self.products_table.focus()
        if selected_item:
            data = self.products_table.item(selected_item, 'values')
            if data[3]:
                self.show_preview_image(data[0])  # Pass the image data directly
            else:
                messagebox.showinfo("Image Not Found", "No image available for this product.", parent=self.root)
        else:
            messagebox.showwarning("No Product Selected", "Please select a product to view its image.",
                                   parent=self.root)

    def show_preview_image(self, productID):
        try:
            # Get the directory where the script file is located
            script_directory = os.path.dirname(os.path.abspath(__file__))
            # Construct the path to the images folder
            images_directory = os.path.join(script_directory, "productImages")
            # Construct the path to the image file
            image_file_path = os.path.join(images_directory, f"{productID}.jpg")
            print(image_file_path)
            # Check if the image file exists
            if os.path.isfile(image_file_path):
                # Load the image and display it
                img = Image.open(image_file_path)
                img = img.resize((400, 400))  # Resize the image for display
                image_preview = ImageTk.PhotoImage(img)
                # Show the image in a new window
                top = tk.Toplevel(self.root)
                top.title("Image Preview")
                top.geometry("400x400")
                label = tk.Label(top, image=image_preview)
                label.image = image_preview
                label.pack()
            else:
                messagebox.showinfo("Image Not Found", "No image available for this product.", parent=self.root)

        except Exception as e:
            messagebox.showerror("Error", f"Unable to display the image: {str(e)}", parent=self.root)

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
        my_cursor.execute("SELECT productID,name,price,image  FROM products WHERE status = 'Active'")
        data = my_cursor.fetchall()
        if len(data) != 0:
            self.products_table.delete(*self.products_table.get_children())
            for i in data:
                image_data = i[3]
                self.products_table.insert("", END, values=i[:-1] + ("Yes" if image_data else "None",))
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
                    conn = mysql.connector.connect(host="localhost",
                                                   user="root",
                                                   passwd="1234",
                                                   database="inventory_management")
                    my_cursor = conn.cursor()
                    select_query = "SELECT qty FROM products WHERE productID=%s"
                    my_cursor.execute(select_query, (self.var_product_id,))
                    available_qty = my_cursor.fetchone()
                    if available_qty is not None:
                        available_qty = int(available_qty[0])
                        print(available_qty)
                    else:
                        print("No data retrieved from the database")
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
            except Exception as e:
                  messagebox.showerror("Error", f"An error occurred: {e}", parent=self.root)

    def clear_cart(self):
        self.cart_frame.delete(*self.cart_frame.get_children())

    def clear(self):
        self.clear_cart()
        self.var_product_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_customer_name.set("")
        self.var_customer_contact.set("")
        self.var_email.set("")
        self.var_num_card.set("")
        self.var_expirationM.set("")
        self.var_expirationY.set("")
        self.var_CVV.set("")

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

    def process_credit_card_payment(self, card_number, expiration_month, expiration_year, cvv):
        total_bill = self.calculate_total()
        if self.var_customer_name.get() == "" or self.var_customer_contact.get() == "" or self.var_email.get()==""\
                or self.var_address.get() == "" or card_number =="" or expiration_month ==""\
                or expiration_year =="" or cvv=="":
            messagebox.showerror("Error", "Customer Details Are Requires", parent=self.root)
        elif total_bill == 0:
            messagebox.showerror("Error", "No Product Are Selected", parent=self.root)
        if not self.is_valid_card_number(card_number):
            messagebox.showerror("Error", "Invalid card number", parent=self.root)
        elif not self.is_valid_expiration_date(expiration_month, expiration_year):
            messagebox.showerror("Error", "Invalid expiration date", parent=self.root)
        elif not self.is_valid_cvv(cvv):
            messagebox.showerror("Error", "Invalid CVV", parent=self.root)
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
            self.textarea.insert(END, "\nPayment Method: Credit")
            self.textarea.insert(END, "\nCard Number: " + card_number)
            self.textarea.insert(END, "\nExpiration Date: {}/{}".format(expiration_month, expiration_year))
            self.textarea.insert(END, "\nCVV: " + cvv)
            self.save_bill()
            self.send_gmail()
            self.release_stock()
            self.add_data_to_orders()
            self.add_data_to_orders_details()
            self.add_data_to_customers()
            self.clear()
            self.fetch_data()
            messagebox.showinfo("Success", f'{self.var_bill_number} is send successfully', parent=self.root)

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
                else:
                    messagebox.showerror("Error", f"Product ID {product_id} is not in the cart.", parent=self.root)
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"An error occurred: {e}", parent=self.root)
        finally:
            conn.close()

    def save_bill(self):
        bill_content = self.textarea.get(1.0, END)
        file = open(f'bills/{self.var_bill_number}.txt', 'w')
        file.write(bill_content)
        file.close()

    def clear_bill(self):
        self.textarea.delete("1.0", END)
        self.clear_cart()
        self.var_customer_contact.set("")
        self.var_customer_name.set("")

    def send_gmail(self):
        try:
            ob = smtplib.SMTP("smtp.gmail.com", 587)
            ob.starttls()
            ob.login("enter_mail", "enter_password")
            message = self.textarea.get(1.0, END)
            ob.sendmail("meytalpython@gmail.com", self.var_email.get(), message)
            ob.quit()
            messagebox.showinfo("Success", "Bill is successfully sent", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

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
                    "From The Customer Software",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "New",
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
            email = self.var_email.get()

            my_cursor.execute(
                "INSERT INTO customers (orderId, name, contact,address,email) VALUES (%s,%s,%s,%s,%s)",
                (
                    order_id,
                    customer_name,
                    customer_contact,
                    self.address_text.get("1.0", tk.END).strip(),
                    email
                ),
            )
            conn.commit()
            self.fetch_data()
            conn.close()
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = for_customers(root)
    root.mainloop()
