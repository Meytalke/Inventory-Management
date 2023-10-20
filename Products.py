from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
from tkinter import scrolledtext
from datetime import datetime
import shutil
import os
from tkinter import filedialog
import pandas as pd

class Product:
    def __init__(self, root):
        self.root = root
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.title("Face Recognition System")

        bg_img = Image.open(r"C:\Users\meyta\inventory_management_images\Product_bg4.jpg")
        bg_img = bg_img.resize((screen_width, screen_height), Image.BILINEAR)
        self.bg_img = ImageTk.PhotoImage(bg_img)

        bg_label = Label(self.root, image=self.bg_img)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title label
        title_lbl = Label(self.root, text="Product Management",
                          font=("Great Vibes", 34, "bold"), bg="white", fg="#2a574a")
        title_lbl.place(x=0, y=2, width=1500, relx=0.5, rely=0.19, anchor="center")

        main_frame = Frame(self.root, bd=2, bg="white", )
        main_frame.place(x=10, y=170, width=1260, height=470)

        # Second image
        img1 = Image.open(r"C:\Users\meyta\inventory_management_images\product_bg2.jpg")
        new_width1 = int(img1.width * 0.35)
        new_height1 = int(img1.height * 0.12)
        img1 = img1.resize((new_width1, new_height1), Image.BILINEAR)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl1 = Label(self.root, image=self.photoimg1)
        f_lbl1.place(x=0, y=0, width=new_width1, height=new_height1)

        # Third image
        img2 = Image.open(r"C:\Users\meyta\inventory_management_images\products_bg3.png")
        new_width2 = int(img2.width * 0.65)
        new_height2 = int(img2.height * 0.202)
        img2 = img2.resize((new_width2, new_height2), Image.BILINEAR)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl2 = Label(self.root, image=self.photoimg2)
        f_lbl2.place(x=(new_width1), y=0, width=new_width2, height=new_height2)

        self.var_productID = StringVar()
        self.var_barcode = StringVar()
        self.var_category = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_shelf_life = StringVar()
        self.var_weight = StringVar()
        self.var_manufacturer = StringVar()
        self.var_product_status = StringVar()
        self.var_qty = StringVar()
        self.var_description = StringVar()
        self.var_creationDate = StringVar()
        self.file_path = ""
        self.var_Serach1 = StringVar()
        self.var_Serach2 = StringVar()

        next_product_id = self.get_next_product_id()
        self.var_productID.set(next_product_id)

        # left label frame
        Left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Product Details",
                                font=("Great Vibes", 12, "bold"))
        Left_frame.place(x=10, y=10, width=625, height=455)


        product_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE,
                                   font=("Great Vibes", 12, "bold"))
        product_frame.place(x=0, y=0, width=620, height=320)

        productID_label = tk.Label(product_frame, text="Product ID:", font=("Great Vibes", 12, "bold"),
                                    bg="white")
        productID_label.grid(row=0, column=0, padx=7, pady=5, sticky=tk.W)

        productID_entry = ttk.Entry(product_frame, textvariable=self.var_productID, width=14,
                                    font=("Great Vibes", 12, "bold"), state='disabled')
        productID_entry.grid(row=0, column=1, padx=7, pady=5, sticky=tk.W)

        barcode_label = tk.Label(product_frame, text="Barcode:", font=("Great Vibes", 12, "bold"),
                                   bg="white")
        barcode_label.grid(row=0, column=2, padx=7, pady=5, sticky=tk.W)

        barcode_entry = ttk.Entry(product_frame, textvariable=self.var_barcode, width=14,
                                    font=("Great Vibes", 12, "bold"))
        barcode_entry.grid(row=0, column=3, padx=7, pady=5, sticky=tk.W)


        category_label = Label(product_frame, text="Category", font=("Great Vibes", 12, "bold"), bg="white")
        category_label.grid(row=1, column=0, padx=7, sticky=W)
        self.category_combo = ttk.Combobox(product_frame, textvariable=self.var_category,
                                           font=("Great Vibes", 12, "bold"),
                                           width=14, state="readonly")
        self.update_category_values()  # Call using self
        self.category_combo.grid(row=1, column=1, padx=8, pady=10, sticky=W)

        name_label = tk.Label(product_frame, text="Name:", font=("Great Vibes", 12, "bold"),
                                   bg="white")
        name_label.grid(row=1, column=2, padx=7, pady=5, sticky=tk.W)

        name_entry = ttk.Entry(product_frame, textvariable=self.var_name, width=14,
                                    font=("Great Vibes", 12, "bold"))
        name_entry.grid(row=1, column=3, padx=7, pady=5, sticky=tk.W)

        price_label = tk.Label(product_frame, text="Price:", font=("Great Vibes", 12, "bold"),
                              bg="white")
        price_label.grid(row=2, column=0, padx=7, pady=5, sticky=tk.W)

        price_entry = ttk.Entry(product_frame, textvariable=self.var_price, width=14,
                               font=("Great Vibes", 12, "bold"))
        price_entry.grid(row=2, column=1, padx=7, pady=5, sticky=tk.W)

        shelf_life_label = tk.Label(product_frame, text="Shelf Life:", font=("Great Vibes", 12, "bold"),
                               bg="white")
        shelf_life_label.grid(row=2, column=2, padx=7, pady=5, sticky=tk.W)

        shelf_life_entry = ttk.Entry(product_frame, textvariable=self.var_shelf_life, width=14,
                                font=("Great Vibes", 12, "bold"))
        shelf_life_entry.grid(row=2, column=3, padx=7, pady=5, sticky=tk.W)

        weight_label = tk.Label(product_frame, text="Weight:", font=("Great Vibes", 12, "bold"),
                                      bg="white")
        weight_label.grid(row=3, column=0, padx=7, pady=5, sticky=tk.W)

        weight_entry = ttk.Entry(product_frame, textvariable=self.var_weight, width=14,
                                       font=("Great Vibes", 12, "bold"))
        weight_entry.grid(row=3, column=1, padx=7, pady=5, sticky=tk.W)

        manufacturer_label = tk.Label(product_frame, text="Manufacturer:", font=("Great Vibes", 12, "bold"),
                                    bg="white")
        manufacturer_label.grid(row=3, column=2, padx=7, pady=5, sticky=tk.W)

        manufacturer_entry = ttk.Entry(product_frame, textvariable=self.var_manufacturer, width=14,
                                     font=("Great Vibes", 12, "bold"))
        manufacturer_entry.grid(row=3, column=3, padx=7, pady=5, sticky=tk.W)

        product_status_label = Label(product_frame, text="Product Status", font=("Great Vibes", 12, "bold"), bg="white")
        product_status_label.grid(row=4, column=0, padx=7, sticky=W)
        product_status_combo = ttk.Combobox(product_frame, textvariable=self.var_product_status, font=("Great Vibes", 12, "bold"),
                                 width=14, state="readonly")
        product_status_combo["values"] = ("Select Status", "Active", "Discontinued", "Out Of Stock")
        product_status_combo.current(0)
        product_status_combo.grid(row=4, column=1, padx=8, pady=10, sticky=W)

        qty_label = tk.Label(product_frame, text="Stock Quantity:", font=("Great Vibes", 12, "bold"),
                                      bg="white")
        qty_label.grid(row=4, column=2, padx=7, pady=5, sticky=tk.W)

        qty_entry = ttk.Entry(product_frame, textvariable=self.var_qty, width=14,
                                       font=("Great Vibes", 12, "bold"))
        qty_entry.grid(row=4, column=3, padx=7, pady=5, sticky=tk.W)


        description_label = tk.Label(product_frame, text="Description:", font=("Great Vibes", 12, "bold"),
                                     bg="white")
        description_label.grid(row=5, column=0, padx=7, pady=5, sticky=tk.W)

        self.description_text = scrolledtext.ScrolledText(product_frame, wrap='word', font=("Great Vibes", 12, "bold"),
                                                          width=45, height=4)
        self.description_text.grid(row=5, column=1, columnspan=3, padx=8, pady=5, sticky=tk.W)

        self.description_text.bind("<KeyRelease>", self.update_description_value)



        # Add a label to display the selected image
        # Add a button to choose image

        btn_frame = Frame(Left_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=0, y=350, width=620, height=70)
        choose_image_btn = Button(btn_frame, bg="#2a574a", fg="white", text="Choose Image",width=15, font=("Great Vibes", 12, "bold"),
                                  command=lambda: self.choose_image(image_label))
        choose_image_btn.grid(row=0, column=0)

        view_image_btn = Button(btn_frame, bg="#2a574a", fg="white", text="View Image", font=("Great Vibes", 12, "bold"),width=15, command=self.view_image)
        view_image_btn.grid(row=0, column=1)
        image_label = Label(product_frame, bg="white")
        save_btn = Button(btn_frame, text="Save", font=("Great Vibes", 12, "bold"),
                          width=15, command=lambda: self.add_data(), bg="#2a574a", fg="white")
        save_btn.grid(row=0, column=2)
        update_btn = Button(btn_frame, text="Update", font=("Great Vibes", 12, "bold"), command=self.update_data,
                            width=15, bg="#2a574a", fg="white")
        update_btn.grid(row=0, column=3)
        delete_btn = Button(btn_frame, text="Delete", font=("Great Vibes", 12, "bold"),command=self.delete_data,
                            width=15, bg="#2a574a", fg="white")
        delete_btn.grid(row=1, column=0)
        reset_btn = Button(btn_frame, text="Reset", font=("Great Vibes", 12, "bold"),command=self.reset_data,
                           width=15, bg="#2a574a", fg="white")
        reset_btn.grid(row=1, column=1)
        restore_btn = Button(btn_frame, text="Restore", font=("Great Vibes", 12, "bold"), command=self.restore_data,
                             width=15, bg="#2a574a", fg="white")
        restore_btn.grid(row=1, column=2)
        Right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Products",
                                 font=("Great Vibes", 12, "bold"))
        Right_frame.place(x=640, y=10, width=615, height=455)
        Serach_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE,
                                  text="Filters",
                                  font=("Great Vibes", 12, "bold"))
        Serach_frame.place(x=5, y=0, width=605, height=120)
        Serach_label = Label(Serach_frame, text="Serach By:", font=("Great Vibes", 12, "bold"),
                             bg="#2a574a", fg="white")
        Serach_label.grid(row=0, column=0, padx=5, pady=7, sticky=W)
        Serach_combo = ttk.Combobox(Serach_frame, font=("Great Vibes", 12, "bold"), width=10, state="readonly", textvariable=self.var_Serach1)
        Serach_combo["values"] = ("Select", "Product ID", "Barcode", "Category", "Name", "Product Status")
        Serach_combo.current(0)
        Serach_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        Serach2_label = Label(Serach_frame, text="Serach By:", font=("Great Vibes", 12, "bold"),
                             bg="#2a574a", fg="white")
        Serach2_label.grid(row=1, column=0, padx=5, pady=7, sticky=W)
        Serach2_combo = ttk.Combobox(Serach_frame, font=("Great Vibes", 12, "bold"), width=10, state="readonly", textvariable=self.var_Serach2)
        Serach2_combo["values"] = ("Select", "Product ID", "Barcode", "Category", "Name", "Product Status")
        Serach2_combo.current(0)
        Serach2_combo.grid(row=1, column=1, padx=2, pady=10, sticky=W)
        Serach_entry = ttk.Entry(Serach_frame, width=15, font=("Great Vibes", 12, "bold"))
        Serach_entry.grid(row=0, column=2, pady=7, padx=5, sticky=W)
        self.Serach_entry = Serach_entry
        Serach2_entry = ttk.Entry(Serach_frame, width=15, font=("Great Vibes", 12, "bold"))
        Serach2_entry.grid(row=1, column=2, pady=7, padx=5, sticky=W)
        self.Serach_entry2 = Serach2_entry
        Serach_btn = Button(Serach_frame, text="Search", font=("Great Vibes", 12, "bold"), width=10, bg="#2a574a", command=self.Search,
                            fg="white")
        Serach_btn.grid(row=0, column=3, padx=3)
        showAll_btn = Button(Serach_frame, text="Reset", font=("Great Vibes", 12, "bold"), width=10, bg="#2a574a",
                             fg="white",command=self.fetch_data)
        showAll_btn.grid(row=0, column=4, padx=3)
        Export_btn = Button(Serach_frame, text="Export", font=("Great Vibes", 12, "bold"), width=10,
                             bg="#2a574a",
                             fg="white", command=self.export_to_excel)
        Export_btn.grid(row=1, column=3, padx=3)
        # ===========Table frame===============
        table_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=5, y=130, width=605, height=300)
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        self.products_table = ttk.Treeview(table_frame, column=(
        "productId", "barcode", "category", "name", "price", "shelfLife", "weight", "manufacturer", "status", "qty", "description", "creationDate", "image"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.products_table.xview)
        scroll_y.config(command=self.products_table.yview)

        self.products_table.heading("productId", text="Product ID")
        self.products_table.heading("barcode", text="Barcode")
        self.products_table.heading("category", text="Category")
        self.products_table.heading("name", text="Name")
        self.products_table.heading("price", text="Price")
        self.products_table.heading("shelfLife", text="Shelf Life")
        self.products_table.heading("weight", text="Weight")
        self.products_table.heading("manufacturer", text="Manufacturer")
        self.products_table.heading("status", text="Product Status")
        self.products_table.heading("qty", text="Quantity")
        self.products_table.heading("description", text="Description")
        self.products_table.heading("creationDate", text="Creation Date")
        self.products_table.heading("image", text="Image")
        self.products_table["show"] = "headings"

        self.products_table.column("productId", width=100)
        self.products_table.column("barcode", width=100)
        self.products_table.column("category", width=100)
        self.products_table.column("name", width=100)
        self.products_table.column("price", width=100)
        self.products_table.column("name", width=100)
        self.products_table.column("shelfLife", width=100)
        self.products_table.column("weight", width=100)
        self.products_table.column("manufacturer", width=100)
        self.products_table.column("status", width=100)
        self.products_table.column("qty", width=100)
        self.products_table.column("description", width=100)
        self.products_table.column("creationDate", width=100)
        self.products_table.column("image", width=100)
        self.products_table.pack(fill=BOTH, expand=1)
        self.products_table.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()
        for iid in self.products_table.get_children():
            self.insert_view_image_button(values=iid)
        self.products_table.tag_bind('button', '<Button-1>')
        self.products_table.tag_configure('button', background='lightblue')
        self.reset_data()
        self.fetch_data()

    def export_to_excel(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], parent=self.root)
        if file_path:
            data = []
            for item in self.products_table.get_children():
                data.append(self.products_table.item(item, "values"))

            # Define the columns for the Excel file
            columns = ["Product ID", "Barcode", "Category", "Name", "Price", "Shelf Life", "Weight",
                       "Manufacturer", "Product Status", "Quantity", "Description", "Creation Date", "Image"]

            # Create a DataFrame using pandas
            df = pd.DataFrame(data, columns=columns)

            # Save the DataFrame to an Excel file
            excel_path = file_path  # Use the selected file path
            df.to_excel(excel_path, index=False)
            messagebox.showinfo("Export", "Data exported to Excel successfully.", parent=self.root)

    def view_image(self):
        selected_item = self.products_table.focus()
        if selected_item:
            data = self.products_table.item(selected_item, 'values')
            if data[12]:
                self.show_preview_image(data[0])  # Pass the image data directly
            else:
                messagebox.showinfo("Image Not Found", "No image available for this product.", parent=self.root)
        else:
            messagebox.showwarning("No Product Selected", "Please select a product to view its image.",
                                   parent=self.root)
    def show_preview_image(self,productID):
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
    def insert_view_image_button(self, values):
        self.products_table.insert("", "end", values=values, tags=('button',))
    def choose_image(self, image_label):
        file_path = filedialog.askopenfilename(title="Select Image",
                                               filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")], parent=self.root)
        if file_path:
            # Load the selected image using PIL and display it
            img = Image.open(file_path)
            img = img.resize((300, 300))  # Resize the image for display
            img = ImageTk.PhotoImage(img)
            image_label.config(image=img)
            image_label.image = img  # Keep a reference to the image to prevent garbage collection

            # Set self.file_path to the selected image file path
            self.file_path = file_path
            messagebox.showinfo(
                "Success", "Image has been added Successfully. Please click update", parent=self.root)

    def get_next_product_id(self):
        try:
            conn = mysql.connector.connect(host="localhost",
                                           user="root",
                                           passwd="1234",
                                           database="inventory_management")
            if conn.is_connected():
                cursor = conn.cursor()
                # Get the maximum productID from both tables
                cursor.execute('SELECT MAX(productID) FROM products')
                max_id_products = cursor.fetchone()[0]
                cursor.execute('SELECT MAX(productID) FROM deleted_products')
                max_id_deleted = cursor.fetchone()[0]
                # Compare and return the maximum ID
                max_id = max(max_id_products, max_id_deleted)
                cursor.close()
                conn.close()
                if max_id is not None:
                    return max_id + 1
                else:
                    return 1
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Due To: {str(e)}", parent=self.root)
        return None

    def update_category_values(self):
        try:
            conn = mysql.connector.connect(host="localhost",
                                           user="root",
                                           passwd="1234",
                                           database="inventory_management")
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM categories WHERE active='Yes'")
                categories = cursor.fetchall()
                cursor.close()
                conn.close()
                # Update the Combobox values with the fetched categories
                category_names = [category[0] for category in categories]
                category_names.insert(0, "Select Category")  # Add an initial default value
                self.category_combo["values"] = category_names
                self.category_combo.current(0)  # Select the default value
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Due To: {str(e)}", parent=self.root)

    def update_description_value(self, event):
        self.var_description.set(event.widget.get("1.0", tk.END).replace("\n", "\n"))

    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM products")
        data = my_cursor.fetchall()
        if len(data) != 0:
            self.products_table.delete(*self.products_table.get_children())
            for i in data:
                image_data = i[12]
                self.products_table.insert("", END, values=i[:-1] + ("Yes" if image_data else "None",))
        conn.commit()
        conn.close()

    # ============== get cursor====================
    def get_cursor(self,event=""):
        cursor_focus = self.products_table.focus()
        content = self.products_table.item(cursor_focus)
        data = content["values"]
        self.var_productID.set(data[0])
        self.var_barcode.set(data[1])
        self.var_category.set(data[2])
        self.var_name.set(data[3])
        self.var_price.set(data[4])
        self.var_shelf_life.set(data[5])
        self.var_weight.set(data[6])
        self.var_manufacturer.set(data[7])
        self.var_product_status.set(data[8])
        self.var_qty.set(data[9])
        if isinstance(data[10], str):
            self.var_description.set(data[10])
            self.description_text.delete("1.0", "end")
            self.description_text.insert("1.0", data[10])
        else:
            self.var_description.set(str(data[10]))
            self.description_text.delete("1.0", "end")
            self.description_text.insert("1.0", str(data[10]))
        self.var_creationDate.set(data[11])
        self.file_path = data[12]

    def add_data2(self, data):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="1234",
                database="inventory_management",
            )
            my_cursor = conn.cursor()

            my_cursor.execute(
                "INSERT INTO products VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                data,
            )
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo(
                "Success", "Product has been added Successfully", parent=self.root
            )
            self.reset_data()
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def add_data(self):
        if (
                self.var_name.get()
                and self.var_barcode.get()
                and self.var_category.get() != "Select Category"
                and self.var_price.get()
                and self.var_product_status.get() != "Select Status"
        ):
            try:
                description = self.description_text.get("1.0", tk.END).strip()
                image_file_path = self.file_path

                if image_file_path:
                    # Generate a unique file name for the image
                    unique_file_name = f"{self.var_productID.get()}.jpg"
                    destination_path = f"productImages/{unique_file_name}"  # Folder named "images" to store the images

                    # Move the image to the destination folder
                    shutil.copy(image_file_path, destination_path)
                else:
                    # If no image is selected, set the destination_path to None
                    destination_path = None

                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="1234",
                    database="inventory_management",
                )
                my_cursor = conn.cursor()
                my_cursor.execute(
                    "INSERT INTO products VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (
                        self.var_productID.get(),
                        self.var_barcode.get(),
                        self.var_category.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_shelf_life.get(),
                        self.var_weight.get(),
                        self.var_manufacturer.get(),
                        self.var_product_status.get(),
                        self.var_qty.get(),
                        description,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        destination_path,  # Store the file path of the image or None
                    ),
                )
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo(
                    "Success", "Product has been added Successfully", parent=self.root
                )
                self.reset_data()
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
        else:
            messagebox.showerror("Error", "All the fields are required", parent=self.root)

    def update_data(self):
        if self.var_name.get() != "" and self.var_barcode.get() != "" and self.var_category.get() != "Select Category" \
                and self.var_price.get() != "" and self.var_product_status.get() != "Select Status":
            try:
                description = self.description_text.get("1.0", tk.END).strip()
                unique_file_name = f"{self.var_productID.get()}.jpg"
                destination_path = f"productImages/{unique_file_name}"
                Update = messagebox.askyesno("Update", "Do you want to update this Product's details",
                                             parent=self.root)
                if Update:
                    conn = mysql.connector.connect(host="localhost", user="root", passwd="1234",
                                                   database="inventory_management")
                    my_cursor = conn.cursor()
                    update_query = (
                        "INSERT INTO products (productID, barcode, category, name, price, shelflife, weight, manufacturer, status, qty, description, creationDate, image) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                        "ON DUPLICATE KEY UPDATE "
                        "barcode=VALUES(barcode), category=VALUES(category), name=VALUES(name), price=VALUES(price), "
                        "shelflife=VALUES(shelflife), weight=VALUES(weight), manufacturer=VALUES(manufacturer), "
                        "status=VALUES(status), qty=VALUES(qty), description=VALUES(description), "
                        "creationDate=VALUES(creationDate), image=VALUES(image)"
                    )
                    # Copy the new image to the images folder if it exists
                    if os.path.isfile(self.file_path):
                        shutil.copy(self.file_path, destination_path)
                    data = (
                        self.var_productID.get(),
                        self.var_barcode.get(),
                        self.var_category.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_shelf_life.get(),
                        self.var_weight.get(),
                        self.var_manufacturer.get(),
                        self.var_product_status.get(),
                        self.var_qty.get(),
                        description,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        destination_path
                    )
                    my_cursor.execute(update_query, data)
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Product details successfully updated", parent=self.root)
                    self.reset_data()
                    self.fetch_data()
                else:
                    if not Update:
                        return
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
        else:
            messagebox.showerror("Error", "All Fields are required", parent=self.root)

    def reset_data(self):
        self.var_productID.set(self.get_next_product_id())
        self.var_barcode.set("")
        self.var_category.set("Select Category")
        self.var_name.set("")
        self.var_price.set("")
        self.var_shelf_life.set("")
        self.var_weight.set("")
        self.var_manufacturer.set("")
        self.var_product_status.set("Select Status")
        self.var_qty.set("")
        self.var_description.set("")  # Clear the description variable
        self.description_text.delete("1.0", "end")  # Clear the description text
        self.file_path = ""
    def delete_data(self):
        if self.var_productID.get() == "":
            messagebox.showerror("Error", "Product ID must be required", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Product Delete", "Do you want to delete this Product?", parent=self.root)
                if delete:
                    conn = mysql.connector.connect(host="localhost", user="root", passwd="1234",
                                                   database="inventory_management")
                    my_cursor = conn.cursor()

                    # Fetch the data of the product before deletion
                    select_query = "SELECT * FROM products WHERE productID=%s"
                    my_cursor.execute(select_query, (self.var_productID.get(),))
                    product_data = my_cursor.fetchone()

                    if product_data:
                        # Insert the data into the 'deleted_products' table
                        insert_query = """
                                INSERT INTO deleted_products 
                                (productID, barcode, category, name, price, shelfLife, weight, manufacturer, status, qty, description, creationDate, image)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
                        my_cursor.execute(insert_query, product_data)

                        # Delete the product from the 'products' table
                        delete_query = "DELETE FROM products WHERE productID=%s"
                        my_cursor.execute(delete_query, (self.var_productID.get(),))
                        conn.commit()
                        conn.close()
                        self.reset_data()  # Reset the form fields
                        self.fetch_data()  # Refresh the products table
                        messagebox.showinfo("Delete",
                                            "Product has been successfully deleted and moved to 'deleted_products' table.",
                                            parent=self.root)
                    else:
                        messagebox.showerror("Error", "Product not found in 'products' table.", parent=self.root)
                else:
                    if not delete:
                        return
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def get_last_deleted_product(self):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", passwd="1234",
                                           database="inventory_management")
            my_cursor = conn.cursor()

            select_query = """
                SELECT * FROM deleted_products
                WHERE deletionDate = (SELECT MAX(deletionDate) FROM deleted_products)
            """
            my_cursor.execute(select_query)
            last_deleted_product = my_cursor.fetchone()

            conn.close()

            return last_deleted_product
        except Exception as e:
            print("Error:", str(e))
            return None

    def restore_data(self):
        try:
            last_deleted_product = self.get_last_deleted_product()
            if last_deleted_product:
                restore = messagebox.askyesno(
                    "Restore Product", "Do you want to restore this product?", parent=self.root
                )
                if restore:
                    product_data = (
                        last_deleted_product[0],  # productID
                        last_deleted_product[1],  # barcode
                        last_deleted_product[2],  # category
                        last_deleted_product[3],  # name
                        last_deleted_product[4],  # price
                        last_deleted_product[5],  # shelfLife
                        last_deleted_product[6],  # weight
                        last_deleted_product[7],  # manufacturer
                        last_deleted_product[8],  # status
                        last_deleted_product[9],  # qty
                        last_deleted_product[10],  # description
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # creationDate
                        last_deleted_product[12],  # image
                    )

                    self.add_data2(product_data)

                    # Delete the restored product from deleted_products table
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        passwd="1234",
                        database="inventory_management",
                    )
                    my_cursor = conn.cursor()

                    delete_query = "DELETE FROM deleted_products WHERE productID=%s"
                    my_cursor.execute(delete_query, (last_deleted_product[0],))

                    conn.commit()
                    conn.close()

                else:
                    messagebox.showerror("Error", "No deleted products found.", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def Search(self):
        search_text = self.var_Serach1.get()
        search_text2 = self.var_Serach2.get()
        search_value = self.Serach_entry.get()
        search_value2 = self.Serach_entry2.get()

        if search_text == "Select" and search_text2 == "Select":
            messagebox.showwarning("Invalid Selection", "Please select at least one search option.", parent=self.root)
            return

        if search_text != "Select" and search_text2 == "Select":
            self.perform_single_filter_search(search_text, search_value)
        elif search_text == "Select" and search_text2 != "Select":
            self.perform_single_filter_search(search_text2, search_value2)
        elif search_text != "Select" and search_text2 != "Select":
            self.perform_combined_filter_search(search_text, search_value, search_text2, search_value2)

    def perform_single_filter_search(self, filter_type, filter_value):
        if filter_type == "Product ID":
            self.search_by_productID(filter_value)
        elif filter_type == "Barcode":
            self.search_by_barcode(filter_value)
        elif filter_type == "Category":
            self.search_by_category(filter_value)
        elif filter_type == "Name":
            self.search_by_name(filter_value)
        elif filter_type == "Product Status":
            self.search_by_product_status(filter_value)

    def perform_combined_filter_search(self, filter_type1, filter_value1, filter_type2, filter_value2):
        query = "SELECT * FROM products WHERE "
        query_conditions = []
        params = []

        if filter_type1 == "Product ID":
            query_conditions.append("productID = %s")
            params.append(filter_value1)
        elif filter_type1 == "Barcode":
            query_conditions.append("barcode = %s")
            params.append(filter_value1)
        elif filter_type1 == "Category":
            query_conditions.append("category = %s")
            params.append(filter_value1)
        elif filter_type1 == "Name":
            query_conditions.append("name = %s")
            params.append(filter_value1)
        elif filter_type1 == "Product Status":
            query_conditions.append("status = %s")
            params.append(filter_value1)

        if filter_type2 == "Product ID":
            query_conditions.append("productID = %s")
            params.append(filter_value2)
        elif filter_type2 == "Barcode":
            query_conditions.append("barcode = %s")
            params.append(filter_value2)
        elif filter_type2 == "Category":
            query_conditions.append("category = %s")
            params.append(filter_value2)
        elif filter_type2 == "Name":
            query_conditions.append("name = %s")
            params.append(filter_value2)
        elif filter_type2 == "Product Status":
            query_conditions.append("status = %s")
            params.append(filter_value2)

        query += " AND ".join(query_conditions)

        self.perform_search(query, tuple(params))

    def perform_search(self, query, params):
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
    def search_by_productID(self, search_value):
        query = "SELECT * FROM products WHERE productID = %s"
        params = (search_value,)
        self.perform_search(query, params)
    def search_by_barcode(self, search_value):
        query = "SELECT * FROM products WHERE barcode = %s"
        params = (search_value,)
        self.perform_search(query, params)
    def search_by_category(self, search_value):
        try:
            conn = mysql.connector.connect(host="localhost",
                                           user="root",
                                           passwd="1234",
                                           database="inventory_management")

            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM categories WHERE active='Yes'")
                categories = cursor.fetchall()
                cursor.close()
                conn.close()
                category_names = [category[0] for category in categories]
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Due To: {str(e)}", parent=self.root)
        if search_value in category_names:
            conn = mysql.connector.connect(host="localhost", user="root", passwd="1234",
                                           database="inventory_management")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM products WHERE category = %s", (search_value,))
            data = my_cursor.fetchall()
            if len(data) != 0:
                self.products_table.delete(*self.products_table.get_children())
                for i in data:
                    self.products_table.insert("", END, values=i)
                conn.commit()
            conn.close()
        else:
            messagebox.showwarning("Invalid Value", "Please select a valid category from the variety of categories found in the system", parent=self.root)
    def search_by_name(self, search_value):
        query = "SELECT * FROM products WHERE name = %s"
        params = (search_value,)
        self.perform_search(query, params)
    def search_by_product_status(self, search_value):
        search_value = search_value.lower()
        if search_value in ("active", "discontinued", "out of stock"):
            query = "SELECT * FROM products WHERE status = %s"
            params = (search_value,)
            self.perform_search(query, params)
        else:
            messagebox.showwarning("Invalid Value",
                                   "Please enter 'Active' or 'Discontinued' or 'Out Of Stock' for Is Active field.",
                                   parent=self.root)
if __name__ == "__main__":
    root = Tk()
    obj = Product(root)
    root.mainloop()
