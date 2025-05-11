import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def toggle_sidebar():
    if sidebar.winfo_viewable():
        sidebar.forget()  # Hide the sidebar frame
        toggle_btn.config(text="Show Sidebar")
    else:
        sidebar.pack(side=LEFT, fill=Y)
        toggle_btn.config(text="Hide Sidebar")

root = ttk.Window(title="Sidebar Example", themename="litera", size=(600, 400))

# Sidebar frame
sidebar = ttk.Frame(root, width=200, bootstyle="secondary")
sidebar.pack(side=LEFT, fill=Y)

# Add some content to sidebar
ttk.Label(sidebar, text="Sidebar Content", bootstyle="info").pack(pady=10)

# Main content frame
main_content = ttk.Frame(root)
main_content.pack(side=LEFT, fill=BOTH, expand=True)

ttk.Label(main_content, text="Main Content Area", bootstyle="primary").pack(pady=20)

# Toggle button to minimize/show sidebar
toggle_btn = ttk.Button(main_content, text="Hide Sidebar", bootstyle=SUCCESS, command=toggle_sidebar)
toggle_btn.pack(pady=10)

root.mainloop()



























