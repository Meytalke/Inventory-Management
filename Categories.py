from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import scrolledtext
from tkinter import messagebox
import mysql.connector
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

class Category:
    def __init__(self, root):
        self.root = root
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.title("Categories")

        self.var_categoryID = StringVar()
        self.var_name = StringVar()
        self.var_description = StringVar()
        self.var_creationDate = StringVar()

        bg_img = Image.open(r"C:\Users\meyta\inventory_management_images\Product_bg4.jpg")
        bg_img = bg_img.resize((screen_width, screen_height), Image.BILINEAR)
        self.bg_img = ImageTk.PhotoImage(bg_img)

        bg_label = Label(self.root, image=self.bg_img)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title label
        title_lbl = Label(self.root, text="Categories Management",
                          font=("Great Vibes", 34, "bold"), bg="#009688", fg="white")
        title_lbl.place(x=0, y=-105, width=1500, relx=0.5, rely=0.19, anchor="center")

        main_frame = Frame(self.root, bd=2, bg="white", )
        main_frame.place(x=10, y=70, width=1260, height=600)

        # left label frame
        Left_frame = tk.LabelFrame(main_frame, bd=2, bg="white", relief=tk.RIDGE, text="Category Details",
                                   font=("Great Vibes", 12, "bold"))
        Left_frame.place(x=10, y=10, width=615, height=550)

        next_category_id = self.get_next_category_id()
        self.var_categoryID.set(next_category_id)

        categoryID_label = tk.Label(Left_frame, text="Category ID:", font=("Great Vibes", 12, "bold"),
                                    bg="white")
        categoryID_label.grid(row=0, column=0, padx=7, pady=5, sticky=tk.W)

        categoryID_entry = ttk.Entry(Left_frame, textvariable=self.var_categoryID, width=19,
                                     font=("Great Vibes", 12, "bold"), state='disabled')
        categoryID_entry.grid(row=0, column=1, padx=7, pady=5, sticky=tk.W)

        name_label = tk.Label(Left_frame, text="Name:", font=("Great Vibes", 12, "bold"),
                              bg="white")
        name_label.grid(row=0, column=2, padx=7, pady=5, sticky=tk.W)

        name_entry = ttk.Entry(Left_frame, textvariable=self.var_name, width=19,
                               font=("Great Vibes", 12, "bold"))
        name_entry.grid(row=0, column=3, padx=7, pady=5, sticky=tk.W)

        description_label = tk.Label(Left_frame, text="Description:", font=("Great Vibes", 12, "bold"),
                                     bg="white")
        description_label.grid(row=1, column=0, padx=7, pady=5, sticky=tk.W)

        self.description_text = scrolledtext.ScrolledText(Left_frame, wrap='word', font=("Great Vibes", 12, "bold"),
                                                          width=50, height=4)
        self.description_text.grid(row=1, column=1, columnspan=3, padx=7, pady=5, sticky=tk.W)

        self.description_text.bind("<KeyRelease>", self.update_description_value)

        self.var_active = StringVar(value="Yes")
        radiobtn1 = ttk.Radiobutton(Left_frame, variable=self.var_active, text="Active",
                                    value="Yes")
        radiobtn1.grid(row=5, column=0)

        radiobtn2 = ttk.Radiobutton(Left_frame, variable=self.var_active, text="InActive", value="No")
        radiobtn2.grid(row=5, column=1)

        btn_frame = Frame(Left_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=0, y=150, width=610, height=38)

        save_btn = Button(btn_frame, text="Save", font=("Great Vibes", 12, "bold"), width=15,command=self.add_data,
                          bg="#009688", fg="white")
        save_btn.grid(row=0, column=0)

        update_btn = Button(btn_frame, text="Update", font=("Great Vibes", 12, "bold"), command=self.update_data,
                            width=15, bg="#009688", fg="white")
        update_btn.grid(row=0, column=1)

        delete_btn = Button(btn_frame, text="Delete", font=("Great Vibes", 12, "bold"),command=self.delete_data,
                            width=15, bg="#009688", fg="white")
        delete_btn.grid(row=0, column=2)

        reset_btn = Button(btn_frame, text="Reset", font=("Great Vibes", 12, "bold"),command=self.reset_data,
                           width=15, bg="#009688", fg="white")
        reset_btn.grid(row=0, column=3)

        Filters_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE,
                                  text="Filters",
                                  font=("Great Vibes", 12, "bold"))
        Filters_frame.place(x=5, y=190, width=605, height=60)

        self.var_Serach= StringVar()


        Serach_label = Label(Filters_frame, text="Serach By:", font=("Great Vibes", 12, "bold"),
                             bg="#009688", fg="white")
        Serach_label.grid(row=0, column=0, padx=7, pady=7, sticky=W)

        Serach_combo = ttk.Combobox(Filters_frame, font=("Great Vibes", 12, "bold"),textvariable=self.var_Serach, width=17, state="readonly")
        Serach_combo["values"] = ("Select", "Category ID", "Name","Is Active")
        Serach_combo.current(0)
        Serach_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        Serach_entry = ttk.Entry(Filters_frame, width=15, font=("Great Vibes", 12, "bold"))
        Serach_entry.grid(row=0, column=2, pady=7, padx=7, sticky=W)
        self.Serach_entry = Serach_entry

        Serach_btn = Button(Filters_frame, text="Search", font=("Great Vibes", 12, "bold"), width=7, bg="#009688",
                            fg="white",command=self.Serach)
        Serach_btn.grid(row=0, column=3, padx=3)

        showAll_btn = Button(Filters_frame, text="Reset", font=("Great Vibes", 12, "bold"), width=7, bg="#009688",
                             fg="white", command=self.fetch_data)
        showAll_btn.grid(row=0, column=4, padx=3)

        table_frame = Frame(Left_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=5, y=260, width=605, height=260)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        self.category_table = ttk.Treeview(table_frame, column=(
        "categoryID", "name", "description", "creationDate","active"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.category_table.xview)
        scroll_y.config(command=self.category_table.yview)

        self.category_table.heading("categoryID", text="Category ID")
        self.category_table.heading("name", text="Name")
        self.category_table.heading("description", text="Description")
        self.category_table.heading("creationDate", text="Creation Date")
        self.category_table.heading("active", text="Is Active")
        self.category_table["show"] = "headings"

        self.category_table.column("categoryID", width=100)
        self.category_table.column("name", width=100)
        self.category_table.column("description", width=100)
        self.category_table.column("creationDate", width=100)
        self.category_table.column("active", width=100)

        self.category_table.pack(fill=BOTH, expand=1)
        self.category_table.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()

        Right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Charts",
                                 font=("Great Vibes", 12, "bold"))
        Right_frame.place(x=640, y=10, width=615, height=550)

        # Create a frame for the first chart
        distribution_frame = Frame(Right_frame)
        distribution_frame.pack(side="top", fill="both", expand=True)
        self.create_distribution_chart(distribution_frame)

        # Create a frame for the second chart
        categories_frame = Frame(Right_frame)
        categories_frame.pack(side="top", fill="both", expand=True)
        self.create_top_categories_chart(categories_frame)

    def create_distribution_chart(self, parent_frame):
        fig = Figure(figsize=(6, 2.2))
        ax = fig.add_subplot(111)

        # Fetch data and create the distribution chart
        data = self.fetch_distribution_data()
        ax.bar(["Active", "Inactive"], data, color=['#00cc99', '#008066'])
        ax.set_title("Distribution of Active and Inactive Categories")

        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


        # Add navigation toolbar
        toolbar = NavigationToolbar2Tk(canvas, parent_frame)
        toolbar.update()
        canvas.get_tk_widget().pack()


    def create_top_categories_chart(self, parent_frame):
        fig = Figure(figsize=(6, 2.2))
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

    def show_distribution_chart(self):
        data = self.fetch_distribution_data()
        self.create_distribution_chart(data)

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

    def Serach(self):
        search_text = self.var_Serach.get()
        search_value = self.Serach_entry.get()

        if search_text == "Category ID":
            self.search_by_categoryID(search_value)
        elif search_text == "Name":
            self.search_by_name(search_value)
        elif search_text == "Is Active":
            self.search_by_active(search_value)
        else:
            messagebox.showwarning("Invalid Selection", "Please select a valid search option.", parent=self.root)

    def search_by_categoryID(self, search_value):
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM categories WHERE categoryID = %s", (search_value,))
        data = my_cursor.fetchall()
        if len(data) != 0:
            self.category_table.delete(*self.category_table.get_children())
            for i in data:
                self.category_table.insert("", END, values=i)
            conn.commit()
        conn.close()

    def search_by_name(self, search_value):
        conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM categories WHERE name LIKE %s", ('%' + search_value + '%',))
        data = my_cursor.fetchall()
        if len(data) != 0:
            self.category_table.delete(*self.category_table.get_children())
            for i in data:
                self.category_table.insert("", END, values=i)
            conn.commit()
        conn.close()

    def search_by_active(self, search_value):
        search_value = search_value.lower()
        if search_value in ("yes", "no"):
            conn = mysql.connector.connect(host="localhost", user="root", passwd="1234",
                                           database="inventory_management")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM categories WHERE active = %s", (search_value,))
            data = my_cursor.fetchall()
            if len(data) != 0:
                self.category_table.delete(*self.category_table.get_children())
                for i in data:
                    self.category_table.insert("", END, values=i)
                conn.commit()
            conn.close()
        else:
            messagebox.showwarning("Invalid Value", "Please enter 'Yes' or 'No' for Is Active field.", parent=self.root)

    def update_description_value(self, event):
        self.var_description.set(event.widget.get("1.0", tk.END).replace("\n", "\n"))

    def get_next_category_id(self):
        try:
            conn = mysql.connector.connect(host="localhost",
                                           user="root",
                                           passwd="1234",
                                           database="inventory_management")

            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute('SELECT MAX(categoryID) FROM categories')
                max_id = cursor.fetchone()[0]
                cursor.close()
                conn.close()

                if max_id is not None:
                    return max_id + 1
                else:
                    return 1

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Due To: {str(e)}", parent=self.root)
        return None



    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost",
                                       user="root",
                                       passwd="1234",
                                       database="inventory_management")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM categories")
        data = my_cursor.fetchall()
        if len(data) != 0:
            self.category_table.delete(*self.category_table.get_children())
            for i in data:
                self.category_table.insert("", END, values=i)
            conn.commit()
        conn.close()
    # ============== get cursor====================
    def get_cursor(self,event=""):
        cursor_focus = self.category_table.focus()
        content = self.category_table.item(cursor_focus)
        data = content["values"]
        self.var_categoryID.set(data[0])
        self.var_name.set(data[1])
        self.var_description.set(data[2])
        self.var_creationDate.set(data[3])
        self.var_active.set(data[4])

        # Set the description in the description_text box
        self.description_text.delete("1.0", "end")
        self.description_text.insert("1.0", data[2])

    def add_data(self):
        if self.var_name.get() != "":
            try:
                description = self.description_text.get("1.0", tk.END).strip()
                conn = mysql.connector.connect(host="localhost",
                                               user="root",
                                               passwd="1234",
                                               database="inventory_management")
                my_cursor = conn.cursor()
                my_cursor.execute("INSERT INTO categories VALUES(%s,%s,%s,%s,%s)", (
                    self.var_categoryID.get(),
                    self.var_name.get(),
                    description,
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    self.var_active.get()
                ))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Category has been added Successfully", parent=self.root)
                self.reset_data()
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
        else:
            messagebox.showerror("Error", "Name is required", parent=self.root)

    def update_data(self):
        if self.var_categoryID.get() != "" and self.var_name.get() != "":
            try:
                Update = messagebox.askyesno("Update", "Do you want to update this Category's details",
                                             parent=self.root)
                if Update:
                    conn = mysql.connector.connect(host="localhost", user="root", passwd="1234",
                                                   database="inventory_management")
                    my_cursor = conn.cursor()
                    my_cursor.execute(
                        "UPDATE categories SET name=%s, description=%s , active=%s WHERE categoryID=%s",
                        (
                            self.var_name.get(),
                            self.var_description.get(),
                            self.var_active.get(),
                            self.var_categoryID.get()
                        ))
                    messagebox.showinfo("Success", "Category details successfully updated", parent=self.root)
                    self.reset_data()
                    conn.commit()
                    self.fetch_data()
                    conn.close()
                else:
                    if not Update:
                        return
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
        else:
            messagebox.showerror("Error", "All Fields are required", parent=self.root)

    def reset_data(self):
        self.var_categoryID.set(self.get_next_category_id())
        self.var_active.set("")
        self.var_name.set("")
        self.var_description.set("")  # Clear the description variable
        self.description_text.delete("1.0", "end")  # Clear the description text

    def delete_data(self):
        if self.var_categoryID.get() == "" or self.var_name.get() == "":
            messagebox.showerror("Error", "Category id must be required", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Category Delete", "Do you want to delete this Category?", parent=self.root)
                if delete:
                     conn = mysql.connector.connect(host="localhost", user="root", passwd="1234",
                                           database="inventory_management")
                     my_cursor = conn.cursor()
                     my_cursor.execute("DELETE FROM categories WHERE categoryID=%s", (self.var_categoryID.get(),))
                     self.reset_data()
                else:
                    if not delete:
                        return
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Delete", "Successfully deleted Category", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)







if __name__ == "__main__":
    root = Tk()
    obj = Category(root)
    root.mainloop()