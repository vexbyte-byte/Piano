import time
import re
from datetime import datetime
import soundfile as sf
import os
import sounddevice as sd
import ctypes
from ctypes import wintypes
import sys
import json
os.environ['TCL_LIBRARY'] = os.path.abspath('E:\\others\\Installers\\python-3.11.5-embed-amd64\\tcl\\tcl8.6')
os.environ['TK_LIBRARY'] = os.path.abspath('E:\\others\\Installers\\python-3.11.5-embed-amd64\\tcl\\tk8.6')
# print("\n".join(sys.path)) # debugger
lib_path = os.path.abspath('E:\\others\\Installers\\python-3.11.5-embed-amd64\\Lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)
import tkinter as tk
from tkinter import colorchooser, simpledialog, messagebox

def name():
    try:
        global root
        clear_screen()
        root.destroy()
    except:
        pass
    shades = [
        "\033[38;5;81m",   # Light Blue
        "\033[38;5;75m",
        "\033[38;5;69m",
        "\033[38;5;63m",
        "\033[38;5;27m",   # Medium Blue
        "\033[38;5;18m",   # Dark Blue
    ]
    reset = "\033[0m"
    text = """
                _____________                     
                ___  __ \__(_)_____ _____________ 
                __  /_/ /_  /_  __ `/_  __ \  __ \ 
                _  ____/_  / / /_/ /_  / / / /_/ /
                /_/     /_/  \__,_/ /_/ /_/\____/                 
    """
    visible_chars = [char for char in text if char.strip() != "" and char != "\n"]
    total_visible = len(visible_chars)

    gradient_text = ""
    count = 0

    for char in text:
        if char.strip() == "" or char == "\n":
            gradient_text += char
        else:
            color_index = int((count / total_visible) * (len(shades) - 1))
            gradient_text += shades[color_index] + char
            count += 1

    gradient_text += reset
    print(gradient_text)

def main_menu():
    try:
        name()
        print("\033[92m")
        print("\033[91m[01]\033[32m Play Piano")
        print("\033[91m[02]\033[32m Play An Audio File")
        print("\033[91m[03]\033[32m Change Themes")
        print("\033[91m[04]\033[32m License")
        print("\033[91m[05]\033[32m About")
        print("\033[91m[06]\033[32m Settings")
        print("\033[91m[06]\033[32m Check For Updates")
        selection = input("Select > ")
        if selection[0] == "0":
            selection = selection[1]

        # define commands
        every_command = {
            "1": keyboard,
            "2": find_directory,
            "3": new_theme_color,
            "4": license,
            "5": about,
            "6": setting,
            "7": check_for_updates
        }
        func = every_command.get(selection)
        func()
    except Exception as e:
        return

def setting():
    clear_screen()
    name()
    print("\033[91m[01]\033[32m Use Python Generated Piano Sound")
    print("\033[91m[02]\033[32m Use Real Piano Sound")
    path_to_save = "E:\\Music\\personalization_database\\user_choice.txt"
    
    # let user select
    selection = input("select > ")
    if selection.startswith("0"):
        selection = selection[1]
    
    if selection == "1":
        path = "E:\\Music\\Keys\\output_wavs"
    elif selection == "2":
        path = "E:\\Music\\database_new"
    else:
        print("Invalid selection.")
        return

    # Save selected path to file
    print()
    try:
        with open(path_to_save, "w") as f:
            f.write(path)
        print(f"\033[92m[+] Path saved to {path_to_save}")
        print("You can now try out the piano or playing a music")
    except Exception as e:
        print(f"\033[91m[!] Failed to save path: {e}")
    input("\nPress any key to continue...")

def find_directory():
    clear_screen()
    name()
    directory = "E:\Music\Keys"
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files.sort()
    print()
    print("\033[32mNo".rjust(12) + "Name".rjust(52))
    print("   " + "-" * 5 + "      " + "-" * 45)
    for i, file in enumerate(files, start=1):
        print(f"\033[91m[{i:02}]".rjust(13) + f"\033[92m{file}".rjust(56))
    print()
    try:
        choice = int(input("\033[96mEnter the number of the file to open: "))
        if 1 <= choice <= len(files):
            selected_file = files[choice - 1]
            file_path = os.path.join(directory, selected_file)
            print(f"\n\033[93mYou selected: {selected_file}")
            extract(file_path)
        else:
            print("\033[91mInvalid choice.")
    except ValueError:
        print("\033[91mPlease enter a valid number.")
    except Exception as e:
        print("\033[91m [!] ", e)
    return None

THEME_PATH = "E:\\Music\\personalization_database\\theme.json"

class ThemeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Piano Theme Editor")
        self.theme = {
            "white_key": "#ffffff",
            "black_key": "#000000",
            "highlight_white": "#ffff99",
            "highlight_black": "#444444",
            "background": "#f0f0f0"
        }

        self.entries = {}

        row = 0
        for key in self.theme:
            tk.Label(root, text=key).grid(row=row, column=0, padx=10, pady=5, sticky="w")
            btn = tk.Button(root, text="Pick Color", command=lambda k=key: self.choose_color(k))
            btn.grid(row=row, column=1)
            entry = tk.Entry(root, width=10)
            entry.insert(0, self.theme[key])
            entry.grid(row=row, column=2)
            self.entries[key] = entry
            row += 1

        tk.Button(root, text="Save Theme", command=self.save_theme).grid(row=row, column=0, columnspan=3, pady=15)

    def choose_color(self, key):
        color = colorchooser.askcolor(title=f"Choose color for {key}")
        if color[1]:
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, color[1])

    def save_theme(self):
        name = simpledialog.askstring("Theme Name", "Enter a name for this theme:")
        if not name:
            return
        theme_data = {key: self.entries[key].get() for key in self.entries}
        try:
            with open(THEME_PATH, "r") as f:
                themes = json.load(f)
        except FileNotFoundError:
            themes = {}
        themes[name] = theme_data
        with open(THEME_PATH, "w") as f:
            json.dump(themes, f, indent=4)
        messagebox.showinfo("Saved", f"Theme '{name}' saved!")

def new_theme_color():
    global root
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", main_menu)
    app = ThemeEditor(root)
    root.mainloop()

def clear_screen():
    try:
        os.system("cls" if os.name == "nt" else "clear")
        print('\033c', end = "")
    except:
        pass

def extract(file_path):    
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            data = data.splitlines()
        
        # define key_path
        key_path = saved_path

        # filtering out notes and time
        pattern = r"Note:\s*([A-G]#?\d)\s+Start:\s*([0-9.]+)s\s+Duration:\s*([0-9.]+)s"
        matches = re.findall(pattern, '\n'.join(data))
        for note, time_str, duration_str in matches:
            try:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                sound_name = f"{note}{extension}"
                full_path = os.path.join(key_path, sound_name)
                data, samplerate = sf.read(full_path)
                print(f"[{current_time}] ", note)
                sd.play(data, samplerate)
                time.sleep(float(duration_str))
            except Exception as e:
                print("\033[91m[!] ", e)

    except Exception as e:
        print("\033[91m[!] ", e)

# idea
""""
def on_close():
    print("Tkinter window closed!")
    root.destroy()  # Close the window

root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_close)

print("Starting Tkinter mainloop")
root.mainloop()

print("Tkinter closed, Python still running!")

# Now keep Python running with a loop or other tasks
while True:
    print("Python script alive...")
    time.sleep(2)
"""
# Constants for key sizes
WHITE_KEY_WIDTH = 24
WHITE_KEY_HEIGHT = 150
BLACK_KEY_WIDTH = 14
BLACK_KEY_HEIGHT = 90

# Notes of one octave starting from A (since piano lowest key is A0)
WHITE_KEYS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
BLACK_KEYS = ['A#', 'C#', 'D#', '', 'F#', 'G#', 'A#']  # Note positions relative to white keys

# Map white keys order on the keyboard from A0 to C8
# 88 keys: from A0 (lowest) to C8 (highest)
# White keys count: 52, black keys: 36

# To know if a key is black, we'll define the pattern of black keys for each octave:
# Black keys appear after these white keys: A, C, D, F, G
BLACK_KEY_POSITIONS_IN_OCTAVE = [0, 2, 3, 5, 6]  # indexes in WHITE_KEYS where black keys appear after

class Piano88(tk.Frame):
    def __init__(self, master=None, theme_name="default"):
        super().__init__(master)
        self.theme = load_theme(theme_name)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Scrollable canvas to hold all 88 keys horizontally
        self.canvas = tk.Canvas(self, width=700, height=WHITE_KEY_HEIGHT)
        self.scroll_x = tk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scroll_x.set)

        self.scroll_x.pack(fill='x', side='bottom')
        self.canvas.pack(fill='both', expand=True)

        self.white_key_ids = []
        self.black_key_ids = []

        self.draw_keys()
        self.canvas.tag_bind('key', '<Button-1>', self.key_pressed)

    def draw_keys(self):
        # Start at A0
        # Total white keys = 52
        # Total black keys = 36

        octave_count = 7  # From A0 to B7 (7 full octaves)
        white_key_number = 0
        black_key_number = 0

        # White key order for 88 keys (52 white keys)
        # White keys from A0 to C8
        white_notes_sequence = []

        # The full piano white key sequence (52 notes)
        # We start at A0, then B0, then 7 full octaves (C-D-E-F-G-A-B), ending at C8
        # So the first octave is partial (A and B only), then full octaves

        # Manually build white keys names for all 52 white keys (including octave number)
        # A0, B0, C1, D1, E1, F1, G1, A1, B1, ..., C8

        # For convenience, list white keys with octave numbers
        white_notes_sequence.append('A0')
        white_notes_sequence.append('B0')
        octave = 1
        while len(white_notes_sequence) < 52:
            for note in ['C', 'D', 'E', 'F', 'G', 'A', 'B']:
                white_notes_sequence.append(note + str(octave))
                if len(white_notes_sequence) == 52:
                    break
            octave += 1

        # Black keys correspond to black notes between white keys,
        # For each white key (except last), check if there's a black key after it.

        # Draw white keys
        for i, note in enumerate(white_notes_sequence):
            x0 = i * WHITE_KEY_WIDTH
            x1 = x0 + WHITE_KEY_WIDTH
            y0 = 0
            y1 = WHITE_KEY_HEIGHT
            key_id = self.canvas.create_rectangle(
                    x0, y0, x1, y1,
                    fill=self.theme["white_key"],
                    outline='black',
                    tags=('key', f'white_{note}')
                )
            self.white_key_ids.append(key_id)
            # Draw note label near bottom
            self.canvas.create_text(x0 + WHITE_KEY_WIDTH / 2, y1 - 15, text=note, font=('Arial', 9))

        # Draw black keys
        # For black keys, we place them after certain white keys:
        # The black keys appear after white keys: A, C, D, F, G in the octave
        black_key_positions = []
        for i in range(len(white_notes_sequence)-1):
            # Extract the note letter without octave number
            note_letter = white_notes_sequence[i][0]  # e.g. 'A' from 'A0'
            # Special case for 'B' (no black key after B)
            # Check if the note_letter is one that has black key after it
            # For simplicity, map notes to indexes in WHITE_KEYS for black key presence
            # WHITE_KEYS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
            # Black keys after notes A, C, D, F, G only
            if note_letter in ['A', 'C', 'D', 'F', 'G']:
                # Calculate position of black key on canvas
                x0 = (i + 1) * WHITE_KEY_WIDTH - BLACK_KEY_WIDTH / 2
                x1 = x0 + BLACK_KEY_WIDTH
                y0 = 0
                y1 = BLACK_KEY_HEIGHT

                # Construct black note name:
                # Black keys are named as note_letter + '#' + octave number
                # But octave for black keys is same as the white key after it, except for A#0 and G#7
                # We'll deduce black key octave as same as the white key after it:
                next_white = white_notes_sequence[i + 1]
                octave_num = next_white[-1]

                black_note = note_letter + '#' + octave_num

                key_id = self.canvas.create_rectangle(
                    x0, y0, x1, y1,
                    fill=self.theme["black_key"],
                    outline='black',
                    tags=('key', f'black_{black_note}')
                )
                self.black_key_ids.append(key_id)
                # Draw black note label (small white text)
                self.canvas.create_text(x0 + BLACK_KEY_WIDTH / 2, y1 - 15, text=black_note, font=('Arial', 7), fill='white')

        # Configure scrolling region
        total_width = WHITE_KEY_WIDTH * len(white_notes_sequence)
        self.canvas.config(scrollregion=(0, 0, total_width, WHITE_KEY_HEIGHT))

    def key_pressed(self, event):
        key_path = saved_path
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        clicked = self.canvas.find_overlapping(x, y, x+1, y+1)
        if clicked:
            # Reverse to prioritize topmost (black keys)
            for item_id in reversed(clicked):
                tags = self.canvas.gettags(item_id)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                for t in tags:
                    if t.startswith('black_'):
                        note = t.replace('black_', '')
                        print(f"\033[93m[{current_time}] \033[92mBlack key pressed: \033[94m{note}")
                        self.canvas.itemconfig(item_id, fill=self.theme["highlight_black"])
                        self.canvas.update_idletasks()
                        self.after(150, lambda key=item_id: self.canvas.itemconfig(key, fill=self.theme["black_key"]))
                    elif t.startswith('white_'):
                        note = t.replace('white_', '')
                        print(f"\033[93m[{current_time}] \033[92mWhite key pressed: \033[94m{note}")
                        self.canvas.itemconfig(item_id, fill=self.theme["highlight_white"])
                        self.canvas.update_idletasks()
                        self.after(150, lambda key=item_id: self.canvas.itemconfig(key, fill=self.theme["white_key"]))
                    else:
                        continue

                # Load and play sound
                audio_name = f"{note}{extension}"
                full_path = os.path.join(key_path, audio_name)
                try:
                    data, samplerate = sf.read(full_path)
                    sd.play(data, samplerate)
                except Exception as e:
                    print(f"Error playing {full_path}: {e}")
                return



def get_taskbar_height():
    # Constants
    ABM_GETTASKBARPOS = 5

    class RECT(ctypes.Structure):
        _fields_ = [('left', wintypes.LONG),
                    ('top', wintypes.LONG),
                    ('right', wintypes.LONG),
                    ('bottom', wintypes.LONG)]

    class APPBARDATA(ctypes.Structure):
        _fields_ = [('cbSize', wintypes.DWORD),
                    ('hWnd', wintypes.HWND),
                    ('uCallbackMessage', wintypes.UINT),
                    ('uEdge', wintypes.UINT),
                    ('rc', RECT),
                    ('lParam', wintypes.LPARAM)]

    appbar = APPBARDATA()
    appbar.cbSize = ctypes.sizeof(APPBARDATA)

    result = ctypes.windll.shell32.SHAppBarMessage(ABM_GETTASKBARPOS, ctypes.byref(appbar))
    if result:
        rect = appbar.rc
        height = rect.bottom - rect.top
        width = rect.right - rect.left

        # Taskbar position can be any edge, let's check if taskbar is at bottom:
        # uEdge: 0=left, 1=top, 2=right, 3=bottom
        if appbar.uEdge == 3:  # bottom
            return height
        elif appbar.uEdge == 1:  # top
            return height
        elif appbar.uEdge in (0, 2):  # left or right taskbar (vertical)
            return width
    return 40  # fallback height

def keyboard():
    global root
    clear_screen()
    # main()
    # extract()
    root = tk.Tk()
    root.lift()
    root.title("Full 88-Key Piano")
    root.resizable(False,False)
    # root.overrideredirect(True)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_height = 200
    taskbar_height = get_taskbar_height()
    y_position = screen_height - window_height - taskbar_height
    root.geometry(f"{screen_width}x{window_height}+0+{y_position}")
    piano = Piano88(root)
    piano.pack(fill='both', expand=True)
    root.mainloop()

def about():
    clear_screen()
    print("\033[92m")
    print("""
About:
------

Virtual Piano App v1.0.0
Developed by Orion Vale

This virtual piano lets you play and record music on your computer or device.
It supports 88 keys, customizable themes, and audio playback with high-quality sound.

Features:
- Realistic piano keyboard with velocity-sensitive keys
- Custom color themes to suit your style
- Save and load your compositions from text-based note files
- Cross-platform support (Windows, macOS, Linux)

Thank you for using this app! Your feedback and support are appreciated.


© 2025 Orion Vale
""")
    input("\033[93mPress Enter to continue... \033[0m")


def license():
    clear_screen()
    print("\033[92m")
    print("""
License:
--------

MIT License

Copyright (c) 2025 Orion Vale

Permission is hereby granted, free of charge, to any person obtaining a copy  
of this software and associated documentation files (the "Software"), to deal  
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all  
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  
SOFTWARE.
""")
    unused_var = input("\033[93mEnter any key to continue... ")

def load_theme(name="default"):
    json_path = "E:\\Music\\personalization_database\\theme.json"
    with open(json_path, "r") as f:
        themes = json.load(f)
    global global_theme
    global_theme = themes.get(name, themes["default"])  # fallback to default
    
    # Return the colors from the loaded theme
    return {
        "white_key": global_theme.get("white_key", "white"),
        "black_key": global_theme.get("black_key", "black"),
        "highlight_white": global_theme.get("highlight_white", "#ddd"),
        "highlight_black": global_theme.get("highlight_black", "#444")
    }

# line 389
def find_def_key():
    global saved_path
    global extension
    path_to_save = "E:\\Music\\personalization_database\\user_choice.txt"
    try:
        with open(path_to_save, "r") as f:
            saved_path = f.read()
        print(f"\033[94m[+] Saved path: {saved_path}")
    except FileNotFoundError:
        print("\033[91m[!] No saved path found.")
    except Exception as e:
        print(f"\033[91m[!] Error reading saved path: {e}")
    try:
        if saved_path == "E:\Music\database_new":
            extension = ".mp3"
        elif saved_path == "E:\Music\Keys\output_wavs":
            extension = ".wav"
    except Exception as e:
        print("\033[91m[!] ", e)

GITHUB_USER = "your-username"
REPO_NAME = "your-repo"
LOCAL_VERSION = "1.0.0"

def get_latest_release_tag():
    url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["tag_name"]
    else:
        print("Error fetching release info.")
        return None

def check_for_updates():
    latest_version = get_latest_release_tag()
    if latest_version:
        if latest_version != LOCAL_VERSION:
            print(f"🔔 New version available: {latest_version} (You have {LOCAL_VERSION})")
        else:
            print("✅ You're up to date.")
    else:
        print("Could not fetch latest version.")

if __name__ == "__main__":
    find_def_key()
    load_theme()
    # print(global_theme)
    while True:
        main_menu()
