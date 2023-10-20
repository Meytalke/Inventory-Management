import shutil
import smtplib
from tkinter import *
from tkinter import ttk, scrolledtext
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
from datetime import datetime, time
from tkcalendar import Calendar
import time
import os
from tkinter import filedialog


class employees:
    def __init__(self, root):
        self.root = root
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.title("Employees Page")

        bg_img = Image.open(r"C:\Users\meyta\inventory_management_images\Product_bg4.jpg")
        bg_img = bg_img.resize((screen_width, screen_height), Image.BILINEAR)
        self.bg_img = ImageTk.PhotoImage(bg_img)

        bg_label = Label(self.root, image=self.bg_img)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title label
        title_lbl = Label(self.root, text="Employees",
                          font=("Great Vibes", 34, "bold"), bg="#697334", fg="white")
        title_lbl.place(x=0, y=-105, width=1500, relx=0.5, rely=0.19, anchor="center")

        main_frame = Frame(self.root, bd=2, bg="white", )
        main_frame.place(x=10, y=70, width=1260, height=600)

        # ==========variables=============
        self.var_employeeNo = StringVar()
        self.var_employeeID = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_DOB = StringVar()
        self.var_password = StringVar()
        self.var_contact_no = StringVar()
        self.var_gender = StringVar()
        self.var_employee_type = StringVar()
        self.var_salary = StringVar()
        self.var_address = StringVar()
        self.var_creationDate = StringVar()
        self.file_path = ""
        self.var_Serach1 = StringVar()
        self.var_Serach2 = StringVar()

        next_employeet_id = self.get_next_employee_id()
        self.var_employeeNo.set(next_employeet_id)

        # left label frame
        Left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,text= "Employee Details",
                                font=("Great Vibes", 12, "bold"))
        Left_frame.place(x=10, y=10, width=620, height=570)

        employees_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE,
                                   font=("Great Vibes", 12, "bold"))
        employees_frame.place(x=0, y=0, width=610, height=570)

        employeeNo_label = tk.Label(employees_frame, text="Employee No:", font=("Great Vibes", 12, "bold"),
                                   bg="white")
        employeeNo_label.grid(row=0, column=0, padx=7, pady=5, sticky=tk.W)

        employeeNo_entry = ttk.Entry(employees_frame, textvariable=self.var_employeeNo, width=16,
                                    font=("Great Vibes", 12, "bold"), state='disabled')
        employeeNo_entry.grid(row=0, column=1, padx=7, pady=5, sticky=tk.W)

        employeeID_label = tk.Label(employees_frame, text="ID:", font=("Great Vibes", 12, "bold"),
                                    bg="white")
        employeeID_label.grid(row=0, column=2, padx=7, pady=5, sticky=tk.W)

        employeeID_entry = ttk.Entry(employees_frame, textvariable=self.var_employeeID, width=16,
                                     font=("Great Vibes", 12, "bold"))
        employeeID_entry.grid(row=0, column=3, padx=7, pady=5, sticky=tk.W)

        name_label = tk.Label(employees_frame, text="Name:", font=("Great Vibes", 12, "bold"),
                                 bg="white")
        name_label.grid(row=1, column=0, padx=7, pady=5, sticky=tk.W)

        name_entry = ttk.Entry(employees_frame, textvariable=self.var_name, width=16,
                                  font=("Great Vibes", 12, "bold"))
        name_entry.grid(row=1, column=1, padx=7, pady=5, sticky=tk.W)

        email_label = Label(employees_frame, text="Email", font=("Great Vibes", 12, "bold"), bg="white")
        email_label.grid(row=1, column=2, padx=7, sticky=W)
        email_entry = ttk.Entry(employees_frame, textvariable=self.var_email, width=16,
                               font=("Great Vibes", 12, "bold"))
        email_entry.grid(row=1, column=3, padx=7, pady=5, sticky=tk.W)


        DOB_label = tk.Label(employees_frame, text="Date Of Birth:", font=("Great Vibes", 12, "bold"),
                              bg="white")
        DOB_label.grid(row=2, column=0, padx=7, pady=5, sticky=tk.W)

        self.DOB_entry = ttk.Entry(employees_frame, textvariable=self.var_DOB, width=16,
                               font=("Great Vibes", 12, "bold"))
        self.DOB_entry.grid(row=2, column=1, padx=7, pady=5, sticky=tk.W)

        self.DOB_entry.bind("<Button-1>", self.open_calendar_popup)

        password_label = tk.Label(employees_frame, text="Password:", font=("Great Vibes", 12, "bold"),
                               bg="white")
        password_label.grid(row=2, column=2, padx=7, pady=5, sticky=tk.W)

        password_entry = ttk.Entry(employees_frame, textvariable=self.var_password, width=16,
                                font=("Great Vibes", 12, "bold"))
        password_entry.grid(row=2, column=3, padx=7, pady=5, sticky=tk.W)

        contact_no_label = tk.Label(employees_frame, text="Contact No:", font=("Great Vibes", 12, "bold"),
                                    bg="white")
        contact_no_label.grid(row=3, column=2, padx=7, pady=5, sticky=tk.W)

        contact_no_entry = ttk.Entry(employees_frame, textvariable=self.var_contact_no, width=16,
                                     font=("Great Vibes", 12, "bold"))
        contact_no_entry.grid(row=3, column=3, padx=7, pady=5, sticky=tk.W)

        gender_label = Label(employees_frame, text="Gender:", font=("Great Vibes", 12, "bold"),
                                     bg="white")
        gender_label.grid(row=3, column=0, padx=7, sticky=W)
        gender_combo = ttk.Combobox(employees_frame, textvariable=self.var_gender,
                                            font=("Great Vibes", 12, "bold"),
                                            width=16, state="readonly")
        gender_combo["values"] = ("Select Gender", "Male", "Female")
        gender_combo.current(0)
        gender_combo.grid(row=3, column=1, padx=8, pady=10, sticky=W)

        employees_type_label = Label(employees_frame, text="Employees Type:", font=("Great Vibes", 12, "bold"),
                             bg="white")
        employees_type_label.grid(row=4, column=0, padx=7, sticky=W)
        employees_type_combo = ttk.Combobox(employees_frame, textvariable=self.var_employee_type,
                                    font=("Great Vibes", 12, "bold"),
                                    width=16, state="readonly")
        employees_type_combo["values"] = ("Select Type", "Manager", "Store employee", "Warehouse employee")
        employees_type_combo.current(0)
        employees_type_combo.grid(row=4, column=1, padx=8, pady=10, sticky=W)

        salary_label = tk.Label(employees_frame, text="Salary:", font=("Great Vibes", 12, "bold"),
                                      bg="white")
        salary_label.grid(row=4, column=2, padx=7, pady=5, sticky=tk.W)

        salary_entry = ttk.Entry(employees_frame, textvariable=self.var_salary, width=16,
                                       font=("Great Vibes", 12, "bold"))
        salary_entry.grid(row=4, column=3, padx=7, pady=5, sticky=tk.W)

        address_label = tk.Label(employees_frame, text="Address:", font=("Great Vibes", 12, "bold"),
                                     bg="white")
        address_label.grid(row=5, column=0, padx=7, pady=5, sticky=tk.W)

        self.address_text = scrolledtext.ScrolledText(employees_frame, wrap='word',
                                                          font=("Great Vibes", 12, "bold"),
                                                          width=47, height=4)
        self.address_text.grid(row=5, column=1, columnspan=3, padx=7, pady=5, sticky=tk.W)

        self.address_text.bind("<KeyRelease>", self.update_address_value)

        # bbtn frame
        btn_frame = Frame(employees_frame, bd=2,relief=RIDGE, bg="white")
        btn_frame.place(x=0, y=415, width=610, height=120)

        save_btn = Button(btn_frame, text="Save", command=self.add_data, font=("Great Vibes", 12, "bold"),width=14,height=2, bg="#697334", fg="white")
        save_btn.grid(row=0, column=0)

        update_btn = Button(btn_frame, text="Update", command=self.update_data, font=("Great Vibes", 12, "bold"),
                            width=14,height=2, bg="#697334", fg="white")
        update_btn.grid(row=0, column=1)

        delete_btn = Button(btn_frame, text="Delete", command=self.delete_data, font=("Great Vibes", 12, "bold"), width=14,height=2, bg="#697334", fg="white")
        delete_btn.grid(row=0, column=2)

        reset_btn = Button(btn_frame, text="Reset", command=self.reset_data, font=("Great Vibes", 12, "bold"), width=14,height=2, bg="#697334", fg="white")
        reset_btn.grid(row=0, column=3)

        take_photo_btn = Button(btn_frame, command=self.Generate_dataset, text="Take Photo",
                                font=("Great Vibes", 12, "bold"), width=14,height=2, bg="#697334", fg="white")
        take_photo_btn.grid(row=1, column=0)

        choose_image_btn = Button(btn_frame, text="Choose Image",
                                font=("Great Vibes", 12, "bold"), width=14,height=2, bg="#697334", fg="white", command=lambda: self.choose_image(image_label))
        choose_image_btn.grid(row=1, column=1,  sticky=tk.W)

        view_image_btn = Button(btn_frame, text="View Image",
                                font=("Great Vibes", 12, "bold"), width=14,height=2, bg="#697334", fg="white",command=self.view_image)
        view_image_btn.grid(row=1, column=2,  sticky=tk.W)

        email_btn = Button(btn_frame, text="Sent Email",
                                font=("Great Vibes", 12, "bold"), width=14, height=2, bg="#697334", fg="white",command=self.send_gmail)
        email_btn.grid(row=1, column=3, sticky=tk.W)

        image_label = Label(employees_frame, bg="white")

        # Right label frame
        Right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                font=("Great Vibes", 12, "bold"))
        Right_frame.place(x=640, y=20, width=615, height=545)

        # ===========Serach System===============

        Serach_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE,text="Filters",
                                         font=("Great Vibes", 12, "bold"))
        Serach_frame.place(x=0, y=0, width=605, height=180)

        employee_No_Serach_label = tk.Label(Serach_frame, text="Employee No", font=("Great Vibes", 12, "bold"),
                                  bg="white")
        employee_No_Serach_label.grid(row=0, column=0, padx=9, pady=5, sticky=tk.W)

        employee_No_Serach_entry = ttk.Entry(Serach_frame, width=10, font=("Great Vibes", 12, "bold"))
        employee_No_Serach_entry.grid(row=1, column=0, pady=7, padx=9, sticky=W)
        self.employee_No_serach = employee_No_Serach_entry

        employee_ID_Serach_label = tk.Label(Serach_frame, text="Employee ID", font=("Great Vibes", 12, "bold"),
                                  bg="white")
        employee_ID_Serach_label.grid(row=0, column=1, padx=9, pady=5, sticky=tk.W)

        employee_ID_Serach_entry = ttk.Entry(Serach_frame, width=10, font=("Great Vibes", 12, "bold"))
        employee_ID_Serach_entry.grid(row=1, column=1, pady=7, padx=9, sticky=W)
        self.employee_ID_serach = employee_ID_Serach_entry

        name_Serach_label = tk.Label(Serach_frame, text="Name", font=("Great Vibes", 12, "bold"),
                                bg="white")
        name_Serach_label.grid(row=0, column=2, padx=9, pady=5, sticky=tk.W)

        name_Serach_entry = ttk.Entry(Serach_frame, width=10, font=("Great Vibes", 12, "bold"))
        name_Serach_entry.grid(row=1, column=2, pady=7, padx=9, sticky=W)
        self.name_serach = name_Serach_entry

        email_Serach_label = tk.Label(Serach_frame, text="Email", font=("Great Vibes", 12, "bold"),
                                     bg="white")
        email_Serach_label.grid(row=0, column=3, padx=9, pady=5, sticky=tk.W)

        email_Serach_entry = ttk.Entry(Serach_frame, width=10, font=("Great Vibes", 12, "bold"))
        email_Serach_entry.grid(row=1, column=3, pady=7, padx=9, sticky=W)
        self.email_serach = email_Serach_entry

        contact_Serach_label = tk.Label(Serach_frame, text="Contact", font=("Great Vibes", 12, "bold"),
                                      bg="white")
        contact_Serach_label.grid(row=0, column=4, padx=9, pady=5, sticky=tk.W)

        contact_Serach_entry = ttk.Entry(Serach_frame, width=10, font=("Great Vibes", 12, "bold"))
        contact_Serach_entry.grid(row=1, column=4, pady=7, padx=9, sticky=W)
        self.contact_serach = contact_Serach_entry

        gender_Serach_label = tk.Label(Serach_frame, text="Gender", font=("Great Vibes", 12, "bold"),
                                bg="white")
        gender_Serach_label.grid(row=2, column=0, padx=9, pady=5, sticky=tk.W)

        gender_Serach_entry = ttk.Combobox(Serach_frame, width=10, font=("Great Vibes", 12, "bold"), state="readonly")
        gender_Serach_entry["values"] = ("Select", "Male", "Female")
        gender_Serach_entry.current(0)
        gender_Serach_entry.grid(row=3, column=0, pady=7, padx=9, sticky=W)
        self.gender_serach = gender_Serach_entry

        type_Serach_label = tk.Label(Serach_frame, text="Type", font=("Great Vibes", 12, "bold"),
                                bg="white")
        type_Serach_label.grid(row=2, column=1, padx=9, pady=5, sticky=tk.W)

        type_Serach_entry = ttk.Combobox(Serach_frame, width=10, font=("Great Vibes", 12, "bold"), state="readonly")
        type_Serach_entry["values"] = ("Select", "Manager", "Store employee", "Warehouse employee")
        type_Serach_entry.current(0)
        type_Serach_entry.grid(row=3, column=1, pady=7, padx=9, sticky=W)
        self.type_serach = type_Serach_entry

        Serach_btn = Button(Serach_frame, text="Search", font=("Great Vibes", 12, "bold"), width=10,
                            command=self.Serach,
                            bg="#697334",
                            fg="white")
        Serach_btn.place(x=280, y=110)
        showAll_btn = Button(Serach_frame, text="Reset", font=("Great Vibes", 12, "bold"), width=10,
                             command=self.fetch_data,
                             bg="#697334",
                             fg="white")
        showAll_btn.place(x=400, y=110)

        # ===========Table frame===============


        table_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=0, y=180, width=605, height=360)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        self.employee_table = ttk.Treeview(table_frame, column=("employeeNo","employeeID", "name", "email", "DOB",
                                                                "password", "contact","gender","type","salary","address","createDate",
                                                                "image"), xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side= BOTTOM, fill=X)
        scroll_y.pack(side= RIGHT,fill=Y)
        scroll_x.config(command=self.employee_table.xview)
        scroll_y.config(command=self.employee_table.yview)

        self.employee_table.heading("employeeNo", text="Employee No")
        self.employee_table.heading("employeeID", text="Employee ID")
        self.employee_table.heading("name", text="Name")
        self.employee_table.heading("email", text="Email")
        self.employee_table.heading("DOB", text="DOB")
        self.employee_table.heading("password", text="Password")
        self.employee_table.heading("contact", text="Contact")
        self.employee_table.heading("gender", text="Gender")
        self.employee_table.heading("type", text="Employee Type")
        self.employee_table.heading("salary", text="Salary")
        self.employee_table.heading("address", text="Address")
        self.employee_table.heading("createDate", text="Create Date")
        self.employee_table.heading("image", text="Image")
        self.employee_table["show"] = "headings"

        self.employee_table.column("employeeNo",width=100)
        self.employee_table.column("employeeID",width=100)
        self.employee_table.column("name",width=100)
        self.employee_table.column("email",width=100)
        self.employee_table.column("DOB",width=100)
        self.employee_table.column("password",width=100)
        self.employee_table.column("contact",width=100)
        self.employee_table.column("gender",width=100)
        self.employee_table.column("type",width=100)
        self.employee_table.column("salary",width=100)
        self.employee_table.column("address",width=100)
        self.employee_table.column("createDate", width=100)
        self.employee_table.column("image", width=100)

        self.employee_table.pack(fill=BOTH, expand=1)
        self.employee_table.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()

    # =======================function decration=================

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
        self.DOB_entry.delete(0, END)
        self.DOB_entry.insert(0, selected_date)
    def update_address_value(self, event):
        self.var_address.set(event.widget.get("1.0", tk.END).replace("\n", "\n"))

    def get_next_employee_id(self):
        try:
            conn = mysql.connector.connect(host="localhost",
                                           user="root",
                                           passwd="1234",
                                           database="inventory_management")
            if conn.is_connected():
                cursor = conn.cursor()
                # Get the maximum productID from both tables
                cursor.execute('SELECT MAX(employeeNo) FROM employees')
                max_id_products = cursor.fetchone()[0]
                cursor.close()
                conn.close()
                if max_id_products is not None:
                    return max_id_products + 1
                else:
                    return 1
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Due To: {str(e)}", parent=self.root)
        return None

    def view_image(self):
        selected_item = self.employee_table.focus()
        if selected_item:
            data = self.employee_table.item(selected_item, 'values')
            if data[12]:
                self.show_preview_image(data[0])  # Pass the image data directly
            else:
                messagebox.showinfo("Image Not Found", "No image available for this employee.", parent=self.root)
        else:
            messagebox.showwarning("No Product Selected", "Please select a employee to view its image.",
                                   parent=self.root)
    def show_preview_image(self,employeeNo):
        try:
            # Get the directory where the script file is located
            script_directory = os.path.dirname(os.path.abspath(__file__))
            # Construct the path to the images folder
            images_directory = os.path.join(script_directory, "employeesImages")
            # Construct the path to the image file
            image_file_path = os.path.join(images_directory, f"{employeeNo}.jpg")
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
                messagebox.showinfo("Image Not Found", "No image available for this employee.", parent=self.root)

        except Exception as e:
            messagebox.showerror("Error", f"Unable to display the image: {str(e)}", parent=self.root)
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
    def add_data(self):
        if self.var_employeeNo.get() != "" and self.var_employeeID.get() != "" and self.var_name.get() != ""\
                and self.var_email.get() != "" and self.var_password.get() != "" and self.var_contact_no.get() != "":
            try:
                address = self.address_text.get("1.0", tk.END).strip()
                dob_date = datetime.strptime(self.var_DOB.get(), '%d/%m/%Y').strftime('%Y-%m-%d')
                image_file_path = self.file_path

                if image_file_path:
                    # Generate a unique file name for the image
                    unique_file_name = f"{self.var_productID.get()}.jpg"
                    destination_path = f"employeesImages/{unique_file_name}"  # Folder named "images" to store the images

                    # Move the image to the destination folder
                    shutil.copy(image_file_path, destination_path)
                else:
                    # If no image is selected, set the destination_path to None
                    destination_path = None
                conn = mysql.connector.connect(host="localhost",
                                               user="root",
                                               passwd="1234",
                                               database="inventory_management")
                my_cursor = conn.cursor()
                my_cursor.execute("INSERT INTO employees VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                    self.var_employeeNo.get(),
                    self.var_employeeID.get(),
                    self.var_name.get(),
                    self.var_email.get(),
                    dob_date,
                    self.var_password.get(),
                    self.var_contact_no.get(),
                    self.var_gender.get(),
                    self.var_employee_type.get(),
                    self.var_salary.get(),
                    address,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    destination_path,

                ))
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
                messagebox.showinfo("Success", "Employee has been added Successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

        else:
             messagebox.showerror("Error", "All Fields are required", parent=self.root)

    # ==================fetch data====================
    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost",
                                       user="root",
                                       passwd="1234",
                                       database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM employees")
        data = my_cursor.fetchall()
        if len(data) != 0:
            self.employee_table.delete(*self.employee_table.get_children())
            for i in data:
                image_data = i[12]
                self.employee_table.insert("", END, values=i[:-1] + ("Yes" if image_data else "None",))
            conn.commit()
        conn.close()
    # ============== get cursor====================
    def get_cursor(self,event=""):
        cursor_focus = self.employee_table.focus()
        content = self.employee_table.item(cursor_focus)
        data = content["values"]
        DOB = datetime.strptime(data[4], "%Y-%m-%d")
        formatted_date = DOB.strftime("%d/%m/%Y")
        self.var_employeeNo.set(data[0])
        self.var_employeeID.set(data[1]),
        self.var_name.set(data[2]),
        self.var_email.set(data[3]),
        self.var_DOB.set(formatted_date),
        self.var_password.set(data[5]),
        self.var_contact_no.set(data[6]),
        self.var_gender.set(data[7]),
        self.var_employee_type.set(data[8]),
        self.var_salary.set(data[9]),
        self.address_text.delete("1.0", "end")
        self.address_text.insert("1.0", data[10])
    # update
    def update_data(self):
        if self.var_employeeNo.get() != "" and self.var_employeeID.get() != "" and self.var_name.get() != "" \
                and self.var_email.get() != "" and self.var_password.get() != "" and self.var_contact_no.get() != "":
            try:
                Update = messagebox.askyesno("Update", "Do you want to update this employee's details", parent=self.root)
                if Update:
                    address = self.address_text.get("1.0", tk.END).strip()
                    dob_date = datetime.strptime(self.var_DOB.get(), '%d/%m/%Y').strftime('%Y-%m-%d')
                    unique_file_name = f"{self.var_employeeNo.get()}.jpg"
                    destination_path = f"employeesImages/{unique_file_name}"
                    conn = mysql.connector.connect(host="localhost", user="root", passwd="1234",
                                                   database="inventory_management")
                    my_cursor = conn.cursor()
                    if os.path.isfile(self.file_path):
                        shutil.copy(self.file_path, destination_path)
                    my_cursor.execute(
                        "UPDATE employees SET employeeID=%s,name=%s,email=%s,DOB=%s,password=%s,contact=%s,gender=%s,type=%s,salary=%s,address=%s ,image=%s WHERE employeeNo=%s",
                        (
                            self.var_employeeID.get(),
                            self.var_name.get(),
                            self.var_email.get(),
                            dob_date,
                            self.var_password.get(),
                            self.var_contact_no.get(),
                            self.var_gender.get(),
                            self.var_employee_type.get(),
                            self.var_salary.get(),
                            address,
                            destination_path,
                            self.var_employeeNo.get()
                        ))
                    messagebox.showinfo("Success", "Employee details successfully updated", parent=self.root)
                    conn.commit()
                    self.fetch_data()
                    self.reset_data()
                    conn.close()
                else:
                    if not Update:
                        return
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

        else:
            messagebox.showerror("Error", "All Fields are required", parent=self.root)

    #delete
    def delete_data(self):
        if self.var_employeeNo.get() == "":
            messagebox.showerror("Error", "Employee No must be required", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Delete", "Do you want to delete this employee", parent=self.root)
                if delete:
                     conn = mysql.connector.connect(host="localhost", user="root", passwd="1234",
                                           database="inventory_management")
                     my_cursor = conn.cursor()
                     sql = "DELETE FROM employees WHERE employeeNo=%s"
                     val = (self.var_employeeNo.get(),)
                     my_cursor.execute(sql, val)
                else:
                    if not delete:
                        return
                conn.commit()
                conn.close()
                self.fetch_data()
                messagebox.showinfo("Delete", "Successfully deleted employee", parent= self.root)
                self.reset_data()
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
    # reset
    def reset_data(self):
        self.var_employeeNo.set(self.get_next_employee_id())
        self.var_employeeID.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_DOB.set("")
        self.var_password.set("")
        self.var_contact_no.set("")
        self.var_gender.set("Select Gender")
        self.var_employee_type.set("Select Type")
        self.var_salary.set("")
        self.var_address.set("")  # Clear the description variable
        self.address_text.delete("1.0", "end")  # Clear the description text
        self.file_path = ""

    # ========== Generate data set or Take photo sample====
    def Generate_dataset(self):
        if self.var_employeeNo.get() != "" and self.var_employeeID.get() != "" and self.var_name.get() != "" \
                and self.var_email.get() != "" and self.var_password.get() != "" and self.var_contact_no.get() != "":
            try:
                    conn = mysql.connector.connect(host="localhost", user="root", passwd="1234",
                                                   database="inventory_management")
                    my_cursor = conn.cursor()
                    my_cursor.execute("SELECT * FROM employees")
                    my_result = my_cursor.fetchall()
                    id = 0
                    for x in my_result:
                        id += 1
                    address = self.address_text.get("1.0", tk.END).strip()
                    dob_date = datetime.strptime(self.var_DOB.get(), '%d/%m/%Y').strftime('%Y-%m-%d')
                    my_cursor.execute(
                        "UPDATE employees SET employeeID=%s,name=%s,email=%s,DOB=%s,password=%s,contact=%s,gender=%s,type=%s,salary=%s,address=%s WHERE employeeNo=%s",
                        (
                            self.var_employeeID.get(),
                            self.var_name.get(),
                            self.var_email.get(),
                            dob_date,
                            self.var_password.get(),
                            self.var_contact_no.get(),
                            self.var_gender.get(),
                            self.var_employee_type.get(),
                            self.var_salary.get(),
                            address,
                            self.var_employeeNo.get() == id+1
                        )
                    )
                    conn.commit()
                    conn.close()

                    # ========== Load predefined data on face frontal from opencv=======
                    face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                    def face_cropped(img):
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
                        # scaling factor = 1.3
                        # Minimum Neighbor = 5
                        for (x, y, w, h) in faces:
                            face_cropped = img[y:y+h, x:x+w]
                            return face_cropped
                    cap = cv2.VideoCapture(0)
                    img_id = 0
                    while True:
                        ret, my_frame = cap.read()
                        cropped_face = face_cropped(my_frame)
                        if cropped_face is not None:
                            img_id += 1
                            face = cv2.resize(cropped_face, (450, 450))
                            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                            file_name_path = "employeesForLogInOut/employee." + str(self.var_employeeNo.get()) + "." + str(img_id) + ".jpg"
                            cv2.imwrite(file_name_path, face)
                            cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                            cv2.imshow("Cropped Face", face)
                            if cv2.waitKey(1) == 13 or int(img_id) == 20:
                                break
                    cap.release()
                    cv2.destroyAllWindows()
                    messagebox.showinfo("Result", "Generating data sets compiled!", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
        else:
            messagebox.showerror("Error", "All Fields are required", parent=self.root)

    def send_gmail2(self):
        try:
            ob = smtplib.SMTP("smtp.gmail.com", 587)
            ob.starttls()
            ob.login(self.sender_Entry.get(), self.password_Entry.get())
            message = self.email_textarea.get(1.0, END)
            ob.sendmail(self.sender_Entry.get(), self.reciever_Entry.get(), message)
            ob.quit()
            messagebox.showinfo("Success", "login details is successfully sent", parent=self.root)
        except:
            messagebox.showerror("Error", "Somthing went wrong, Please try again", parent=self.root)


    def send_gmail(self):
        if self.var_employeeNo.get() != "" and self.var_employeeID.get() != "" and self.var_name.get() != "" \
                and self.var_email.get() != "" and self.var_password.get() != "" and self.var_contact_no.get() != "":
            send_gmail = Toplevel()
            send_gmail.title("Sent Gmail")
            send_gmail.config(bg="#2f3030")
            send_gmail.resizable(0, 0)
            senderFrame = LabelFrame(send_gmail, text="Sender", font=("Great Vibes", 12, "bold"), bd=6,
                                     bg="#2f3030",
                                     fg="white")
            senderFrame.grid(row=0, column=0, padx=10, pady=8)
            gmailIdLabel = Label(senderFrame, text="Sender's Gmail", font=("Great Vibes", 12, "bold"), bg="#2f3030",
                                 fg="white")
            gmailIdLabel.grid(row=0, column=0, padx=10, pady=8)
            self.sender_Entry = Entry(senderFrame, font=("Great Vibes", 12, "bold"), bd=2, width=20, bg="white")
            self.sender_Entry.grid(row=0, column=1, padx=10, pady=8)

            passwordLabel = Label(senderFrame, text="Password", font=("Great Vibes", 12, "bold"), bg="#2f3030",
                                  fg="white")
            passwordLabel.grid(row=1, column=0, padx=10, pady=8)
            self.password_Entry = Entry(senderFrame, font=("Great Vibes", 12, "bold"), bd=2, width=20, bg="white",
                                        show='*')
            self.password_Entry.grid(row=1, column=1, padx=10, pady=8)

            recipient_Frame = LabelFrame(send_gmail, text="Recipient", font=("Great Vibes", 12, "bold"), bd=6,
                                         bg="#2f3030", fg="white")
            recipient_Frame.grid(row=1, column=0, padx=10, pady=8)
            reciever_Label = Label(recipient_Frame, text="Gmail Address", font=("Great Vibes", 12, "bold"),
                                   bg="#2f3030",
                                   fg="white")
            reciever_Label.grid(row=0, column=0, padx=10, pady=8)

            self.reciever_Entry = Entry(recipient_Frame, font=("Great Vibes", 12, "bold"), bd=2, width=20,
                                        bg="white", textvariable=self.var_email)
            self.reciever_Entry.grid(row=0, column=1, padx=10, pady=8)

            message_Label = Label(recipient_Frame, text="Message", font=("Great Vibes", 12, "bold"),
                                  bg="#2f3030",
                                  fg="white")
            message_Label.grid(row=1, column=0, padx=10, pady=8)

            self.email_textarea = Text(recipient_Frame, font=("Great Vibes", 12, "bold"), bd=2, relief=SUNKEN,
                                       width=40,
                                       height=11)
            self.email_textarea.grid(row=2, column=0, columnspan=2)
            self.email_textarea.delete(1.0, END)
            self.email_textarea.insert(END, "Hello " + self.var_name.get() + "\nYour login details are:\n" + "Email: "
                                       + self.var_email.get() + "\nPassword: " + self.var_password.get())

            send_btn = Button(send_gmail, text="Send", font=("Great Vibes", 12, "bold"), command=self.send_gmail2)
            send_btn.grid(row=3, column=0)
        else:
            messagebox.showerror("Error", "All Fields are required", parent=self.root)

    def Serach(self):
        selected_employee_No = self.employee_No_serach.get()
        selected_employee_ID = self.employee_ID_serach.get()
        selected_name = self.name_serach.get()
        selected_email = self.email_serach.get()
        selected_contact = self.contact_serach.get()
        selected_gender = self.gender_serach.get()
        selected_type = self.type_serach.get()

        query = "SELECT * FROM employees WHERE 1=1"

        if selected_employee_No:
            query += f" AND employeeNo = '{selected_employee_No}'"
        if selected_employee_ID:
            query += f" AND employeeID = '{selected_employee_ID}'"
        if selected_name:
            query += f" AND name = '{selected_name}'"
        if selected_email:
            query += f" AND email = '{selected_email}'"
        if selected_contact:
            query += f" AND contact = '{selected_contact}'"
        if selected_gender != "Select":
            query += f" AND gender = '{selected_gender}'"
        if selected_type != "Select":
            query += f" AND type = '{selected_type}'"

        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute(query)
        data = my_cursor.fetchall()

        if len(data) != 0:
            self.employee_table.delete(*self.employee_table.get_children())
            for i in data:
                self.employee_table.insert("", END, values=i)
            conn.commit()
        else:
            messagebox.showinfo("No Results", "No matching records found.", parent=self.root)

        conn.close()

if __name__ == "__main__":
    root = Tk()
    obj = employees(root)
    root.mainloop()