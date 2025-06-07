import os
os.environ['TCL_LIBRARY'] = os.path.abspath('E:\\others\\Installers\\python-3.11.5-embed-amd64\\tcl\\tcl8.6')
os.environ['TK_LIBRARY'] = os.path.abspath('E:\\others\\Installers\\python-3.11.5-embed-amd64\\tcl\\tk8.6')


import sys
print("\n".join(sys.path))

lib_path = os.path.abspath('E:\\others\\Installers\\python-3.11.5-embed-amd64\\Lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

import tkinter as tk

root = tk.Tk()
root.title("Test Window")
root.geometry("300x100")

label = tk.Label(root, text="Tkinter is working!", font=("Arial", 14))
label.pack(pady=20)

root.mainloop()

"""
portable_python\
├── python.exe
├── Lib\
│   ├── tkinter\
│   │   ├── __init__.py
│   │   ├── colorchooser.py
│   │   ├── dialog.py
│   │   ├── filedialog.py
│   │   ├── font.py
│   │   ├── messagebox.py
│   │   ├── simpledialog.py
│   │   ├── scrolledtext.py
│   │   └── __pycache__\
├── DLLs\
├── ├── _tkinter.pyd
│   ├── tk86t.dll
│   └── tcl86t.dll
├── tcl\
│   ├── tcl8.6\
│   └── tk8.6\
"""