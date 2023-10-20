from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import pandas as pd

class inventory:
    def __init__(self, root):
        self.root = root
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.title("Inventory Page")

        bg_img = Image.open(r"C:\Users\meyta\inventory_management_images\Product_bg4.jpg")
        bg_img = bg_img.resize((screen_width, screen_height), Image.BILINEAR)
        self.bg_img = ImageTk.PhotoImage(bg_img)

        bg_label = Label(self.root, image=self.bg_img)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title label
        title_lbl = Label(self.root, text="Inventory",
                          font=("Great Vibes", 34, "bold"), bg="#964e00", fg="white")
        title_lbl.place(x=0, y=-105, width=1500, relx=0.5, rely=0.19, anchor="center")

        main_frame = Frame(self.root, bd=2, bg="white", )
        main_frame.place(x=10, y=70, width=1260, height=600)

        self.var_name_add = StringVar()
        self.var_productId_add = StringVar()
        self.var_qty_add = StringVar()

        self.var_name_update = StringVar()
        self.var_productId_update = StringVar()
        self.var_qty_update = StringVar()

        self.var_Serach = StringVar()




        Left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Add/Update inventory",
                                font=("Great Vibes", 12, "bold"))
        Left_frame.place(x=10, y=10, width=615, height=550)

        add_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE, text="Add inventory",
                                font=("Great Vibes", 12, "bold"))
        add_frame.place(x=0, y=0, width=300, height=180)

        productId_add_label = Label(add_frame, text="Product ID:", font=("Great Vibes", 12, "bold"), bg="white")
        productId_add_label.grid(row=0, column=0, padx=7, pady=5, sticky=W)

        self.product_add_combo = ttk.Combobox(add_frame, font=("Great Vibes", 12, "bold"), textvariable=self.var_productId_add,
                                          width=14, state="readonly")
        self.product_add_combo.grid(row=0, column=1, padx=8, pady=10, sticky=W)

        # Call the update_products_values function
        self.update_products_values_add()

        self.product_add_combo.bind("<<ComboboxSelected>>", self.on_add_product_selected)

        name_add_label = tk.Label(add_frame, text="Product Name:", font=("Great Vibes", 12, "bold"),
                             bg="white")
        name_add_label.grid(row=1, column=0, padx=7, pady=5, sticky=tk.W)

        self.name_add_entry = ttk.Entry(add_frame, width=16, state='disabled',textvariable=self.var_name_add,
                                        font=("Great Vibes", 12, "bold"))
        self.name_add_entry.grid(row=1, column=1, padx=7, pady=5, sticky=tk.W)

        qty_add_label = tk.Label(add_frame, text="Qty:", font=("Great Vibes", 12, "bold"),
                              bg="white")
        qty_add_label.grid(row=2, column=0, padx=7, pady=5, sticky=tk.W)

        qty_add_entry = ttk.Entry(add_frame, width=16, textvariable=self.var_qty_add,
                               font=("Great Vibes", 12, "bold"))
        qty_add_entry.grid(row=2, column=1, padx=7, pady=5, sticky=tk.W)

        add_btn = Button(add_frame, text="Add", font=("Great Vibes", 12, "bold"), command=self.Add_Inventory,
                          width=7, bg="#964e00", fg="white")

        add_btn.grid(row=3, column=0)

        update_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE, text="Update inventory",
                               font=("Great Vibes", 12, "bold"))
        update_frame.place(x=310, y=0, width=300, height=180)

        productId_update_label = Label(update_frame, text="Product ID:", font=("Great Vibes", 12, "bold"), bg="white")
        productId_update_label.grid(row=0, column=0, padx=7, pady=5, sticky=W)

        self.product_update_combo = ttk.Combobox(update_frame, font=("Great Vibes", 12, "bold"), textvariable=self.var_productId_update,
                                          width=14, state="readonly")
        self.product_update_combo.grid(row=0, column=1, padx=8, pady=10, sticky=W)

        # Call the update_products_values function
        self.update_products_values_update()

        self.product_update_combo.bind("<<ComboboxSelected>>", self.on_update_product_selected)

        name_update_label = tk.Label(update_frame, text="Product Name:", font=("Great Vibes", 12, "bold"),
                              bg="white")
        name_update_label.grid(row=1, column=0, padx=7, pady=5, sticky=tk.W)

        self.name_update_entry = ttk.Entry(update_frame, width=16, state='disabled', textvariable=self.var_name_update,
                               font=("Great Vibes", 12, "bold"))
        self.name_update_entry.grid(row=1, column=1, padx=7, pady=5, sticky=tk.W)

        qty_update_label = tk.Label(update_frame, text="Qty:", font=("Great Vibes", 12, "bold"),
                             bg="white")
        qty_update_label.grid(row=2, column=0, padx=7, pady=5, sticky=tk.W)

        qty_update_entry = ttk.Entry(update_frame, width=16, textvariable=self.var_qty_update,
                              font=("Great Vibes", 12, "bold"))
        qty_update_entry.grid(row=2, column=1, padx=7, pady=5, sticky=tk.W)

        update_btn = Button(update_frame, text="Update", font=("Great Vibes", 12, "bold"),command=self.update_Inventory,
                          width=7, bg="#964e00", fg="white")

        update_btn.grid(row=3, column=0)

        moves_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE, text="Inventory Movements",
                                  font=("Great Vibes", 12, "bold"))
        moves_frame.place(x=0, y=180, width=610, height=345)

        Serach_frame = LabelFrame(moves_frame, bd=2, bg="white", relief=RIDGE,
                                  text="Filters",
                                  font=("Great Vibes", 12, "bold"))
        Serach_frame.place(x=5, y=0, width=600, height=70)

        Serach_combo = ttk.Combobox(Serach_frame, font=("Great Vibes", 12, "bold"), width=11, state="readonly",textvariable=self.var_Serach,                             )
        Serach_combo["values"] = ("Serach By", "Type",'ID', "Name", "Qty")
        Serach_combo.current(0)
        Serach_combo.grid(row=0, column=0, padx=2, pady=10, sticky=W)

        Serach_entry = ttk.Entry(Serach_frame, width=11, font=("Great Vibes", 12, "bold"))
        Serach_entry.grid(row=0, column=1, pady=7, padx=7, sticky=W)
        self.Serach_entry = Serach_entry
        Serach_btn = Button(Serach_frame, text="Search", font=("Great Vibes", 12, "bold"), width=10, command=self.Serach,
                            bg="#964e00",
                            fg="white")
        Serach_btn.grid(row=0, column=2, padx=3)
        showAll_btn = Button(Serach_frame, text="Reset", font=("Great Vibes", 12, "bold"), width=10,command=self.fetch_data,
                             bg="#964e00",
                             fg="white")
        showAll_btn.grid(row=0, column=3, padx=3)

        # Export_btn = Button(Serach_frame, text="Export", font=("Great Vibes", 12, "bold"), width=10,
        #                    bg="Dark Green",
        #                    fg="white")
        # Export_btn.grid(row=1, column=3, padx=3)

        table_moves_frame = Frame(moves_frame, bd=2, bg="white", relief=RIDGE)
        table_moves_frame.place(x=0, y=80, width=600, height=237)

        scroll_y = ttk.Scrollbar(table_moves_frame, orient=VERTICAL)
        self.moves_table = ttk.Treeview(table_moves_frame, column=(
            "type", "name", "productId",  "qty", "date"),  yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.moves_table.yview)

        self.moves_table.heading("type", text="Type")
        self.moves_table.heading("name", text="Name")
        self.moves_table.heading("productId", text="Product ID")
        self.moves_table.heading("qty", text="Quantity")
        self.moves_table.heading("date", text="Date")
        self.moves_table["show"] = "headings"

        self.moves_table.column("type",  width=100)
        self.moves_table.column("name", width=100)
        self.moves_table.column("productId", width=100)
        self.moves_table.column("qty", width=100)
        self.moves_table.column("date", width=100)
        self.moves_table.pack(fill=BOTH, expand=1)
        self.moves_table.bind("<ButtonRelease>")
        self.moves_table.tag_bind('button', '<Button-1>')
        self.moves_table.tag_configure('button', background='lightblue')

        Right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Charts",
                                 font=("Great Vibes", 12, "bold"))
        Right_frame.place(x=640, y=10, width=615, height=550)

        top_products_frame = Frame(Right_frame)
        top_products_frame.pack(side="top", fill="both", expand=True)
        self.create_top_products_chart(top_products_frame)


        self.fetch_data()
    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost",
                                       user="root",
                                       passwd="1234",
                                       database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM inventory_movenent")
        data = my_cursor.fetchall()
        if len(data) != 0:
            self.moves_table.delete(*self.moves_table.get_children())
            for i in data:
                self.moves_table.insert("", END, values=i)
            conn.commit()
        conn.close()

    def update_products_values(self):
        try:
            conn = mysql.connector.connect(host="localhost",
                                           user="root",
                                           passwd="1234",
                                           database="inventory_management")

            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("SELECT productId FROM products WHERE status='Active'")
                products = cursor.fetchall()
                cursor.close()
                conn.close()

                # Update the Combobox values with the fetched categories
                self.product_id = [product[0] for product in products]
                self.product_id.insert(0, "Select Product ID")  # Add an initial default value
                self.product_combo["values"] = self.product_id
                self.product_combo.current(0)  # Select the default value

                # Enable autocompletion for the product_combo
                self.product_combo.bind('<KeyRelease>', self.update_autocomplete)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Due To: {str(e)}", parent=self.root)

    def update_products_values_add(self):
        try:
            conn = mysql.connector.connect(host="localhost",
                                           user="root",
                                           passwd="1234",
                                           database="inventory_management")

            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("SELECT productId FROM products WHERE status='Active'")
                products = cursor.fetchall()
                cursor.close()
                conn.close()
                # Update the Combobox values with the fetched categories
                self.product_id = [product[0] for product in products]
                self.product_id.insert(0, "Select Product ID")  # Add an initial default value
                self.product_add_combo["values"] = self.product_id
                self.product_add_combo.current(0)  # Select the default value
                # Enable autocompletion for the product_combo
                self.product_add_combo.bind('<KeyRelease>', self.update_autocomplete)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Due To: {str(e)}", parent=self.root)

    def update_products_values_update(self):
        try:
            conn = mysql.connector.connect(host="localhost",
                                           user="root",
                                           passwd="1234",
                                           database="inventory_management")

            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("SELECT productId FROM products WHERE status='Active'")
                products = cursor.fetchall()
                cursor.close()
                conn.close()
                # Update the Combobox values with the fetched categories
                self.product_id = [product[0] for product in products]
                self.product_id.insert(0, "Select Product ID")  # Add an initial default value
                self.product_update_combo["values"] = self.product_id
                self.product_update_combo.current(0)  # Select the default value
                # Enable autocompletion for the product_combo
                self.product_update_combo.bind('<KeyRelease>', self.update_autocomplete)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Due To: {str(e)}", parent=self.root)

    def update_autocomplete(self, event):
        search_term = self.search_entry.get().lower()
        filtered_products = []
        print(self.product_names)
        for product in self.product_names:
            if search_term in product.lower():
                filtered_products.append(product)
        self.product_combo["values"] = filtered_products

    def on_add_product_selected(self, event):
        selected_product = self.product_add_combo.get()  # Corrected attribute name
        if selected_product != "Select Product ID":
            try:
                conn = mysql.connector.connect(host="localhost",
                                               user="root",
                                               passwd="1234",
                                               database="inventory_management")
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM products WHERE productId=%s", (selected_product,))
                product_name = cursor.fetchone()[0]
                cursor.close()
                conn.close()
                # Update the name_entry with the fetched product name
                self.name_add_entry.config(state='normal')  # Corrected attribute name
                self.name_add_entry.delete(0, tk.END)
                self.name_add_entry.insert(0, product_name)
                self.name_add_entry.config(state='disabled')  # Corrected attribute name
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Due To: {str(e)}", parent=self.root)
    def on_update_product_selected(self, event):
        selected_product = self.product_update_combo.get()
        if selected_product != "Select Product ID":
            try:
                conn = mysql.connector.connect(host="localhost",
                                               user="root",
                                               passwd="1234",
                                               database="inventory_management")
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM products WHERE productId=%s", (selected_product,))
                product_name = cursor.fetchone()[0]
                cursor.close()
                conn.close()
                # Update the name_entry with the fetched product name
                self.name_update_entry.config(state='normal')
                self.name_update_entry.delete(0, tk.END)
                self.name_update_entry.insert(0, product_name)
                self.name_update_entry.config(state='disabled')

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Due To: {str(e)}", parent=self.root)

    def Add_Inventory(self):
        if self.var_qty_add.get()!= "" and self.var_name_add.get() != 'Select Product':
            try:
                conn = mysql.connector.connect(host="localhost",
                                               user="root",
                                               passwd="1234",
                                               database="inventory_management")
                my_cursor = conn.cursor()

                my_cursor.execute("INSERT INTO inventory_movenent VALUES(%s,%s,%s,%s,%s)", (
                    "Add Inventory",
                    self.var_name_add.get(),
                    self.var_productId_add.get(),
                    self.var_qty_add.get(),
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                ))
                conn.commit()

                update_qty_query = "UPDATE products SET qty = qty + %s WHERE productID = %s"
                my_cursor.execute(update_qty_query, (self.var_qty_add.get(), self.var_productId_add.get()))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Inventory has been added Successfully", parent=self.root)
                self.reset_data()

            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
        else:
            messagebox.showerror("Error", "qty and product are required", parent=self.root)

    def update_Inventory(self):
        if self.var_qty_update.get() != "" and self.var_name_update.get() != 'Select Product':
            try:
                conn = mysql.connector.connect(host="localhost",
                                               user="root",
                                               passwd="1234",
                                               database="inventory_management")
                my_cursor = conn.cursor()

                my_cursor.execute("INSERT INTO inventory_movenent VALUES(%s,%s,%s,%s,%s)", (
                    "Update Inventory",
                    self.var_name_update.get(),
                    self.var_productId_update.get(),
                    self.var_qty_update.get(),
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                ))
                conn.commit()

                update_qty_query = "UPDATE products SET qty = %s WHERE productID = %s"
                my_cursor.execute(update_qty_query, (self.var_qty_update.get(), self.var_productId_update.get()))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Inventory has been updated Successfully", parent=self.root)
                self.reset_data()

            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
        else:
            messagebox.showerror("Error", "qty and product are required", parent=self.root)

    def reset_data(self):
        self.var_productId_add.set("Select Product ID")
        self.var_name_add.set("")
        self.var_qty_add.set("")
        self.var_productId_update.set("Select Product ID")
        self.var_name_update.set("")
        self.var_qty_update.set("")

    def Serach(self):
        search_text = self.var_Serach.get()
        search_value = self.Serach_entry.get()

        if search_text == "Type":
            self.search_by_Type(search_value)
        elif search_text == "ID":
            self.search_by_ID(search_value)
        elif search_text == "Name":
            self.search_by_name(search_value)
        elif search_text == "Qty":
            self.search_by_qty(search_value)
        else:
            messagebox.showwarning("Invalid Selection", "Please select a valid search option.", parent=self.root)


    def search_by_Type(self, search_value):

        if search_value in ("Add Inventory", "Update Inventory"):
            conn = mysql.connector.connect(host="localhost", user="root", passwd="1234",
                                           database="inventory_management")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM inventory_movenent WHERE type = %s", (search_value,))
            data = my_cursor.fetchall()
            if len(data) != 0:
                self.moves_table.delete(*self.moves_table.get_children())
                for i in data:
                    self.moves_table.insert("", END, values=i)
                conn.commit()
            conn.close()
        else:
            messagebox.showwarning("Invalid Value", "Please enter 'Add Inventory' or 'Update Inventory' for Is type field", parent=self.root)

    def search_by_ID(self, search_value):
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM inventory_movenent WHERE productId = %s", (search_value,))
        data = my_cursor.fetchall()
        if len(data) != 0:
            self.moves_table.delete(*self.moves_table.get_children())
            for i in data:
                self.moves_table.insert("", END, values=i)
            conn.commit()
        conn.close()

    def search_by_name(self, search_value):
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM inventory_movenent WHERE name LIKE %s", ('%' + search_value + '%',))
        data = my_cursor.fetchall()
        if len(data) != 0:
            self.moves_table.delete(*self.moves_table.get_children())
            for i in data:
                self.moves_table.insert("", END, values=i)
            conn.commit()
        conn.close()

    def search_by_qty(self, search_value):
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM inventory_movenent WHERE qty LIKE %s", ('%' + search_value + '%',))
        data = my_cursor.fetchall()
        if len(data) != 0:
            self.moves_table.delete(*self.moves_table.get_children())
            for i in data:
                self.moves_table.insert("", END, values=i)
            conn.commit()
        conn.close()

    def create_top_products_chart(self, parent_frame):
        fig = Figure(figsize=(10, 4.8))
        ax = fig.add_subplot(111)

        # Fetch data for the top products chart
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        sql_query = """
            SELECT name, SUM(qty) as total_quantity
            FROM products
            GROUP BY name
            ORDER BY total_quantity DESC
            LIMIT 5
        """
        df = pd.read_sql(sql_query, conn)
        conn.close()

        # Create the bar chart
        ax.bar(df['name'], df['total_quantity'], color='#964e00')
        ax.set_title("Top 5 Products by Total Quantity")
        ax.set_xlabel("Product Name")
        ax.set_ylabel("Total Quantity")

        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Add navigation toolbar
        toolbar = NavigationToolbar2Tk(canvas, parent_frame)
        toolbar.update()
        canvas.get_tk_widget().pack()


if __name__ == "__main__":
    root = Tk()
    obj = inventory(root)
    root.mainloop()



