import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from ttkbootstrap import ttk
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.tooltip import ToolTip
from PIL import Image, ImageTk
import mysql.connector as mys
import os


#BEFORE RUNNING THIS CODE..DROP YOUR DATABASE,CREATE IT AGAIN AND SOURCE YOUR DUMP FILE(dump20250414)

# >>>>>>>>>>>>>>>> Define the main window <<<<<<<<<<<<<<<<
root = tb.Window(themename="cyborg")
root.geometry('1600x1400')
root.title("Real Estate Management")

# Connecting MySQL to Python Interface
mycon = mys.connect(host="localhost", user="root", passwd="root", database="re_estate")
cursor = mycon.cursor()


# make sure 'interested_users' table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS interested_users (
    tenant_username VARCHAR(100),
    property_id VARCHAR(100),
    PRIMARY KEY (tenant_username, property_id),
    FOREIGN KEY (tenant_username) REFERENCES users(username),
    FOREIGN KEY (property_id) REFERENCES properties(property_id)
)
""")
mycon.commit()


# make sure 'transaction_type' column exists in the table
try:
    cursor.execute("ALTER TABLE interested_users ADD COLUMN transaction_type VARCHAR(20)")
    mycon.commit()
except mys.errors.ProgrammingError as e:
    if "Duplicate column name" in str(e):
        pass  # Column already exists: ignore
    else:
        raise  # Raise unexpected errors



# >>>>> Create Frames
login_frame=tb.Frame(root)
login_frame.pack(expand=True, fill='both')

main_frame=tb.Frame(root)

profile_frame = tb.Frame(root)

prop_detail_frame = tb.Frame(root)

post_prop_frame = tb.Frame(root)

my_tent_frame = tb.Frame(root)




# >>>>>>>>>> THE LOGIN FRAME FUNCTIONS <<<<<<<<<<

# COMMON Functions For The Login Page
def login_success():
    username_entry_si.delete(0,END)
    password_entry_si.delete(0,END)
    login_frame.pack_forget()
    main_frame.pack(expand=True, fill='both')


def role_select(uname):
    global img_tent, img_own  # Keep reference to images

    role_select_frame = tk.Toplevel(main_frame)
    role_select_frame.title("Select your role")
    role_select_frame.geometry("500x600")

    tb.Label(role_select_frame, text="What are you here as?", font=("Arial", 14)).pack(pady=20)

    rframe = ttk.Frame(role_select_frame)
    rframe.pack(pady=10)

    # Tenant Role Button
    img_tent = Image.open("images/tenant.jpg").resize((100, 100))
    img_tent = ImageTk.PhotoImage(img_tent)
    img_btn_tent = tb.Button(rframe, image=img_tent, bootstyle=tb.LINK, 
                             command=lambda: select_role("Tenant",uname,role_select_frame))
    img_btn_tent.pack(pady=10)
    tb.Label(rframe, text="TENANT", font=("Arial", 14), bootstyle="primary").pack()

    # Owner Role Button
    img_own = Image.open("images/owner.jpeg").resize((100, 100))
    img_own = ImageTk.PhotoImage(img_own)
    img_btn_own = tb.Button(rframe, image=img_own, bootstyle=tb.LINK, 
                            command=lambda: select_role("Owner",uname,role_select_frame))
    img_btn_own.pack(pady=10)
    tb.Label(rframe, text="OWNER", font=("Arial", 14), bootstyle="primary").pack()
    
def select_role(role,uname,frame):
    cursor.execute("update users set role='{}' where username = '{}'".format(role,uname))
    mycon.commit()
    create_profile(uname)
    frame.destroy()
    
import re
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None 

# Functions under the SIGN IN Button
def sign_in():
    
    cursor.execute("select * from users")
    users_data = cursor.fetchall()
    
    current_users = {}
    for name,username,password,phone,role,profile_pic in users_data:
        current_users.update({username:[name, username, password, phone, role, profile_pic]})
    
    if not username_entry_si.get() or not password_entry_si.get():
         messagebox.showerror("Error", "All fields are required!")

    elif not is_valid_email(username_entry_si.get()):
        messagebox.showerror("Error", "Invalid email address!")

    else:
        user_email = username_entry_si.get()
        user_pass = password_entry_si.get()
        
        if user_email in current_users and user_pass == current_users[user_email][2]:
            messagebox.showinfo("Success", f"Welcome {current_users[user_email][0]}!") 
            create_profile(user_email)
            login_success()
            
        elif user_email not in current_users:
            messagebox.showerror("Error", "Invalid username. Try signing up instead.")
            
        elif user_pass != current_users[user_email][2]:
            messagebox.showerror("Error", "Incorrect password.")
            forgot.configure(state=NORMAL)


pfp_user_email = None
def create_profile(the_username):                               ## prev user data is shown ## To be used in forgot password button as well
    global profile_btn, l1, pfp_user_email, bigger_profile_img  # Keep reference to avoid garbage collection
    
    pfp_user_email = the_username
    
    # Clear only dynamic widgets
    for widget in profile_frame.winfo_children():
        if hasattr(widget, "dynamic"):  # Only remove widgets we marked as dynamic
            widget.destroy()
            
    cursor.execute("select * from users where username='{}'".format(the_username))
    user_data = cursor.fetchone()
    
    name, _, _, phone, role, profile_pic = user_data
   
    img = Image.open(profile_pic)
    img = img.resize((70,70))
    profile_img = ImageTk.PhotoImage(img)
    img2=Image.open(profile_pic).resize((130,130))
    bigger_profile_img = ImageTk.PhotoImage(img2)
    
    # If the profile button already exists, just update the image
    if "profile_btn" in globals():
        profile_btn.config(image=profile_img)
        profile_btn.image = profile_img  # Keep reference
    else:
        profile_btn = tb.Button(sidebar, image=profile_img, bootstyle=tb.LINK, 
                                command=lambda: new_frame_open(profile_frame, main_frame))
        profile_btn.image = profile_img  # Keep reference
        profile_btn.grid(row=0, column=0, sticky=EW, pady=10)

    profile_btn = tb.Button(sidebar, image=profile_img, bootstyle=tb.LINK, command=lambda: new_frame_open(profile_frame, main_frame))
    profile_btn.grid(row=0,column=0,sticky=EW, pady=10,)

        
    l1 = tb.Label(profile_frame, image=bigger_profile_img)
    l1.grid(row=0,column=2,pady=20, columnspan=2)
    l1.dynamic = True  # Mark as dynamic
    
    l2 = tb.Label(profile_frame, text=f"{name}", font=("Arial Bold",12))
    l2.grid(row=2,column=3,padx=100,pady=20,sticky=E)
    l2.dynamic = True  # Mark as dynamic
    
    l3 = tb.Label(profile_frame, text=f"{the_username}", font=("Arial Bold",12))
    l3.grid(row=3,column=3,padx=100,pady=20,sticky=E)
    l3.dynamic = True  # Mark as dynamic
    
    l4 = tb.Label(profile_frame, text=f"{phone}", font=("Arial Bold",12))
    l4.grid(row=4,column=3,padx=100,pady=20,sticky=E)
    l4.dynamic = True  # Mark as dynamic
    
    l5 = tb.Label(profile_frame, text=f"{role}", font=("Arial Bold",12))
    l5.grid(row=5,column=3,padx=100,pady=20,sticky=E)
    l5.dynamic = True  # Mark as dynamic
    
    #"Post your property button for user:OWNER"
    if role == "Owner":
        post_prop_button=tb.Button(sidebar,text="POST\nYOUR\nPROPERTY",bootstyle=SUCCESS,command=post_prop_open)
        post_prop_button.grid(row=1,column=0,pady=10)
        
        tb.Button(sidebar, text="My\nProperties",bootstyle=SUCCESS,command=my_tent_open).grid(row=2, column=0, pady=10)
    
    else:
        for widget in sidebar.winfo_children():
            if isinstance(widget,tb.Button) and widget.cget("text")=="POST\nYOUR\nPROPERTY":
                widget.destroy()
    
    if role == "Tenant":
        tb.Button(sidebar, text="Look For\nProperties", bootstyle=SUCCESS, command= tenant_dashboard_open).grid(row=2, column=0, pady=10)
                

# Functions under the SIGN UP Button
def show_signup_window():

    signup_window = tk.Toplevel(login_frame)
    signup_window.title("Sign Up")
    signup_window.geometry("400x400")
    
    ttk.Label(signup_window, text="Name:").pack(pady=10)
    name_entry = ttk.Entry(signup_window)
    name_entry.pack(pady=5)
    
    ttk.Label(signup_window, text="Username:").pack(pady=10)
    username_entry_su = ttk.Entry(signup_window)
    username_entry_su.pack(pady=5)

    ttk.Label(signup_window, text="Password:").pack(pady=10)
    password_entry_su = ttk.Entry(signup_window, show="*")
    password_entry_su.pack(pady=5)
    
    ttk.Label(signup_window, text="Confirm Password:").pack(pady=10)
    confirm_password_entry = ttk.Entry(signup_window, show="*")
    confirm_password_entry.pack(pady=5)
    
    def submit_signup():
        
        cursor.execute("select username from users")
        users = cursor.fetchall()

        current_users = []
        for u in users:
            current_users.append(u[0])
        
        username_su = username_entry_su.get()
        password_su = password_entry_su.get()
        confirm_password_su = confirm_password_entry.get()
        name_su = name_entry.get()

        if not username_entry_su.get() or not password_entry_su.get() or not confirm_password_entry.get() or not name_entry.get():
            messagebox.showerror("Error", "All fields are required!") 
        
        elif password_su != confirm_password_su:
            messagebox.showerror("Error","Passwords do not match.")
            
        elif not is_valid_email(username_su):
            messagebox.showerror("Error", "Invalid email address!")
        
        
        elif username_su in current_users:
            messagebox.showerror("Error", "This email is already registered with us")
            
        else:
            cursor.execute("insert into users(name, username, password) values('{}','{}','{}')".format(name_su, username_su, password_su))
            mycon.commit()
            
            messagebox.showinfo("Success","Sign-up successful!")
            role_select(username_su)
            login_success()
            signup_window.destroy()


    submit_button = ttk.Button(signup_window, text="Sign Up", command=submit_signup)
    submit_button.pack(pady=20)


# Functions under the FORGOT PASSWORD Button
def reset_password(uname):  # Move reset_password OUTSIDE check_reg_email
    rpass_window = tk.Toplevel(login_frame)
    rpass_window.title("Reset Password")
    rpass_window.geometry("400x350")
    
    ttk.Label(rpass_window, text="Enter new password").pack(pady=10)
    new_pass_entry = ttk.Entry(rpass_window)
    new_pass_entry.pack(pady=5)
    
    ttk.Label(rpass_window, text="Confirm Password").pack(pady=10)
    confirm_pass_entry = ttk.Entry(rpass_window)
    confirm_pass_entry.pack(pady=5)
    
    def rpass():
        new_pass = new_pass_entry.get()
        confirm_pass = confirm_pass_entry.get()
        
        if not new_pass or not confirm_pass:
            messagebox.showerror("Error", "All Fields Are Mandatory")
        elif new_pass != confirm_pass:
            messagebox.showerror("Error", "Passwords do not match")
        else:
            messagebox.showinfo("Success", "Password has been Reset!")
            cursor.execute("UPDATE users SET password = '{}' WHERE username = '{}'".format(new_pass, uname))
            mycon.commit()
            create_profile(uname)
            login_success()
            rpass_window.destory()
    
    ttk.Button(rpass_window, text="Confirm", command=rpass).pack(pady=10)

def check_reg_email():  
    cursor.execute("select * from users")
    users_data = cursor.fetchall()
    
    current_users = {username: [name, username, password, phone, role, profile_pic] for name, username, password, phone, role, profile_pic in users_data}
    
    if username_entry_si.get() in current_users:
        messagebox.showinfo("Success", "We have sent a verification link to your email address. Please click 'ok' once you've verified your email address.")
        reset_password(username_entry_si.get())  # Now reset_password is properly defined
    else:
        messagebox.showerror("Error", "This email is not registered with us.")

       
# Function under the SHOW PASSWORD Button   
def show_password():
    if show_passVar.get():
        password_entry_si.configure(show="")
    else:
        password_entry_si.configure(show="*")     
     







# >>>>>>>>>>>>>>>>> THE LOGIN FRAME UI <<<<<<<<<<<<<<<<

tb.Label(login_frame,text="Login or Sign Up", font=("Verdana", 24)).pack(side=TOP, pady=10 )

un_frame=tb.LabelFrame(login_frame, text="Enter Username", width=100)
un_frame.pack(side=TOP, pady=10)

username_entry_si= tb.Entry(un_frame, bootstyle=PRIMARY, width=90)
username_entry_si.pack(side=TOP, padx=5, pady=10)

p_frame=tb.LabelFrame(login_frame, text="Enter Password", width=100)
p_frame.pack(side=TOP, pady=10)

password_entry_si= tb.Entry(p_frame,  bootstyle=PRIMARY,show="*",width=90 )
password_entry_si.pack(side=TOP, padx=5,pady=10)

show_passVar = tk.BooleanVar()
show_pass = tb.Checkbutton(p_frame, text="Show password", variable=show_passVar, onvalue=1, offvalue=0,bootstyle="PRIMARY-ROUND-TOGGLE",command=show_password)
show_pass.pack(side=LEFT, padx=5,pady=(0,10))

container = tk.Frame(login_frame) 
container.pack(side ="top",pady=10) 
   
tb.Button(container, text="Sign In", bootstyle=SUCCESS, width=10, command=sign_in).pack(side=LEFT, padx=5, pady=10)
tb.Button(container, text="Sign Up", bootstyle=(INFO, OUTLINE), width=10,command=show_signup_window).pack(side=LEFT, padx=5, pady=10)

forgot = tb.Button(login_frame, text="Forgot Password", bootstyle=(INFO, LINK),width=25,state=DISABLED, command=check_reg_email)
forgot.pack(side=TOP, padx=5, pady=0)








# >>>>>>>>>>>>>>>>> MAIN FRAME FUNCTIONS <<<<<<<<<<<<<<<<

# UI IN MAINFRAME
tb.Label(main_frame, text="Real Estate Management", font=("Helvetica", 18)).grid(column=1,row=0,padx=10,pady=10)

search_entry_frame = tb.Labelframe(main_frame,text="Search property by location")
search_entry_frame.grid(row=1,column=1,columnspan=2)

sf = ScrolledFrame(main_frame, autohide=True,width=1250, height=550)
sf.grid(row=2,column=1, padx=10, pady=10)

sidebar = tb.Frame(main_frame, width=0, height=750)
sidebar.grid(row=0,column=0,sticky=NW, rowspan=3)

# COMMON Functions   
def back_to_main_frame(oldFrame, newFrame):
    oldFrame.pack_forget()
    newFrame.pack(expand=TRUE,fill=BOTH)

def new_frame_open(newFrame, oldFrame):
    oldFrame.pack_forget()
    newFrame.pack(expand=TRUE, fill=BOTH)


# >>>>> SEARCH FRAME
cursor.execute("select city from loc")
loc_cty = cursor.fetchall()
search_options=[]
for cty in loc_cty:
    search_options.append(cty[0])


def suggest_places(event):
    inp_text= search_entry_var.get().lower()

    matching_places=[]

    for text in search_options:
        if text.lower().startswith(inp_text):
            listbox.grid(row=1,column=0)
            matching_places.append(text)

    listbox.delete(0,tk.END)
    
    for place in matching_places:
        listbox.insert(tk.END,place)

    if matching_places:
        listbox.grid(row=1,column=0,pady=10,padx=10)

    else:
        listbox.grid_forget()

selected_city = None  # Add this at the top

def entry_fill(event):
    global selected_city
    selection = listbox.curselection()
    if not selection:
        return  # No selection, do nothing

    selected_place = listbox.get(selection)
    search_entry_var.set(selected_place)
    selected_city = selected_place
    listbox.grid_forget()
    update_properties()


def clear_city_filter():
    global selected_city
    selected_city = None
    search_entry_var.set("")
    update_properties()

    
# UI FOR SEARCH FRAME

search_entry_frame = tb.Labelframe(main_frame, text="Search property by location")
search_entry_frame.grid(row=1, column=1, columnspan=2)

# Combo Box for Property Type
property_type_var = tk.StringVar()
property_type_combo = tb.Combobox(search_entry_frame, textvariable=property_type_var, values=["All Properties", "Properties for Sale", "Properties for Lease"],state="readonly", width=20)
property_type_combo.grid(row=0, column=0, padx=5, pady=5)
property_type_combo.current(0)  # Set default selection to "All Properties"


# Search Entry Box
search_entry_var = tk.StringVar()
search_entry = tb.Entry(search_entry_frame, textvariable=search_entry_var, bootstyle=SUCCESS, width=50)
search_entry.grid(row=0, column=1, padx=5, pady=5)

# Go Button
search_entry_button = tb.Button(search_entry_frame, text="Clear", command=clear_city_filter, bootstyle=(SUCCESS, OUTLINE))
search_entry_button.grid(row=0, column=2, padx=5, pady=5)

# Bind the search entry to suggest places
search_entry.bind("<KeyRelease>", suggest_places)

# Listbox for suggestions
listbox = tk.Listbox(search_entry_frame)
listbox.bind("<<ListboxSelect>>", entry_fill)







# >>>>> The PROPERTY FRAME

def create_property_frame(property_data, parent_frame, index):
     # Determine row and column based on index
    row = index // 3  # Ensures every 3 items go to the next row
    column = index % 3  # 3 columns per row

    if property_data["pid"].startswith("S"):
        t = "Buy"
    else:
        t = "Rent"

    prop_frame = tb.Labelframe(parent_frame, text=t)
    prop_frame.grid(row=row, column=column, padx=10, pady=10, sticky="ew")

    # Load image
    imgVar = ImageTk.PhotoImage(Image.open(property_data["img"]).resize((350, 200)))
    img_button = tb.Button(prop_frame, image=imgVar, bootstyle=tb.LINK, command=lambda: prop_det_open(property_data["pid"]))
    img_button.image = imgVar  # Keep reference to avoid garbage collection
    img_button.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

    # Property name and builder
    tb.Label(prop_frame, text=property_data["title"], font=("montserrat", 12), anchor="w").grid(row=1, column=0, padx=10, sticky="w")
    tb.Label(prop_frame, text=property_data["name"], font=("montserrat", 8), anchor="w").grid(row=2, column=0, padx=(10, 0), pady=(0, 10), sticky="w")

    # Property category and location
    tb.Label(prop_frame, text=property_data["cat"], font=("montserrat", 12), anchor="w").grid(row=3, column=0, padx=10, sticky="w")
    tb.Label(prop_frame, text=property_data["city"], font=("montserrat", 8), anchor="w").grid(row=4, column=0, padx=10, sticky="w")

    # Price range
    tb.Label(prop_frame, text=property_data["price"], font=("montserrat", 12), anchor="e").grid(row=1, column=1, padx=(0, 10), sticky="e")

cursor.execute("select image_path img, title, owner_username name, property_category cat, location_city city, rent_price price, i.property_id from res_prop_img i, properties p where i.property_id = p.property_id;")
prop_list = cursor.fetchall()
print(cursor.rowcount)

# UI Under PROPERTY FRAME
unique_properties = {}
for prop in prop_list:
    pid = prop[6]
    if pid not in unique_properties:
        unique_properties[pid] = {
            "img": prop[0],
            "title": prop[1],
            "name": prop[2],
            "cat": prop[3],
            "city": prop[4],
            "price": prop[5],
            "pid": prop[6]
        }

properties = list(unique_properties.values())


for idx, prop in enumerate(properties):
    create_property_frame(prop, sf, idx)


def update_properties(*args):
    for widget in sf.winfo_children():
        widget.destroy()

    selected_type = property_type_var.get()
    filtered_props = []

    for prop in properties:
        type_match = (
            selected_type == "All Properties" or
            (selected_type == "Properties for Sale" and prop["pid"].startswith("S")) or
            (selected_type == "Properties for Lease" and prop["pid"].startswith("L"))
        )

        city_match = (
            selected_city is None or selected_city.lower() == prop["city"].lower()
        )

        if type_match and city_match:
            filtered_props.append(prop)

    for idx, prop in enumerate(filtered_props):
        create_property_frame(prop, sf, idx)

property_type_combo.bind("<<ComboboxSelected>>", update_properties)     







# >>>>>>>>>>>>>>>> PROFILE PAGE FRAME FUNCTIONS <<<<<<<<<<<<<<<<
def logout():
    profile_frame.pack_forget()
    login_frame.pack(expand=True, fill='both')
    forgot.configure(state=DISABLED)

def edit_profile():
    editprof_window=tk.Toplevel(profile_frame)
    editprof_window.title("Edit your profile")
    editprof_window.geometry("600x600")
    
    cursor.execute("select * from users where username='{}'".format(pfp_user_email))
    user_data = cursor.fetchone()
    
    name, _, _, phone, role, profile_pic = user_data
    # Load and store image reference
    img = Image.open(profile_pic).resize((130,130))
    profile_icon_lb_img = ImageTk.PhotoImage(img)  # Store in a variable
    
    def upload_profile_image(profile_icon_lb):
        global profile_img_path, l1  # Keep reference to avoid garbage collection

        # Open file dialog to select image
        file_path = filedialog.askopenfilename(
            title="Select Profile Picture",
            filetypes=[("Image Files", ".png;.jpg;.jpeg;.gif;*.bmp")]
        )
        
        if file_path:  # If a file was selected
            profile_img_path = os.path.relpath(file_path)
            profile_img_path = os.path.normpath(profile_img_path)
            profile_img_path = profile_img_path.replace("\\", "\\\\")  # Double backslashes for MySQL

            img = Image.open(profile_img_path).resize((130, 130), Image.Resampling.LANCZOS)  # Resize image
            profile_img = ImageTk.PhotoImage(img)

            # Update the displayed image in GUI
            profile_btn.config(image=profile_img)
            profile_btn.image = profile_img  # Keep reference
            
            profile_icon_lb.config(image=profile_img)  # Update label
            profile_icon_lb.image = profile_img  # Keep reference to avoid garbage collection

            print(file_path)
            print(profile_img_path)

            # Update database with new profile image path
            cursor.execute("UPDATE users SET profile_pic = '{}' WHERE username = '{}'".format(profile_img_path, pfp_user_email))
            mycon.commit()

            print(f"Profile image updated in database: {profile_img_path}")
    

    def reset_pass(uname):
        # Move reset_password OUTSIDE check_reg_email
        rpass_window = tk.Toplevel(login_frame)
        rpass_window.title("Reset Password")
        rpass_window.geometry("400x350")
        
        ttk.Label(rpass_window, text="Enter new password").pack(pady=10)
        new_pass_entry = ttk.Entry(rpass_window)
        new_pass_entry.pack(pady=5)
        
        ttk.Label(rpass_window, text="Confirm Password").pack(pady=10)
        confirm_pass_entry = ttk.Entry(rpass_window)
        confirm_pass_entry.pack(pady=5)
        
        def rpassdd():
            new_pass = new_pass_entry.get()
            confirm_pass = confirm_pass_entry.get()
            
            if not new_pass or not confirm_pass:
                messagebox.showerror("Error", "All Fields Are Mandatory")
            elif new_pass != confirm_pass:
                messagebox.showerror("Error", "Passwords do not match")
            else:
                messagebox.showinfo("Success", "Password has been Reset!")
                cursor.execute("UPDATE users SET password = '{}' WHERE username = '{}'".format(new_pass, uname))
                mycon.commit()
                rpass_window.destroy()
    
        ttk.Button(rpass_window, text="Confirm", command=lambda: rpassdd()).pack(pady=10)

    def delete_account():
        confirm = messagebox.askyesno("Delete Account", "Are you sure you want to DELETE your account? Your data will not be recovered.")

        if confirm:
                query = "DELETE FROM users WHERE username = '{}'".format(pfp_user_email)
                cursor.execute(query)
                mycon.commit()
                messagebox.showinfo("Success", "Your Account Has Been Deleted")
                logout()
            
            
    def edit_profile_submit():
        global pfp_user_email, l1
        
        new_name=full_name_entry.get()
        new_phone=phone_entry.get()
        new_uname=emailadd_entry.get()

        if not new_name or not new_phone or not new_uname:
            messagebox.showerror("ERROR","All fields are required")
            return

        if new_phone is not None:
            if new_phone.isdigit() and len(new_phone) == 10:
                cursor.execute("UPDATE users SET phone = %s WHERE username = %s", (new_phone, pfp_user_email))
                mycon.commit()
            else:
                messagebox.showerror("ERROR","Invalid phone number!")
                return
    
        if new_name != name:
            cursor.execute("UPDATE users SET name = %s WHERE username = %s", (new_name, pfp_user_email))
            mycon.commit()

        if new_uname != pfp_user_email:
            if not is_valid_email(new_uname):
                messagebox.showerror("ERROR", "Invalid email address")
                return
            else:
                cursor.execute("UPDATE users SET username = %s WHERE username = %s", (new_uname, pfp_user_email))
                mycon.commit()
                pfp_user_email = new_uname  # Update the variable after committing

        bigger_profile_img = ImageTk.PhotoImage(Image.open(profile_img_path).resize((130,130), Image.Resampling.LANCZOS))

        if l1 is not None:
            l1.config(image=bigger_profile_img)
            l1.image = bigger_profile_img  # Store reference to avoid garbage collection    

        messagebox.showinfo("Success","Profile updated successfully!")
        create_profile(pfp_user_email)
        editprof_window.destroy()

    

    # Assign image to label and keep a reference
    profile_icon_lb = tb.Label(editprof_window, image=profile_icon_lb_img)
    profile_icon_lb.image = profile_icon_lb_img  # Store reference to prevent garbage collection
    profile_icon_lb.pack(pady=(18,6))
    
    
    tb.Button(editprof_window, text="Change your profile photo", bootstyle=(WARNING,LINK), command=lambda: upload_profile_image(profile_icon_lb)).pack(pady=(0,18)) 
      
    info_frame= tb.LabelFrame(editprof_window,text="User Details",bootstyle=SECONDARY)
    info_frame.pack(padx=10,pady=10,fill=X)
      
    tb.Label(info_frame, text="Full name:", font=("Arial bold",12)).grid(row=0,column=0,padx=(14,0),pady=10)
    full_name_entry = tb.Entry(info_frame, width=30)
    full_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=E)
    full_name_entry.insert(0, f"{name}")
    
    tb.Label(info_frame, text="Email Address:", font=("Arial bold",12)).grid(row=1,column=0,padx=(14,0),pady=10)
    emailadd_entry = tb.Entry(info_frame, width=30)
    emailadd_entry.grid(row=1, column=1, padx=5, pady=5, sticky=E)
    emailadd_entry.insert(0, f"{pfp_user_email}")

    tb.Label(info_frame, text="Phone:", font=("Arial bold",12)).grid(row=2,column=0,padx=(17,0),pady=10)
    phone_entry = tb.Entry(info_frame, width=30)
    phone_entry.grid(row=2, column=1, padx=14, pady=14, sticky=E)
    phone_entry.insert(0, f"{phone}")

    tb.Label(info_frame, text="Role:", font=("Arial bold",12)).grid(row=3,column=0,padx=(15,0),pady=10)
    role_entry=tb.Entry(info_frame, width = 30)
    role_entry.grid(row=3, column=1, padx=10, pady=10, sticky=E)
    role_entry.insert(0, f"{role}")
    role_entry.configure(state=DISABLED)
            
    tb.Button(editprof_window, text="Reset Password", bootstyle = (WARNING, LINK), command=lambda: reset_pass(pfp_user_email)).pack(pady=5,padx=10)    
    
    tb.Button(editprof_window, text="Delete Your Account", bootstyle = (DANGER, LINK), command=delete_account).pack(pady=5, padx=10)
    
    tb.Button(editprof_window, text="SAVE CHANGES", bootstyle = SUCCESS, command=edit_profile_submit).pack(pady=20)
    
    
    
    
# PROFILE PAGE UI 

pfp_btn_frame = tb.Frame(profile_frame)
pfp_btn_frame.grid(row=0, column=0, rowspan=3)
  
tb.Button(pfp_btn_frame, text="Go Back", command=lambda: back_to_main_frame(profile_frame, main_frame)).pack(pady=(0,20), fill=BOTH, padx=(10,0))
tb.Button(pfp_btn_frame,text="Edit", bootstyle=WARNING, command=edit_profile).pack(pady=(0,20), fill=BOTH, padx=(10,0)) 
tb.Button(pfp_btn_frame, text="Logout", bootstyle=SECONDARY,command=logout).pack(pady=(0,20), fill=BOTH, padx=(10,0))

tb.Separator(profile_frame, orient=VERTICAL).grid(row=0,column=1,sticky=NS,rowspan=50, padx=(10,400))

tb.Label(profile_frame, text="Full name:", font=("Arial bold",12)).grid(row=2,column=2,padx=(20,0),pady=20,sticky=W)
tb.Label(profile_frame, text="Email Address:", font=("Arial bold",12)).grid(row=3,column=2,padx=(20,0),pady=20,sticky=W)
tb.Label(profile_frame, text="Phone:", font=("Arial bold",12)).grid(row=4,column=2,padx=(20,0),pady=20,sticky=W)
tb.Label(profile_frame, text="Role:", font=("Arial bold",12)).grid(row=5,column=2,padx=(20,0),pady=20,sticky=W)







# >>>>>>>>>>>>>>>> POST PROP FRAME <<<<<<<<<<<<<<<<
def post_prop_open():
    new_frame_open(post_prop_frame, main_frame)
    ##sidebar
    post_btn_frame = tb.Frame(post_prop_frame, width=0, height=750)
    post_btn_frame.grid(row=0, column=0, sticky=tk.NW, rowspan=17)
    tb.Button(post_btn_frame, text="Go back", command=lambda: back_to_main_frame(post_prop_frame, main_frame)).grid(row=0, column=0, pady=20, padx=20)
    tb.Separator(post_prop_frame, orient=VERTICAL).grid(row=0, column=1, padx=(20, 20), sticky=NS, rowspan=4)

    tb.Label(post_prop_frame, text="POST YOUR PROPERTY", font=("Montserrat", 28, "bold")).grid(row=0, column=2, columnspan=3, padx=250, pady=20, sticky=tk.W)

    sf2 = ScrolledFrame(post_prop_frame, autohide=True, width=1050, height=550)
    sf2.grid(row=1, column=2, columnspan=3, padx=20, pady=20, sticky=W)

    sell_lease = tk.StringVar()

    # SELL OR LEASE
    tb.Label(sf2, text="SELL OR LEASE:", font=("Montserrat", 14, "bold")).grid(row=0, column=0, pady=15, sticky=tk.W)
    sell = tb.Radiobutton(sf2, text="SELL", variable=sell_lease, value="SELL", bootstyle="info")
    sell.grid(row=0, column=1, padx=10, pady=5)
    lease = tb.Radiobutton(sf2, text="LEASE", variable=sell_lease, value="LEASE", bootstyle="info")
    lease.grid(row=0, column=2, padx=10, pady=5)

    # PROPERTY TYPE
    tb.Label(sf2, text="PROPERTY TYPE:", font=("Montserrat", 14, "bold")).grid(row=1, column=0, pady=15, sticky=tk.W)
    prop_type_list = ['Apartment','Independent House','Villa','Commercial','Land/Plot']
    prop_type = tb.Combobox(sf2, bootstyle="primary", values=prop_type_list, width=25)
    prop_type.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky=tk.W)

    # PROPERTY DETAILS FRAME
    Prop_dets_frame = tb.LabelFrame(sf2, text="PROPERTY DETAILS", bootstyle="info")
    Prop_dets_frame.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky=tk.EW)

    # Title
    tb.Label(Prop_dets_frame, text="Title:", font=("Montserrat", 12)).grid(column=0, row=0, sticky=tk.W, padx=20, pady=10)
    title = tb.Entry(Prop_dets_frame, width=40)
    title.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky=tk.EW)

    # Location
    tb.Label(Prop_dets_frame, text="Location:", font=("Montserrat", 12)).grid(column=0, row=1, sticky=tk.W, padx=20, pady=10)
    loc = tb.Combobox(Prop_dets_frame, bootstyle="primary", values=search_options, width=40)  # Replace with actual options
    loc.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky=tk.EW)

    # Address
    tb.Label(Prop_dets_frame, text="Address:", font=("Montserrat", 12)).grid(column=0, row=2, sticky=tk.W, padx=20, pady=10)
    address = tb.Entry(Prop_dets_frame, width=40)
    address.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky=tk.EW)

    # Number of rooms
    tb.Label(Prop_dets_frame, text="No of rooms (BHK):", font=("Montserrat", 12)).grid(column=0, row=3, sticky=tk.W, padx=20, pady=10)
    bhk = tb.Entry(Prop_dets_frame, width=40)
    bhk.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky=tk.EW)

    # Area sqft
    tb.Label(Prop_dets_frame, text="Area sqft:", font=("Montserrat", 12)).grid(column=0, row=4, sticky=tk.W, padx=20, pady=10)
    area = tb.Entry(Prop_dets_frame, width=40)
    area.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky=tk.EW)

    # Furnishing details
    tb.Label(Prop_dets_frame, text="Furnishing details:", font=("Montserrat", 12)).grid(column=0, row=5, sticky=tk.W, padx=20, pady=10)
    fur_list = ["Unfurnished", "Semi-furnished", "Furnished"]
    fur = tb.Combobox(Prop_dets_frame, bootstyle="primary", values=fur_list, width=40)
    fur.grid(row=5, column=1, columnspan=2, padx=10, pady=10, sticky=tk.EW)

    # Parking Availability
    tb.Label(Prop_dets_frame, text="Parking Availability", font=("Montserrat", 12)).grid(column=0, row=6, sticky=tk.W, padx=20, pady=10)
    park = tk.BooleanVar()
    Yes = tb.Radiobutton(Prop_dets_frame, text="YES", variable=park, value=1, bootstyle="info")
    Yes.grid(row=6, column=1, padx=10, pady=10)
    No = tb.Radiobutton(Prop_dets_frame, text="NO", variable=park, value=0, bootstyle="info")
    No.grid(row=6, column=2, padx=10, pady=10)

    # Age of Property
    tb.Label(Prop_dets_frame, text="Age of Property", font=("Montserrat", 12)).grid(column=0, row=7, sticky=tk.W, padx=20, pady=10)
    age = tb.Entry(Prop_dets_frame, width=40)
    age.grid(row=7, column=1, columnspan=2, padx=10, pady=10, sticky=tk.EW)

    # Description
    tb.Label(Prop_dets_frame, text="Description", font=("Montserrat", 12)).grid(column=0, row=8, sticky=tk.W, padx=20, pady=10)
    desc = tb.Entry(Prop_dets_frame, width=40)
    desc.grid(row=8, column=1, columnspan=2, padx=10, pady=10, sticky=tk.EW)

    # UPLOADING MEDIA
    style = tb.Style()
    style.configure("Warning.Link.TButton", font=("Montserrat", 12), foreground="#FFC107")

    sf3 = ScrolledFrame(sf2, autohide=True, height=300, width=900)
    sf3.grid(row=4, column=0, columnspan=5, padx=20, pady=20, sticky=W)

    # PRICING DETAILS FRAME
    Price_frame = tb.LabelFrame(sf2, text="PRICING DETAILS", bootstyle="info")
    Price_frame.grid(row=5, column=0, columnspan=3, padx=20, pady=20, sticky=tk.EW)

    # Price/Rent
    price = tb.Label(Price_frame, text="Price:", font=("Montserrat", 12))
    price.grid(column=0, row=0, sticky=tk.W, padx=20, pady=10)
    price_entry = tb.Entry(Price_frame, width=40)
    price_entry.grid(column=1, row=0, padx=10, pady=10, sticky=tk.EW)

    '''# Lease Duration
    tb.Label(Price_frame, text="Lease Duration:", font=("Montserrat", 12)).grid(column=0, row=1, sticky=tk.W, padx=20, pady=10)
    lease_duration_entry = tb.Entry(Price_frame, width=40)
    lease_duration_entry.grid(column=1, row=1, padx=10, pady=10, sticky=tk.EW)

    # Extra Bills
    tb.Label(Price_frame, text="Extra Bills:", font=("Montserrat", 12)).grid(column=0, row=2, sticky=tk.W, padx=20, pady=10)
    extra_bills_entry = tb.Entry(Price_frame, width=40)
    extra_bills_entry.grid(column=1, row=2, padx=10, pady=10, sticky=tk.EW)'''
  
    def val_null():
        print("sell_lease says:", sell_lease.get())
        if sell_lease == None:
            messagebox.showerror("Error", "Please select whether you wish to Sell or put up your property for Lease")
            return
        if prop_type.get() == "":
            messagebox.showerror("Error", "Please select category of property")
            return
        if not title.get() or loc.get() == "" or not address.get() or not bhk.get() or not area.get() or fur.get() == "" or not age.get() or not desc.get() or not price_entry.get():
            messagebox.showerror("Error", "All Fields are Required")
            return
        else:
            post_prop()
        
    def upload_images():
        file_paths = filedialog.askopenfilenames(title="Select Images", 
                                                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if file_paths:
            for widget in sf3.winfo_children():
                widget.destroy()  # Clear previous images
            print(file_paths)   # tuple of strings of absolute path
            images.clear()
            fp.clear()
            
            for path in file_paths:
                img = Image.open(path)
                img.thumbnail((300, 300))  # Resize for display
                img_tk = ImageTk.PhotoImage(img)
                images.append(img_tk)  # Store reference to prevent garbage collection
                fp.append(path)
                
                index = file_paths.index(path)
                row = index // 3
                column = index % 3
                
                label = tk.Label(sf3, image=img_tk)
                label.grid(row=row, column=column, padx=5, pady=5)
    images =[]
    fp = []    
    
    def img_in_db(fpp, pid):
        for p in fpp:
            ip = os.path.relpath(p)
            ip = os.path.normpath(ip)
            ip = ip.replace("\\", "\\\\")

            query = f"insert into res_prop_img(property_id,image_path) values ('{pid}','{ip}')"
            cursor.execute(query)
            mycon.commit()
       
    def post_prop(): 
        global pfp_user_email
        prop_id = prop_id_gen()
        p_cat = prop_type.get()
        p_tit = title.get()
        p_loc = loc.get()
        p_add = address.get()
        p_bhk = bhk.get()
        p_area = area.get()
        p_fur = fur.get()
        p_park = park.get()
        p_age = age.get()
        p_desc = desc.get()
        p_price = price_entry.get()
        
        
        query = f"insert into properties(property_id, owner_username, property_category, location_city, title, address, rent_price, bhk) values('{prop_id}', '{pfp_user_email}', '{p_cat}', '{p_loc}', '{p_tit}', '{p_add}', {p_price}, {p_bhk})"
        cursor.execute(query)
        mycon.commit()
        
        if p_cat in ('Apartment','Independent House','Villa'):
            query = f"insert into res_prop_det(property_id, area_sqft, furnishing_details, parking_availability, age_of_property, description) values ('{prop_id}', {p_area}, '{p_fur}', {p_park}, {p_age}, '{p_desc}')"
            cursor.execute(query)
            mycon.commit()
        if len(fp) == 0:
            messagebox.showerror("No Images Uploaded", "Please upload images of your property")
        else:          
            img_in_db(fp, f"{prop_id}")
            messagebox.showinfo("Success", "Your property has been listed! Buyers can now view it.")
    
    
    #upload imgs
    ub = tb.Button(sf2, text="Upload images and other media of your property", style="Warning.Link.TButton", command=upload_images)
    ub.grid(row=3, column=0, columnspan=3, padx=20, pady=20, sticky=W)
    ToolTip(ub, text="Upload atleast 3 pictures of you property for the user to see. It is recommended to upload the image you want to be as the cover first.", bootstyle=(WARNING, INVERSE))
    
    ## SUBMIT
    submit_button = tb.Button(sf2, text="SUBMIT", bootstyle=SUCCESS, width=20, command=val_null)
    submit_button.grid(row=8, column=0, columnspan=3, pady=30)
    
    def prop_id_gen():
        sell_or_lease="S" if sell_lease.get()=="SELL" else "L"
        
        prop_code={"Apartment":"RA","Independent House": "RI","Villa":"RV","Commercial":"C","Land/Plot":"P"}.get(prop_type.get(),"XX")
        
        city_to_state={"Bangalore": "KA", "Noida": "UP","Mumbai": "MH","Vijaywada": "AP","Trivandrum": "KL","Dehradun": "UK","New Delhi": "DL","Old Delhi": "DL","Chennai": "TN", "Panaji": "GA","Hyderabad": "TS","Patna": "BR","Jaipur": "RJ","Jaisalmer": "RJ","Gurugram": "HR","Secunderabad": "TS","Pune": "MH","Ahmedabad": "GJ","Kolkata": "WB"}

        state_code=city_to_state.get(loc.get(),"XX")
        prefix=f"{sell_or_lease}{prop_code}{state_code}"
        serial=1
        while True:
            new_id = f"{prefix}{serial:04d}"
            
            cursor.execute(f"SELECT 1 FROM properties WHERE property_id = '{new_id}'")
            
            if not cursor.fetchone():
                return new_id
            
            serial+=1
            
            if serial>9999:
                raise Exception("Property ID couldnt be generated after 9999 attempts")
                
        
      
    



# >>>>>>>>>>>>>>>> PROP DETAIL FRAME <<<<<<<<<<<<<<<<

def prop_det_open(pid):
    # 1. Verify property exists first
    cursor.execute("SELECT 1 FROM properties WHERE property_id = %s", (pid,))
    if not cursor.fetchone():
        messagebox.showerror("Error", f"Property ID {pid} doesn't exist!")
        return

    # 2. Only proceed if valid
    new_frame_open(prop_detail_frame, main_frame)
    pdet_btn_frame = tb.Frame(prop_detail_frame, width=0, height=750)
    pdet_btn_frame.grid(row=0, column=0, sticky=tk.NW, rowspan=17)
    cursor.execute("SELECT role FROM users WHERE username = %s", (pfp_user_email,))
    user_role = cursor.fetchone()[0]

    if user_role == "Tenant":
        tb.Button(pdet_btn_frame, text="Rent/Buy", bootstyle=SUCCESS,
              command=lambda: rent_buy_property(pid, "Rent")).grid(row=3, column=1, pady=10)
    

    tb.Button(pdet_btn_frame, text="Go back", command=lambda: back_to_main_frame(prop_detail_frame, main_frame)).grid(row=0, column=0, pady=20, padx=20)
    tb.Separator(pdet_btn_frame, orient=VERTICAL).grid(row=0, column=1, padx=(20, 150), sticky=NS, rowspan=4)

    query = """
    SELECT
        properties.property_id,
        properties.owner_username,
        properties.property_category,
        properties.location_city,
        properties.title,
        properties.address,
        properties.rent_price,
        properties.bhk,
        res_prop_det.sno AS detail_sno,
        res_prop_det.area_sqft,
        res_prop_det.furnishing_details,
        res_prop_det.parking_availability,
        res_prop_det.age_of_property,
        res_prop_det.description,
        res_prop_img.sno,
        res_prop_img.image_path
    FROM properties
    LEFT JOIN res_prop_det ON properties.property_id = res_prop_det.property_id
    LEFT JOIN res_prop_img ON properties.property_id = res_prop_img.property_id
    WHERE properties.property_id = %s;
    """

    cursor.execute(query, (pid,))
    result = cursor.fetchall()

    if result:
        first_row = result[0]
        (
            property_id, owner_username, property_category, location_city, title,
            address, rent_price, bhk, detail_sno, area_sqft, furnishing_details,
            parking_availability, age_of_property, description, image_sno, image_path
        ) = first_row

        # Collect all images
        images = [row[-1] for row in result if row[-1]]
    else:
        # Fallback if somehow no rows returned
        (
            property_id, owner_username, property_category, location_city, title,
            address, rent_price, bhk, detail_sno, area_sqft, furnishing_details,
            parking_availability, age_of_property, description, image_sno, image_path
        ) = ("N/A", "Unknown", "Unknown", "Unknown", "No Title", 
             "No Address", 0, 0, 0, 0, "N/A", "No", 0, "No description", 0, "default.jpg")

        images = ["default.jpg"]

    cursor.execute(f"select * from properties where property_id = '{pid}'")
    (property_id, _, property_category, location_city, title, address, rent_price, bhk) = cursor.fetchone()
    cursor.execute(f"select * from res_prop_det where property_id = '{pid}'")
    (_, _, area_sqft, furnishing_details, parking_availability, age_of_property, description) = cursor.fetchone()
    cursor.execute(f"select * from loc where city = '{location_city}'")
    (state, _) = cursor.fetchone()

    # ----------------- DISPLAY START ----------------- #

    tb.Label(pdet_btn_frame, text=title, font=("Montserrat",18)).grid(row=0, column=1, columnspan=5, sticky=W, pady=2, padx=(200,20))
    tb.Label(pdet_btn_frame, text=f"{location_city}, {state}", font=("Montserrat",16)).grid(row=1, column=1, columnspan=5, sticky=W, pady=2, padx=(200,20))      
    tb.Label(pdet_btn_frame, text=pid , font=("Montserrat",12)).grid(row=2, column=1, columnspan=5, sticky=W, pady=2, padx=(200,20))

    sf3 = ScrolledFrame(pdet_btn_frame, autohide=True, width=900, height=550)
    sf3.grid(row=3, column=2, columnspan=3, padx=20, pady=20, sticky=NSEW)
    sf3.container.columnconfigure(1, weight=1)
    sf3.container.columnconfigure(2, weight=2)

    cursor.execute(f"select * from res_prop_img where property_id = '{pid}'")
    imgs = cursor.fetchall()
        
    for idx, i in enumerate(imgs):
        imgVar = ImageTk.PhotoImage(Image.open(i[2]).resize((300, 150)))
        img_label = tb.Label(sf3.container, image=imgVar)
        img_label.image = imgVar
        img_label.grid(row=idx*3, column=0, rowspan=3, sticky=E, padx=10, pady=10)

    def add_row(label, value, r):
            tb.Label(sf3.container, text=label, font=("Montserrat", 12)).grid(column=1, row=r, sticky="w", padx=20, pady=10)
            tb.Label(sf3.container, text=value, font=("Montserrat", 12)).grid(column=2, row=r, sticky="nsew", padx=20, pady=10)

    add_row("Location:", f"{address}\n{location_city}\n{state}", 0)
    add_row("Property Category:", property_category, 1)
    add_row("Price:", f"₹{rent_price}", 2)
    add_row("BHK:", bhk, 3)
    add_row("Area sqft:", f"{area_sqft} sq.ft", 4)
    add_row("Furnishing details:", furnishing_details, 5)
    add_row("Parking availability:", parking_availability, 6)
    add_row("Age of property:", f"{age_of_property} years", 7)

    tb.Label(sf3.container, text="Description:", font=("Montserrat", 12)).grid(column=1, row=8, sticky="w", padx=20, pady=10)
    tb.Label(sf3.container, text=description, font=("Montserrat", 12), wraplength=600, justify="left").grid(column=2, row=8, sticky="w", padx=20, pady=10)




# >>>>>>>>>>>>>>>> MY PROPERTIES PAGE <<<<<<<<<<<<<<<<<<<

def my_tent_open():
    def see_prop(pid):

        def delete_prop():
            if messagebox.askyesno("Confirm", "Are you sure you want to remove this property? You will not be able to recover your property again."):
                messagebox.showwarning("Success", "Your property has been removed")
                cursor.execute(f"DELETE FROM RES_PROP_DET WHERE PROPERTY_ID = '{pid}'")
                cursor.execute(f"DELETE FROM RES_PROP_IMG WHERE PROPERTY_ID = '{pid}'")
                cursor.execute(f"DELETE FROM PROPERTIES WHERE PROPERTY_ID = '{pid}'")
                mycon.commit()
                back_to_main_frame(f1, my_tent_frame)
                f1.destroy()
            else:
                messagebox.showwarning("Failed", "Your property has not been removed.")
                
        def edit_prop():
            edit_win = tb.Toplevel(root)
            edit_win.title("Edit Property")
            edit_win.geometry("1200x800")  # Adjust as needed
            
            eframe = tb.Frame(edit_win)
            eframe.pack(fill=BOTH, expand=TRUE)
            ebtn_frame = tb.Frame(eframe, width=0, height=750)
            ebtn_frame.grid(row=0, column=0, sticky=tk.NW, rowspan=17)
            tb.Button(ebtn_frame, text="Cancel", command=edit_win.destroy).grid(row=0, column=0, pady=20, padx=20)
            tb.Separator(eframe, orient=VERTICAL).grid(row=0, column=1, padx=(20, 150), sticky=NS, rowspan=4)

            tb.Label(eframe, text="EDIT YOUR PROPERTY", font=("Montserrat", 28, "bold")).grid(row=0, column=2, columnspan=3, padx=250, pady=20, sticky=tk.W)

            sf2 = ScrolledFrame(eframe, autohide=True, width=1050, height=550)
            sf2.grid(row=1, column=2, columnspan=3, padx=20, pady=20, sticky=W)

            cursor.execute(f"select * from properties where property_id = '{pid}'")
            (_, _, pcat, eloc, etit, ead, erp, ebhk) = cursor.fetchone()
            cursor.execute(f"select * from res_prop_Det where property_id = '{pid}'")
            (_, _, ear, efur, epar, eage, edesc) = cursor.fetchone()
            cursor.execute(f"select image_path from res_prop_img where property_id = '{pid}'")
            ii = cursor.fetchall()
            fp = []
            for ei in ii:
                fp.append(ei[0])
           
            if "S" in pid:
                sell_lease = "SELL"
            else:
                sell_lease = "LEASE"

            # SELL OR LEASE
            tb.Label(sf2, text="SELL OR LEASE:", font=("Montserrat", 14, "bold")).grid(row=0, column=0, pady=15, sticky=tk.W)
            sell = tb.Radiobutton(sf2, text="SELL", variable=sell_lease, value="SELL", bootstyle="info")
            sell.grid(row=0, column=1, padx=10, pady=5)
            lease = tb.Radiobutton(sf2, text="LEASE", variable=sell_lease, value="LEASE", bootstyle="info")
            lease.grid(row=0, column=2, padx=10, pady=5)

            # PROPERTY TYPE
            tb.Label(sf2, text="PROPERTY TYPE:", font=("Montserrat", 14, "bold")).grid(row=1, column=0, pady=15, sticky=tk.W)
            prop_type_list = ['Apartment','Independent House','Villa','Commercial','Land/Plot']
            prop_type = tb.Combobox(sf2, bootstyle="primary", values=prop_type_list, width=25)
            prop_type.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky=tk.W)
            prop_type.set(pcat)

            # PROPERTY DETAILS FRAME
            Prop_dets_frame = tb.LabelFrame(sf2, text="PROPERTY DETAILS", bootstyle="info")
            Prop_dets_frame.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky=tk.EW)

            # Title
            tb.Label(Prop_dets_frame, text="Title:", font=("Montserrat", 12)).grid(column=0, row=0, sticky=tk.W, padx=20, pady=10)
            deft1 = tb.StringVar(value=etit)
            title = tb.Entry(Prop_dets_frame, width=40, textvariable= deft1)
            title.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky=tk.EW)

            # Location
            tb.Label(Prop_dets_frame, text="Location:", font=("Montserrat", 12)).grid(column=0, row=1, sticky=tk.W, padx=20, pady=10)
            loc = tb.Combobox(Prop_dets_frame, bootstyle="primary", values=search_options, width=40)  # Replace with actual options
            loc.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky=tk.EW)
            loc.set(eloc)

            # Address
            tb.Label(Prop_dets_frame, text="Address:", font=("Montserrat", 12)).grid(column=0, row=2, sticky=tk.W, padx=20, pady=10)
            deft2 = tb.StringVar(value=ead)
            address = tb.Entry(Prop_dets_frame, width=40, textvariable= deft2)
            address.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky=tk.EW)

            # Number of rooms
            tb.Label(Prop_dets_frame, text="No of rooms (BHK):", font=("Montserrat", 12)).grid(column=0, row=3, sticky=tk.W, padx=20, pady=10)
            deft3 = tb.StringVar(value=ebhk)
            bhk = tb.Entry(Prop_dets_frame, width=40, textvariable=deft3)
            bhk.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky=tk.EW)

            # Area sqft
            tb.Label(Prop_dets_frame, text="Area sqft:", font=("Montserrat", 12)).grid(column=0, row=4, sticky=tk.W, padx=20, pady=10)
            deft4 = tb.StringVar(value=ear)
            area = tb.Entry(Prop_dets_frame, width=40, textvariable=deft4)
            area.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky=tk.EW)

            # Furnishing details
            tb.Label(Prop_dets_frame, text="Furnishing details:", font=("Montserrat", 12)).grid(column=0, row=5, sticky=tk.W, padx=20, pady=10)
            fur_list = ["Unfurnished", "Semi-furnished", "Furnished"]
            fur = tb.Combobox(Prop_dets_frame, bootstyle="primary", values=fur_list, width=40)
            fur.grid(row=5, column=1, columnspan=2, padx=10, pady=10, sticky=tk.EW)
            fur.set(efur)

            # Parking Availability
            tb.Label(Prop_dets_frame, text="Parking Availability", font=("Montserrat", 12)).grid(column=0, row=6, sticky=tk.W, padx=20, pady=10)
            park = tk.BooleanVar(value=bool(epar))
            
            Yes = tb.Radiobutton(Prop_dets_frame, text="YES", variable=park, value=True, bootstyle="info")
            Yes.grid(row=6, column=1, padx=10, pady=10)
            No = tb.Radiobutton(Prop_dets_frame, text="NO", variable=park, value=False, bootstyle="info")
            No.grid(row=6, column=2, padx=10, pady=10)

            # Age of Property
            tb.Label(Prop_dets_frame, text="Age of Property", font=("Montserrat", 12)).grid(column=0, row=7, sticky=tk.W, padx=20, pady=10)
            deft5 = tb.StringVar(value=eage)
            age = tb.Entry(Prop_dets_frame, width=40, textvariable=deft5)
            age.grid(row=7, column=1, columnspan=2, padx=10, pady=10, sticky=tk.EW)

            # Description
            tb.Label(Prop_dets_frame, text="Description", font=("Montserrat", 12)).grid(column=0, row=8, sticky=tk.W, padx=20, pady=10)
            deft6 = tb.StringVar(value=edesc)            
            desc = tb.Entry(Prop_dets_frame, width=40, textvariable=deft6)
            desc.grid(row=8, column=1, columnspan=2, padx=10, pady=10, sticky=tk.EW)

            # UPLOADING MEDIA
            style = tb.Style()
            style.configure("Warning.Link.TButton", font=("Montserrat", 12), foreground="#FFC107")

            sf3 = ScrolledFrame(sf2, autohide=True, height=300, width=900)
            sf3.grid(row=4, column=0, columnspan=5, padx=20, pady=20, sticky=W)

            # PRICING DETAILS FRAME
            Price_frame = tb.LabelFrame(sf2, text="PRICING DETAILS", bootstyle="info")
            Price_frame.grid(row=5, column=0, columnspan=3, padx=20, pady=20, sticky=tk.EW)

            # Price/Rent
            price = tb.Label(Price_frame, text="Price:", font=("Montserrat", 12))
            price.grid(column=0, row=0, sticky=tk.W, padx=20, pady=10)
            deft7 = tb.StringVar(value=erp)
            price_entry = tb.Entry(Price_frame, width=40, textvariable=deft7)
            price_entry.grid(column=1, row=0, padx=10, pady=10, sticky=tk.EW)
        
            for path in fp:
                img = Image.open(path)
                img.thumbnail((300, 300))  # Resize for display
                img_tk = ImageTk.PhotoImage(img)
                
                index = fp.index(path)
                row = index // 3
                column = index % 3
                
                label = tk.Label(sf3, image=img_tk)
                label.grid(row=row, column=column, padx=5, pady=5)
        
            def upload_images():
                file_paths = filedialog.askopenfilenames(title="Select Images", 
                                                        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
                if file_paths:
                    for widget in sf3.winfo_children():
                        widget.destroy()  # Clear previous images
                    print(file_paths)   # tuple of strings of absolute path
                    images.clear()
                    fp.clear()
                    
                    for path in file_paths:
                        img = Image.open(path)
                        img.thumbnail((300, 300))  # Resize for display
                        img_tk = ImageTk.PhotoImage(img)
                        images.append(img_tk)  # Store reference to prevent garbage collection
                        fp.append(path)
                        
                        index = file_paths.index(path)
                        row = index // 3
                        column = index % 3
                        
                        label = tk.Label(sf3, image=img_tk)
                        label.grid(row=row, column=column, padx=5, pady=5)
            images = []
            
            def img_in_db(fpp, pid):
                for p in fpp:
                    ip = os.path.relpath(p)
                    ip = os.path.normpath(ip)
                    ip = ip.replace("\\", "\\\\")

                    query = f"update res_prop_img set image_path = '{ip}' where property_id = '{pid}'"
                    cursor.execute(query)
                    mycon.commit()
            
            def post_prop(): 
                p_cat = prop_type.get()
                p_tit = title.get()
                p_loc = loc.get()
                p_add = address.get()
                p_bhk = bhk.get()
                p_area = area.get()
                p_fur = fur.get()
                p_park = park.get()
                p_age = age.get()
                p_desc = desc.get()
                p_price = price_entry.get()
                
                
                query = f"update properties set property_category = '{p_cat}', location_city = '{p_loc}', title = '{p_tit}', address = '{p_add}', rent_price = {p_price}, bhk = {p_bhk} where property_id = '{pid}'"
                cursor.execute(query)
                mycon.commit()
                
                if p_cat in ('Apartment','Independent House','Villa'):
                    query = f"update res_prop_det set area_sqft = {p_area}, furnishing_details = '{p_fur}', parking_availability = {p_park}, age_of_property = {p_age}, description = '{p_desc}' where property_id = '{pid}'"
                    cursor.execute(query)
                    mycon.commit()
                if len(fp) == 0:
                    messagebox.showerror("No Images Uploaded", "Please upload images of your property")
                else:          
                    img_in_db(fp, f"{pid}")
                    messagebox.showinfo("Success", "Your property has been listed! Buyers can now view it.")
            
                               
            #upload imgs
            ub = tb.Button(sf2, text="Upload images and other media of your property", style="Warning.Link.TButton", command=upload_images)
            ub.grid(row=3, column=0, columnspan=3, padx=20, pady=20, sticky=W)
            ToolTip(ub, text="Upload atleast 3 pictures of you property for the user to see. It is recommended to upload the image you want to be as the cover first.", bootstyle=(WARNING, INVERSE))
            
            ## SUBMIT
            submit_button = tb.Button(sf2, text="SUBMIT", bootstyle=SUCCESS, width=20, command=post_prop)
            submit_button.grid(row=8, column=0, columnspan=3, pady=30)
                
            
            
            

        f1 = tb.Frame(root)
        new_frame_open(f1, my_tent_frame)

        # Grid layout configuration
        f1.columnconfigure(0, weight=0)  # Sidebar
        f1.columnconfigure(1, weight=1)  # Main content
        f1.columnconfigure(2, weight=0)  # User sidebar
        f1.rowconfigure(3, weight=1)     # Main scrollable row

        # Button sidebar
        f1_btn_frame = tb.Frame(f1, width=120)
        f1_btn_frame.grid(row=0, column=0, rowspan=20, sticky="ns")
        f1_btn_frame.grid_propagate(False)

        tb.Button(f1_btn_frame, text="Go back", command=lambda: back_to_main_frame(f1, my_tent_frame)).grid(row=0, column=0, pady=10, padx=10)
        tb.Button(f1_btn_frame, text="Edit\nProperty", bootstyle=(INFO, OUTLINE), command= edit_prop).grid(row=1, column=0, pady=10, padx=10)
        db = tb.Button(f1_btn_frame, text="Remove\nProperty", bootstyle=(DANGER, OUTLINE), command=delete_prop)
        db.grid(row=2, column=0, pady=10, padx=10)
        ToolTip(db, "This action cannot be undone.")

        # Toggle button for user sidebar
        toggle_btn = tb.Button(f1, text="Hide Sidebar", bootstyle=SUCCESS)
        toggle_btn.grid(row=2, column=2, pady=10, sticky="n")

       # User sidebar in a ScrolledFrame to prevent overflow
        user_sidebar = ScrolledFrame(f1, width=350, height=600)
        user_sidebar.grid(row=3, column=2, sticky="ns", padx=(10, 10), pady=(0, 10))
        user_sidebar.grid_propagate(False)

        f1_user_frame = user_sidebar.container
        tb.Label(f1_user_frame, text="Users who are\ncurrently interested in your property", font=("Montserrat", 12)).grid(row=0, column=0, pady=10)

        print(f"[DEBUG] see_prop() called with pid='{pid}'")

# Show all interested_users for this property, using TRIM to handle space issue
        cursor.execute("""
         SELECT u.name, u.username, u.phone, iu.transaction_type
        FROM interested_users iu
        JOIN users u ON iu.tenant_username = u.username
        WHERE TRIM(iu.property_id) = %s
        """, (pid.strip(),))
        interested_users = cursor.fetchall()

# Optional full dump — you can comment this out later
        cursor.execute("SELECT tenant_username, HEX(property_id), property_id, transaction_type FROM interested_users")
        all_interests = cursor.fetchall()
        print("[DEBUG] All rows in interested_users table:")
        for row in all_interests:
            print(row)

# Display sidebar
        if not interested_users:
            tb.Label(f1_user_frame, text="No interest yet.").grid(row=1, column=0, padx=10, pady=5, sticky=W)
        else:
            
            for i, (name, username, phone, transaction_type) in enumerate(interested_users, start=1):
                tb.Label(f1_user_frame, text=f"{i}. {name}\n📧 {username}\n📞 {phone}\nTransaction: {transaction_type}", wraplength=300, justify="left").grid(row=i, column=0, padx=10, pady=5, sticky=W)

                
        def toggle_sidebar():
            if user_sidebar.winfo_ismapped():
                user_sidebar.grid_remove()
                toggle_btn.config(text="Show Sidebar")
            else:
                user_sidebar.grid()
                toggle_btn.config(text="Hide Sidebar")

        toggle_btn.config(command=toggle_sidebar)

        # Property data
        cursor.execute(f"SELECT * FROM properties WHERE property_id = '{pid}'")
        (_, _, property_category, location_city, title, address, rent_price, bhk) = cursor.fetchone()
        cursor.execute(f"SELECT * FROM res_prop_det WHERE property_id = '{pid}'")
        (_, _, area_sqft, furnishing_details, parking_availability, age_of_property, description) = cursor.fetchone()
        cursor.execute(f"SELECT * FROM loc WHERE city = '{location_city}'")
        (state, _) = cursor.fetchone()

        # Titles
        tb.Label(f1, text=title, font=("Montserrat", 18)).grid(row=0, column=1, sticky="ew", columnspan=1, pady=2, padx=10)
        tb.Label(f1, text=f"{location_city}, {state}", font=("Montserrat", 16)).grid(row=1, column=1, sticky="ew", columnspan=1, pady=2, padx=10)
        tb.Label(f1, text=pid, font=("Montserrat", 12)).grid(row=2, column=1, sticky="ew", columnspan=1, pady=2, padx=10)

        # Main content scrolled frame
        sf3 = ScrolledFrame(f1, width=900, height=575)
        sf3.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)
        sf3.container.columnconfigure(1, weight=1)
        sf3.container.columnconfigure(2, weight=2)

        # Images
        cursor.execute(f"SELECT * FROM res_prop_img WHERE property_id = '{pid}'")
        imgs = cursor.fetchall()
        for idx, i in enumerate(imgs):
            imgVar = ImageTk.PhotoImage(Image.open(i[2]).resize((300, 150)))
            img_label = tb.Label(sf3.container, image=imgVar)
            img_label.image = imgVar
            img_label.grid(row=idx * 3, column=0, rowspan=3, padx=10, pady=10)

        # Info rows
        def add_row(label, value, r):
            tb.Label(sf3.container, text=label, font=("Montserrat", 12)).grid(column=1, row=r, sticky="w", padx=20, pady=10)
            tb.Label(sf3.container, text=value, font=("Montserrat", 12)).grid(column=2, row=r, sticky="nsew", padx=20, pady=10)

        add_row("Location:", f"{address}\n{location_city}\n{state}", 0)
        add_row("Property Category:", property_category, 1)
        add_row("Price:", f"₹{rent_price}", 2)
        add_row("BHK:", bhk, 3)
        add_row("Area sqft:", f"{area_sqft} sq.ft", 4)
        add_row("Furnishing details:", furnishing_details, 5)
        add_row("Parking availability:", parking_availability, 6)
        add_row("Age of property:", f"{age_of_property} years", 7)

        tb.Label(sf3.container, text="Description:", font=("Montserrat", 12)).grid(column=1, row=8, sticky="w", padx=20, pady=10)
        tb.Label(sf3.container, text=description, font=("Montserrat", 12), wraplength=600, justify="left").grid(column=2, row=8, sticky="w", padx=20, pady=10)

    
    new_frame_open(my_tent_frame, main_frame)
    
    tent_btn_frame = tb.Frame(my_tent_frame, width=0, height=750)
    tent_btn_frame.grid(row=0, column=0, sticky=tk.NW, rowspan=17)

    tb.Button(tent_btn_frame, text="Go back", command=lambda: back_to_main_frame(my_tent_frame, main_frame)).grid(row=0, column=0, pady=20, padx=10)

    sf2 = ScrolledFrame(my_tent_frame, autohide=True, width=1250, height=600)
    sf2.grid(row=1, column=2)

    cursor.execute(f"select * from properties where owner_username = '{pfp_user_email}'")
    my_prop = cursor.fetchall()
    no_prop = cursor.rowcount
    
    tb.Label(my_tent_frame, text=f"You currently have {no_prop} properties", font=("Monsterrat",18)).grid(row=0,column=2, pady=20)
    
    for p in my_prop:
        print(p)
        r = my_prop.index(p) // 3
        c = my_prop.index(p) % 3
        
        if p[0].startswith("L"):
            t = "For LEASE"
        else:
            t = "For SALE"
        
        f = tb.Labelframe(sf2, text=t)
        f.grid(row=r, column=c, padx=5, pady=10, sticky=EW)
        
        cursor.execute(f"select  i.property_id, image_path from res_prop_img i, properties p where i.property_id = p.property_id and p.owner_username = '{pfp_user_email}'")
        img = cursor.fetchall()
        
        for i in img:
            if p[0] == i[0]:
                imgVar = ImageTk.PhotoImage(Image.open(i[1]).resize((350, 200)))
                img_button = tb.Button(f, image=imgVar, bootstyle=tb.LINK, command=lambda pid=p[0]: see_prop(pid))
                img_button.image = imgVar  # Keep reference to avoid garbage collection
                img_button.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
                break
        
        # Property name and status
        tb.Label(f, text=p[4], font=("montserrat", 12), anchor="w").grid(row=1, column=0, padx=10, sticky="w")
        tb.Label(f, text=p[0], font=("montserrat", 8), anchor="w").grid(row=2, column=0, padx=(10, 0), pady=(0, 10), sticky="w")

        # Property category and location
        tb.Label(f, text=p[2], font=("montserrat", 12), anchor="w").grid(row=3, column=0, padx=10, sticky="w")
        tb.Label(f, text=p[3], font=("montserrat", 8), anchor="w").grid(row=4, column=0, padx=10, sticky="w")

        # Price range
        tb.Label(f, text=p[6], font=("montserrat", 12), anchor="e").grid(row=1, column=1, padx=(0, 10), sticky="e")









# >>>>>>>>>>>>>>>> TENANT DASHBOARD FRAME <<<<<<<<<<<<<<<<

def tenant_dashboard_open():
    # Create tenant dashboard frame
    tenant_frame = tb.Frame(root)
   
    # Create tables for tenant-specific data if they don't exist
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tenant_favorites (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tenant_username VARCHAR(60),
            property_id CHAR(10),
            FOREIGN KEY (tenant_username) REFERENCES users(username),
            FOREIGN KEY (property_id) REFERENCES properties(property_id),
            UNIQUE KEY unique_favorite (tenant_username, property_id)
        )
        """)
       
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tenant_properties (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tenant_username VARCHAR(60),
            property_id CHAR(10),
            transaction_type ENUM('rented', 'bought'),
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_username) REFERENCES users(username),
            FOREIGN KEY (property_id) REFERENCES properties(property_id)
        )
        """)
        mycon.commit()
    except mys.Error as err:
        print(f"Error creating tenant tables: {err}")

    # Back button
    back_frame = tb.Frame(tenant_frame)
    back_frame.pack(side=LEFT, fill=Y, padx=10, pady=10)
    tb.Button(back_frame, text="Go Back",
              command=lambda: back_to_main_frame(tenant_frame, main_frame)).pack(pady=10)

    # Filter frame
    filter_frame = tb.LabelFrame(tenant_frame, text="Filters", bootstyle=INFO)
    filter_frame.pack(side=LEFT, fill=Y, padx=10, pady=10)

    # Price range filter
    tb.Label(filter_frame, text="Price Range:").pack(pady=5)
    price_ranges = [
    "All Prices",
    "Under ₹20,000,000",
    "₹20,000,000 - ₹50,000,000",
    "₹50,000,000 - ₹100,000,000",
    "₹100,000,000 - ₹200,000,000",
    "₹200,000,000 - ₹400,000,000",
    "Above ₹400,000,000"]
    
    price_combo = tb.Combobox(filter_frame, values=price_ranges, state="readonly")
    price_combo.pack(pady=5)
    price_combo.current(0)

    # Property type filter
    tb.Label(filter_frame, text="Property Type:").pack(pady=5)
    prop_types = ["All Types", "Apartment", "Independent House", "Villa", "Commercial", "Land/Plot"]
    type_combo = tb.Combobox(filter_frame, values=prop_types, state="readonly")
    type_combo.pack(pady=5)
    type_combo.current(0)

    # Location filter
    tb.Label(filter_frame, text="Location:").pack(pady=5)
    cursor.execute("SELECT DISTINCT city FROM loc")
    locations = ["All Locations"] + [loc[0] for loc in cursor.fetchall()]
    loc_combo = tb.Combobox(filter_frame, values=locations, state="readonly")
    loc_combo.pack(pady=5)
    loc_combo.current(0)

    # Apply filters button
    apply_btn = tb.Button(filter_frame, text="Apply Filters", bootstyle=SUCCESS,
                         command=lambda: update_tenant_properties())
    apply_btn.pack(pady=10)

    # Main content frame
    content_frame = tb.Frame(tenant_frame)
    content_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

    # Property display frame
    prop_display = ScrolledFrame(content_frame, autohide=True, width=1000, height=700)
    prop_display.pack(fill=BOTH, expand=True)

    # Favorites and My Properties buttons
    btn_frame = tb.Frame(content_frame)
    btn_frame.pack(fill=X, pady=10)
   
    favorites_btn = tb.Button(back_frame, text="My Favorites", bootstyle=INFO,
                             command=lambda: show_favorites())
    favorites_btn.pack(pady=10, padx=5)
   
    my_props_btn = tb.Button(back_frame, text="My Properties", bootstyle=INFO,
                            command=lambda: show_my_properties())
    my_props_btn.pack(pady=10, padx=5)

    # Function to update property display based on filters
    def update_tenant_properties():
        # Clear previous properties
        for widget in prop_display.winfo_children():
            widget.destroy()

        # Get filter values
        price_filter = price_combo.get()
        type_filter = type_combo.get()
        loc_filter = loc_combo.get()

        # Build SQL query based on filters
        query = """
    SELECT
        p.property_id,
        p.title,
        p.owner_username,
        p.location_city,
        p.rent_price,
        p.property_category,
        p.bhk,
        MAX(r.image_path) as image_path,
        rp.furnishing_details,
        rp.area_sqft
    FROM properties p
    LEFT JOIN res_prop_img r ON p.property_id = r.property_id
    LEFT JOIN res_prop_det rp ON p.property_id = rp.property_id
    WHERE 1=1
    """

        # Apply filters
        if type_filter != "All Types":
            query += f" AND p.property_category = '{type_filter}'"
        if loc_filter != "All Locations":
            query += f" AND p.location_city = '{loc_filter}'"

        # Apply price filter
        if price_filter == "Under ₹20,000,000":
            query += " AND p.rent_price < 20000000"
        elif price_filter == "₹20,000,000 - ₹50,000,000":
            query += " AND p.rent_price BETWEEN 20000000 AND 50000000"
        elif price_filter == "₹50,000,000 - ₹100,000,000":
            query += " AND p.rent_price BETWEEN 50000000 AND 100000000"
        elif price_filter == "₹100,000,000 - ₹200,000,000":
            query += " AND p.rent_price BETWEEN 100000000 AND 200000000"
        elif price_filter == "₹200,000,000 - ₹400,000,000":
            query += " AND p.rent_price BETWEEN 200000000 AND 400000000"
        elif price_filter == "Above ₹400,000,000":
            query += " AND p.rent_price > 400000000"
    
        query += """
    GROUP BY
        p.property_id,
        p.title,
        p.owner_username,
        p.location_city,
        p.rent_price,
        p.property_category,
        p.bhk,
        rp.furnishing_details,
        rp.area_sqft
    """

        cursor.execute(query)
        properties = cursor.fetchall()

        # Display properties
        for idx, prop in enumerate(properties):
            (pid, title, owner, city, price, ptype, bhk, img_path, furnishing, area) = prop
           
            # Create property frame
            prop_frame = tb.Frame(prop_display, borderwidth=1, relief="solid", padding=10)
            prop_frame.pack(fill=X, pady=5, padx=5)

            # Load property image
            try:
                img = Image.open(img_path).resize((150, 100))
                img_tk = ImageTk.PhotoImage(img)
                img_label = tb.Label(prop_frame, image=img_tk)
                img_label.image = img_tk  # Keep reference
                img_label.pack(side=LEFT, padx=10)
            except:
                # Use placeholder if image fails to load
                img_label = tb.Label(prop_frame, text="No Image", width=15, height=6)
                img_label.pack(side=LEFT, padx=10)

            # Property details
            details_frame = tb.Frame(prop_frame)
            details_frame.pack(side=LEFT, fill=BOTH, expand=True)

            tb.Label(details_frame, text=title, font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=W)
            tb.Label(details_frame, text=f"Owner: {owner}").grid(row=1, column=0, sticky=W)
            tb.Label(details_frame, text=f"Location: {city}").grid(row=2, column=0, sticky=W)
            tb.Label(details_frame, text=f"Type: {ptype} | BHK: {bhk}").grid(row=3, column=0, sticky=W)
            tb.Label(details_frame, text=f"Furnishing: {furnishing} | Area: {area} sqft").grid(row=4, column=0, sticky=W)
            tb.Label(details_frame, text=f"Price: ₹{price:,.2f}", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky=W)

            # Action buttons
            btn_frame = tb.Frame(prop_frame)
            btn_frame.pack(side=RIGHT, padx=10)

            # Check if property is already favorited
            cursor.execute("SELECT 1 FROM tenant_favorites WHERE tenant_username = %s AND property_id = %s",
                          (pfp_user_email, pid))
            is_favorited = cursor.fetchone() is not None

            fav_btn = tb.Button(btn_frame, text="★ Favorite" if not is_favorited else "❤ Favorited",
                              bootstyle=SUCCESS if not is_favorited else DANGER,
                              command=lambda pid=pid: toggle_favorite(pid))
            fav_btn.pack(pady=2, fill=X)

            view_btn = tb.Button(btn_frame, text="View Details",
                               command=lambda pid=pid: prop_det_open(pid))
            view_btn.pack(pady=2, fill=X)

            rent_buy_btn = tb.Button(btn_frame, text="Rent/Buy",
                                   bootstyle=INFO,
                                   command=lambda pid=pid: rent_buy_property(pid, "Rent" if pid.startswith("L") else "Buy"))

            rent_buy_btn.pack(pady=2, fill=X)

    # Function to toggle favorite status
    def toggle_favorite(property_id):
        
        try:
        # Check if prop is already favorited
            cursor.execute("SELECT 1 FROM tenant_favorites WHERE tenant_username = %s AND property_id = %s",
                      (pfp_user_email, property_id))
        
            if cursor.fetchone():
                
            # Remove from favorites
                cursor.execute("DELETE FROM tenant_favorites WHERE tenant_username = %s AND property_id = %s",
                          (pfp_user_email, property_id))
                messagebox.showinfo("Success", "Property removed from favorites")
            else:
            # Add to favorites
                cursor.execute("INSERT INTO tenant_favorites (tenant_username, property_id) VALUES (%s, %s)",
                          (pfp_user_email, property_id))
                messagebox.showinfo("Success", "Property added to favorites")
          
            mycon.commit()
            update_tenant_properties()
        except mys.Error as err:
            
            messagebox.showerror("Database Error", f"Failed to update favorites: {err}")
    # Function to handle rent/buy action
    def rent_buy_property(property_id,transaction_type):
    # Ask the user whether they want to Rent or Buy
        choice = messagebox.askquestion("Rent or Buy", "Are you interested in **Renting** or **Buying** this property?", icon='question', type='yesnocancel', default='yes', detail="Click 'Yes' for Rent, 'No' for Buy, or Cancel to abort.")

        if choice == "cancel":
            return
        elif choice == "yes":
            transaction_type = "Rent"
        elif choice == "no":
            transaction_type = "Buy"

        try:
        # Insert the interest with proper padding (if needed)
            property_id_padded = property_id.ljust(10)
            print(f"[DEBUG] INSERTING: tenant_username={pfp_user_email}, property_id='[{property_id}]', transaction_type={transaction_type}")

            cursor.execute("""
            INSERT IGNORE INTO interested_users (tenant_username, property_id, transaction_type)
            VALUES (%s, %s, %s) """, (pfp_user_email, property_id_padded, transaction_type))
            mycon.commit()

        # Show success message
            messagebox.showinfo("Success", f"You've chosen to **{transaction_type}** this property.\nYour interest has been shared with the owner.")

        except Exception as e:
            messagebox.showerror("Error", f"Could not contact the owner.\n\nReason: {e}")

    # Function to show favorite properties
    def show_favorites():
        
        
    # Clear previous properties
        for widget in prop_display.winfo_children():
            widget.destroy()

        try:
            
            
        # Subquery approach to safely get one image per property
            query = """
        SELECT
            p.property_id,
            p.title,
            p.owner_username,
            p.location_city,
            p.rent_price,
            p.property_category,
            p.bhk,
            (
                SELECT MIN(image_path)
                FROM res_prop_img
                WHERE property_id = p.property_id
            ) AS image_path,
            rp.furnishing_details,
            rp.area_sqft
        FROM properties p
        JOIN tenant_favorites tf ON p.property_id = tf.property_id
        LEFT JOIN res_prop_det rp ON p.property_id = rp.property_id
        WHERE tf.tenant_username = %s
        """
            cursor.execute(query, (pfp_user_email,))
            favorites = cursor.fetchall()

            if not favorites:
                tb.Label(prop_display, text="You haven't favorited any properties yet").pack(pady=50)
                return

            for idx, prop in enumerate(favorites):
                (pid, title, owner, city, price, ptype, bhk, img_path, furnishing, area) = prop

            # Create property frame
                prop_frame = tb.Frame(prop_display, borderwidth=1, relief="solid", padding=10)
                prop_frame.pack(fill=X, pady=5, padx=5)

            # Load property image
                try:
                    img = Image.open(img_path).resize((150, 100))
                    img_tk = ImageTk.PhotoImage(img)
                    img_label = tb.Label(prop_frame, image=img_tk)
                    img_label.image = img_tk  # Keep reference
                    img_label.pack(side=LEFT, padx=10)
                except:
                    img_label = tb.Label(prop_frame, text="No Image", width=15, height=6)
                    img_label.pack(side=LEFT, padx=10)

            # Property details
                details_frame = tb.Frame(prop_frame)
                details_frame.pack(side=LEFT, fill=BOTH, expand=True)

                tb.Label(details_frame, text=title, font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=W)
                tb.Label(details_frame, text=f"Owner: {owner}").grid(row=1, column=0, sticky=W)
                tb.Label(details_frame, text=f"Location: {city}").grid(row=2, column=0, sticky=W)
                tb.Label(details_frame, text=f"Type: {ptype} | BHK: {bhk}").grid(row=3, column=0, sticky=W)
                tb.Label(details_frame, text=f"Furnishing: {furnishing} | Area: {area} sqft").grid(row=4, column=0, sticky=W)
                tb.Label(details_frame, text=f"Price: ₹{price:,}").grid(row=5, column=0, sticky=W)

            # Buttons
                btn_frame = tb.Frame(prop_frame)
                btn_frame.pack(side=RIGHT, padx=10)

                remove_btn = tb.Button(btn_frame, text="Remove Favorite", bootstyle=DANGER,
                                   command=lambda pid=pid: toggle_favorite(pid))
                remove_btn.pack(pady=2, fill=X)
  
                view_btn = tb.Button(btn_frame, text="View Details",
                                 command=lambda pid=pid: prop_det_open(pid))
                view_btn.pack(pady=2, fill=X)

                rent_buy_btn = tb.Button(btn_frame, text="Rent/Buy", bootstyle=INFO,
                                     command=lambda pid=pid: rent_buy_property(pid))
                rent_buy_btn.pack(pady=2, fill=X)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load favorites: {str(e)}")


    # Function to show rented/bought properties
    def show_my_properties():
       
       
        # Clear previous properties
        for widget in prop_display.winfo_children():
            widget.destroy()

        try:
            cursor.execute("SET SESSION sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''))")
            cursor.execute("""
            SELECT p.property_id, p.title, p.owner_username, p.location_city,
                   p.rent_price, p.property_category, p.bhk,
                   r.image_path, rp.furnishing_details, rp.area_sqft,
                   tp.transaction_type, tp.transaction_date
            FROM properties p
            JOIN tenant_properties tp ON p.property_id = tp.property_id
            LEFT JOIN res_prop_img r ON p.property_id = r.property_id
            LEFT JOIN res_prop_det rp ON p.property_id = rp.property_id
            WHERE tp.tenant_username = %s
            GROUP BY p.property_id
            """, (pfp_user_email,))
           
            my_properties = cursor.fetchall()
           
            cursor.execute("SET SESSION sql_mode=(SELECT CONCAT(@@sql_mode,',ONLY_FULL_GROUP_BY'))")
           
            if not my_properties:
                tb.Label(prop_display, text="You haven't rented or bought any properties yet").pack(pady=50)
                return
               
               
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
          

        # Display rented/bought properties
        for idx, prop in enumerate(my_properties):
            (pid, title, owner, city, price, ptype, bhk, img_path, furnishing, area, trans_type, trans_date) = prop
           
            # Create property frame
            prop_frame = tb.Frame(prop_display, borderwidth=1, relief="solid", padding=10)
            prop_frame.pack(fill=X, pady=5, padx=5)

            # Load property image
            try:
                img = Image.open(img_path).resize((150, 100))
                img_tk = ImageTk.PhotoImage(img)
                img_label = tb.Label(prop_frame, image=img_tk)
                img_label.image = img_tk  # Keep reference
                img_label.pack(side=LEFT, padx=10)
            except:
                # Use placeholder if image fails to load
                img_label = tb.Label(prop_frame, text="No Image", width=15, height=6)
                img_label.pack(side=LEFT, padx=10)

            # Property details
            details_frame = tb.Frame(prop_frame)
            details_frame.pack(side=LEFT, fill=BOTH, expand=True)

            tb.Label(details_frame, text=title, font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=W)
            tb.Label(details_frame, text=f"Owner: {owner}").grid(row=1, column=0, sticky=W)
            tb.Label(details_frame, text=f"Location: {city}").grid(row=2, column=0, sticky=W)
            tb.Label(details_frame, text=f"Type: {ptype} | BHK: {bhk}").grid(row=3, column=0, sticky=W)
            tb.Label(details_frame, text=f"Furnishing: {furnishing} | Area: {area} sqft").grid(row=4, column=0, sticky=W)
            tb.Label(details_frame, text=f"Price: ₹{price:,.2f}", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky=W)
            tb.Label(details_frame, text=f"Status: {trans_type.capitalize()} on {trans_date.strftime('%Y-%m-%d')}",
                   font=("Arial", 10, "italic")).grid(row=6, column=0, sticky=W)

            # Action buttons
            btn_frame = tb.Frame(prop_frame)
            btn_frame.pack(side=RIGHT, padx=10)

           # view_btn = tb.Button(btn_frame, text="View Details",
            #                   command=view_prop)
            #view_btn.pack(pady=2, fill=X)

    # Initialize with all properties
    update_tenant_properties()

    # Open the tenant dashboard
    new_frame_open(tenant_frame, main_frame)
     
        
        
        


#>>>>>>>>>>>>>>>>>> End of Code <<<<<<<<<<<<<<<<<<<<<<
root.mainloop()
