import ttkbootstrap as tb
from ttkbootstrap.constants import *

app = tb.Window(themename="cosmo")

default_text = tb.StringVar(value="Hello, default world!")

entry = tb.Entry(app, textvariable=default_text)
entry.pack(pady=10)

app.mainloop()
