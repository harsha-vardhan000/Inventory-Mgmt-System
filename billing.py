from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import time
import os
import tempfile
import re

class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System | Developed by Harsha")
        self.root.config(bg="white")
        self.cart_list = []
        self.chk_print = 0
        
        #===title===
        try:
            self.icon_title = PhotoImage(file="images/logo1.png")
            title = Label(self.root, text="Inventory Management System", image=self.icon_title, 
                         compound=LEFT, font=("times new roman", 40, "bold"), bg="#010c48", 
                         fg="white", anchor='w', padx=20)
            title.place(x=0, y=0, relwidth=1, height=70)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load logo: {str(e)}")
            title = Label(self.root, text="Inventory Management System", 
                         font=("times new roman", 40, "bold"), bg="#010c48", 
                         fg="white", anchor='w', padx=20)
            title.place(x=0, y=0, relwidth=1, height=70)

        #===button===
        btn_logout = Button(self.root, text="Logout", command=self.logout, 
                          font=("times new roman", 15, "bold"), bg="yellow", 
                          cursor="hand2")
        btn_logout.place(x=1100, y=10, height=50, width=150)
        
        #==clock==
        self.lbl_clock = Label(self.root, 
                              text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",
                              font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        #===========Product_Frame========
        ProductFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        ProductFrame1.place(x=6, y=110, width=410, height=550)

        pTitle = Label(ProductFrame1, text="All Products", font=("goudy old style", 20, "bold"), 
                      bg="#262626", fg="white").pack(side=TOP, fill=X)

        #=====Product Search Frame=============
        self.var_search = StringVar()
        ProductFrame2 = Frame(ProductFrame1, bd=2, relief=RIDGE, bg="white")
        ProductFrame2.place(x=2, y=42, width=398, height=90)

        lbl_search = Label(ProductFrame2, text="Search Product | By Name", 
                          font=("times new roman", 15, "bold"), bg="white", fg="green").place(x=2, y=5)

        lbl_name = Label(ProductFrame2, text="Product Name", font=("times new roman", 15, "bold"), 
                       bg="white").place(x=2, y=45)
        txt_search = Entry(ProductFrame2, textvariable=self.var_search, 
                          font=("times new roman", 15), bg="lightyellow")
        txt_search.place(x=128, y=47, width=150, height=22)
        btn_search = Button(ProductFrame2, text="Search", command=self.search, 
                           font=("goudy old style", 15), bg="#2196f3", fg="white", 
                           cursor="hand2").place(x=285, y=45, width=100, height=25)
        btn_show_all = Button(ProductFrame2, text="Show All", command=self.show, 
                             font=("goudy old style", 15), bg="#083531", fg="white", 
                             cursor="hand2").place(x=285, y=10, width=100, height=25)

        #=======Product Details Frame============
        ProductFrame3 = Frame(ProductFrame1, bd=3, relief=RIDGE)
        ProductFrame3.place(x=2, y=140, width=395, height=375)

        scrolly = Scrollbar(ProductFrame3, orient=VERTICAL)
        scrollx = Scrollbar(ProductFrame3, orient=HORIZONTAL)

        self.product_Table = ttk.Treeview(ProductFrame3, columns=("pid", "name", "price", "qty", "status"), 
                                         yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)
        
        self.product_Table.heading("pid", text="PID")
        self.product_Table.heading("name", text="Name")
        self.product_Table.heading("price", text="Price")
        self.product_Table.heading("qty", text="QTY")
        self.product_Table.heading("status", text="Status")
        self.product_Table["show"] = "headings"

        self.product_Table.column("pid", width=40)
        self.product_Table.column("name", width=100)
        self.product_Table.column("price", width=100)
        self.product_Table.column("qty", width=40)
        self.product_Table.column("status", width=90)
        self.product_Table.pack(fill=BOTH, expand=1)
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)
        
        lbl_note = Label(ProductFrame1, 
                         text="Note: Enter 0 Quantity to remove product from cart.", 
                         font=("goudy old style", 11), anchor='w', bg="white", fg="red")
        lbl_note.pack(side=BOTTOM, fill=X)

        #======Customer Frame=======
        self.var_cname = StringVar()
        self.var_contact = StringVar()
        CustomerFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        CustomerFrame.place(x=420, y=110, width=530, height=70)

        cTitle = Label(CustomerFrame, text="Customer Details", font=("goudy old style", 15), 
                      bg="lightgray").pack(side=TOP, fill=X)
        lbl_name = Label(CustomerFrame, text="Name", font=("times new roman", 15), 
                        bg="white").place(x=5, y=35)
        txt_name = Entry(CustomerFrame, textvariable=self.var_cname, 
                         font=("times new roman", 13), bg="lightyellow").place(x=80, y=35, width=180)
        
        lbl_contact = Label(CustomerFrame, text="Contact No.", font=("times new roman", 15), 
                           bg="white").place(x=270, y=35)
        txt_contact = Entry(CustomerFrame, textvariable=self.var_contact, 
                            font=("times new roman", 13), bg="lightyellow").place(x=380, y=35, width=140)
        
        #====Cal Cart Frame==========
        Cal_Cart_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        Cal_Cart_Frame.place(x=420, y=190, width=530, height=360)

        #====Calculator Frame==========
        self.var_cal_input = StringVar()

        Cal_Frame = Frame(Cal_Cart_Frame, bd=9, relief=RIDGE, bg="white")
        Cal_Frame.place(x=5, y=10, width=268, height=340)

        txt_cal_input = Entry(Cal_Frame, textvariable=self.var_cal_input, 
                              font=('arial', 15, 'bold'), width=21, bd=10, 
                              relief=GROOVE, state='readonly', justify=RIGHT)
        txt_cal_input.grid(row=0, columnspan=4)

        btn_7 = Button(Cal_Frame, text='7', font=('arial', 15, 'bold'), 
                       command=lambda: self.get_input(7), bd=5, width=4, pady=10, 
                       cursor="hand2").grid(row=1, column=0)
        btn_8 = Button(Cal_Frame, text='8', font=('arial', 15, 'bold'), 
                       command=lambda: self.get_input(8), bd=5, width=4, pady=10, 
                       cursor="hand2").grid(row=1, column=1)
        btn_9 = Button(Cal_Frame, text='9', font=('arial', 15, 'bold'), 
                       command=lambda: self.get_input(9), bd=5, width=4, pady=10, 
                       cursor="hand2").grid(row=1, column=2)
        btn_sum = Button(Cal_Frame, text='+', font=('arial', 15, 'bold'), 
                         command=lambda: self.get_input('+'), bd=5, width=4, pady=10, 
                         cursor="hand2").grid(row=1, column=3)

        btn_4 = Button(Cal_Frame, text='4', font=('arial', 15, 'bold'), 
                       command=lambda: self.get_input(4), bd=5, width=4, pady=10, 
                       cursor="hand2").grid(row=2, column=0)
        btn_5 = Button(Cal_Frame, text='5', font=('arial', 15, 'bold'), 
                       command=lambda: self.get_input(5), bd=5, width=4, pady=10, 
                       cursor="hand2").grid(row=2, column=1)
        btn_6 = Button(Cal_Frame, text='6', font=('arial', 15, 'bold'), 
                       command=lambda: self.get_input(6), bd=5, width=4, pady=10, 
                       cursor="hand2").grid(row=2, column=2)
        btn_sub = Button(Cal_Frame, text='-', font=('arial', 15, 'bold'), 
                         command=lambda: self.get_input('-'), bd=5, width=4, pady=10, 
                         cursor="hand2").grid(row=2, column=3)

        btn_1 = Button(Cal_Frame, text='1', font=('arial', 15, 'bold'), 
                       command=lambda: self.get_input(1), bd=5, width=4, pady=10, 
                       cursor="hand2").grid(row=3, column=0)
        btn_2 = Button(Cal_Frame, text='2', font=('arial', 15, 'bold'), 
                       command=lambda: self.get_input(2), bd=5, width=4, pady=10, 
                       cursor="hand2").grid(row=3, column=1)
        btn_3 = Button(Cal_Frame, text='3', font=('arial', 15, 'bold'), 
                       command=lambda: self.get_input(3), bd=5, width=4, pady=10, 
                       cursor="hand2").grid(row=3, column=2)
        btn_mul = Button(Cal_Frame, text='*', font=('arial', 15, 'bold'), 
                         command=lambda: self.get_input('*'), bd=5, width=4, pady=10, 
                         cursor="hand2").grid(row=3, column=3)

        btn_0 = Button(Cal_Frame, text='0', font=('arial', 15, 'bold'), 
                       command=lambda: self.get_input(0), bd=5, width=4, pady=15, 
                       cursor="hand2").grid(row=4, column=0)
        btn_c = Button(Cal_Frame, text='C', font=('arial', 15, 'bold'), 
                       command=self.clear_cal, bd=5, width=4, pady=15, 
                       cursor="hand2").grid(row=4, column=1)
        btn_eq = Button(Cal_Frame, text='=', font=('arial', 15, 'bold'), 
                        command=self.perform_cal, bd=5, width=4, pady=15, 
                        cursor="hand2").grid(row=4, column=2)
        btn_div = Button(Cal_Frame, text='/', font=('arial', 15, 'bold'), 
                         command=lambda: self.get_input('/'), bd=5, width=4, pady=15, 
                         cursor="hand2").grid(row=4, column=3)

        #====Cart Frame==========
        cart_Frame = Frame(Cal_Cart_Frame, bd=3, relief=RIDGE)
        cart_Frame.place(x=280, y=8, width=245, height=342)
        self.cartTitle = Label(cart_Frame, text="Cart \t Total Product: [0]", 
                              font=("goudy old style", 15), bg="lightgray")
        self.cartTitle.pack(side=TOP, fill=X)
        
        scrolly = Scrollbar(cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(cart_Frame, orient=HORIZONTAL)

        self.CartTable = ttk.Treeview(cart_Frame, columns=("pid", "name", "price", "qty", "stock"), 
                                     yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        
        self.CartTable.heading("pid", text="PID")
        self.CartTable.heading("name", text="Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="QTY")
        self.CartTable["show"] = "headings"

        self.CartTable.column("pid", width=40)
        self.CartTable.column("name", width=90)
        self.CartTable.column("price", width=90)
        self.CartTable.column("qty", width=40)
        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)
        
        #====ADD Cart Widget Frame==========
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()
        
        Add_CartWidgetsFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        Add_CartWidgetsFrame.place(x=420, y=550, width=530, height=110)

        lbl_p_name = Label(Add_CartWidgetsFrame, text="Product Name", 
                           font=("times new roman", 15), bg="white").place(x=5, y=5)
        txt_p_name = Entry(Add_CartWidgetsFrame, textvariable=self.var_pname, 
                           font=("times new roman", 15), bg="lightyellow", state='readonly')
        txt_p_name.place(x=5, y=35, width=190, height=22)

        lbl_p_price = Label(Add_CartWidgetsFrame, text="Price Per Qty", 
                            font=("times new roman", 15), bg="white").place(x=230, y=5)
        txt_p_price = Entry(Add_CartWidgetsFrame, textvariable=self.var_price, 
                             font=("times new roman", 15), bg="lightyellow", state='readonly')
        txt_p_price.place(x=230, y=35, width=150, height=22)

        lbl_p_qty = Label(Add_CartWidgetsFrame, text="Quantity", 
                          font=("times new roman", 15), bg="white").place(x=390, y=5)
        txt_p_qty = Entry(Add_CartWidgetsFrame, textvariable=self.var_qty, 
                           font=("times new roman", 15), bg="lightyellow")
        txt_p_qty.place(x=390, y=35, width=120, height=22)

        self.lbl_inStock = Label(Add_CartWidgetsFrame, text="In Stock", 
                                 font=("times new roman", 15), bg="white")
        self.lbl_inStock.place(x=5, y=70)
        
        btn_clear_cart = Button(Add_CartWidgetsFrame, text="Clear", command=self.clear_cart, 
                                font=("times new roman", 15, "bold"), bg="lightgray", 
                                cursor="hand2").place(x=180, y=70, width=150, height=30)
        btn_add_cart = Button(Add_CartWidgetsFrame, text="Add | Update Cart", 
                              command=self.add_update_cart, font=("times new roman", 15, "bold"), 
                              bg="orange", cursor="hand2").place(x=340, y=70, width=180, height=30)

        #==========billing area================
        billFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billFrame.place(x=953, y=110, width=410, height=410)

        BTitle = Label(billFrame, text="Customer Bill Area", 
                       font=("goudy old style", 20, "bold"), bg="#f44336", fg="white")
        BTitle.pack(side=TOP, fill=X)
        
        scrolly = Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #==============billing buttons==================
        billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billMenuFrame.place(x=953, y=520, width=410, height=140)

        self.lbl_amt = Label(billMenuFrame, text='Bill Amount\n[0]', 
                             font=("goudy old style", 15, "bold"), bg="#3f51b5", fg="white")
        self.lbl_amt.place(x=2, y=5, width=120, height=70)

        self.lbl_discount = Label(billMenuFrame, text='Discount\n[5%]', 
                                  font=("goudy old style", 15, "bold"), bg="#8bc34a", fg="white")
        self.lbl_discount.place(x=124, y=5, width=120, height=70)

        self.lbl_net_pay = Label(billMenuFrame, text='Net Pay\n[0]', 
                                 font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white")
        self.lbl_net_pay.place(x=246, y=5, width=160, height=70)

        btn_print = Button(billMenuFrame, text='Print', command=self.print_bill, 
                           font=("goudy old style", 15, "bold"), bg="lightgreen", 
                           fg="white", cursor="hand2")
        btn_print.place(x=2, y=80, width=120, height=50)

        btn_clear_all = Button(billMenuFrame, text='Clear All', command=self.clear_all, 
                               font=("goudy old style", 15, "bold"), bg="gray", 
                               fg="white", cursor="hand2")
        btn_clear_all.place(x=124, y=80, width=120, height=50)

        btn_generate = Button(billMenuFrame, text='Generate Bill/Save Bill', 
                              command=self.generate_bill, 
                              font=("goudy old style", 15, "bold"), bg="#009688", 
                              fg="white", cursor="hand2")
        btn_generate.place(x=246, y=80, width=160, height=50)

        #===========Footer==============
        footer = Label(self.root, 
                       text="IMS-Inventory Management System | Developed by Harsha\nFor any issues contact: 6361xxx852", 
                       font=("times new roman", 11), bg="#4d636d", fg="white")
        footer.pack(side=BOTTOM, fill=X)

        self.show()
        self.update_date_time()

    #==========================All Functions======================
    def get_input(self, num):
        current = self.var_cal_input.get()
        if num in '+-*/' and current and current[-1] in '+-*/':
            return  # Prevent consecutive operators
        self.var_cal_input.set(current + str(num))

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        try:
            result = eval(self.var_cal_input.get())
            self.var_cal_input.set(str(result))
        except:
            messagebox.showerror("Error", "Invalid calculation", parent=self.root)
            self.var_cal_input.set('')

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT pid, name, price, qty, status FROM product WHERE status='Active'")
            rows = cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if not self.var_search.get():
                messagebox.showerror("Error", "Search input is required", parent=self.root)
                return
            
            search_term = f"%{self.var_search.get()}%"
            cur.execute("SELECT pid, name, price, qty, status FROM product WHERE name LIKE ? AND status='Active'", 
                        (search_term,))
            rows = cur.fetchall()
            
            self.product_Table.delete(*self.product_Table.get_children())
            if rows:
                for row in rows:
                    self.product_Table.insert('', END, values=row)
            else:
                messagebox.showinfo("Info", "No products found matching your search", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.product_Table.focus()
        content = self.product_Table.item(f)
        row = content['values']
        if row:
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            self.var_price.set(row[2])
            self.var_stock.set(row[3])  # Set the stock value
            self.lbl_inStock.config(text=f"In Stock [{row[3]}]")
            self.var_qty.set('1')

    def get_data_cart(self, ev):
        f = self.CartTable.focus()
        content = self.CartTable.item(f)
        row = content['values']
        if row:
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            self.var_price.set(row[2])
            self.var_qty.set(row[3])
            self.var_stock.set(row[4])  # Set the stock value
            self.lbl_inStock.config(text=f"In Stock [{row[4]}]")

    def add_update_cart(self):
        # Validate inputs
        if not self.var_pid.get():
            messagebox.showerror('Error', "Please select a product from the list", parent=self.root)
            return
        
        if not self.var_qty.get() or not self.var_qty.get().isdigit():
            messagebox.showerror('Error', "Please enter a valid quantity (numbers only)", parent=self.root)
            return
        
        qty = int(self.var_qty.get())
        stock = int(self.var_stock.get())
        
        if qty <= 0:
            messagebox.showerror('Error', "Quantity must be greater than 0", parent=self.root)
            return
        
        if qty > stock:
            messagebox.showerror('Error', f"Only {stock} items available in stock", parent=self.root)
            return
        
        # Calculate total price for the quantity
        price = float(self.var_price.get())
        total_price = price * qty
        
        cart_data = [
            self.var_pid.get(),
            self.var_pname.get(),
            price,
            str(qty),
            str(stock)
        ]
        
        # Check if product already in cart
        present = False
        index = 0
        for i, item in enumerate(self.cart_list):
            if item[0] == self.var_pid.get():
                present = True
                index = i
                break
        
        if present:
            if qty == 0:
                self.cart_list.pop(index)
            else:
                self.cart_list[index] = cart_data
        else:
            self.cart_list.append(cart_data)
        
        self.show_cart()
        self.bill_updates()
        self.clear_cart()

    def bill_updates(self):
        self.bill_amt = 0
        self.net_pay = 0
        self.discount = 0
        
        for item in self.cart_list:
            self.bill_amt += (float(item[2]) * int(item[3]))
        
        self.discount = (self.bill_amt * 5) / 100
        self.net_pay = self.bill_amt - self.discount
        
        self.lbl_amt.config(text=f'Bill Amount\nRs.{self.bill_amt:.2f}')
        self.lbl_discount.config(text=f'Discount\nRs.{self.discount:.2f}')
        self.lbl_net_pay.config(text=f'Net Pay\nRs.{self.net_pay:.2f}')
        self.cartTitle.config(text=f"Cart \t Total Product: [{len(self.cart_list)}]")

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for item in self.cart_list:
                self.CartTable.insert('', END, values=item)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def generate_bill(self):
        # Validate customer details
        if not self.var_cname.get():
            messagebox.showerror("Error", "Customer Name is required", parent=self.root)
            return
        
        if not self.var_contact.get():
            messagebox.showerror("Error", "Contact Number is required", parent=self.root)
            return
        
        if not re.match(r'^\d{10}$', self.var_contact.get()):
            messagebox.showerror("Error", "Invalid Contact Number (10 digits required)", parent=self.root)
            return
        
        if not self.cart_list:
            messagebox.showerror("Error", "Please add products to the cart", parent=self.root)
            return
        
        # Generate bill
        self.bill_top()
        self.bill_middle()
        self.bill_bottom()
        
        # Save bill to file
        bill_dir = 'bills'
        if not os.path.exists(bill_dir):
            os.makedirs(bill_dir)
        
        bill_path = os.path.join(bill_dir, f'{self.invoice}.txt')
        try:
            with open(bill_path, 'w') as f:
                f.write(self.txt_bill_area.get('1.0', END))
            messagebox.showinfo('Success', f"Bill has been saved as {bill_path}", parent=self.root)
            self.chk_print = 1
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save bill: {str(e)}", parent=self.root)

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_temp = f"""
{'='*50}
\t\tXYZ INVENTORY SYSTEM
\tPhone: 6361******, Bangalore-560097
{'='*50}
Customer Name: {self.var_cname.get()}
Contact No.: {self.var_contact.get()}
Bill No.: {self.invoice}\t\tDate: {time.strftime("%d/%m/%Y %I:%M %p")}
{'='*50}
{'Product Name'.ljust(30)}{'Qty'.center(10)}{'Price'.rjust(10)}
{'='*50}
"""
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)

    def bill_middle(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            for item in self.cart_list:
                pid = item[0]
                name = item[1]
                qty_sold = int(item[3])
                new_qty = int(item[4]) - qty_sold
                status = 'Active' if new_qty > 0 else 'Inactive'
                price = float(item[2]) * qty_sold
                
                # Add to bill display
                self.txt_bill_area.insert(END, f"\n{name.ljust(30)}{str(qty_sold).center(10)}{f'Rs.{price:.2f}'.rjust(10)}")
                
                # Update database
                cur.execute('UPDATE product SET qty=?, status=? WHERE pid=?', 
                           (new_qty, status, pid))
                con.commit()
            
            self.show()  # Refresh product list
        except Exception as ex:
            messagebox.showerror("Error", f"Error updating inventory: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def bill_bottom(self):
        bill_bottom_temp = f"""
{'='*50}
{'Bill Amount:'.ljust(40)}Rs.{self.bill_amt:.2f}
{'Discount (5%):'.ljust(40)}Rs.{self.discount:.2f}
{'Net Pay:'.ljust(40)}Rs.{self.net_pay:.2f}
{'='*50}
\nThank you for shopping with us!
"""
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.var_stock.set('')
        self.lbl_inStock.config(text="In Stock")

    def clear_all(self):
        self.cart_list = []
        self.var_cname.set('')
        self.var_contact.set('')
        self.var_search.set('')
        self.txt_bill_area.delete('1.0', END)
        self.cartTitle.config(text="Cart \t Total Product: [0]")
        self.lbl_amt.config(text='Bill Amount\n[0]')
        self.lbl_discount.config(text='Discount\n[5%]')
        self.lbl_net_pay.config(text='Net Pay\n[0]')
        self.clear_cart()
        self.show()
        self.show_cart()
        self.chk_print = 0

    def update_date_time(self):
        time_ = time.strftime("%I:%M:%S")
        date_ = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {date_}\t\t Time: {time_}")
        self.lbl_clock.after(200, self.update_date_time)

    def print_bill(self):
        if self.chk_print == 0:
            messagebox.showerror('Error', "Please generate bill first", parent=self.root)
            return
        
        try:
            # Create temporary file
            temp_file = tempfile.mktemp('.txt')
            with open(temp_file, 'w') as f:
                f.write(self.txt_bill_area.get('1.0', END))
            
            # Print based on OS
            if os.name == 'nt':  # Windows
                os.startfile(temp_file, 'print')
            else:  # Mac/Linux
                os.system(f'lpr {temp_file}')
            
            messagebox.showinfo('Print', "Printing started", parent=self.root)
        except Exception as e:
            messagebox.showerror("Print Error", f"Could not print: {str(e)}", parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

if __name__ == "__main__":
    root = Tk()
    obj = BillClass(root)
    root.mainloop()