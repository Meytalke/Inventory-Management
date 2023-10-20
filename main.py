import tkinter.messagebox
from tkcalendar import Calendar
from tkinter import *
import tkinter
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import os
from time import strftime
from datetime import datetime
import pandas as pd


from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Products import Product
from Categories import Category
from orders import orders
from inventory import inventory
from employee import employees
from EmployeeCheckInOut import checkInOut
from BillingSystem import BillingSystem
import mysql.connector

class Inventory_Management:
    def __init__(self, root):
        self.root = root
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.title("Inventory Management System")
        bg_img = Image.open(r"C:\Users\meyta\inventory_management_images\login.png")
        bg_img = bg_img.resize((int(screen_width*0.7), int(screen_height*0.7)), Image.BILINEAR)
        self.bg_img = ImageTk.PhotoImage(bg_img)

        bg_label = Label(self.root, image=self.bg_img)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        title_lbl = tk.Label(root, text="Inventory Management System", font=("Great Vibes", 27, "bold"),
                             fg="white", bg="#00555B")
        title_lbl.place(x=-50, y=0, width=1500, height=45)

        def time():
            string = strftime('%H:%M:%S %p')
            lbl.config(text=string)
            lbl.after(1000, time)

        lbl = Label(title_lbl, font=('root', 14, 'bold'), fg="white", bg="#00555B")
        lbl.place(x=130, y=0, width=110, height=50)
        time()

        Products_btn = tk.Button(self.root, text="Products", command=self.product_details, cursor="hand2", font=("Great Vibes", 15, "bold"), bg="#2f3030", fg="white")
        Products_btn.place(x=50, y=45, width=150, height=30)

        Categories_btn = tk.Button(self.root, text="Categories", command=self.category_details, cursor="hand2", font=("Great Vibes", 15, "bold"),
                         bg="#2f3030", fg="white")
        Categories_btn.place(x=205, y=45, width=150, height=30)

        Orders_btn = tk.Button(self.root, text="Orders", cursor="hand2", command=self.orders_details,font=("Great Vibes", 15, "bold"),
                         bg="#2f3030", fg="white")
        Orders_btn.place(x=360, y=45, width=150, height=30)

        Inventory_btn = tk.Button(self.root, text="Inventory", cursor="hand2", command=self.inventory_details, font=("Great Vibes", 15, "bold"),
                         bg="#2f3030", fg="white")
        Inventory_btn.place(x=515, y=45, width=150, height=30)

        Employees_btn = tk.Button(self.root, text="Employees", cursor="hand2", command=self.employees_details, font=("Great Vibes", 15, "bold"),
                         bg="#2f3030", fg="white")
        Employees_btn.place(x=670, y=45, width=150, height=30)

        checkInOut_btn = tk.Button(self.root, text="Check In/Out", command=self.checkInOut_details, cursor="hand2", font=("Great Vibes", 15, "bold"),
                         bg="#2f3030", fg="white")
        checkInOut_btn.place(x=825, y=45, width=150, height=30)

        Billing_System_btn = tk.Button(self.root, text="Billing System",command=self.BillingSystem_details, cursor="hand2", font=("Great Vibes", 15, "bold"),
                         bg="#2f3030", fg="white")
        Billing_System_btn.place(x=980, y=45, width=150, height=30)

        Exit_btn = tk.Button(self.root, text="Exit",command=self.iExit, cursor="hand2", font=("Great Vibes", 15, "bold"),
                         bg="#2f3030", fg="white")
        Exit_btn.place(x=1135, y=45, width=150, height=30)

        self.items = self.total_items()
        self.products = self.total_products()
        self.categories = self.total_categories()
        self.orders = self.total_orders()
        self.employees = self.total_employees()
        self.expenses = self.total_amount_of_expenses()
        self.revenue = self.total_amount_of_revenue()

        items_lbl = tk.Label(root, text=str(self.items)+"\n\nTotal Items", font=("Great Vibes", 17, "bold"),
                             fg="white", bg="#009999")
        items_lbl.place(x=100, y=100, width=300, height=100)

        items_btn = tk.Button(self.root, text="More Info", cursor="hand2",
                             font=("Great Vibes", 15, "bold"),command=self.items_dashboard,
                             fg="white", bg="#006666")
        items_btn.place(x=100, y=200, width=300, height=30)

        products_lbl = tk.Label(root, text=str(self.products) + "\n\nTotal Products", font=("Great Vibes", 17, "bold"),
                             fg="white", bg="#DB0218")
        products_lbl.place(x=500, y=100, width=300, height=100)

        products_btn = tk.Button(self.root, text="More Info", cursor="hand2",command=self.products_create_charts_window
                             , font=("Great Vibes", 15, "bold"),
                              fg="white", bg="#A80011")
        products_btn.place(x=500, y=200, width=300, height=30)

        categories_lbl = tk.Label(root, text=str(self.categories) + "\n\nTotal Categories",
                                font=("Great Vibes", 17, "bold"),
                                fg="white", bg="#C5D204")
        categories_lbl.place(x=900, y=100, width=300, height=100)

        categories_btn = tk.Button(self.root, text="More Info", cursor="hand2",command=self.categories_create_charts_window,
                                 font=("Great Vibes", 15, "bold"),
                                 fg="white", bg="#96A100")
        categories_btn.place(x=900, y=200, width=300, height=30)

        orders_lbl = tk.Label(root, text=str(self.orders) + "\n\nTotal Orders",
                                  font=("Great Vibes", 17, "bold"),
                                  fg="white", bg="#009999")
        orders_lbl.place(x=100, y=300, width=300, height=100)

        orders_btn = tk.Button(self.root, text="More Info", cursor="hand2",
                                   font=("Great Vibes", 15, "bold"),command=self.orders_create_charts_window,
                                   fg="white", bg="#006666")
        orders_btn.place(x=100, y=400, width=300, height=30)

        employees_lbl = tk.Label(root, text=str(self.employees) + "\n\nTotal Employees",
                              font=("Great Vibes", 17, "bold"),
                              fg="white", bg="#DB0218")
        employees_lbl.place(x=500, y=300, width=300, height=100)

        employees_btn = tk.Button(self.root, text="More Info", cursor="hand2",
                               font=("Great Vibes", 15, "bold"), command=self.employees_create_charts_window,
                               fg="white", bg="#A80011")
        employees_btn.place(x=500, y=400, width=300, height=30)

        expenses_lbl = tk.Label(root, text=str(self.expenses) + "\n\nTotal Amount Of Expenses",
                                 font=("Great Vibes", 17, "bold"),
                                 fg="white", bg="#C5D204")
        expenses_lbl.place(x=900, y=300, width=300, height=130)

        #expenses_btn = tk.Button(self.root, text="More Info", cursor="hand2",
        #                          font=("Great Vibes", 15, "bold"),
        #                          fg="white", bg="#96A100")
        #expenses_btn.place(x=900, y=400, width=300, height=30)

        revenue_lbl = tk.Label(root, text=str(self.revenue) + "\n\nTotal Amount Of Revenue",
                                font=("Great Vibes", 17, "bold"),
                                fg="white", bg="#009999")
        revenue_lbl.place(x=100, y=500, width=300, height=130)

        #revenue_btn = tk.Button(self.root, text="More Info", cursor="hand2",
        #                         font=("Great Vibes", 15, "bold"),
        #                         fg="white", bg="#006666")
        #revenue_btn.place(x=100, y=600, width=300, height=30)

    def open_calendar_popup_start(self, event=None):
        self.calendar_window = Toplevel(self.root)
        self.calendar_window.title("Choose a Date")

        self.date_calendar = Calendar(self.calendar_window, selectmode="day", date_pattern="dd/MM/yyyy",
                                      showweeknumbers=False)
        self.date_calendar.pack()

        select_button = Button(self.calendar_window, text="Select Date", command=self.select_date_start)
        select_button.pack()

    def select_date_start(self):
        selected_date = self.date_calendar.get_date()
        self.calendar_window.destroy()
        self.start_day_entry.delete(0, END)
        self.start_day_entry.insert(0, selected_date)

    def open_calendar_popup_end(self, event=None):
        self.calendar_window = Toplevel(self.root)
        self.calendar_window.title("Choose a Date")

        self.date_calendar = Calendar(self.calendar_window, selectmode="day", date_pattern="dd/MM/yyyy",
                                      showweeknumbers=False)
        self.date_calendar.pack()

        select_button = Button(self.calendar_window, text="Select Date", command=self.select_date_end)
        select_button.pack()

    def select_date_end(self):
        selected_date = self.date_calendar.get_date()
        self.calendar_window.destroy()
        self.end_day_entry.delete(0, END)
        self.end_day_entry.insert(0, selected_date)

    # open items- dashboard

    def items_dashboard(self):
        self.charts_window = tk.Toplevel(self.root)
        screen_width1 = self.root.winfo_screenwidth()
        screen_height1 = self.root.winfo_screenheight()
        self.charts_window.geometry(f"{screen_width1}x{screen_height1}+0+0")
        self.charts_window.title("Reports")
        title_lbl = tk.Label(self.charts_window, text="Items Reports Window", font=("Great Vibes", 27, "bold"),
                             fg="white", bg="#00555B")
        title_lbl.place(x=-50, y=0, width=1500, height=45)

        main_frame = Frame(self.charts_window, bd=2, bg="white", )
        main_frame.place(x=0, y=50, width=1260, height=600)

        top_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,text="Filters",
                                font=("Great Vibes", 12, "bold"))
        top_frame.place(x=0, y=0, width=1255, height=130)

        self.bottom_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                  font=("Great Vibes", 12, "bold"))
        self.bottom_frame.place(x=0, y=140, width=1255, height=440)

        Report_label = tk.Label(top_frame, text="Choose Report", font=("Great Vibes", 12, "bold"),
                                  bg="white")
        Report_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        Report_items_entry = ttk.Combobox(top_frame, font=("Great Vibes", 12, "bold"), width=15, state="readonly")
        Report_items_entry["values"] = ("Choose Report", "All Products",'Inventory Report',"Missing Inventory Report", "Sales Report")
        Report_items_entry.current(0)
        Report_items_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)
        self.Report_items_serach = Report_items_entry

        Product_label = tk.Label(top_frame, text="Choose Product", font=("Great Vibes", 12, "bold"),
                                bg="white")
        Product_label.grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)

        self.var_product= StringVar()
        self.var_start_day = StringVar()
        self.var_end_day = StringVar()

        self.Product_entry = ttk.Combobox(top_frame, font=("Great Vibes", 12, "bold"), width=15, state="readonly",textvariable=self.var_product)
        self.Product_entry.grid(row=0, column=3, padx=10, pady=5, sticky=W)
        self.update_products_values()

        start_day_label = tk.Label(top_frame, text="Start Day:", font=("Great Vibes", 12, "bold"),
                             bg="white")
        start_day_label.grid(row=0, column=4, padx=7, pady=5, sticky=tk.W)

        self.start_day_entry = ttk.Entry(top_frame, width=19, textvariable=self.var_start_day,
                                   font=("Great Vibes", 12, "bold"))
        self.start_day_entry.grid(row=0, column=5, padx=7, pady=5, sticky=tk.W)

        self.start_day_entry.bind("<Button-1>", self.open_calendar_popup_start)

        end_day_label = tk.Label(top_frame, text="End Day:", font=("Great Vibes", 12, "bold"),
                                   bg="white")
        end_day_label.grid(row=0, column=6, padx=7, pady=5, sticky=tk.W)

        self.end_day_entry = ttk.Entry(top_frame, width=19,textvariable=self.var_end_day,
                                         font=("Great Vibes", 12, "bold"))
        self.end_day_entry.grid(row=0, column=7, padx=7, pady=5, sticky=tk.W)

        self.end_day_entry.bind("<Button-1>", self.open_calendar_popup_end)

        Apply_btn = Button(top_frame, text="Apply", font=("Great Vibes", 12, "bold"), width=10,command=self.apply,
                            bg="#00555B",
                            fg="white")
        Apply_btn.grid(row=1, column=6, padx=10, pady=5, sticky=W)
        Export_btn = Button(top_frame, text="Export", font=("Great Vibes", 12, "bold"), width=10,command=self.export,
                             bg="#00555B",
                             fg="white")
        Export_btn.grid(row=1, column=7, padx=10, pady=5, sticky=W)

    def export(self):
        selected_rep = self.Report_items_serach.get()
        if selected_rep != "Choose Report":
            if selected_rep == "All Products":
                self.export_all_products()
            elif selected_rep =="Inventory Report":
                self.export_inventory_moves()
            elif selected_rep =="Missing Inventory Report":
                self.export_missing_products()
            elif selected_rep == "Sales Report":
                self.export_sales_reports()
        else:
            messagebox.showinfo("Choose Any Report", "Please Choose Any Report", parent=self.charts_window)

    def export_all_products(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], parent=self.charts_window)
        if file_path:
            data = []
            for item in self.products_table.get_children():
                data.append(self.products_table.item(item, "values"))

            columns = ["Product ID", "Barcode", "Category", "Name", "Price", "Shelf Life", "Weight",
                       "Manufacturer", "Product Status", "Quantity", "Description", "Creation Date", "Image"]

            df = pd.DataFrame(data, columns=columns)

            excel_path = file_path
            df.to_excel(excel_path, index=False)
            messagebox.showinfo("Export", "Data exported to Excel successfully.", parent=self.charts_window)

    def export_inventory_moves(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], parent=self.charts_window)
        if file_path:
            data = []
            for item in self.moves_table.get_children():
                data.append(self.moves_table.item(item, "values"))

            columns = ["Type", "Name", "Product ID", "Quantity", "Date"]

            df = pd.DataFrame(data, columns=columns)

            excel_path = file_path
            df.to_excel(excel_path, index=False)
            messagebox.showinfo("Export", "Data exported to Excel successfully.", parent=self.charts_window)

    def export_missing_products(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], parent=self.charts_window)
        if file_path:
            data = []
            for item in self.products_table.get_children():
                data.append(self.products_table.item(item, "values"))

            columns = ["Product ID", "Barcode", "Category", "Name", "Price", "Shelf Life", "Weight",
                       "Manufacturer", "Product Status", "Quantity", "Description", "Creation Date", "Image"]

            df = pd.DataFrame(data, columns=columns)
            excel_path = file_path
            df.to_excel(excel_path, index=False)
            messagebox.showinfo("Export", "Data exported to Excel successfully.", parent=self.charts_window)

    def export_sales_reports(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], parent=self.charts_window)
        if file_path:
            data = []
            for item in self.orders_frame.get_children():
                data.append(self.orders_frame.item(item, "values"))

            columns = ["Order ID", "Product ID", "Product Name", "Qty", "Price","Total"]

            df = pd.DataFrame(data, columns=columns)

            excel_path = file_path
            df.to_excel(excel_path, index=False)
            messagebox.showinfo("Export", "Data exported to Excel successfully.", parent=self.charts_window)

    def apply(self):
        selected_rep = self.Report_items_serach.get()
        if selected_rep != "Choose Report":
            if selected_rep == "All Products":
                self.all_products()
            elif selected_rep =="Inventory Report":
                self.inventory_moves()
            elif selected_rep =="Missing Inventory Report":
                self.missing_products()
            elif selected_rep == "Sales Report":
                self.sales_reports()
        else:
            messagebox.showinfo("Choose Any Report", "Please Choose Any Report", parent=self.charts_window)

    def sales_reports(self):
        table_frame = Frame(self.bottom_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=0, y=0, width=1250, height=430)
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        self.orders_frame = ttk.Treeview(table_frame, column=(
            "orderId", "productId", "productName", "qty", "price", "total"), yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.orders_frame.xview)
        scroll_y.config(command=self.orders_frame.yview)
        self.orders_frame.heading("orderId", text="Order ID")
        self.orders_frame.heading("productId", text="Product ID")
        self.orders_frame.heading("productName", text="Product Name")
        self.orders_frame.heading("qty", text="Qty")
        self.orders_frame.heading("price", text="Price")
        self.orders_frame.heading("total", text="Total")
        self.orders_frame["show"] = "headings"

        self.orders_frame.column("orderId", width=100)
        self.orders_frame.column("productId", width=100)
        self.orders_frame.column("productName", width=150)
        self.orders_frame.column("qty", width=100)
        self.orders_frame.column("price", width=100)
        self.orders_frame.column("total", width=100)
        self.orders_frame.pack(fill=BOTH, expand=1)
        self.orders_frame.tag_configure('button', background='lightblue')
        self.orders_frame.bind("<ButtonRelease-1>")
        self.fetch_data_orders_details()

    def fetch_data_orders_details(self):
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()

        if self.var_product.get() != "Select Product ID":
                my_cursor.execute("SELECT * FROM orders_details WHERE productId = %s",
                                  (self.var_product.get(),))
        else:
            my_cursor.execute("SELECT * FROM orders_details")
        data = my_cursor.fetchall()
        if len(data) != 0:
            self.orders_frame.delete(*self.orders_frame.get_children())
            for i in data:
                self.orders_frame.insert("", END, values=i)
            conn.commit()
        else:
            messagebox.showinfo("No Results", "No products found that match the criteria.", parent=self.charts_window)
        conn.close()

    def all_products(self):
        table_frame = Frame(self.bottom_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=0, y=0, width=1250, height=430)
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        self.products_table = ttk.Treeview(table_frame, column=(
            "productId", "barcode", "category", "name", "price", "shelfLife", "weight", "manufacturer", "status", "qty",
            "description", "creationDate", "image"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
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
        self.products_table.bind("<ButtonRelease>")
        for iid in self.products_table.get_children():
            self.insert_view_image_button(values=iid)
        self.products_table.tag_bind('button', '<Button-1>')
        self.products_table.tag_configure('button', background='lightblue')
        self.fetch_data_orders()

    def missing_products(self):
        table_frame = Frame(self.bottom_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=0, y=0, width=1250, height=430)
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        self.products_table = ttk.Treeview(table_frame, column=(
            "productId", "barcode", "category", "name", "price", "shelfLife", "weight", "manufacturer", "status", "qty",
            "description", "creationDate", "image"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
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
        self.products_table.bind("<ButtonRelease>")
        for iid in self.products_table.get_children():
            self.insert_view_image_button(values=iid)
        self.products_table.tag_bind('button', '<Button-1>')
        self.products_table.tag_configure('button', background='lightblue')
        self.fetch_data_missing()

    def inventory_moves(self):
        table_moves_frame = Frame(self.bottom_frame, bd=2, bg="white", relief=RIDGE)
        table_moves_frame.place(x=0, y=0, width=1250, height=430)

        scroll_y = ttk.Scrollbar(table_moves_frame, orient=VERTICAL)
        self.moves_table = ttk.Treeview(table_moves_frame, column=(
            "type", "name", "productId", "qty", "date"), yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.moves_table.yview)

        self.moves_table.heading("type", text="Type")
        self.moves_table.heading("name", text="Name")
        self.moves_table.heading("productId", text="Product ID")
        self.moves_table.heading("qty", text="Quantity")
        self.moves_table.heading("date", text="Date")
        self.moves_table["show"] = "headings"

        self.moves_table.column("type", width=100)
        self.moves_table.column("name", width=100)
        self.moves_table.column("productId", width=100)
        self.moves_table.column("qty", width=100)
        self.moves_table.column("date", width=100)
        self.moves_table.pack(fill=BOTH, expand=1)
        self.moves_table.bind("<ButtonRelease>")
        self.moves_table.tag_bind('button', '<Button-1>')
        self.moves_table.tag_configure('button', background='lightblue')
        self.fetch_data_inventory()

    def fetch_data_inventory(self):
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        current_date_format = "%d/%m/%Y"
        desired_date_format = "%y-%m-%d"

        if self.var_product.get() != "Select Product ID":
            if self.var_start_day.get() and self.var_end_day.get():
                start_date = datetime.strptime(self.var_start_day.get(), current_date_format).strftime(
                    desired_date_format)
                end_date = datetime.strptime(self.var_end_day.get(), current_date_format).strftime(desired_date_format)
                my_cursor.execute(
                    "SELECT * FROM inventory_movenent WHERE productId = %s AND date BETWEEN %s AND %s",
                    (self.var_product.get(), start_date, end_date))
            elif self.var_start_day.get():
                start_date = datetime.strptime(self.var_start_day.get(), current_date_format).strftime(
                    desired_date_format)
                my_cursor.execute("SELECT * FROM inventory_movenent WHERE productId = %s AND date >= %s",
                                  (self.var_product.get(), start_date))
            elif self.var_end_day.get():
                end_date = datetime.strptime(self.var_end_day.get(), current_date_format).strftime(desired_date_format)
                my_cursor.execute("SELECT * FROM inventory_movenent WHERE productId = %s AND date <= %s",
                                  (self.var_product.get(), end_date))
            else:
                my_cursor.execute("SELECT * FROM inventory_movenent WHERE productId = %s",
                                  (self.var_product.get(),))
        elif self.var_start_day.get() and self.var_end_day.get():
            start_date = datetime.strptime(self.var_start_day.get(), current_date_format).strftime(desired_date_format)
            end_date = datetime.strptime(self.var_end_day.get(), current_date_format).strftime(desired_date_format)
            my_cursor.execute(
                "SELECT * FROM inventory_movenent WHERE date BETWEEN %s AND %s",
                (start_date, end_date))
        elif self.var_start_day.get():
            start_date = datetime.strptime(self.var_start_day.get(), current_date_format).strftime(desired_date_format)
            my_cursor.execute("SELECT * FROM inventory_movenent WHERE date >= %s", (start_date,))
        elif self.var_end_day.get():
            end_date = datetime.strptime(self.var_end_day.get(), current_date_format).strftime(desired_date_format)
            my_cursor.execute("SELECT * FROM inventory_movenent WHERE date <= %s", (end_date,))
        else:
            my_cursor.execute("SELECT * FROM inventory_movenent")

        data = my_cursor.fetchall()
        if len(data) != 0:
            self.moves_table.delete(*self.moves_table.get_children())
            for i in data:
                self.moves_table.insert("", END, values=i)
            conn.commit()
        else:
            messagebox.showinfo("No Results", "No products found that match the criteria.", parent=self.charts_window)
        conn.close()

    def fetch_data_missing(self):
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        current_date_format = "%d/%m/%Y"
        desired_date_format = "%y-%m-%d"

        if self.var_product.get() != "Select Product ID":
            if self.var_start_day.get() and self.var_end_day.get():
                start_date = datetime.strptime(self.var_start_day.get(), current_date_format).strftime(
                    desired_date_format)
                end_date = datetime.strptime(self.var_end_day.get(), current_date_format).strftime(desired_date_format)
                my_cursor.execute(
                    "SELECT * FROM products WHERE qty < 11 AND productID = %s AND creationDate BETWEEN %s AND %s",
                    (self.var_product.get(), start_date, end_date))
            elif self.var_start_day.get():
                start_date = datetime.strptime(self.var_start_day.get(), current_date_format).strftime(
                    desired_date_format)
                my_cursor.execute("SELECT * FROM products WHERE qty < 11 AND productID = %s AND creationDate >= %s",
                                  (self.var_product.get(), start_date))
            elif self.var_end_day.get():
                end_date = datetime.strptime(self.var_end_day.get(), current_date_format).strftime(desired_date_format)
                my_cursor.execute("SELECT * FROM products WHERE qty < 11 AND productID = %s AND creationDate <= %s",
                                  (self.var_product.get(), end_date))
            else:
                my_cursor.execute("SELECT * FROM products WHERE qty < 11 AND productID = %s",
                                  (self.var_product.get(),))
        elif self.var_start_day.get() and self.var_end_day.get():
            start_date = datetime.strptime(self.var_start_day.get(), current_date_format).strftime(desired_date_format)
            end_date = datetime.strptime(self.var_end_day.get(), current_date_format).strftime(desired_date_format)
            my_cursor.execute(
                "SELECT * FROM products WHERE qty < 11 AND creationDate BETWEEN %s AND %s",
                (start_date, end_date))
        elif self.var_start_day.get():
            start_date = datetime.strptime(self.var_start_day.get(), current_date_format).strftime(desired_date_format)
            my_cursor.execute("SELECT * FROM products WHERE qty < 11 AND creationDate >= %s", (start_date,))
        elif self.var_end_day.get():
            end_date = datetime.strptime(self.var_end_day.get(), current_date_format).strftime(desired_date_format)
            my_cursor.execute("SELECT * FROM products WHERE qty < 11 AND creationDate <= %s", (end_date,))
        else:
            my_cursor.execute("SELECT * FROM products WHERE qty < 11")

        data = my_cursor.fetchall()
        if len(data) != 0:
            self.products_table.delete(*self.products_table.get_children())
            for i in data:
                image_data = i[12]
                self.products_table.insert("", END, values=i[:-1] + ("Yes" if image_data else "None",))
        else:
            messagebox.showinfo("No Results", "No products found that match the criteria.", parent=self.charts_window)
        conn.commit()
        conn.close()

    def fetch_data_orders(self):
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        current_date_format = "%d/%m/%Y"
        desired_date_format = "%y-%m-%d"

        if self.var_product.get() != "Select Product ID":
            if self.var_start_day.get() and self.var_end_day.get():
                start_date = datetime.strptime(self.var_start_day.get(), current_date_format).strftime(
                    desired_date_format)
                end_date = datetime.strptime(self.var_end_day.get(), current_date_format).strftime(desired_date_format)
                my_cursor.execute(
                    "SELECT * FROM products WHERE productID = %s AND creationDate BETWEEN %s AND %s",
                    (self.var_product.get(), start_date, end_date))
            elif self.var_start_day.get():
                start_date = datetime.strptime(self.var_start_day.get(), current_date_format).strftime(
                    desired_date_format)
                my_cursor.execute("SELECT * FROM products WHERE productID = %s AND creationDate >= %s",
                                  (self.var_product.get(), start_date))
            elif self.var_end_day.get():
                end_date = datetime.strptime(self.var_end_day.get(), current_date_format).strftime(desired_date_format)
                my_cursor.execute("SELECT * FROM products WHERE productID = %s AND creationDate <= %s",
                                  (self.var_product.get(), end_date))
            else:
                my_cursor.execute("SELECT * FROM products WHERE productID = %s",
                                  (self.var_product.get(),))
        elif self.var_start_day.get() and self.var_end_day.get():
            start_date = datetime.strptime(self.var_start_day.get(), current_date_format).strftime(desired_date_format)
            end_date = datetime.strptime(self.var_end_day.get(), current_date_format).strftime(desired_date_format)
            my_cursor.execute(
                "SELECT * FROM products WHERE creationDate BETWEEN %s AND %s",
                (start_date, end_date))
        elif self.var_start_day.get():
            start_date = datetime.strptime(self.var_start_day.get(), current_date_format).strftime(desired_date_format)
            my_cursor.execute("SELECT * FROM products WHERE creationDate >= %s", (start_date,))
        elif self.var_end_day.get():
            end_date = datetime.strptime(self.var_end_day.get(), current_date_format).strftime(desired_date_format)
            my_cursor.execute("SELECT * FROM products WHERE creationDate <= %s", (end_date,))
        else:
            my_cursor.execute("SELECT * FROM products")

        data = my_cursor.fetchall()
        if len(data) != 0:
            self.products_table.delete(*self.products_table.get_children())
            for i in data:
                image_data = i[12]
                self.products_table.insert("", END, values=i[:-1] + ("Yes" if image_data else "None",))
        else:
            messagebox.showinfo("No Results", "No products found that match the criteria.", parent=self.charts_window)
        conn.commit()
        conn.close()

    def insert_view_image_button(self, values):
        self.products_table.insert("", "end", values=values, tags=('button',))

    def update_products_values(self):
        try:
            conn = mysql.connector.connect(host="localhost",
                                           user="root",
                                           passwd="1234",
                                           database="inventory_management")

            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("SELECT productId FROM products")
                products = cursor.fetchall()
                cursor.close()
                conn.close()

                # Update the Combobox values with the fetched categories
                self.product_id = [product[0] for product in products]
                self.product_id.insert(0, "Select Product ID")  # Add an initial default value
                self.Product_entry["values"] = self.product_id
                self.Product_entry.current(0)  # Select the default value

                # Enable autocompletion for the product_combo
                self.Product_entry.bind('<KeyRelease>')
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Due To: {str(e)}", parent=self.root)

    def update_employees_values(self):
        try:
            conn = mysql.connector.connect(host="localhost",
                                           user="root",
                                           passwd="1234",
                                           database="inventory_management")

            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("SELECT employeeID FROM employees")
                products = cursor.fetchall()
                cursor.close()
                conn.close()

                self.employees_id = [product[0] for product in products]
                self.employees_id.insert(0, "Select Employee ID")  # Add an initial default value
                self.employee_entry["values"] = self.employees_id
                self.employee_entry.current(0)  # Select the default value

                # Enable autocompletion for the product_combo
                self.employee_entry.bind('<KeyRelease>')
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Due To: {str(e)}", parent=self.root)

    # open products - dashboard

    def products_create_charts_window(self):
        self.charts_window = tk.Toplevel(self.root)
        screen_width1 = self.root.winfo_screenwidth()
        screen_height1 = self.root.winfo_screenheight()
        self.charts_window.geometry(f"{screen_width1}x{screen_height1}+0+0")
        self.charts_window.title("Charts")
        title_lbl = tk.Label(self.charts_window, text="Products Charts Window", font=("Great Vibes", 27, "bold"),
                             fg="white", bg="#00555B")
        title_lbl.place(x=-50, y=0, width=1500, height=45)
        main_frame = Frame(self.charts_window, bd=2, bg="white", )
        main_frame.place(x=10, y=50, width=1260, height=600)
        left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                 font=("Great Vibes", 12, "bold"))
        left_frame.place(x=0, y=0, width=615, height=580)

        distribution_frame = Frame(left_frame)
        distribution_frame.pack(side="top", fill="both", expand=True)
        self.create_distribution_chart_products(distribution_frame)

        Right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                 font=("Great Vibes", 12, "bold"))
        Right_frame.place(x=640, y=0, width=615, height=580)


        products_frame = Frame(Right_frame)
        products_frame.pack(side="top", fill="both", expand=True)
        self.create_top_products_chart(products_frame)

    def fetch_distribution_data_products_active_inactive(self):
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT COUNT(*) FROM products WHERE status = 'Active'")
        active_count = my_cursor.fetchone()[0]
        my_cursor.execute("SELECT COUNT(*) FROM products WHERE status = 'Discontinued'")
        discontinued_count = my_cursor.fetchone()[0]
        my_cursor.execute("SELECT COUNT(*) FROM products WHERE status = 'Out Of Stock'")
        Out_Of_Stock_count = my_cursor.fetchone()[0]
        conn.close()
        return [active_count, discontinued_count,Out_Of_Stock_count]

    def create_distribution_chart_products(self, parent_frame):
        fig, ax = plt.subplots()

        # Fetch data and create the distribution chart
        data = self.fetch_distribution_data_products_active_inactive()
        labels = ["Active", "Discontinued", "Out Of Stock"]
        colors = ['#00cc99', '#008066', '#009688']

        ax.pie(data, labels=labels, colors=colors, autopct='%1.1f%%',
               shadow=True, startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title("Distribution of Active, Discontinued, and Out Of Stock Products")

        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Add navigation toolbar
        toolbar = NavigationToolbar2Tk(canvas, parent_frame)
        toolbar.update()
        canvas.get_tk_widget().pack()

    def fetch_top_products_by_qty(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="1234",
                database="inventory_management"
            )

            my_cursor = conn.cursor()

            my_cursor.execute("""
               SELECT name, SUM(qty) as qty
               FROM products
               GROUP BY name
               ORDER BY qty DESC
               LIMIT 5
           """)

            data = my_cursor.fetchall()
            conn.close()
            return data
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
            return None

    def create_top_products_chart(self, parent_frame):
        fig = Figure(figsize=(6, 5.3))
        ax = fig.add_subplot(111)

        # Fetch data and create the top categories by product count chart
        data = self.fetch_top_products_by_qty()
        products = [item[0] for item in data]
        product_counts = [item[1] for item in data]

        max_display_products = 10  # Maximum number of categories to display
        if len(products) > max_display_products:
            products = products[:max_display_products]
            product_counts = product_counts[:max_display_products]
            products.append("Other")
            product_counts.append(sum(product_counts[max_display_products:]))

        ax.bar(products, product_counts, color='#009688')  # Use the theme color #009688
        ax.set_title("Top products By Qty")
        ax.set_xlabel("products")

        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        # Add navigation toolbar
        toolbar = NavigationToolbar2Tk(canvas, parent_frame)
        toolbar.update()
        canvas.get_tk_widget().pack()

    # open categories - dashboard
    def categories_create_charts_window(self):
        self.charts_window = tk.Toplevel(self.root)
        screen_width1 = self.root.winfo_screenwidth()
        screen_height1 = self.root.winfo_screenheight()
        self.charts_window.geometry(f"{screen_width1}x{screen_height1}+0+0")
        self.charts_window.title("Charts")
        title_lbl = tk.Label(self.charts_window, text="Categories Charts Window", font=("Great Vibes", 27, "bold"),
                             fg="white", bg="#00555B")
        title_lbl.place(x=-50, y=0, width=1500, height=45)
        main_frame = Frame(self.charts_window, bd=2, bg="white", )
        main_frame.place(x=10, y=50, width=1260, height=600)
        left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                 font=("Great Vibes", 12, "bold"))
        left_frame.place(x=0, y=0, width=615, height=580)

        distribution_frame = Frame(left_frame)
        distribution_frame.pack(side="top", fill="both", expand=True)
        self.create_distribution_chart(distribution_frame)


        Right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                 font=("Great Vibes", 12, "bold"))
        Right_frame.place(x=640, y=0, width=615, height=580)

        categories_frame = Frame(Right_frame)
        categories_frame.pack(side="top", fill="both", expand=True)
        self.create_top_categories_chart(categories_frame)

    def create_distribution_chart(self, parent_frame):
        fig, ax = plt.subplots()

        # Fetch data and create the distribution chart
        data = self.fetch_distribution_data()
        labels = ["Active", "Inactive"]
        colors = ['#00cc99', '#008066']

        ax.pie(data, labels=labels, colors=colors, autopct='%1.1f%%',
               shadow=True, startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title("Distribution of Active and Inactive Categories")

        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Add navigation toolbar
        toolbar = NavigationToolbar2Tk(canvas, parent_frame)
        toolbar.update()
        canvas.get_tk_widget().pack()

    def create_top_categories_chart(self, parent_frame):
        fig = Figure(figsize=(6, 5.3))
        ax = fig.add_subplot(111)

        # Fetch data and create the top categories by product count chart
        data = self.fetch_top_categories_data()
        categories = [item[0] for item in data]
        product_counts = [item[1] for item in data]

        max_display_categories = 10  # Maximum number of categories to display
        if len(categories) > max_display_categories:
            categories = categories[:max_display_categories]
            product_counts = product_counts[:max_display_categories]
            categories.append("Other")
            product_counts.append(sum(product_counts[max_display_categories:]))

        ax.bar(categories, product_counts, color='#009688')  # Use the theme color #009688
        ax.set_title("Top Categories by Product Count")
        ax.set_xlabel("Categories")
        ax.set_ylabel("Product Count")

        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        # Add navigation toolbar
        toolbar = NavigationToolbar2Tk(canvas, parent_frame)
        toolbar.update()
        canvas.get_tk_widget().pack()

    def fetch_distribution_data(self):
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT COUNT(*) FROM categories WHERE active = 'Yes'")
        active_count = my_cursor.fetchone()[0]
        my_cursor.execute("SELECT COUNT(*) FROM categories WHERE active = 'No'")
        inactive_count = my_cursor.fetchone()[0]
        conn.close()
        return [active_count, inactive_count]

    def fetch_top_categories_data(self):
        # Connect to the database and fetch data for the chart
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute("""
               SELECT category, COUNT(*) as product_count
               FROM products
               GROUP BY category
               ORDER BY product_count DESC
               LIMIT 5
           """)
        data = my_cursor.fetchall()
        conn.close()
        return data

        # open orders - dashboard

    # open orders - dashboard

    def orders_create_charts_window(self):
        self.charts_orders_window = tk.Toplevel(self.root)
        screen_width1 = self.root.winfo_screenwidth()
        screen_height1 = self.root.winfo_screenheight()
        self.charts_orders_window.geometry(f"{screen_width1}x{screen_height1}+0+0")
        self.charts_orders_window.title("Charts")
        title_lbl = tk.Label(self.charts_orders_window, text="Orders Charts Window",
                                font=("Great Vibes", 27, "bold"),
                                fg="white", bg="#00555B")
        title_lbl.place(x=-50, y=0, width=1500, height=45)
        main_frame = Frame(self.charts_orders_window, bd=2, bg="white", )
        main_frame.place(x=10, y=50, width=1260, height=600)
        left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                    font=("Great Vibes", 12, "bold"))
        left_frame.place(x=0, y=0, width=615, height=580)

        distribution_frame = Frame(left_frame)
        distribution_frame.pack(side="top", fill="both", expand=True)
        self.create_distribution_chart_orders(distribution_frame)

        Right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                     font=("Great Vibes", 12, "bold"))
        Right_frame.place(x=640, y=0, width=615, height=580)

        Report_orders_label = tk.Label(Right_frame, text="Choose Report", font=("Great Vibes", 12, "bold"),
                                bg="white")
        Report_orders_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        Report_orders = ttk.Combobox(Right_frame, font=("Great Vibes", 12, "bold"), width=15, state="readonly")
        Report_orders["values"] = (
        "Choose Report", "All Orders","Close Report", 'New Orders Report', "Canceled Orders Report", "Picked Orders Report",
        "Packed Orders Report","Staged Orders Report","Loaded Orders Report","Shipped Orders Report")
        Report_orders.current(0)
        Report_orders.grid(row=0, column=1, padx=10, pady=5, sticky=W)
        self.Report_orders_serach = Report_orders

        Apply_btn = Button(Right_frame, text="Apply", font=("Great Vibes", 12, "bold"), width=10,command=self.fetch_data_orders_details_for_report,
                           bg="#00555B",
                           fg="white")
        Apply_btn.grid(row=0, column=2, padx=10, pady=5, sticky=W)
        Export_btn = Button(Right_frame, text="Export", font=("Great Vibes", 12, "bold"), width=10,command=self.export_to_excel,
                            bg="#00555B",
                            fg="white")
        Export_btn.grid(row=0, column=3, padx=10, pady=5, sticky=W)

        table_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=0, y=50, width=600, height=530)
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        self.orders_rep_frame = ttk.Treeview(table_frame, column=(
            "orderId", "customer", "source", "date", "status", "total"), yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.orders_rep_frame.xview)
        scroll_y.config(command=self.orders_rep_frame.yview)
        self.orders_rep_frame.heading("orderId", text="Order ID")
        self.orders_rep_frame.heading("customer", text="Customer")
        self.orders_rep_frame.heading("source", text="Source")
        self.orders_rep_frame.heading("date", text="Date")
        self.orders_rep_frame.heading("status", text="Status")
        self.orders_rep_frame.heading("total", text="Total")
        self.orders_rep_frame["show"] = "headings"

        self.orders_rep_frame.column("orderId", width=150)
        self.orders_rep_frame.column("customer", width=150)
        self.orders_rep_frame.column("source", width=200)
        self.orders_rep_frame.column("date", width=150)
        self.orders_rep_frame.column("status", width=150)
        self.orders_rep_frame.column("total", width=150)
        self.orders_rep_frame.pack(fill=BOTH, expand=1)
        self.orders_rep_frame.tag_configure('button', background='lightblue')
        self.orders_rep_frame.bind("<ButtonRelease-1>")

    def export_to_excel(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], parent=self.charts_orders_window)
        if file_path:
            data = []
            for item in self.orders_rep_frame.get_children():
                data.append(self.orders_rep_frame.item(item, "values"))

            # Define the columns for the Excel file
            columns = ["Order ID", "Customer", "Source", "Date", "Status", "Total"]

            # Create a DataFrame using pandas
            df = pd.DataFrame(data, columns=columns)

            # Save the DataFrame to an Excel file
            excel_path = file_path  # Use the selected file path
            df.to_excel(excel_path, index=False)
            messagebox.showinfo("Export", "Data exported to Excel successfully.", parent=self.charts_orders_window)

    def fetch_data_orders_details_for_report(self):
        selected_rep = self.Report_orders_serach.get()
        print(selected_rep)
        if selected_rep != "Choose Report":
            if selected_rep == "All Orders":
                self.fetch_data_all_orders()
            elif selected_rep =="Close Report":
                self.fetch_data_status_orders("Close- Store")
            elif selected_rep =="New Orders Report":
                self.fetch_data_status_orders("New")
            elif selected_rep == "Canceled Orders Report":
                self.fetch_data_status_orders("Cancelled")
            elif selected_rep == "Picked Orders Report":
                self.fetch_data_status_orders("Picked")
            elif selected_rep == "Packed Orders Report":
                self.fetch_data_status_orders("Packed")
            elif selected_rep == "Staged Orders Report":
                self.fetch_data_status_orders("Staged")
            elif selected_rep == "Loaded Orders Report":
                self.fetch_data_status_orders("Loaded")
            elif selected_rep == "Shipped Orders Report":
                self.fetch_data_status_orders("Shipped")
        else:
            messagebox.showinfo("Choose Any Report", "Please Choose Any Report", parent=self.charts_orders_window)

    def fetch_data_all_orders(self):
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM orders")
        data = my_cursor.fetchall()
        if len(data) != 0:
            self.orders_rep_frame.delete(*self.orders_rep_frame.get_children())
            for i in data:
                self.orders_rep_frame.insert("", END, values=i)
        else:
            messagebox.showinfo("No Results", "No orders found that match the criteria.", parent=self.charts_orders_window)
        conn.commit()
        conn.close()

    def fetch_data_status_orders(self,status):
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM orders WHERE status=%s",(status,))
        data = my_cursor.fetchall()
        if len(data) != 0:
            self.orders_rep_frame.delete(*self.orders_rep_frame.get_children())
            for i in data:
                self.orders_rep_frame.insert("", END, values=i)
        else:
            messagebox.showinfo("No Results", "No orders found that match the criteria.", parent=self.charts_orders_window)
        conn.commit()
        conn.close()

    def create_distribution_chart_orders(self, parent_frame):
        fig, ax = plt.subplots()

        data = self.fetch_distribution_data_orders()
        labels = ["Close- Store", "New","Picked", "Packed","Staged", "Loaded","Shipped", "Cancelled"]
        colors = ['#009688','#76a8a7', '#5c918c','#3a5e5b','#134f5e','#13355e','#191d80','#272dc2']

        ax.pie(data, labels=labels, colors=colors, autopct='%1.1f%%',
                   shadow=True, startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title("Distribution The Status Of Orders")

        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Add navigation toolbar
        toolbar = NavigationToolbar2Tk(canvas, parent_frame)
        toolbar.update()
        canvas.get_tk_widget().pack()

    def fetch_distribution_data_orders(self):
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234",
                                           database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'Close- Store'")
        Close = my_cursor.fetchone()[0]
        my_cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'New'")
        New = my_cursor.fetchone()[0]
        my_cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'Picked'")
        Picked = my_cursor.fetchone()[0]
        my_cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'Packed'")
        Packed = my_cursor.fetchone()[0]
        my_cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'Staged'")
        Staged = my_cursor.fetchone()[0]
        my_cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'Loaded'")
        Loaded = my_cursor.fetchone()[0]
        my_cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'Shipped'")
        Shipped = my_cursor.fetchone()[0]
        my_cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'Cancelled'")
        Cancelled = my_cursor.fetchone()[0]
        conn.close()
        return [Close, New,Picked,Packed,Staged,Loaded,Shipped,Cancelled]

    # open employees
    def employees_create_charts_window(self):
        self.charts_employees_window = tk.Toplevel(self.root)
        screen_width1 = self.root.winfo_screenwidth()
        screen_height1 = self.root.winfo_screenheight()
        self.charts_employees_window.geometry(f"{screen_width1}x{screen_height1}+0+0")
        self.charts_employees_window.title("Charts")
        title_lbl = tk.Label(self.charts_employees_window, text="Orders Charts Window",
                                font=("Great Vibes", 27, "bold"),
                                fg="white", bg="#00555B")
        title_lbl.place(x=-50, y=0, width=1500, height=45)
        main_frame = Frame(self.charts_employees_window, bd=2, bg="white", )
        main_frame.place(x=10, y=50, width=1260, height=600)
        left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                    font=("Great Vibes", 12, "bold"))
        left_frame.place(x=0, y=0, width=615, height=580)

        distribution_frame = Frame(left_frame)
        distribution_frame.pack(side="top", fill="both", expand=True)
        self.create_distribution_chart_employees(distribution_frame)

        Right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                     font=("Great Vibes", 12, "bold"))
        Right_frame.place(x=640, y=0, width=615, height=580)

        Product_label = tk.Label(Right_frame, text="Choose Employee", font=("Great Vibes", 12, "bold"),
                                 bg="white")
        Product_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.var_employees_id = StringVar()

        self.employee_entry = ttk.Combobox(Right_frame, font=("Great Vibes", 12, "bold"), width=18, state="readonly",
                                          textvariable=self.var_employees_id)
        self.employee_entry.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        self.update_employees_values()
        self.var_product_id_serach = self.employee_entry

        Month_label = tk.Label(Right_frame, text="Choose Month", font=("Great Vibes", 12, "bold"),
                                 bg="white")
        Month_label.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        self.var_Month = StringVar()

        self.Month_entry = ttk.Combobox(Right_frame, font=("Great Vibes", 12, "bold"), values=list(range(1, 13)),width=15, state="readonly",
                                          textvariable=self.var_Month)
        self.Month_entry.grid(row=1, column=1, padx=10, pady=5, sticky=W)
        self.Month_entry.current(0)
        self.var_Month_serach = self.Month_entry

        self.var_year = StringVar()
        year_label = tk.Label(Right_frame, text="Choose Year", font=("Great Vibes", 12, "bold"),
                               bg="white")
        year_label.grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)

        self.year_entry = ttk.Combobox(Right_frame, font=("Great Vibes", 12, "bold"), values=list(range(2023, 2099)),
                                        width=15, state="readonly",
                                        textvariable=self.var_year)
        self.year_entry.grid(row=1, column=2, padx=10, pady=5, sticky=W)
        self.year_entry.current(0)
        self.var_year_entry_serach = self.year_entry

        Total_salary_label = tk.Label(Right_frame, text="Total salary:", font=("Great Vibes", 15, "bold"),
                                   bg="white")
        Total_salary_label.place(x=5,y=545)
        self.var_Total_salary= StringVar()

        self.Total_salary = ttk.Entry(Right_frame, width=25, textvariable=self.var_Total_salary,
                                         font=("Great Vibes", 12, "bold"), state='disabled')
        self.Total_salary.place(x=150,y=545)

        Apply_btn = Button(Right_frame, text="Apply", font=("Great Vibes", 12, "bold"), width=10,command=self.fetch_data_employee_for_report,
                           bg="#00555B",
                           fg="white")
        Apply_btn.grid(row=2, column=1, padx=10, pady=5, sticky=W)
        Export_btn = Button(Right_frame, text="Export", font=("Great Vibes", 12, "bold"), width=10,command=self.export_to_excel_employee,
                            bg="#00555B",
                            fg="white")
        Export_btn.grid(row=2, column=2, padx=10, pady=5, sticky=W)

        table_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=0, y=120, width=600, height=420)
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        self.employees_rep_frame = ttk.Treeview(table_frame, column=(
            "employee_no", "employee_name", "date", "login", "logout"), yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.employees_rep_frame.xview)
        scroll_y.config(command=self.employees_rep_frame.yview)
        self.employees_rep_frame.heading("employee_no", text="Employee No")
        self.employees_rep_frame.heading("employee_name", text="Employee Name")
        self.employees_rep_frame.heading("date", text="Date")
        self.employees_rep_frame.heading("login", text="Log In")
        self.employees_rep_frame.heading("logout", text="Log Out")
        self.employees_rep_frame["show"] = "headings"

        self.employees_rep_frame.column("employee_no", width=100)
        self.employees_rep_frame.column("employee_name", width=100)
        self.employees_rep_frame.column("date", width=100)
        self.employees_rep_frame.column("login", width=100)
        self.employees_rep_frame.column("logout", width=100)
        self.employees_rep_frame.pack(fill=BOTH, expand=1)
        self.employees_rep_frame.tag_configure('button', background='lightblue')
        self.employees_rep_frame.bind("<ButtonRelease-1>")

    def export_to_excel_employee(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")],
                                                 initialfile=f"{self.var_product_id_serach.get()}_{self.var_Month_serach.get()}_{self.var_year_entry_serach.get()}.xlsx",
                                                 parent=self.charts_employees_window)
        if file_path:
            data = []
            columns = ["Employee No", "Employee Name", "Date", "Log In", "Log Out", "Total Salary"]
            for item in self.employees_rep_frame.get_children():
                values = self.employees_rep_frame.item(item, "values")
                if len(values) < len(columns):
                    values = values + (None,)  # הוספת None ל-tuple
                data.append(values)

            # Create a DataFrame using pandas
            df = pd.DataFrame(data, columns=columns)

            # Add a row for Total Salary
            total_salary_row = ["", "", "", "", "", self.var_Total_salary.get()]
            df.loc[df.index.max() + 1] = total_salary_row  # הוספת השורה החדשה ל-DataFrame

            # Save the DataFrame to an Excel file
            excel_path = file_path
            df.to_excel(excel_path, index=False)

            # Show a message confirming the export
            messagebox.showinfo("Export", "Data exported to Excel successfully.", parent=self.charts_employees_window)

    def search_by_id(self, id):
        query = "SELECT employeeNo FROM employees WHERE employeeID = %s"
        params = (id,)
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute(query, params)
        data = my_cursor.fetchone()
        conn.close()

        if data:
            employee_no = data[0]
            return employee_no
        else:
            return None

    def search_by_salary(self, id):
        query = "SELECT salary FROM employees WHERE employeeID = %s"
        params = (id,)
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute(query, params)
        data = my_cursor.fetchone()
        conn.close()

        if data:
            employee_no = data[0]
            return employee_no
        else:
            return None

    def fetch_data_employee_for_report(self):
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        employeeNo = self.search_by_id(self.var_employees_id.get())
        month = self.var_Month.get()
        year = str(self.var_year.get())
        month = str(month)

        start_date = f"{year}-{month}-01"
        month = int(month) + 1
        month = str(month)
        end_date = f"{year}-{month}-01"

        my_cursor.execute(
            "SELECT * FROM log_in_out_employees WHERE employee_no = %s AND date >= %s AND date < %s",
            (employeeNo, start_date, end_date))

        data = my_cursor.fetchall()
        if len(data) != 0:
            self.employees_rep_frame.delete(*self.employees_rep_frame.get_children())
            for i in data:
                self.employees_rep_frame.insert("", END, values=i)
            self.calculate_hourly_salary()
        else:
            messagebox.showinfo("No Results", "No results found that match the criteria.",
                                parent=self.charts_employees_window)
        conn.commit()
        conn.close()

    def calculate_hourly_salary(self):
        hourly_wage = self.search_by_salary(self.var_employees_id.get())
        print(hourly_wage)
        total_salary = 0

        for row in self.employees_rep_frame.get_children():
            log_in = self.employees_rep_frame.item(row, "values")[3]
            log_out = self.employees_rep_frame.item(row, "values")[4]

            if log_in and log_out:
                log_in_time = datetime.strptime(log_in, "%H:%M:%S")
                log_out_time = datetime.strptime(log_out, "%H:%M:%S")

                hours_worked = (log_out_time - log_in_time).total_seconds() / 3600
                print(hours_worked)
                salary = hours_worked * hourly_wage
                total_salary += salary

        self.var_Total_salary.set(total_salary)

    def create_distribution_chart_employees(self, parent_frame):
        fig, ax = plt.subplots()

        data = self.fetch_distribution_data_employees()
        labels = ["Manager", "Store employee", "Warehouse employee"]
        colors = ['#00cc99', '#008066', '#009688']

        ax.pie(data, labels=labels, colors=colors, autopct='%1.1f%%',
                   shadow=True, startangle=90)
        ax.axis('equal')
        ax.set_title("Distribution The Type Of Employees")

        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Add navigation toolbar
        toolbar = NavigationToolbar2Tk(canvas, parent_frame)
        toolbar.update()
        canvas.get_tk_widget().pack()

    def fetch_distribution_data_employees(self):
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234",
                                           database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT COUNT(*) FROM employees WHERE type = 'Manager'")
        Manager = my_cursor.fetchone()[0]
        my_cursor.execute("SELECT COUNT(*) FROM employees WHERE type = 'Store employee'")
        Store_employee = my_cursor.fetchone()[0]
        my_cursor.execute("SELECT COUNT(*) FROM employees WHERE type = 'Warehouse employee'")
        Warehouse_employee = my_cursor.fetchone()[0]

        conn.close()
        return [Manager, Store_employee,Warehouse_employee]


    # open windows
    def iExit(self):
        self.iExit= tkinter.messagebox.askyesno("Face recognition", "Are you sure exit this project?", parent=self.root)
        if self.iExit != 0:
            self.root.destroy()
        else:
            return

    def product_details(self):
        self.new_window= Toplevel(self.root)
        self.app= Product(self.new_window)

    def category_details(self):
        self.new_window= Toplevel(self.root)
        self.app= Category(self.new_window)

    def orders_details(self):
        self.new_window= Toplevel(self.root)
        self.app= orders(self.new_window)

    def inventory_details(self):
        self.new_window = Toplevel(self.root)
        self.app = inventory(self.new_window)

    def employees_details(self):
        self.new_window = Toplevel(self.root)
        self.app = employees(self.new_window)

    def checkInOut_details(self):
        self.new_window = Toplevel(self.root)
        self.app = checkInOut(self.new_window)

    def BillingSystem_details(self):
        self.new_window = Toplevel(self.root)
        self.app = BillingSystem(self.new_window)

    # Total
    def total_products(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="1234",
                database="inventory_management"
            )
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM products"
            cursor.execute(query)
            product_count = cursor.fetchone()[0]
            conn.close()
            return product_count
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
            return None

    def total_categories(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="1234",
                database="inventory_management"
            )
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM categories"
            cursor.execute(query)
            categories_count = cursor.fetchone()[0]
            conn.close()
            return categories_count
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
            return None

    def total_orders(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="1234",
                database="inventory_management"
            )
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM orders"
            cursor.execute(query)
            order_count = cursor.fetchone()[0]
            conn.close()
            return order_count
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
            return None

    def total_items(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="1234",
                database="inventory_management"
            )
            cursor = conn.cursor()
            query = "SELECT SUM(qty) FROM products"
            cursor.execute(query)
            total_qty = cursor.fetchone()[0]
            conn.close()
            return total_qty
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
            return None

    def total_employees(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="1234",
                database="inventory_management"
            )
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM employees"
            cursor.execute(query)
            product_count = cursor.fetchone()[0]
            conn.close()
            return product_count
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
            return None

    def total_amount_of_expenses(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="1234",
                database="inventory_management"
            )
            cursor = conn.cursor()
            query = "SELECT SUM(price*qty) FROM products"
            cursor.execute(query)
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
            return None

    def total_amount_of_revenue(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="1234",
                database="inventory_management"
            )
            cursor = conn.cursor()
            query = "SELECT SUM(total) FROM orders"
            cursor.execute(query)
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
            return None


if __name__ == "__main__":
    root = Tk()
    obj = Inventory_Management(root)
    root.mainloop()
