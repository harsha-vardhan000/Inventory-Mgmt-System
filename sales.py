from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os

class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed by Harsha")
        self.root.config(bg="white")
        self.root.focus_force()

        # Create bills directory if not exists
        if not os.path.exists('bills'):
            os.makedirs('bills')

        self.bill_list = []
        self.var_invoice = StringVar()
        
        # =========== Title ==============
        lbl_title = Label(self.root, text="View Customer Bills", font=("goudy old style", 30), 
                        bg="#184a45", fg="white", bd=3, relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X, padx=10, pady=20)
        
        # =========== Search Frame ===========
        lbl_invoice = Label(self.root, text="Invoice No.", font=("times new roman", 15), bg="white")
        lbl_invoice.place(x=50, y=100)
        
        txt_invoice = Entry(self.root, textvariable=self.var_invoice, font=("times new roman", 15), 
                          bg="lightyellow")
        txt_invoice.place(x=160, y=100, width=180, height=28)

        btn_search = Button(self.root, text="Search", command=self.search, 
                          font=("times new roman", 15, "bold"), bg="#2196f3", 
                          fg="white", cursor="hand2")
        btn_search.place(x=360, y=100, width=120, height=28)
        
        btn_clear = Button(self.root, text="Clear", command=self.clear, 
                         font=("times new roman", 15, "bold"), bg="lightgray", 
                         cursor="hand2")
        btn_clear.place(x=490, y=100, width=120, height=28)
        
        btn_refresh = Button(self.root, text="Refresh", command=self.show, 
                           font=("times new roman", 15, "bold"), bg="#4CAF50", 
                           fg="white", cursor="hand2")
        btn_refresh.place(x=620, y=100, width=120, height=28)

        # =========== Bill List Frame ===========
        sales_Frame = Frame(self.root, bd=3, relief=RIDGE)
        sales_Frame.place(x=50, y=140, width=200, height=330)

        scrolly = Scrollbar(sales_Frame, orient=VERTICAL)
        self.Sales_List = Listbox(sales_Frame, font=("goudy old style", 15), 
                                bg="white", yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH, expand=1)
        self.Sales_List.bind("<ButtonRelease-1>", self.get_data)

        # =========== Bill Area ===========
        bill_Frame = Frame(self.root, bd=3, relief=RIDGE)
        bill_Frame.place(x=280, y=140, width=410, height=330)
        
        lbl_title2 = Label(bill_Frame, text="Customer Bill Area", 
                         font=("goudy old style", 20), bg="orange")
        lbl_title2.pack(side=TOP, fill=X)
       
        scrolly2 = Scrollbar(bill_Frame, orient=VERTICAL)
        self.bill_area = Text(bill_Frame, bg="lightyellow", 
                            yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1)

        # =========== Image ===========
        self.load_image()
        
        lbl_image = Label(self.root, image=self.bill_photo, bd=0)
        lbl_image.place(x=700, y=110)

        # =========== Delete Button ===========
        btn_delete = Button(self.root, text="Delete", command=self.delete_bill, 
                          font=("times new roman", 15, "bold"), bg="#f44336", 
                          fg="white", cursor="hand2")
        btn_delete.place(x=50, y=480, width=200, height=30)

        self.show()

    def load_image(self):
        """Load the bill image with error handling"""
        try:
            self.bill_photo = Image.open("images/cat2.jpg")
            self.bill_photo = self.bill_photo.resize((450, 300))
            self.bill_photo = ImageTk.PhotoImage(self.bill_photo)
        except Exception as e:
            print(f"Image loading error: {e}")
            # Create blank image as fallback
            self.bill_photo = Image.new('RGB', (450, 300), color='white')
            self.bill_photo = ImageTk.PhotoImage(self.bill_photo)

    def show(self):
        """Load all bill files into the listbox"""
        self.bill_list.clear()
        self.Sales_List.delete(0, END)
        
        try:
            for file in os.listdir('bills'):
                if file.endswith('.txt'):
                    self.Sales_List.insert(END, file)
                    self.bill_list.append(file[:-4])  # Remove .txt extension
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load bills: {str(e)}", parent=self.root)

    def get_data(self, ev=None):
        """Display the content of selected bill"""
        if not self.Sales_List.curselection():
            return
            
        file_name = self.Sales_List.get(self.Sales_List.curselection()[0])
        file_path = os.path.join('bills', file_name)
        
        self.bill_area.delete('1.0', END)
        try:
            with open(file_path, 'r') as fp:
                content = fp.read()
                self.bill_area.insert(END, content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read bill: {str(e)}", parent=self.root)

    def search(self):
        """Search for a bill by invoice number"""
        search_term = self.var_invoice.get().strip()
        if not search_term:
            messagebox.showerror("Error", "Invoice No. is required", parent=self.root)
            return
        
        found = False
        for bill in self.bill_list:
            if search_term.lower() in bill.lower():
                self.show_bill_content(bill)
                found = True
                break
        
        if not found:
            messagebox.showerror("Error", "No matching invoice found", parent=self.root)

    def show_bill_content(self, bill_name):
        """Display content of a specific bill"""
        file_path = os.path.join('bills', f"{bill_name}.txt")
        self.bill_area.delete('1.0', END)
        try:
            with open(file_path, 'r') as fp:
                content = fp.read()
                self.bill_area.insert(END, content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read bill: {str(e)}", parent=self.root)

    def clear(self):
        """Clear search and bill display"""
        self.var_invoice.set("")
        self.show()
        self.bill_area.delete('1.0', END)

    def delete_bill(self):
        """Delete the currently selected bill"""
        if not self.Sales_List.curselection():
            messagebox.showwarning("Warning", "Please select a bill to delete", parent=self.root)
            return
        
        file_name = self.Sales_List.get(self.Sales_List.curselection()[0])
        confirm = messagebox.askyesno("Confirm", f"Delete bill {file_name}?", parent=self.root)
        if not confirm:
            return
            
        try:
            os.remove(os.path.join('bills', file_name))
            self.show()
            self.bill_area.delete('1.0', END)
            messagebox.showinfo("Success", "Bill deleted successfully", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete bill: {str(e)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()