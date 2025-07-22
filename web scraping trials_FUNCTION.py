import subprocess
from sys import executable
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter as ctk
from bs4 import BeautifulSoup
import requests
import re
import pyperclip
import os
import pyttsx3
import threading
from datetime import datetime
import matplotlib.pyplot as plt

# Function to install libraries
def install_libraries():
    libraries = {"beautifulsoup4": "bs4",
                "requests": "requests",
                "pyperclip": "pyperclip",
                "customtkinter": "customtkinter"}
    for lib, pip_name in libraries.items():
        try:
            __import__(lib)
        except ImportError:
            print(f"{lib} module isn't installed on your PC...")
            print(f"Installing {lib}...\n\n")
            subprocess.run([executable, "-m", "pip", "install", pip_name],
                           check=True)
# install_libraries() 

try:
    import pyperclip
except ImportError:
    subprocess.Popen([executable, "-m", "pip", "install", "pyperclip"])

try:
    import requests
except ImportError:
    subprocess.Popen([executable, "-m", "pip", "install", "requests"])

try:
    from bs4 import BeautifulSoup
except ImportError:
    subprocess.Popen([executable, "-m", "pip", "install", "bs4"])

try:
    from datetime import datetime
except ImportError:
    subprocess.Popen([executable, "-m", "pip", "install", "datetime"])

try:
    import customtkinter
except ImportError:
    subprocess.Popen([executable, "-m", "pip", "install", "customtkinter"])

def name():
    with open("IDs/PRESENT_USER.txt","r") as f:
        name_of_user=f.readlines()[-1] 
        return name_of_user

def save_to_file(name, clear=False):
    if check_var.get():
        return 
    else:
        month_dict = {'01': 'JANUARY', '02': 'FEBRUARY', '03': 'MARCH',
                    '04': 'APRIL', '05': 'MAY', '06': 'JUNE',
                    '07': 'JULY', '08': 'AUGUST', '09': 'SEPTEMBER',
                    '10': 'OCTOBER', '11': 'NOVEMBER', '12': 'DECEMBER'}
        now = datetime.now()
        formatted_datetime = now.strftime("%d/%m %H:%M:%S")
        with open("IDs/PRESENT_USER.txt", "r") as f:
            name_of_user = f.readlines()[-1]
            try:
                os.mkdir(f"HISTORY/{name_of_user.upper()}")
            except FileExistsError:
                pass
        with open("HISTORY/PERMANENT_HISTORY.txt", "a+") as f:
            f.write(name + '\t' + formatted_datetime + f"   -{name_of_user}" + '\n')
        
        user_folder = f"HISTORY/{name_of_user.upper()}"
        with open(user_folder + f"/{name_of_user}.txt", "a+") as f:
            f.write(name + '\t' + formatted_datetime + '\n')


# Function to plot PERFORMANCE graph
def performance():
    with open("HISTORY/PERMANENT_HISTORY.txt", 'r') as f:
        lines = f.readlines()
    now = datetime.now()
    lst = [line[-15:-13].strip() for line in lines]
    date_counts = {str(i): lst.count(f"{i:02d}") for i in range(1, 32)}
    x_axis = list(date_counts.keys())
    y_axis = list(date_counts.values())
    
    plt.figure(figsize=(10, 5))
    for i in range(len(x_axis) - 1):
        x_segment = [x_axis[i], x_axis[i + 1]]
        y_segment = [y_axis[i], y_axis[i + 1]]
        color = 'blue' if y_axis[i + 1] >= y_axis[i] else 'red'
        plt.plot(x_segment, y_segment, color=color)
    
    plt.grid(True)
    plt.ylim(0, max(y_axis) + 1)
    plt.xlabel('DATE')
    plt.ylabel('NUMBER OF SEARCHES')
    plt.show()

# Function to clear history
def clear_history():
    with open('HISTORY/history.txt', 'a+') as f:
        f.truncate(0)
    show_message("HISTORY CLEARED", "#A027E6")

# Function to read history
def read_from_file():
    filename = 'HISTORY/history.txt'
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f.readlines()] 
    except FileNotFoundError:
        return []

# Function to copy summary
def copy_to_clipboard(text):
    pyperclip.copy(text)
    show_message("Text copied to clipboard", "#008080")

def get_pos(event):
    print(f"x: {event.x} y: {event.y}")

# Function to show messages on screen
def show_message(message, bg_color):
    msg_label = ctk.CTkLabel(screen, text=message, 
                             font=("Agency FB", 20), bg_color=bg_color)
    msg_label.place(relx=0.5,rely=0.9,anchor="center")
    screen.after(3000, msg_label.destroy)

# Function to close the main window
def close(e=None):
    screen.destroy()

# Function to toggle full screen mode
def full_screen(e):
    state = not screen.attributes('-fullscreen')
    screen.attributes('-fullscreen', state)

# Function to save the summary
def save_text():
    text = summary_textb.get("1.0", tk.END).strip()
    topic = link.get().title()
    if len(topic) > 0:
        with open(f"SAVE_SUMMARY_TEXT/{topic}.txt", 'a+') as f:
            f.write(text)
    else:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                  initialfile="topic.txt",
                                                 title="Save as")
        if file_path:
            with open(file_path, 'a+') as f:
                f.write(text)

# Summary Function
def get_wikipedia_summary(topic=None):
    vox_button.place(x=4, y=3)
    save_button.place(x=550, y=3)
    if not topic:
        topic = link.get()
    save_to_file(topic)
    search_url = f"https://en.wikipedia.org/wiki/{topic}"
    print(search_url)
    try:
        response = requests.get(search_url, 
                                headers={"User-Agent": "Mozilla/5.0"},
                                verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            sentences_printed = 0
            summary = "\n\n"
            for para in paragraphs:
                text = para.get_text().strip()
                if text and len(text) > 50:
                    if not text.startswith("This article is about"):
                        if not text.startswith("For other uses") and text!="":
                            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s',
                                                  text)
                            for sentence in sentences:
                                if sentences_printed < 10:
                                    summary += (f"{sentences_printed + 1}. {sentence}\n")
                                    sentences_printed += 1
                            if sentences_printed >= 10:
                                break
            if summary:
                summary_textb.delete("1.0", tk.END)
                summary_textb.insert(tk.END, summary)
            else:
                summary_textb.delete("1.0", tk.END)
                summary_textb.insert(tk.END, "\n\nNo suitable content found.")
        else:
            summary_textb.delete("1.0", tk.END)
            summary_textb.insert(tk.END, 
                                 f"\n\nFailed to retrieve page. Status code: {response.status_code}", 
                                 "red")
    except requests.exceptions.RequestException as e:
        summary_textb.delete("1.0", tk.END)
        summary_textb.insert(tk.END, f"\n\nError: {e}", "red")

def settings():
    selected_values = None  

    def close(event=None):
        setting_screen.destroy()

    def enter():
        windowsize_get = combo_box_winsize.get()
        font_get = combo_box_font.get()
        theme_get = combo_box_theme.get()
        return windowsize_get, font_get, theme_get

    setting_screen = ctk.CTk()
    setting_screen.geometry("500x300+500+290")
    setting_screen.title("Settings")

    set_label = ctk.CTkLabel(setting_screen, text="SETTINGS", font=("AMCAP Eternal", 40))
    set_label.place(relx=0.55, rely=0.1, anchor="center")

    win_size1 = ctk.CTkLabel(setting_screen, text="Window ", font=("Arial", 15))
    win_size1.place(relx=0.1, rely=0.23, anchor="center")
    win_size = ctk.CTkLabel(setting_screen, text="size: ", font=("Arial", 15))
    win_size.place(relx=0.1, rely=0.3, anchor="center")

    win_size_lst = ["720x500", "750x530", "700x480"]
    combo_box_winsize = ctk.CTkComboBox(setting_screen, values=win_size_lst)
    combo_box_winsize.place(relx=0.3, rely=0.3, anchor="center")

    font_label = ctk.CTkLabel(setting_screen, text="Font: ", font=("Arial", 15))
    font_label.place(relx=0.1, rely=0.5, anchor="center")

    fonts_lst = ["Bahnschrift Condensed","Arial", "Verdana", "Helvetica", "Times New Roman",
                "Courier New", "Georgia", "Comic Sans MS", "Impact",
                "Trebuchet MS", "Lucida Console", "Tahoma", "Palatino Linotype",
                "Segoe UI", "Arial Black", "Garamond", "Bookman Old Style"]
    combo_box_font = ctk.CTkComboBox(setting_screen, values=fonts_lst)
    combo_box_font.place(relx=0.3, rely=0.5, anchor="center")

    theme_label = ctk.CTkLabel(setting_screen, text="Theme: ", font=("Arial", 15))
    theme_label.place(relx=0.1, rely=0.7, anchor="center")

    theme_lst = ["Dark", "Light", "Blue", "Dark-Blue", "Green",
                "Dark-Green", "Red", "Dark-Red", "Purple",
                "Dark-Purple", "Orange", "Dark-Orange"]
    combo_box_theme = ctk.CTkComboBox(setting_screen, values=theme_lst)
    combo_box_theme.place(relx=0.3, rely=0.7, anchor="center")

    cancel_label = ctk.CTkButton(setting_screen, text="Cancel", font=("Arial", 15), 
                                 width=90, fg_color="grey", command=close)
    cancel_label.place(relx=0.7, rely=0.9, anchor="center")

    apply_label = ctk.CTkButton(setting_screen, text="Apply", font=("Arial", 15), 
                                width=90, command=lambda: set_values_and_close())
    apply_label.place(relx=0.9, rely=0.9, anchor="center")
    # setting_screen.bind("<Enter>",set_values_and_close)

    def set_values_and_close():
        nonlocal selected_values 
        selected_values = enter() 
        if selected_values:
            window_size, font_name, theme_name = selected_values
            ctk.set_appearance_mode(theme_name)
            summary_textb.configure(font=(font_name, 12))  

        setting_screen.destroy()


    setting_screen.bind("<Escape>", close)

    setting_screen.mainloop()
    print("Returned values:", selected_values)
    return selected_values  


def on_press_settings():
    returned_values = settings()
    

# Function to toggle more options frame visibility
def more_options(clear=False):
    global frame_visible, frame, history_frame_visible
    if frame_visible:
        frame.place_forget()
        frame_visible = False
        hide_history_frame()
        history_frame_visible = False
    else:
        frame = ctk.CTkFrame(screen, bg_color="grey")
        frame.place(x=5, y=25)
        his = ctk.CTkButton(frame, text='HISTORY', fg_color='black',
                             command=toggle_history_frame)
        his.pack()
        clear_his = ctk.CTkButton(frame, text='CLEAR HISTORY', fg_color='black',
                                   command=clear_history)
        clear_his.pack()
        per = ctk.CTkButton(frame, text="SEARCH STATS", fg_color='black', 
                            command=performance)
        per.pack()
        manual_btn=ctk.CTkButton(frame,text="MANUAL", fg_color='black',
                                 command=manual)
        manual_btn.pack()
        set = ctk.CTkButton(frame, text='SETTINGS', fg_color='black',
                            command=on_press_settings)
        set.pack()
        frame_visible = True

def manual():
    manual_screen=ctk.CTk()
    manual_screen.geometry(f"800x500+200+100")
    manual_screen.title("Manual")
    mscrollabar=ctk.CTkScrollableFrame(manual_screen,width=500,height=300)
    mscrollabar.pack(expand=True,fill="both")
    with open(r"others\MANUAL.txt","r") as f:
        text_1=f.readlines()
    for i in text_1:
        if i.isupper():
            mlabel = ctk.CTkLabel(mscrollabar, text=i, 
                                  font=("Arial Black", 18, "bold"))
        else:
            mlabel=ctk.CTkLabel(mscrollabar,text=i)
        mlabel.pack()
    manual_screen.mainloop()

engine = pyttsx3.init()
def thread_speech():
    speech_thread = threading.Thread(target=speak)
    speech_thread.start()

def speak():
    text = summary_textb.get("1.0", tk.END).strip()
    f_text = "".join(c for c in text if not c.isdigit())
    engine.say(f_text)
    engine.runAndWait()

# Function to toggle history frame visibility
def toggle_history_frame():
    global history_frame_visible
    if history_frame_visible:
        hide_history_frame()
        history_frame_visible = False
    else:
        show_history_frame()
        history_frame_visible = True

# Function to show history frame
def show_history_frame():
    hover_frame.place(x=146, y=24)
    lst = read_from_file()
    for widget in hover_frame.winfo_children():
        widget.destroy()
    history_buttons.clear()
    if not lst:
        his_singlebutton = ctk.CTkButton(hover_frame,text="No History",
                                         fg_color='black')
        his_singlebutton.pack()
    else:
        namee=name()
        with open(f'HISTORY/{namee.upper()}/{namee}.txt', 'r') as f:
            lines = f.readlines()
            no_of_his = min(len(lines), 10)
            for i in range(1, no_of_his + 1):
                item_wd = lines[-i]
                item = item_wd[0:-15].strip()
                his_singlebutton = ctk.CTkButton(hover_frame,text=item_wd,
                                                fg_color='black')
                his_singlebutton.pack()
                his_singlebutton.bind("<Button-1>", lambda e, 
                            item=item: get_wikipedia_summary(item))
                history_buttons.append(his_singlebutton)

# Function to hide history frame
def hide_history_frame():
    hover_frame.place_forget()


# def on_enter(event):
#     if event.widget in history_buttons or event.widget == frame or event.widget == more_op:
#         show_history_frame()

# def on_leave(event):
#     if event.widget != hover_frame and event.widget not in history_buttons:
#         hide_history_frame()

def incognito_entered():
    if check_var.get():
        show_message("You're on INCOGNITO","#000000")
    else:
        show_message("You logged out of INCOGNITO","#000000")

# Initialize global variables
frame_visible = False
history_frame_visible = False
incognito=False
history_window = None
customization_window = None
TOTAL_LST = []

ctk.set_appearance_mode("Dark")
screen = ctk.CTk()
screen.geometry("720x500+340+150")
screen.title("WEB SCRAPER")

label=ctk.CTkLabel(screen,text="WEB SCRAPER",font=("AMCAP Eternal",30))
label.place(relx=0.5, rely=0.06, anchor="center")

link = ctk.CTkEntry(screen, placeholder_text="Enter Topic..", width=350, 
                    height=30,font=("Bahnschrift Condensed",20))
link.place(relx=0.5,rely=0.15,anchor="center")

submit = ctk.CTkButton(screen, text="Find", font=("Bauhaus 93",20),
                       command=lambda: get_wikipedia_summary(),hover_color="#8E36E6")
submit.place(relx=0.5,rely=0.23,anchor="center")

summary_textb = ctk.CTkTextbox(screen, width=600, height=300,
                               font=("Bahnschrift SemiBold SemiConden",12))
summary_textb.place(relx=0.5,rely=0.57,anchor="center")

more_op = ctk.CTkButton(screen, text="☰", width=5, height=5, hover_color="#2199AB",
                        command=more_options)
more_op.place(relx=0.03, rely=0.01,anchor="ne")

copy_image=Image.open(r"PICS\copy_light.png")
copy_img=ImageTk.PhotoImage(copy_image.resize((20,20),Image.LANCZOS))
copy_button = ctk.CTkButton(screen, compound="left", width=10, height=3, 
                            hover_color="#9901E5",text="", image=copy_img,
            command=lambda: copy_to_clipboard(summary_textb.get("1.0", tk.END).strip()))
copy_button.place(relx=0.88,rely=0.2,anchor="nw")

check_var = ctk.BooleanVar(value=False)
incog = ctk.CTkCheckBox(screen, text="INCOGNITO",font=("Bauhaus 93",20), 
                        variable=check_var, command=incognito_entered)
incog.place(relx=0.89,rely=0.03,anchor="center")

name_label=ctk.CTkLabel(screen,text=f"signed as: {name()}",font=("Comic Sans MS",20))
name_label.place(relx=0.75,rely=0.06,anchor="nw")

speak_image=Image.open(r"PICS\speaker-removebg-preview.png")
photo=ImageTk.PhotoImage(speak_image.resize((20,20),Image.LANCZOS))
vox_button = ctk.CTkButton(summary_textb, text="", image=photo,
                           command=lambda: thread_speech(), width=0.1, height=0.1)

save_button = ctk.CTkButton(summary_textb, text="SAVE", width=7, height=5,
                             command=lambda: save_text())

hover_frame = ctk.CTkFrame(screen, width=200, height=200,fg_color="black")
history_buttons = []

# Bind keyboard shortcuts
screen.bind("<Return>", lambda event: get_wikipedia_summary())
screen.bind("<Escape>", lambda e: close(e))
screen.bind("<F11>", lambda e: full_screen(e))
screen.bind("<Control-v>", lambda e: thread_speech())
screen.bind("<Control-s>", lambda e: save_text())
# screen.bind("<Motion>",get_pos)
  
screen.mainloop()
