from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk

class categoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed by Harsha")
        self.root.config(bg="white")
        self.root.focus_force()

        # ====== Variables ======
        self.var_cat_id = StringVar()
        self.var_name = StringVar()
        
        # =========== Title ==============
        lbl_title = Label(self.root, text="Manage Product Category", font=("goudy old style", 30), bg="#184a45", fg="white", bd=3, relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X, padx=10, pady=20)
        
        # =========== Category Entry ==============
        lbl_name = Label(self.root, text="Enter Category Name", font=("goudy old style", 20), bg="white")
        lbl_name.place(x=50, y=100)
        
        self.txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 18), bg="lightyellow")
        self.txt_name.place(x=50, y=140, width=300)
        
        # =========== Buttons ==============
        btn_add = Button(self.root, text="Add", command=self.add,font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2")
        btn_add.place(x=360, y=140, width=150, height=30)
        
        btn_delete = Button(self.root, text="Delete", command=self.delete,font=("goudy old style", 15), bg="red", fg="white", cursor="hand2")
        btn_delete.place(x=520, y=140, width=150, height=30)

        # ====== Category Details Table ========
        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=700, y=100, width=380, height=350)

        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)

        self.category_table = ttk.Treeview(cat_frame, columns=("cid", "name"),
                                         yscrollcommand=scrolly.set, 
                                         xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.category_table.xview)
        scrolly.config(command=self.category_table.yview)
        
        self.category_table.heading("cid", text="Category ID")
        self.category_table.heading("name", text="Name")
        self.category_table["show"] = "headings"
        self.category_table.column("cid", width=100)
        self.category_table.column("name", width=250)
        self.category_table.pack(fill=BOTH, expand=1)
        self.category_table.bind("<ButtonRelease-1>", self.get_data)

        # ====== Images ======
        try:
            self.im1 = Image.open("images/cat.jpg")
            self.im1 = self.im1.resize((500, 250), Image.LANCZOS)
            self.im1 = ImageTk.PhotoImage(self.im1)
            self.lbl_im1 = Label(self.root, image=self.im1, bd=2, relief=RAISED)
            self.lbl_im1.place(x=50, y=200)
        except FileNotFoundError:
            messagebox.showwarning("Warning", "Category image not found", parent=self.root)

        try:
            self.im2 = Image.open("images/category.jpg")
            self.im2 = self.im2.resize((500, 250), Image.LANCZOS)
            self.im2 = ImageTk.PhotoImage(self.im2)
            self.lbl_im2 = Label(self.root, image=self.im2, bd=2, relief=RAISED)
            self.lbl_im2.place(x=580, y=200)
        except FileNotFoundError:
            messagebox.showwarning("Warning", "Category image not found", parent=self.root)

        self.show()
        self.txt_name.focus_set()

    # ============ Functions ==========
    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if not self.var_name.get().strip():
                messagebox.showerror("Error", "Category name is required", parent=self.root)
                self.txt_name.focus_set()
                return
            
            # Check if category already exists (case-insensitive)
            cur.execute("SELECT * FROM category WHERE LOWER(name)=LOWER(?)", 
                       (self.var_name.get().strip(),))
            row = cur.fetchone()
            
            if row:
                messagebox.showerror("Error", "This category already exists", parent=self.root)
                self.txt_name.focus_set()
            else:
                cur.execute("INSERT INTO category (name) VALUES (?)",
                           (self.var_name.get().strip(),))
                con.commit()
                messagebox.showinfo("Success", "Category added successfully", parent=self.root)
                self.show()
                self.clear_fields()
        except Exception as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM category ORDER BY name")
            rows = cur.fetchall()
            self.category_table.delete(*self.category_table.get_children())
            for row in rows:
                self.category_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error loading categories: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        selected_item = self.category_table.focus()
        if not selected_item:
            return
            
        data = self.category_table.item(selected_item)
        row = data['values']
        if row:
            self.var_cat_id.set(row[0])
            self.var_name.set(row[1])
            self.txt_name.focus_set()

    def delete(self):
        if not self.var_cat_id.get():
            messagebox.showerror("Error", "Please select a category to delete", parent=self.root)
            return
            
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Check if category is used in products
            cur.execute("SELECT COUNT(*) FROM products WHERE category=?", (self.var_cat_id.get(),))
            product_count = cur.fetchone()[0]
            
            if product_count > 0:
                messagebox.showerror("Error", 
                    f"Cannot delete - this category has {product_count} associated product(s)", 
                    parent=self.root)
                return
                
            if messagebox.askyesno("Confirm", 
                "Are you sure you want to delete this category?", parent=self.root):
                cur.execute("DELETE FROM category WHERE cid=?", (self.var_cat_id.get(),))
                con.commit()
                messagebox.showinfo("Success", "Category deleted successfully", parent=self.root)
                self.show()
                self.clear_fields()
        except Exception as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear_fields(self):
        self.var_cat_id.set("")
        self.var_name.set("")
        self.txt_name.focus_set()


if __name__ == "__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()