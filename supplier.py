from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk

class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed by Harsha")
        self.root.config(bg="white")
        self.root.focus_force()
        
        # ================== Variables ==================
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_sup_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()

        # ================== Search Frame ==================
        Label(self.root, text="Invoice No.", bg="white", font=("times new roman", 15)).place(x=700, y=80)
        Entry(self.root, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow").place(x=800, y=80, width=160)
        Button(self.root, text="Search", command=self.search, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=980, y=79, width=100, height=28)

        # ================== Title ==================
        title = Label(self.root, text="Manage Supplier Details", font=("goudy old style", 20), bg="#0f4d7d", fg="white").place(x=50, y=10, width=1000, height=40)

        # ================== Content ==================
        # Row 1
        Label(self.root, text="Invoice No.", font=("goudy old style", 15), bg="white").place(x=50, y=80)
        Entry(self.root, textvariable=self.var_sup_invoice, font=("goudy old style", 15), bg="lightyellow").place(x=180, y=80, width=180)
        
        # Row 2
        Label(self.root, text="Name", font=("goudy old style", 15), bg="white").place(x=50, y=120)
        Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(x=180, y=120, width=180)
        
        # Row 3
        Label(self.root, text="Contact", font=("goudy old style", 15), bg="white").place(x=50, y=160)
        Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow").place(x=180, y=160, width=180)
        
        # Row 4
        Label(self.root, text="Description", font=("goudy old style", 15), bg="white").place(x=50, y=200)
        self.txt_desc = Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_desc.place(x=180, y=200, width=470, height=120)
        
        # ================== Buttons ==================
        Button(self.root, text="Save", command=self.add, font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2").place(x=180, y=370, width=110, height=35)
        Button(self.root, text="Update", command=self.update, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=300, y=370, width=110, height=35)
        Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15), bg="#f44336", fg="white", cursor="hand2").place(x=420, y=370, width=110, height=35)
        Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15), bg="#607d8b", fg="white", cursor="hand2").place(x=540, y=370, width=110, height=35)

        # ================== Supplier Table ==================
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=700, y=120, width=380, height=350)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.supplierTable = ttk.Treeview(emp_frame, columns=("invoice", "name", "contact", "desc"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)
        
        self.supplierTable.heading("invoice", text="Invoice No.")
        self.supplierTable.heading("name", text="Name")
        self.supplierTable.heading("contact", text="Contact")
        self.supplierTable.heading("desc", text="Description")
        self.supplierTable["show"] = "headings"
        
        self.supplierTable.column("invoice", width=90)
        self.supplierTable.column("name", width=100)
        self.supplierTable.column("contact", width=100)
        self.supplierTable.column("desc", width=100)
        
        self.supplierTable.pack(fill=BOTH, expand=1)
        self.supplierTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # ================== Database Methods ==================
    def add(self):
        if not self.validate_inputs():
            return
            
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
            if cur.fetchone() is not None:
                messagebox.showerror("Error", "Invoice number already exists", parent=self.root)
                return
                
            cur.execute("INSERT INTO supplier (invoice, name, contact, desc) VALUES (?,?,?,?)",
                       (self.var_sup_invoice.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0', END)))
            con.commit()
            messagebox.showinfo("Success", "Supplier added successfully", parent=self.root)
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def update(self):
        if not self.validate_inputs():
            return
            
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
            if cur.fetchone() is None:
                messagebox.showerror("Error", "Select a supplier to update", parent=self.root)
                return
                
            cur.execute("UPDATE supplier SET name=?, contact=?, desc=? WHERE invoice=?",
                       (self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0', END),
                        self.var_sup_invoice.get()))
            con.commit()
            messagebox.showinfo("Success", "Supplier updated successfully", parent=self.root)
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        if not self.var_sup_invoice.get():
            messagebox.showerror("Error", "Select a supplier to delete", parent=self.root)
            return
            
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
            if cur.fetchone() is None:
                messagebox.showerror("Error", "Supplier not found", parent=self.root)
                return
                
            if messagebox.askyesno("Confirm", "Are you sure you want to delete?", parent=self.root):
                cur.execute("DELETE FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                con.commit()
                messagebox.showinfo("Success", "Supplier deleted successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier")
            rows = cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        selected_row = self.supplierTable.focus()
        if not selected_row:
            return
            
        data = self.supplierTable.item(selected_row)
        row = data['values']
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0', END)
        self.txt_desc.insert(END, row[3])

    def search(self):
        if not self.var_searchtxt.get():
            messagebox.showerror("Error", "Invoice number is required", parent=self.root)
            return
            
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_searchtxt.get(),))
            rows = cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            if rows:
                for row in rows:
                    self.supplierTable.insert('', END, values=row)
            else:
                messagebox.showinfo("Not Found", "No matching records found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.var_searchtxt.set("")
        self.txt_desc.delete('1.0', END)
        self.show()

    def validate_inputs(self):
        if not self.var_sup_invoice.get():
            messagebox.showerror("Error", "Invoice number is required", parent=self.root)
            return False
        if not self.var_name.get():
            messagebox.showerror("Error", "Name is required", parent=self.root)
            return False
        if not self.var_contact.get() or not self.var_contact.get().isdigit() or len(self.var_contact.get()) < 10:
            messagebox.showerror("Error", "Valid contact number (10+ digits) is required", parent=self.root)
            return False
        return True


if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()