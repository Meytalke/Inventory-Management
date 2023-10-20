import smtplib
from tkinter import *
from tkinter import ttk, filedialog
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
import cv2
import os
import numpy as np
import random
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from email.mime.text import MIMEText

class checkInOut:
    def __init__(self, root):
        self.root = root
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.title("Employee Check-In/Out System")

        self.var_employeeNo = StringVar()
        self.var_employeeID = StringVar()
        self.var_email = StringVar()
        self.var_password = StringVar()
        self.var_contact_no = StringVar()
        self.var_type = StringVar()
        self.var_type1 = StringVar()
        self.var_type2 = StringVar()
        self.var_id_for_sent= StringVar()
        self.var_code = StringVar()
        self.is_send = 0

        bg_img = Image.open(r"C:\Users\meyta\inventory_management_images\Product_bg4.jpg")
        bg_img = bg_img.resize((screen_width, screen_height), Image.BILINEAR)
        self.bg_img = ImageTk.PhotoImage(bg_img)

        bg_label = Label(self.root, image=self.bg_img)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title label
        title_lbl = Label(self.root, text="Employee Check-In/Out System",
                          font=("Great Vibes", 34, "bold"), bg="#4c7344", fg="white")
        title_lbl.place(x=0, y=-105, width=1500, relx=0.5, rely=0.19, anchor="center")

        main_frame = Frame(self.root, bd=2, bg="white", )
        main_frame.place(x=10, y=70, width=1260, height=600)

        # left label frame
        manual_Entry_frame = tk.LabelFrame(main_frame, bd=2, bg="white", relief=tk.RIDGE,text="Manual Entry",
                                   font=("Great Vibes", 12, "bold"))
        manual_Entry_frame.place(x=10, y=10, width=615, height=200)

        type_label = Label(manual_Entry_frame, text="Check In/Out:", font=("Great Vibes", 12, "bold"),
                                     bg="white")
        type_label.grid(row=0, column=0, padx=7, sticky=W)
        type_combo = ttk.Combobox(manual_Entry_frame, textvariable=self.var_type,
                                            font=("Great Vibes", 12, "bold"),
                                            width=17, state="readonly")
        type_combo["values"] = ("Select", "Check In", "Check Out")
        type_combo.current(0)
        type_combo.grid(row=0, column=1, padx=8, pady=10, sticky=W)

        employeeNo_label = tk.Label(manual_Entry_frame, text="Employee No:", font=("Great Vibes", 12, "bold"),
                                    bg="white")
        employeeNo_label.grid(row=0, column=2, padx=7, pady=5, sticky=tk.W)

        employeeNo_entry = ttk.Entry(manual_Entry_frame, textvariable=self.var_employeeNo, width=17,
                                     font=("Great Vibes", 12, "bold"))
        employeeNo_entry.grid(row=0, column=3, padx=7, pady=5, sticky=tk.W)

        employeeID_label = tk.Label(manual_Entry_frame, text="ID:", font=("Great Vibes", 12, "bold"),
                                    bg="white")
        employeeID_label.grid(row=1, column=0, padx=7, pady=5, sticky=tk.W)

        employeeID_entry = ttk.Entry(manual_Entry_frame, textvariable=self.var_employeeID, width=17,
                                     font=("Great Vibes", 12, "bold"))
        employeeID_entry.grid(row=1, column=1, padx=7, pady=5, sticky=tk.W)

        email_label = Label(manual_Entry_frame, text="Email", font=("Great Vibes", 12, "bold"), bg="white")
        email_label.grid(row=1, column=2, padx=7, sticky=W)
        email_entry = ttk.Entry(manual_Entry_frame, textvariable=self.var_email, width=17,
                                font=("Great Vibes", 12, "bold"))
        email_entry.grid(row=1, column=3, padx=7, pady=5, sticky=tk.W)

        password_label = tk.Label(manual_Entry_frame, text="Password:", font=("Great Vibes", 12, "bold"),
                                  bg="white")
        password_label.grid(row=2, column=0, padx=7, pady=5, sticky=tk.W)

        password_entry = ttk.Entry(manual_Entry_frame, textvariable=self.var_password, width=17,
                                   font=("Great Vibes", 12, "bold"))
        password_entry.grid(row=2, column=1, padx=7, pady=5, sticky=tk.W)

        save_btn = Button(manual_Entry_frame, text="Save", font=("Great Vibes", 12, "bold"), width=10, bg="#4c7344",fg="white",command=self.add_data_manual)
        save_btn.place(x=250,y=130)

        facial_recognition_frame = tk.LabelFrame(main_frame, bd=2, bg="white", relief=tk.RIDGE,
                                                 text="Facial Recognition Employee Entry and Exit System",
                                                 font=("Great Vibes", 12, "bold"))
        facial_recognition_frame.place(x=10, y=220, width=615, height=130)

        type1_label = Label(facial_recognition_frame, text="Check In/Out:", font=("Great Vibes", 12, "bold"),
                           bg="white")
        type1_label.grid(row=0, column=0, padx=7, sticky=W)
        type1_combo = ttk.Combobox(facial_recognition_frame, textvariable=self.var_type1,
                                  font=("Great Vibes", 12, "bold"),
                                  width=17, state="readonly")
        type1_combo["values"] = ("Select", "Check In", "Check Out")
        type1_combo.current(0)
        type1_combo.grid(row=0, column=1, padx=8, pady=10, sticky=W)

        face_recognition = tk.Button(facial_recognition_frame, text="Face Recognition", cursor="hand2", command=self.face_Recognition,
                         font=("Great Vibes", 12, "bold"), width=15, bg="#4c7344", fg="white")
        face_recognition.place(x=230,y=50)

        Single_entry_or_exit_frame = tk.LabelFrame(main_frame, bd=2, bg="white", relief=tk.RIDGE,
                                                 text="One-time entry/exit using a code sent to email",
                                                 font=("Great Vibes", 12, "bold"))
        Single_entry_or_exit_frame.place(x=10, y=355, width=615, height=205)

        type2_label = Label(Single_entry_or_exit_frame, text="Check In/Out:", font=("Great Vibes", 12, "bold"),
                            bg="white")
        type2_label.grid(row=0, column=0, padx=7, sticky=W)
        type2_combo = ttk.Combobox(Single_entry_or_exit_frame, textvariable=self.var_type2,
                                   font=("Great Vibes", 12, "bold"),
                                   width=17, state="readonly")
        type2_combo["values"] = ("Select", "Check In", "Check Out")
        type2_combo.current(0)
        type2_combo.grid(row=0, column=1, padx=8, pady=10, sticky=W)

        Id_label = Label(Single_entry_or_exit_frame, text="ID", font=("Great Vibes", 12, "bold"), bg="white")
        Id_label.grid(row=0, column=2, padx=7, sticky=W)
        Id_entry = ttk.Entry(Single_entry_or_exit_frame, textvariable=self.var_id_for_sent, width=19,
                                font=("Great Vibes", 12, "bold"))
        Id_entry.grid(row=0, column=3, padx=7, pady=5, sticky=tk.W)

        Send_btn = Button(Single_entry_or_exit_frame, text="Send", font=("Great Vibes", 12, "bold"), width=10, bg="#4c7344",
                          fg="white",command=self.send_gmail)
        Send_btn.place(x=250, y=60)

        code_label = Label(Single_entry_or_exit_frame, text="Code:", font=("Great Vibes", 12, "bold"),
                                     bg="white")
        code_label.place(x=10,y=100)
        code_entry = ttk.Entry(Single_entry_or_exit_frame, width=19,
                                         font=("Great Vibes", 12, "bold"),textvariable=self.var_code)
        code_entry.place(x=100,y=100)

        apply_btn = Button(Single_entry_or_exit_frame, text="Apply", font=("Great Vibes", 12, "bold"), width=10,
                          bg="#4c7344",
                          fg="white",command=self.apply_data)
        apply_btn.place(x=250, y=130)

        Right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,text="Filters",
                                 font=("Great Vibes", 12, "bold"))
        Right_frame.place(x=640, y=10, width=615, height=550)

        Serach_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE,
                                 font=("Great Vibes", 12, "bold"))
        Serach_frame.place(x=0, y=0, width=610, height=100)

        employee_No_Serach_label = tk.Label(Serach_frame, text="Employee No", font=("Great Vibes", 12, "bold"),
                                            bg="white")
        employee_No_Serach_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        employee_No_Serach_entry = ttk.Entry(Serach_frame, width=11, font=("Great Vibes", 12, "bold"))
        employee_No_Serach_entry.grid(row=1, column=0, pady=7, padx=10, sticky=W)
        self.employee_No_serach = employee_No_Serach_entry


        name_Serach_label = tk.Label(Serach_frame, text="Name", font=("Great Vibes", 12, "bold"),
                                     bg="white")
        name_Serach_label.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        name_Serach_entry = ttk.Entry(Serach_frame, width=11, font=("Great Vibes", 12, "bold"))
        name_Serach_entry.grid(row=1, column=1, pady=7, padx=10, sticky=W)
        self.name_serach = name_Serach_entry


        Serach_btn = Button(Serach_frame, text="Search", font=("Great Vibes", 12, "bold"), width=9,
                            command=self.Serach,
                            bg="#4c7344",
                            fg="white")
        Serach_btn.grid(row=1, column=2, pady=7, padx=10, sticky=W)
        showAll_btn = Button(Serach_frame, text="Reset", font=("Great Vibes", 12, "bold"), width=9,
                             command=self.fetch_data,
                             bg="#4c7344",
                             fg="white")
        showAll_btn.grid(row=1, column=3, pady=7, padx=10, sticky=W)

        export_btn = Button(Serach_frame, text="Export", font=("Great Vibes", 12, "bold"), width=9,
                             bg="#4c7344",
                             fg="white",command=self.export_to_excel)
        export_btn.grid(row=1, column=4, pady=7, padx=10, sticky=W)

        table_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=0, y=105, width=605, height=420)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        self.log_in_out_employees_table = ttk.Treeview(table_frame, column=(
        "employeeNo", "employeeName","date","entryTime", "exitTime"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.log_in_out_employees_table.xview)
        scroll_y.config(command=self.log_in_out_employees_table.yview)

        self.log_in_out_employees_table.heading("employeeNo", text="Employee No")
        self.log_in_out_employees_table.heading("employeeName", text="Employee Name")
        self.log_in_out_employees_table.heading("entryTime", text="Entry Time")
        self.log_in_out_employees_table.heading("exitTime", text="Exit Time")
        self.log_in_out_employees_table.heading("date", text="Date")
        self.log_in_out_employees_table["show"] = "headings"

        self.log_in_out_employees_table.column("employeeNo", width=100)
        self.log_in_out_employees_table.column("employeeName", width=100)
        self.log_in_out_employees_table.column("entryTime", width=100)
        self.log_in_out_employees_table.column("exitTime", width=100)
        self.log_in_out_employees_table.column("date", width=100)

        self.log_in_out_employees_table.pack(fill=BOTH, expand=1)
        self.log_in_out_employees_table.bind("<ButtonRelease>")
        self.fetch_data()

    def Serach(self):
        selected_employee_No = self.employee_No_serach.get()
        selected_name = self.name_serach.get()

        query = "SELECT * FROM log_in_out_employees WHERE 1=1"

        if selected_employee_No:
            query += f" AND employee_no = '{selected_employee_No}'"
        if selected_name:
            query += f" AND employee_name = '{selected_name}'"

        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute(query)
        data = my_cursor.fetchall()

        if len(data) != 0:
            self.log_in_out_employees_table.delete(*self.log_in_out_employees_table.get_children())
            for i in data:
                self.log_in_out_employees_table.insert("", END, values=i)
            conn.commit()
        else:
            messagebox.showinfo("No Results", "No matching records found.", parent=self.root)

        conn.close()
    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost",
                                       user="root",
                                       passwd="1234",
                                       database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM log_in_out_employees")
        data = my_cursor.fetchall()
        if len(data) != 0:
            self.log_in_out_employees_table.delete(*self.log_in_out_employees_table.get_children())
            for i in data:
                self.log_in_out_employees_table.insert("", END, values=i)
            conn.commit()
        conn.close()

    def name_of_employee(self,employeeNo):
        try:
            conn = mysql.connector.connect(host="localhost",
                                           user="root",
                                           passwd="1234",
                                           database="inventory_management")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT name FROM employees WHERE employeeNo = %s", (employeeNo,))
            employee_name = my_cursor.fetchone()
            if employee_name:
                return employee_name[0]
            else:
                return "Employee not found"
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def id_of_employee(self,employeeNo):
        try:
            conn = mysql.connector.connect(host="localhost",
                                           user="root",
                                           passwd="1234",
                                           database="inventory_management")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT employeeID FROM employees WHERE employeeNo = %s", (employeeNo,))
            id = my_cursor.fetchone()
            if id:
                return id[0]
            else:
                return "Employee not found"
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def email_of_employee(self,employeeNo):
        try:
            conn = mysql.connector.connect(host="localhost",
                                           user="root",
                                           passwd="1234",
                                           database="inventory_management")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT email FROM employees WHERE employeeNo = %s", (employeeNo,))
            email = my_cursor.fetchone()
            if email:
                return email[0]
            else:
                return "Employee not found"
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def password_of_employee(self,employeeNo):
        try:
            conn = mysql.connector.connect(host="localhost",
                                           user="root",
                                           passwd="1234",
                                           database="inventory_management")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT password FROM employees WHERE employeeNo = %s", (employeeNo,))
            password = my_cursor.fetchone()
            if password:
                return password[0]
            else:
                return "Employee not found"
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def add_data_manual(self):
        if self.var_type.get() == "Check In":
            self.check_in_manual()
        elif self.var_type.get() == "Check Out":
            self.check_out_manual()
        else:
            messagebox.showerror("Error", "Please select a valid operation type", parent=self.root)

    def check_in_manual(self):
        try:
            employeeNo = self.var_employeeNo.get()
            name = self.name_of_employee(employeeNo)
            id = self.id_of_employee(employeeNo)
            email = self.email_of_employee(employeeNo)
            password = self.password_of_employee(employeeNo)
            if name == "Employee not found" or password == "Employee not found" or id == "Employee not found" \
                    or email == "Employee not found":
                messagebox.showerror("Error", "Employee not found", parent=self.root)
            elif str(id) != str(self.var_employeeID.get()):
                messagebox.showerror("Incorrect login details", "The ID is incorrect", parent=self.root)
            elif email != self.var_email.get():
                messagebox.showerror("Incorrect login details", "The email is incorrect", parent=self.root)
            elif password != self.var_password.get():
                messagebox.showerror("Incorrect login details", "The password is incorrect", parent=self.root)
            else:
                conn = mysql.connector.connect(host="localhost",
                                               user="root",
                                               passwd="1234",
                                               database="inventory_management")
                my_cursor = conn.cursor()
                my_cursor.execute(
                    "SELECT * FROM log_in_out_employees WHERE employee_no = %s AND date = %s ORDER BY logIn DESC LIMIT 1",
                    (id, datetime.now().date()))

                check_in_exists = my_cursor.fetchone()
                print(check_in_exists)

                if check_in_exists is not None and check_in_exists[4] is None:
                    print(check_in_exists[4])
                    messagebox.showerror("Error", "Check In already done today", parent=self.root)
                else:
                    my_cursor.execute(
                        "INSERT INTO log_in_out_employees (employee_no, employee_name, date, logIn) VALUES (%s, %s, CURDATE(), %s)",
                        (self.var_employeeNo.get(), name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                    conn.commit()
                    self.fetch_data()
                    conn.close()
                    messagebox.showinfo("Success", "Successfully Check In", parent=self.root)
                    self.reset_data()
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def check_out_manual(self):
        try:
            employeeNo = self.var_employeeNo.get()
            name = self.name_of_employee(employeeNo)
            id = self.id_of_employee(employeeNo)
            email = self.email_of_employee(employeeNo)
            password = self.password_of_employee(employeeNo)
            if name == "Employee not found" or password == "Employee not found" or id == "Employee not found" \
                    or email == "Employee not found":
                messagebox.showerror("Error", "Employee not found", parent=self.root)
            elif str(id) != str(self.var_employeeID.get()):
                messagebox.showerror("Incorrect login details", "The ID is incorrect", parent=self.root)
            elif email != self.var_email.get():
                messagebox.showerror("Incorrect login details", "The email is incorrect", parent=self.root)
            elif password != self.var_password.get():
                messagebox.showerror("Incorrect login details", "The password is incorrect", parent=self.root)
            else:
                conn = mysql.connector.connect(host="localhost",
                                               user="root",
                                               passwd="1234",
                                               database="inventory_management")
                my_cursor = conn.cursor()

                my_cursor.execute("SELECT * FROM log_in_out_employees WHERE employee_no = %s AND date = %s AND logOut IS NULL ORDER BY logIn DESC LIMIT 1",
                                  (id, datetime.now().date()))
                check_in_exists = my_cursor.fetchone()
                print(check_in_exists)

                if check_in_exists is None:
                    messagebox.showerror("No Check In", "No Check In done today", parent=self.root)

                elif int(check_in_exists[0]) != int(employeeNo):
                    print(check_in_exists[0])
                    print(employeeNo)
                    messagebox.showerror("No Check In", "No Check In done today for this employee", parent=self.root)

                else:
                    my_cursor.execute("UPDATE log_in_out_employees SET logOut = %s WHERE Employee_No = %s AND DATE(logIn) = CURDATE() AND logOut IS NULL ORDER BY logIn DESC LIMIT 1", (datetime.now(), self.var_employeeNo.get()))
                    conn.commit()
                    self.fetch_data()
                    conn.close()
                    messagebox.showinfo("Success", "Successfully Check Out", parent=self.root)
                    self.reset_data()
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def reset_data(self):
        self.var_employeeNo.set("")
        self.var_email.set("")
        self.var_employeeID.set("")
        self.var_password.set("")
        self.var_contact_no.set("")
        self.var_id_for_sent.set("")
        self.var_type.set("Select")
        self.var_type1.set("Select")
        self.var_type2.set("Select")
        self.var_code.set("")

    def face_Recognition(self):
        if self.var_type1.get() == "Select":
            messagebox.showerror("Error", "Please Choose In/Out", parent=self.root)
            return

        self.train_classfier()

        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
            if self.var_type1.get() == "Select":
                messagebox.showerror("Error", "Please Choose In/Out", parent=self.root)
                return
            else:
                self.error = 0
                self.success = 0
                coord = []
                for (x, y, w, h) in features:
                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
                    id, predict = clf.predict(gray_image[y:y + h, x:x + w])
                    confidence = int((100 * (1 - predict / 300)))
                    conn = mysql.connector.connect(host="localhost", user="root", passwd="1234",
                                                   database="inventory_management")
                    my_cursor = conn.cursor()

                    my_cursor.execute("SELECT name FROM employees WHERE employeeNo=" + str(id))
                    n = my_cursor.fetchone()
                    n = "+".join(n)

                    my_cursor.execute("SELECT email FROM employees WHERE employeeNo=" + str(id))
                    e = my_cursor.fetchone()
                    e = "+".join(e)

                    my_cursor.execute("SELECT employeeNo FROM employees WHERE employeeNo=" + str(id))
                    i = my_cursor.fetchone()
                    i = "+".join(str(id))

                    my_cursor.execute("SELECT contact FROM employees WHERE employeeNo=" + str(id))
                    c = my_cursor.fetchone()
                    c = "+".join(c)

                    if confidence > 80:
                        cv2.putText(img, f"ID:{str(id)}", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255),
                                    3)
                        cv2.putText(img, f"Name:{n}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                        cv2.putText(img, f"Email:{e}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                        cv2.putText(img, f"Contact:{c}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                        conn = mysql.connector.connect(host="localhost",
                                                       user="root",
                                                       passwd="1234",
                                                       database="inventory_management")
                        my_cursor = conn.cursor()

                        my_cursor.execute("SELECT * FROM log_in_out_employees WHERE employee_no = %s AND date = %s ORDER BY logIn DESC LIMIT 1", (id, datetime.now().date()))
                        check_in_exists = my_cursor.fetchone()
                        print(check_in_exists)


                        if self.var_type1.get() == "Check In":
                            if check_in_exists is not None and check_in_exists[4] is None:
                                print(check_in_exists[4])
                                messagebox.showerror("Error", "Check In already done today", parent=self.root)
                                self.error = 1
                                return
                            else:
                                my_cursor.execute(
                                    "INSERT INTO log_in_out_employees (employee_no, employee_name, date, logIn) VALUES (%s, %s, CURDATE(), %s)",
                                    (i, n, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                                conn.commit()
                                self.fetch_data()
                                conn.close()
                                messagebox.showinfo("Success", "Successfully Check In", parent=self.root)
                                self.reset_data()
                                self.success = 1
                        elif self.var_type1.get() == "Check Out":
                            if check_in_exists[4] is not None:
                                messagebox.showerror("No Check In", "No Check In done today", parent=self.root)
                                self.error = 1
                            elif int(check_in_exists[0]) != int(id):
                                print(check_in_exists[0])
                                print(int(id))
                                messagebox.showerror("No Check In", "No Check In done today for this employee",
                                                     parent=self.root)
                            else:
                                my_cursor.execute(
                                    "UPDATE log_in_out_employees SET logOut = %s WHERE Employee_No = %s AND DATE(logIn) = CURDATE() AND logOut IS NULL ORDER BY logIn DESC LIMIT 1",
                                    (datetime.now(), check_in_exists[0]))
                                conn.commit()
                                self.fetch_data()
                                conn.close()
                                messagebox.showinfo("Success", "Successfully Check Out", parent=self.root)
                                self.success=1
                                self.reset_data()

                else:
                     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                     cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
            coord = [x, y, w, h]
            return coord

        def recognize(img, clf, faceCascade):
            coord = draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 255), "Face", clf)
            return img

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("trained_classifier.xml")

        video_cap = cv2.VideoCapture(0)
        while True:
            ret, img = video_cap.read()
            img = recognize(img, clf, faceCascade)
            cv2.imshow("Face Recognition", img)

            if cv2.waitKey(1) == 13 or self.error == 1 or self.success == 1:
                self.reset_data()
                break
                return

        video_cap.release()
        cv2.destroyAllWindows()

    def train_classfier(self):
        data_dir = ("employeesForLogInOut")
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]
        faces = []
        ids = []

        for image in path:
            img = Image.open(image).convert('L')
            imageNp = np.array(img, 'uint8')
            id = int(os.path.split(image)[1].split('.')[1])
            faces.append((imageNp))
            ids.append(id)
        ids = np.array(ids)

        # train the classifier and save
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("trained_classifier.xml")
        cv2.destroyAllWindows()

    def send_gmail2(self):
        try:
            ob = smtplib.SMTP("smtp.gmail.com", 587)
            ob.starttls()
            ob.login(self.sender_Entry.get(), self.password_Entry.get())
            message = self.email_textarea.get(1.0, END)
            ob.sendmail(self.sender_Entry.get(), self.reciever_Entry.get(), message)
            ob.quit()
            messagebox.showinfo("Success", "login details is successfully sent", parent=self.root)
            self.is_send = 1
        except:
            messagebox.showerror("Error", "Somthing went wrong, Please try again", parent=self.root)


    def send_gmail(self):
        if self.var_id_for_sent.get() != "" and self.var_type2.get() != "Select":
            self.var_email1 = StringVar()
            email = self.email_of_employee(self.var_id_for_sent.get())
            if email == "Employee not found":
                messagebox.showerror("Error","Employee not found", parent=self.root)
                return
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
                                        bg="white", textvariable=self.var_email1)
            self.reciever_Entry.grid(row=0, column=1, padx=10, pady=8)

            self.var_email1.set(email)

            message_Label = Label(recipient_Frame, text="Message", font=("Great Vibes", 12, "bold"),
                                  bg="#2f3030",
                                  fg="white")
            message_Label.grid(row=1, column=0, padx=10, pady=8)

            self.email_textarea = Text(recipient_Frame, font=("Great Vibes", 12, "bold"), bd=2, relief=SUNKEN,
                                       width=40,
                                       height=11)
            self.email_textarea.grid(row=2, column=0, columnspan=2)
            self.email_textarea.delete(1.0, END)
            name = self.name_of_employee(self.var_id_for_sent.get())
            self.random_code = random.randint(1000, 999999)
            self.email_textarea.insert(END, "Hello " + name + "\nYour login details are:\n" + "Email: "
                                       + email + "\nCode: " + str(self.random_code))

            send_btn = Button(send_gmail, text="Send", font=("Great Vibes", 12, "bold"), command=self.send_gmail2)
            send_btn.grid(row=3, column=0)
        else:
            messagebox.showerror("Error", "Fields are required", parent=self.root)

    def apply_data(self):
        if self.var_type2.get() != "Select" and self.var_id_for_sent.get() != "" and self.var_code.get() != "":
            if self.is_send != 1:
                messagebox.showerror("Error", "No email sent. Please send mail", parent=self.root)
            elif str(self.var_code.get()) != str(self.random_code):
                messagebox.showerror("Error", "The codes do not match", parent=self.root)
            else:
                self.is_send = 0
                employeeNo = self.var_id_for_sent.get()
                name = self.name_of_employee(employeeNo)
                conn = mysql.connector.connect(host="localhost",
                                               user="root",
                                               passwd="1234",
                                               database="inventory_management")
                my_cursor = conn.cursor()
                my_cursor.execute("SELECT * FROM log_in_out_employees WHERE employee_no = %s AND date = %s ORDER BY logIn DESC LIMIT 1", (employeeNo, datetime.now().date()))
                check_in_exists = my_cursor.fetchone()
                print(check_in_exists)

                if self.var_type2.get() == "Check In":
                    if check_in_exists is not None and check_in_exists[4] is None:
                        print(check_in_exists[4])
                        messagebox.showerror("Error", "Check In already done today", parent=self.root)
                        return
                    else:
                        my_cursor.execute(
                            "INSERT INTO log_in_out_employees (employee_no, employee_name, date, logIn) VALUES (%s, %s, CURDATE(), %s)",
                            (employeeNo, name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                        conn.commit()
                        self.fetch_data()
                        conn.close()
                        messagebox.showinfo("Success", "Successfully Check In", parent=self.root)
                        self.reset_data()
                elif self.var_type2.get() == "Check Out":
                    if check_in_exists[4] is not None:
                        messagebox.showerror("No Check In", "No Check In done today", parent=self.root)
                    elif int(check_in_exists[0]) != int(self.var_id_for_sent.get()):
                        messagebox.showerror("No Check In", "No Check In done today for this employee",
                                             parent=self.root)
                    else:
                        my_cursor.execute(
                            "UPDATE log_in_out_employees SET logOut = %s WHERE Employee_No = %s AND DATE(logIn) = CURDATE() AND logOut IS NULL ORDER BY logIn DESC LIMIT 1",
                            (datetime.now(), check_in_exists[0]))
                        conn.commit()
                        self.fetch_data()
                        conn.close()
                        messagebox.showinfo("Success", "Successfully Check Out", parent=self.root)
                        self.reset_data()

        else:
            messagebox.showerror("Error", "Fields are required", parent=self.root)
    def export_to_excel(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], parent=self.root)
        if file_path:
            data = []
            for item in self.log_in_out_employees_table.get_children():
                data.append(self.log_in_out_employees_table.item(item, "values"))

            # Define the columns for the Excel file
            columns = ["Employee No", "Employee Name", "Date", "Log In", "Log Out"]

            # Create a DataFrame using pandas
            df = pd.DataFrame(data, columns=columns)

            # Save the DataFrame to an Excel file
            excel_path = file_path  # Use the selected file path
            df.to_excel(excel_path, index=False)
            messagebox.showinfo("Export", "Data exported to Excel successfully.", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    your_instance = checkInOut(root)
    root.mainloop()
