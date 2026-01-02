import tkinter as tk
from tkinter import messagebox
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from ttkbootstrap import ttk
import mysql.connector as mys

def create_login_window(root_window):
    login_frame=tb.Frame(root_window)
    login_frame.pack(expand=True, fill='both')

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

    return login_window
