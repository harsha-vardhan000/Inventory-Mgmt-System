from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk

class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed by Harsha")
        self.root.config(bg="white")
        self.root.focus_force()

        # Variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_pid = StringVar()
        self.var_cat = StringVar()
        self.var_sup = StringVar()
        self.cat_list = []
        self.sup_list = []
        self.fetch_cat_sup()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()

        # Product Frame
        product_Frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        product_Frame.place(x=10, y=10, width=450, height=480)

        # Title
        title = Label(product_Frame, text="Manage Product Details", 
                    font=("goudy old style", 18), bg="#0f4d7d", fg="white")
        title.pack(side=TOP, fill=X)

        # Column 1 - Labels
        lbl_category = Label(product_Frame, text="Category", 
                           font=("goudy old style", 18), bg="white").place(x=30, y=60)
        lbl_supplier = Label(product_Frame, text="Supplier", 
                           font=("goudy old style", 18), bg="white").place(x=30, y=110)
        lbl_product_name = Label(product_Frame, text="Name", 
                               font=("goudy old style", 18), bg="white").place(x=30, y=160)
        lbl_price = Label(product_Frame, text="Price", 
                         font=("goudy old style", 18), bg="white").place(x=30, y=210)
        lbl_quantity = Label(product_Frame, text="Quantity", 
                            font=("goudy old style", 18), bg="white").place(x=30, y=260)
        lbl_status = Label(product_Frame, text="Status", 
                          font=("goudy old style", 18), bg="white").place(x=30, y=310)

        # Column 2 - Entry Fields
        self.cmb_cat = ttk.Combobox(product_Frame, textvariable=self.var_cat, 
                                  values=self.cat_list, state='readonly', 
                                  font=("goudy old style", 15))
        self.cmb_cat.place(x=150, y=60, width=200)
        self.cmb_cat.current(0)

        self.cmb_sup = ttk.Combobox(product_Frame, textvariable=self.var_sup, 
                                  values=self.sup_list, state='readonly', 
                                  font=("goudy old style", 15))
        self.cmb_sup.place(x=150, y=110, width=200)
        self.cmb_sup.current(0)

        self.txt_name = Entry(product_Frame, textvariable=self.var_name, 
                            font=("goudy old style", 15), bg="lightyellow")
        self.txt_name.place(x=150, y=160, width=200)

        self.txt_price = Entry(product_Frame, textvariable=self.var_price, 
                              font=("goudy old style", 15), bg="lightyellow")
        self.txt_price.place(x=150, y=210, width=200)

        self.txt_qty = Entry(product_Frame, textvariable=self.var_qty, 
                            font=("goudy old style", 15), bg="lightyellow")
        self.txt_qty.place(x=150, y=260, width=200)

        self.cmb_status = ttk.Combobox(product_Frame, textvariable=self.var_status, 
                                     values=("Active", "Inactive"), state='readonly', 
                                     font=("goudy old style", 15))
        self.cmb_status.place(x=150, y=310, width=200)
        self.cmb_status.current(0)

        # Buttons
        btn_add = Button(product_Frame, text="Save", command=self.add, 
                        font=("goudy old style", 15), bg="#2196f3", 
                        fg="white", cursor="hand2")
        btn_add.place(x=10, y=400, width=100, height=40)

        btn_update = Button(product_Frame, text="Update", command=self.update, 
                           font=("goudy old style", 15), bg="#4caf50", 
                           fg="white", cursor="hand2")
        btn_update.place(x=120, y=400, width=100, height=40)

        btn_delete = Button(product_Frame, text="Delete", command=self.delete, 
                           font=("goudy old style", 15), bg="#f44336", 
                           fg="white", cursor="hand2")
        btn_delete.place(x=230, y=400, width=100, height=40)

        btn_clear = Button(product_Frame, text="Clear", command=self.clear, 
                          font=("goudy old style", 15), bg="#607d8b", 
                          fg="white", cursor="hand2")
        btn_clear.place(x=340, y=400, width=100, height=40)

        # Search Frame
        SearchFrame = LabelFrame(self.root, text="Search Product", 
                               font=("goudy old style", 12, "bold"), 
                               bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=480, y=10, width=600, height=80)

        # Search Options
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, 
                                 values=("Select", "Category", "Supplier", "Name"), 
                                 state='readonly', font=("times new roman", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, 
                          font=("goudy old style", 15), bg="lightyellow")
        txt_search.place(x=200, y=10, width=200)

        btn_search = Button(SearchFrame, text="Search", command=self.search, 
                           font=("goudy old style", 15), bg="#4caf50", 
                           fg="white", cursor="hand2")
        btn_search.place(x=410, y=9, width=150, height=30)

        # Product Details Table
        p_frame = Frame(self.root, bd=3, relief=RIDGE)
        p_frame.place(x=480, y=100, width=600, height=390)

        scrolly = Scrollbar(p_frame, orient=VERTICAL)
        scrollx = Scrollbar(p_frame, orient=HORIZONTAL)

        self.product_table = ttk.Treeview(p_frame, columns=("pid", "Supplier", "Category", "name", 
                                                          "price", "qty", "status"), 
                                        yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)

        # Configure table headings
        self.product_table.heading("pid", text="P ID")
        self.product_table.heading("Category", text="Category")
        self.product_table.heading("Supplier", text="Supplier")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("qty", text="Quantity")
        self.product_table.heading("status", text="Status")
        self.product_table["show"] = "headings"

        # Configure column widths
        self.product_table.column("pid", width=50)
        self.product_table.column("Category", width=100)
        self.product_table.column("Supplier", width=100)
        self.product_table.column("name", width=120)
        self.product_table.column("price", width=80)
        self.product_table.column("qty", width=80)
        self.product_table.column("status", width=80)

        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def fetch_cat_sup(self):
        self.cat_list = ["Select"]
        self.sup_list = ["Select"]
        
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Fetch categories
            cur.execute("SELECT name FROM category")
            categories = cur.fetchall()
            if categories:
                for cat in categories:
                    self.cat_list.append(cat[0])

            # Fetch suppliers
            cur.execute("SELECT name FROM supplier")
            suppliers = cur.fetchall()
            if suppliers:
                for sup in suppliers:
                    self.sup_list.append(sup[0])
                    
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching data: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if (self.var_cat.get() == "Select" or self.var_sup.get() == "Select" or 
                not self.var_name.get().strip() or not self.var_price.get() or 
                not self.var_qty.get()):
                messagebox.showerror("Error", "All fields are required", parent=self.root)
                return

            # Validate price and quantity are numeric
            try:
                float(self.var_price.get())
                int(self.var_qty.get())
            except ValueError:
                messagebox.showerror("Error", "Price must be numeric and Quantity must be integer", 
                                    parent=self.root)
                return

            # Check if product already exists
            cur.execute("SELECT * FROM product WHERE LOWER(name)=LOWER(?)", 
                       (self.var_name.get().strip(),))
            if cur.fetchone():
                messagebox.showerror("Error", "Product already exists", parent=self.root)
                return

            # Insert new product
            cur.execute("INSERT INTO product (Category, Supplier, name, price, qty, status) VALUES (?,?,?,?,?,?)",
                       (self.var_cat.get(), self.var_sup.get(), self.var_name.get().strip(),
                        self.var_price.get(), self.var_qty.get(), self.var_status.get()))
            con.commit()
            messagebox.showinfo("Success", "Product added successfully", parent=self.root)
            self.show()
            self.clear()
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error adding product: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error loading products: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        selected_item = self.product_table.focus()
        if not selected_item:
            return
            
        data = self.product_table.item(selected_item)
        row = data['values']
        if row:
            self.var_pid.set(row[0])
            self.var_sup.set(row[1])
            self.var_cat.set(row[2])
            self.var_name.set(row[3])
            self.var_price.set(row[4])
            self.var_qty.set(row[5])
            self.var_status.set(row[6])
            self.cmb_status.set(row[6])

    def update(self):
        if not self.var_pid.get():
            messagebox.showerror("Error", "Please select a product to update", parent=self.root)
            return
            
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Validate inputs
            if (self.var_cat.get() == "Select" or self.var_sup.get() == "Select" or 
                not self.var_name.get().strip() or not self.var_price.get() or 
                not self.var_qty.get()):
                messagebox.showerror("Error", "All fields are required", parent=self.root)
                return

            # Validate price and quantity are numeric
            try:
                float(self.var_price.get())
                int(self.var_qty.get())
            except ValueError:
                messagebox.showerror("Error", "Price must be numeric and Quantity must be integer", 
                                    parent=self.root)
                return

            # Check if product exists
            cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
            if not cur.fetchone():
                messagebox.showerror("Error", "Invalid product ID", parent=self.root)
                return

            # Update product
            cur.execute("""UPDATE product SET 
                        Category=?, Supplier=?, name=?, price=?, qty=?, status=? 
                        WHERE pid=?""",
                       (self.var_cat.get(), self.var_sup.get(), self.var_name.get().strip(),
                        self.var_price.get(), self.var_qty.get(), self.var_status.get(),
                        self.var_pid.get()))
            
            if cur.rowcount == 0:
                messagebox.showwarning("Warning", "No changes made to the product", parent=self.root)
            else:
                con.commit()
                messagebox.showinfo("Success", "Product updated successfully", parent=self.root)
                self.show()
                self.clear()
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error updating product: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        if not self.var_pid.get():
            messagebox.showerror("Error", "Please select a product to delete", parent=self.root)
            return
            
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this product?", parent=self.root):
            return
            
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM product WHERE pid=?", (self.var_pid.get(),))
            if cur.rowcount == 0:
                messagebox.showerror("Error", "Product not found", parent=self.root)
            else:
                con.commit()
                messagebox.showinfo("Success", "Product deleted successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error deleting product: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_pid.set("")
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()
        self.txt_name.focus_set()

    def search(self):
        if self.var_searchby.get() == "Select":
            messagebox.showerror("Error", "Select search criteria", parent=self.root)
            return
            
        if not self.var_searchtxt.get().strip():
            messagebox.showerror("Error", "Search input is required", parent=self.root)
            return
            
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            search_term = f"%{self.var_searchtxt.get().strip()}%"
            query = f"SELECT * FROM product WHERE {self.var_searchby.get()} LIKE ?"
            cur.execute(query, (search_term,))
            
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            
            if rows:
                for row in rows:
                    self.product_table.insert('', END, values=row)
            else:
                messagebox.showinfo("Info", "No matching products found", parent=self.root)
                
        except Exception as ex:
            messagebox.showerror("Error", f"Search error: {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()