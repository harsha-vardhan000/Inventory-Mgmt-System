from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os

class Login_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System | Developed by Harsha")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")
        
        # Variables
        self.employee_id = StringVar()
        self.password = StringVar()
        
        # Images
        self.phone_image = ImageTk.PhotoImage(file="images/phone.png")
        self.lbl_Phone_image = Label(self.root, image=self.phone_image, bd=0).place(x=200, y=50)

        # Login Frame
        login_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        login_frame.place(x=650, y=90, width=350, height=460)

        title = Label(login_frame, text="Login System", font=("Elephant", 30, "bold"), bg="white").place(x=0, y=30, relwidth=1)

        lbl_user = Label(login_frame, text="Employee ID", font=("Andalus", 15), bg="white", fg="#767171").place(x=50, y=100)
        txt_employee_id = Entry(login_frame, textvariable=self.employee_id, font=("times new roman", 15), bg="#ECECEC").place(x=50, y=140, width=250)

        lbl_pass = Label(login_frame, text="Password", font=("Andalus", 15), bg="white", fg="#767171").place(x=50, y=190)
        txt_pass = Entry(login_frame, textvariable=self.password, show="*", font=("times new roman", 15), bg="#ECECEC").place(x=50, y=240, width=250)

        btn_login = Button(login_frame, command=self.login, text="Log In", font=("Arial Rounded MT Bold", 15), bg="#00B0F0", activebackground="#00B0F0", fg="white", activeforeground="white", cursor="hand2").place(x=50, y=300, width=250, height=35)

        hr = Label(login_frame, bg="lightgray").place(x=50, y=370, width=250, height=2)
        or_ = Label(login_frame, text="OR", bg="white", fg="lightgray", font=("times new roman", 15, "bold")).place(x=150, y=355)

        btn_forget = Button(login_frame, text="Forgot Password", command=self.forget_window, font=("times new roman", 13), bg="white", fg="#00759E", bd=0, activebackground="white", activeforeground="#00759E", cursor="hand2").place(x=100, y=390)

        #======animation images========
        self.im1=ImageTk.PhotoImage(file="images/im1.png")
        self.im2=ImageTk.PhotoImage(file="images/im2.png")
        self.im3=ImageTk.PhotoImage(file="images/im3.png")

        self.lbl_change_image=Label(self.root,bg="gray")
        self.lbl_change_image.place(x=367,y=153,width=240,height=428)

        self.animate()

#===========All Functions================

    def animate(self):
        self.im=self.im1
        self.im1=self.im2
        self.im2=self.im3
        self.im3=self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000,self.animate)

    def validate_login(self, eid, password):
        """Validate login credentials against database"""
        try:
            with sqlite3.connect(database=r'ims.db') as con:
                cur = con.cursor()
                # Check if employee exists
                cur.execute("SELECT eid, pass, utype FROM employee WHERE eid=?", (eid,))
                employee = cur.fetchone()
                
                if not employee:
                    return None, "Employee ID not found"
                
                stored_password = employee[1]
                input_password = password
                
                if stored_password != input_password:
                    return None, "Invalid password"
                
                return employee[2], None  # Return utype if successful
                
        except sqlite3.Error as e:
            return None, f"Database error: {str(e)}"
        except Exception as e:
            return None, f"Unexpected error: {str(e)}"

    def login(self):
        """Handle login button click"""
        eid = self.employee_id.get().strip()
        password = self.password.get().strip()
        
        if not eid or not password:
            messagebox.showerror('Error', "Both Employee ID and Password are required", parent=self.root)
            return
        
        utype, error = self.validate_login(eid, password)
        
        if error:
            messagebox.showerror('Login Failed', error, parent=self.root)
            return
        
        # Login successful - redirect based on user type
        self.root.destroy()
        if utype == "Admin":
            os.system("python dashboard.py")
        else:
            os.system("python billing.py")

    def forget_window(self):
        """Create password reset window"""
        self.forget_win = Toplevel(self.root)
        self.forget_win.title('Reset Password')
        self.forget_win.geometry('400x350+500+100')
        self.forget_win.focus_force()

        title = Label(self.forget_win, text='Reset Password', font=('goudy old style', 15, 'bold'), bg="#3f51b5", fg="white").pack(side=TOP, fill=X)

        Label(self.forget_win, text="Enter Employee ID", font=("times new roman", 15)).place(x=20, y=60)
        Entry(self.forget_win, textvariable=self.employee_id, font=("times new roman", 15), bg="lightyellow").place(x=20, y=90, width=250, height=30)

        Label(self.forget_win, text="New Password", font=("times new roman", 15)).place(x=20, y=140)
        Entry(self.forget_win, textvariable=self.password, show="*", font=("times new roman", 15), bg="lightyellow").place(x=20, y=170, width=250, height=30)

        btn_update = Button(self.forget_win, text="Update Password", command=self.update_password, font=("times new roman", 15), bg="lightblue")
        btn_update.place(x=100, y=230, width=200, height=30)

    def update_password(self):
        """Handle password update"""
        eid = self.employee_id.get()
        new_pass = self.password.get()
        
        if not eid or not new_pass:
            messagebox.showerror("Error", "Employee ID and new password are required", parent=self.forget_win)
            return
        
        if len(new_pass) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters", parent=self.forget_win)
            return
        
        try:
            with sqlite3.connect(database=r'ims.db') as con:
                cur = con.cursor()
                # Check if employee exists
                cur.execute("SELECT eid FROM employee WHERE eid=?", (eid,))
                if not cur.fetchone():
                    messagebox.showerror("Error", "Employee ID not found", parent=self.forget_win)
                    return
                
                # Update password
                cur.execute("UPDATE employee SET pass=? WHERE eid=?", (new_pass, eid))
                con.commit()
                
                messagebox.showinfo("Success", "Password updated successfully", parent=self.forget_win)
                self.forget_win.destroy()
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to update password: {str(e)}", parent=self.forget_win)
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}", parent=self.forget_win)


# Initialize database and run application
if __name__ == "__main__":
    root = Tk()
    obj = Login_System(root)
    root.mainloop()