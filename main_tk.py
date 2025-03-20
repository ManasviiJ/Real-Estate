import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from ttkbootstrap import ttk
from ttkbootstrap.scrolled import ScrolledFrame
from PIL import Image, ImageTk
import mysql.connector as mys
import os


# >>>>>>>>>>>>>>>> Define the main window <<<<<<<<<<<<<<<<
root = tb.Window(themename="superhero")
root.geometry('1600x1400')
root.title("Real Estate Management")

# Connecting MySQL to Python Interface
mycon = mys.connect(host="localhost", user="root", passwd="root", database="re_estate")
cursor = mycon.cursor()

# >>>>> Create Frames
login_frame=tb.Frame(root)
login_frame.pack(expand=True, fill='both')

main_frame=tb.Frame(root)

profile_frame = tb.Frame(root)

prop_detail_frame = tb.Frame(root)

post_prop_frame = tb.Frame(root)

# >>>>>>>>>> THE LOGIN FRAME FUNCTIONS <<<<<<<<<<

# COMMON Functions For The Login Page
def login_success():
    username_entry_si.delete(0,END)
    password_entry_si.delete(0,END)
    login_frame.pack_forget()
    main_frame.pack(expand=True, fill='both')


def role_select(uname):
    global img_tent, img_agent, img_own  # Keep reference to images

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

    # Agent Role Button
    img_agent = Image.open("images/agent.jpeg").resize((100, 100))
    img_agent = ImageTk.PhotoImage(img_agent)
    img_btn_agent = tb.Button(rframe, image=img_agent, bootstyle=tb.LINK, 
                              command=lambda: select_role("Agent",uname,role_select_frame))
    img_btn_agent.pack(pady=10)
    tb.Label(rframe, text="AGENT", font=("Arial", 14), bootstyle="primary").pack()

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
                                command=lambda: new_frame_open(profile_frame))
        profile_btn.image = profile_img  # Keep reference
        profile_btn.grid(row=0, column=0, sticky=EW, pady=10)

    profile_btn = tb.Button(sidebar, image=profile_img, bootstyle=tb.LINK, command=lambda: new_frame_open(profile_frame))
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

# Frames in Main Frame - UI
search_entry_frame = tb.Labelframe(main_frame,text="Search property by location")
search_entry_frame.grid(row=1,column=1,columnspan=2)

sf = ScrolledFrame(main_frame, autohide=True,width=1250, height=550)
sf.grid(row=2,column=1, padx=10, pady=10)

sidebar = tb.Frame(main_frame, width=0, height=750)
sidebar.grid(row=0,column=0,sticky=NW, rowspan=3)

# COMMON Functions   
def back_to_main_frame(frame):
    frame.pack_forget()
    main_frame.pack(expand=TRUE,fill=BOTH)

def new_frame_open(frame):
    main_frame.pack_forget()
    frame.pack(expand=TRUE, fill=BOTH)
    pass

# Functions under the SEARCH FRAME
search_options = [
    "Bellandur", "CV Raman Nagar", "Hoodi", "Krishnarajapuram", "Mahadevapura", "Marathahalli", "Varthur", "Varthur",
    "Banaswadi", "HBR Layout", "Horamavu", "Kalyan Nagar", "Kammanahalli", "Lingarajapuram", "Ramamurthy Nagar",
    "Hebbal", "Mathikere", "Jalahalli", "Peenya", "Vidyaranyapura", "Yelahanka", "Yeshwanthpur",
    "Banashankari", "Basavanagudi", "Girinagar", "J. P. Nagar", "Jayanagar", "Kumaraswamy Layout", "Padmanabhanagar", "Uttarahalli",
    "Basaveshwaranagar", "Kamakshipalya", "Kengeri", "Mahalakshmi Layout", "Nagarbhavi", "Nandini Layout", "Nayandahalli", "Rajajinagar", 
    "Rajarajeshwari Nagar", "Vijayanagar", "Cantonment area", "Domlur", "Indiranagar", "Rajajinagar", "Malleswaram", "Pete area", 
    "Sadashivanagar", "Seshadripuram", "Shivajinagar", "Ulsoor", "Vasanth Nagar", "R.T.Nagar", 
    "Bommanahalli", "Bommasandra", "BTM Layout", "Electronic City", "HSR Layout", "Koramangala", "Madiwala",
    "Anjanapura", "Arekere", "Begur", "Gottigere", "Hulimavu", "Kothnur", "Sarjapura", "Jigani", "Attibele"
    ]


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

def entry_fill(event):
    selected_place = listbox.get(listbox.curselection())
    search_entry_var.set(selected_place)
    listbox.grid_forget()

# Functions Under The PROPERTY FRAME
def create_property_frame(property_data, parent_frame):
    index = properties.index(property_data)
    
     # Determine row and column based on index
    row = index // 3  # Ensures every 3 items go to the next row
    column = index % 3  # 3 columns per row

    prop_frame = tb.Labelframe(parent_frame, text="Buy")
    prop_frame.grid(row=row, column=column, padx=10, pady=10, sticky="ew")

    # Load image
    imgVar = ImageTk.PhotoImage(Image.open(property_data["image_path"]).resize((350, 200)))
    img_button = tb.Button(prop_frame, image=imgVar, bootstyle=tb.LINK, command=lambda: new_frame_open(prop_detail_frame))
    img_button.image = imgVar  # Keep reference to avoid garbage collection
    img_button.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

    # Property name and builder
    tb.Label(prop_frame, text=property_data["name"], font=("montserrat", 12), anchor="w").grid(row=1, column=0, padx=10, sticky="w")
    tb.Label(prop_frame, text=property_data["builder"], font=("montserrat", 8), anchor="w").grid(row=2, column=0, padx=(10, 0), pady=(0, 10), sticky="w")

    # Property details and location
    tb.Label(prop_frame, text=property_data["details"], font=("montserrat", 12), anchor="w").grid(row=3, column=0, padx=10, sticky="w")
    tb.Label(prop_frame, text=property_data["location"], font=("montserrat", 8), anchor="w").grid(row=4, column=0, padx=10, sticky="w")

    # Price range
    tb.Label(prop_frame, text=property_data["price_range"], font=("montserrat", 12), anchor="e").grid(row=1, column=1, padx=(0, 10), sticky="e")

cursor.execute("select * from prop_buy")
prop_list = cursor.fetchall()
properties = []
for prop in prop_list:
    properties.append({
        "image_path":prop[0],
        "name":prop[1],
        "builder":prop[2],
        "details":prop[3],
        "location":prop[4],
        "price_range":prop[5]
    })
    
# UI Under PROPERTY FRAME

for prop in properties:
    create_property_frame(prop, sf)


# >>>>>>>>>>>>>>>> MAIN FRAME UI <<<<<<<<<<<<<<<<

tb.Label(main_frame, text="Real Estate Management", font=("Helvetica", 18)).grid(column=1,row=0,padx=10,pady=10)

# UI Under SEARCH FRAME
search_entry_button = tb.Button(search_entry_frame, text="Go", bootstyle=(SUCCESS,OUTLINE))
search_entry_button.grid(row=0,column=1,pady=5,padx=10)

search_entry_var=tk.StringVar()

search_entry=tb.Entry(search_entry_frame,textvariable=search_entry_var, bootstyle=SUCCESS, width=80)
search_entry.grid(row=0,column=0,padx=5,pady=5)

search_entry.bind("<KeyRelease>",suggest_places)

listbox=tk.Listbox(search_entry_frame)
listbox.bind("<<ListboxSelect>>",entry_fill)

# UI Under SIDEBAR
if pfp_user_email is not None:
    cursor.execute("select * from users where username = '{}'".format(pfp_user_email))
    data = cursor.fetchall
    if data[4] == "Owner":
        tb.Button(sidebar, text="Post\nyour\nproperty", bootstyle=SUCCESS, command=lambda: new_frame_open(post_prop_frame)).pack(pady=10)

style = tb.Style()
style.configure("success.TButton", anchor="center", justify="center")

tb.Button(sidebar, text="Post\nyour\nproperty", bootstyle=SUCCESS, command=lambda: new_frame_open(post_prop_frame)).grid(row=1,column=0,pady=10)




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
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
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

        if new_phone != phone:
            if new_phone.isdigit() and len(new_phone) <= 10:
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
    
# >>>>>>>>>>>>>>>> PROFILE PAGE UI <<<<<<<<<<<<<<<<

pfp_btn_frame = tb.Frame(profile_frame)
pfp_btn_frame.grid(row=0, column=0, rowspan=3)
  
tb.Button(pfp_btn_frame, text="Go Back", command=lambda: back_to_main_frame(profile_frame)).pack(pady=(0,20), fill=BOTH, padx=(10,0))
tb.Button(pfp_btn_frame,text="Edit", bootstyle=WARNING, command=edit_profile).pack(pady=(0,20), fill=BOTH, padx=(10,0)) 
tb.Button(pfp_btn_frame, text="Logout", bootstyle=SECONDARY,command=logout).pack(pady=(0,20), fill=BOTH, padx=(10,0))

tb.Separator(profile_frame, orient=VERTICAL).grid(row=0,column=1,sticky=NS,rowspan=50, padx=(10,400))

tb.Label(profile_frame, text="Full name:", font=("Arial bold",12)).grid(row=2,column=2,padx=(20,0),pady=20,sticky=W)
tb.Label(profile_frame, text="Email Address:", font=("Arial bold",12)).grid(row=3,column=2,padx=(20,0),pady=20,sticky=W)
tb.Label(profile_frame, text="Phone:", font=("Arial bold",12)).grid(row=4,column=2,padx=(20,0),pady=20,sticky=W)
tb.Label(profile_frame, text="Role:", font=("Arial bold",12)).grid(row=5,column=2,padx=(20,0),pady=20,sticky=W)






# >>>>>>>>>>>>>>>> POST PROP FRAME UI <<<<<<<<<<<<<<<<
##sidebar
post_btn_frame = tb.Frame(post_prop_frame, width=0, height=750)
post_btn_frame.grid(row=0, column=0, sticky=tk.NW, rowspan=17)
tb.Button(post_btn_frame, text="Go back", command=lambda: back_to_main_frame(post_prop_frame)).grid(row=0, column=0, pady=10, padx=10)
tb.Separator(post_prop_frame, orient=VERTICAL).grid(row=0, column=1, padx=(10,100), sticky=NS, rowspan=4)


tb.Label(post_prop_frame, text="POST YOUR PROPERTY", font=("Montserrat", 24)).grid(row=0, column=2, columnspan=3, padx=300, pady=10, sticky=tk.W)

sf2 = ScrolledFrame(post_prop_frame, autohide=True, width=1200, height=600)
sf2.grid(row=1, column=2, columnspan=3, padx=10, pady=10, sticky=W)

sell_lease = tk.StringVar()

# SELL OR LEASE
tb.Label(sf2, text="SELL OR LEASE:", font=("Montserrat", 12)).grid(row=0, column=0, pady=10, sticky=tk.W)
sell = tb.Radiobutton(sf2, text="SELL", variable=sell_lease, value="SELL")
sell.grid(row=0, column=1)
lease = tb.Radiobutton(sf2, text="LEASE", variable=sell_lease, value="LEASE")
lease.grid(row=0, column=2)

# PROPERTY TYPE
tb.Label(sf2, text="PROPERTY TYPE:", font=("Montserrat", 12)).grid(row=1, column=0, pady=10, sticky=tk.W)
prop_type_list = ["Residential Property", "Commercial/Industrial Property", "Land/Plot"]
prop_type = tb.Combobox(sf2, bootstyle="primary", values=prop_type_list)
prop_type.grid(row=1, column=1, columnspan=2)

# PROPERTY DETAILS FRAME
Prop_dets_frame = tb.LabelFrame(sf2, text="PROPERTY DETAILS")
Prop_dets_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky=W)

# Title
tb.Label(Prop_dets_frame, text="Title:", font=("Montserrat", 12)).grid(column=0, row=0, sticky=tk.W, padx=20)
title = tb.Entry(Prop_dets_frame)
title.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky=tk.EW)

# Location
tb.Label(Prop_dets_frame, text="Location:", font=("Montserrat", 12)).grid(column=0, row=1, sticky=tk.W, padx=20)
loc = tb.Combobox(Prop_dets_frame, bootstyle="primary", values=["Option1", "Option2"])  # Replace with actual options
loc.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=tk.EW)

# Address
tb.Label(Prop_dets_frame, text="Address:", font=("Montserrat", 12)).grid(column=0, row=2, sticky=tk.W, padx=20)
address = tb.Entry(Prop_dets_frame)
address.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky=tk.EW)

# Number of rooms
tb.Label(Prop_dets_frame, text="No of rooms (BHK):", font=("Montserrat", 12)).grid(column=0, row=3, sticky=tk.W, padx=20)
bhk = tb.Entry(Prop_dets_frame)
bhk.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky=tk.EW)

# Area sqft
tb.Label(Prop_dets_frame, text="Area sqft:", font=("Montserrat", 12)).grid(column=0, row=4, sticky=tk.W, padx=20)
area = tb.Entry(Prop_dets_frame)
area.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky=tk.EW)

# Furnishing details
tb.Label(Prop_dets_frame, text="Furnishing details:", font=("Montserrat", 12)).grid(column=0, row=5, sticky=tk.W, padx=20)
fur_list = ["Unfurnished", "Semi-Furnished", "Fully-Furnished"]
fur = tb.Combobox(Prop_dets_frame, bootstyle="primary", values=fur_list)
fur.grid(row=5, column=1, columnspan=2, padx=5, pady=5, sticky=tk.EW)

# Parking Availability
tb.Label(Prop_dets_frame, text="Parking Availability", font=("Montserrat", 12)).grid(column=0, row=6, sticky=tk.W, padx=20)
park = tk.BooleanVar()
Yes = tb.Radiobutton(Prop_dets_frame, text="YES", variable=park, value=1)
Yes.grid(row=6, column=1, padx=5, pady=5)
No = tb.Radiobutton(Prop_dets_frame, text="NO", variable=park, value=0)
No.grid(row=6, column=2, padx=5, pady=5)

# Age of Property
tb.Label(Prop_dets_frame, text="Age of Property", font=("Montserrat", 12)).grid(column=0, row=7, sticky=tk.W, padx=20)
age = tb.Entry(Prop_dets_frame)
age.grid(row=7, column=1, columnspan=2, padx=5, pady=5, sticky=tk.EW)

# Description
tb.Label(Prop_dets_frame, text="Description", font=("Montserrat", 12)).grid(column=0, row=8, sticky=tk.W, padx=20)
desc = tb.Entry(Prop_dets_frame)
desc.grid(row=8, column=1, columnspan=2, padx=5, pady=5, sticky=tk.EW)

# UPLOADING MEDIA
style = tb.Style()
style.configure("Warning.Link.TButton", font=("montserrat", 12), foreground="#FFC107")

tb.Button(sf2, text="Upload images and other media of your property", style="Warning.Link.TButton").grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky=W)

sf3 = ScrolledFrame(sf2, autohide=True, height=100)
sf3.grid(row=4, column=0, columnspan=5, padx=10, pady=10, sticky=W)

# PRICING DETAILS FRAME
Price_frame = tb.LabelFrame(sf2, text="PRICING DETAILS")
Price_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky=tk.EW)

# Price/Rent
tb.Label(Price_frame, text="Price/Rent:", font=("Montserrat", 12)).grid(column=0, row=0, sticky=tk.W, padx=20)
price_entry = tb.Entry(Price_frame)
price_entry.grid(column=1, row=0, padx=5, pady=5, sticky=tk.EW)

# Lease Duration
tb.Label(Price_frame, text="Lease Duration:", font=("Montserrat", 12)).grid(column=0, row=1, sticky=tk.W, padx=20)
lease_duration_entry = tb.Entry(Price_frame)
lease_duration_entry.grid(column=1, row=1, padx=5, pady=5, sticky=tk.EW)

# Extra Bills
tb.Label(Price_frame, text="Extra Bills:", font=("Montserrat", 12)).grid(column=0, row=2, sticky=tk.W, padx=20)
extra_bills_entry = tb.Entry(Price_frame)
extra_bills_entry.grid(column=1, row=2, padx=5, pady=5, sticky=tk.EW)

# CONTACT INFORMATION FRAME
Contact_frame = tb.LabelFrame(sf2, text="CONTACT INFORMATION")
Contact_frame.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky=tk.EW)

# Name
tb.Label(Contact_frame, text="Name:", font=("Montserrat", 12)).grid(column=0, row=0, sticky=tk.W, padx=20)
nm_entry = tb.Entry(Contact_frame)
nm_entry.grid(column=1, row=0, padx=5, pady=5, sticky=tk.EW)

# Email Id
tb.Label(Contact_frame, text="Email Id:", font=("Montserrat", 12)).grid(column=0, row=1, sticky=tk.W, padx=20)
eid_entry = tb.Entry(Contact_frame)
eid_entry.grid(column=1, row=1, padx=5, pady=5, sticky=tk.EW)

# Phone
tb.Label(Contact_frame, text="Phone:", font=("Montserrat", 12)).grid(column=0, row=2, sticky=tk.W, padx=20)
phone_entry = tb.Entry(Contact_frame)
phone_entry.grid(column=1, row=2, padx=5, pady=5, sticky=tk.EW)

## SUBMIT
# style.configure("Success.TButton", font=("Montserrat",12), background="#198754",  borderwidth=2)
# style.map("Success.TButton",
#     background=[("active", "#198754")],  # Darker green on hover
#     bordercolor=[("active", "#198754")],  # Ensure border changes as well
# )

submit_button = tb.Button(sf2, text="SUBMIT", bootstyle=SUCCESS)
submit_button.grid(row=8, column=0, columnspan=3, pady=20)


#>>>>>>>>>>>>>>>>>> End of Code <<<<<<<<<<<<<<<<<<<<<<
root.mainloop()
