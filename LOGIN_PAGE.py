import customtkinter as ctk
import os
import subprocess

def get_pos(e):
    print(f"x:{e.x} y:{e.y}")

def close(e):
    login_screen.destroy()

def open_login_screen():
    global login_screen, user_entry, pass_entry, error_label 
    if 'sign_window' in globals():
        sign_window.destroy() 

    ctk.set_appearance_mode("Dark")
    login_screen = ctk.CTk()
    login_screen.geometry("800x400")
    login_screen.title("Login")

    D_W = login_screen.winfo_screenwidth()
    D_H = login_screen.winfo_screenheight()
    x = (D_W // 2) - (800 // 2)
    y = (D_H // 2) - (400 // 2)
    login_screen.geometry(f"800x400+{x}+{y}")

    login_label = ctk.CTkLabel(login_screen, text="LOGIN PAGE", 
                               font=("AMCAP Eternal", 50))
    login_label.pack(pady=5)

    user_label = ctk.CTkLabel(login_screen, text="USERNAME:",
                               font=("AMCAP Eternal", 30))
    user_label.place(x=154, y=133)
    user_entry = ctk.CTkEntry(login_screen, width=300, height=35,
                               font=("Bahnschrift SemiBold Condensed", 20))
    user_entry.place(x=360, y=133)

    pass_label = ctk.CTkLabel(login_screen, text="PASSWORD:",
                               font=("AMCAP Eternal", 30))
    pass_label.place(x=154, y=200)
    pass_entry = ctk.CTkEntry(login_screen, width=300, height=35, 
                    font=("Bahnschrift SemiBold Condensed", 20), show='*')
    pass_entry.place(x=360, y=200)

    Enter_button = ctk.CTkButton(login_screen, text="ENTER", 
                                 font=("AMCAP Eternal", 30), command=enter)
    Enter_button.place(x=336, y=286)

    sign_button = ctk.CTkButton(login_screen, text="SIGN UP", 
                                font=("AMCAP Eternal", 20), command=sign_up)
    sign_button.place(x=649, y=5)

    error_label = ctk.CTkLabel(login_screen, text="", 
            font=("Bahnschrift SemiBold Condensed", 20), text_color="red")
    error_label.place(x=269, y=343)

    login_screen.bind("<Escape>", close)
    login_screen.bind("<Return>", enter)

    login_screen.mainloop()

def sign_up():
    def post_sign():
        username = signup_user_entry.get()
        password = signup_pass_entry.get()
        name = signup_name_entry.get()
        if not username or not password or not name:
            print("Error!!!")
        else:
            enter_to_file = f"{str(username)}~{str(password)}~{str(name)}"
            with open(r"IDs\LOGIN_INFO.txt", "a+") as f:
                f.write("\n" + enter_to_file)
            print("SUCCESFULLY SIGNED UP")
            subprocess.Popen(['python', 'web scraping trials_FUNCTION.py'])
            with open("IDs/PRESENT_USER.txt", "a+") as f:
                f.write("\n" + name)

    if 'login_screen' in globals():
        login_screen.destroy()  

    global sign_window, signup_user_entry, signup_pass_entry
    global signup_name_entry, signup_Enter_button
    ctk.set_appearance_mode("Dark")
    sign_window = ctk.CTk()
    sign_window.geometry(f"800x400+320+250")
    sign_window.title("Sign Up")

    signup_login_label = ctk.CTkLabel(sign_window, text="SIGNUP PAGE",
                                       font=("AMCAP Eternal", 50))
    signup_login_label.pack(pady=5)

    signup_user_label = ctk.CTkLabel(sign_window, text="USERNAME:",
                                     font=("AMCAP Eternal", 30))
    signup_user_label.place(x=154, y=100)
    signup_user_entry = ctk.CTkEntry(sign_window, width=300, height=35, 
                                     font=("Bahnschrift SemiBold Condensed", 20))
    signup_user_entry.place(x=360, y=100)

    signup_pass_label = ctk.CTkLabel(sign_window, text="PASSWORD:",
                                      font=("AMCAP Eternal", 30))
    signup_pass_label.place(x=154, y=157)
    signup_pass_entry = ctk.CTkEntry(sign_window, width=300, height=35,
                            font=("Bahnschrift SemiBold Condensed", 20), show='*')
    signup_pass_entry.place(x=360, y=157)

    signup_name_label = ctk.CTkLabel(sign_window, text="NAME:", 
                                    font=("AMCAP Eternal", 30))
    signup_name_label.place(x=154, y=214)
    signup_name_entry = ctk.CTkEntry(sign_window, width=300, height=35,
                            font=("Bahnschrift SemiBold Condensed", 20),
                              placeholder_text="what do you want to be called...")
    signup_name_entry.place(x=360, y=214)

    signup_Enter_button = ctk.CTkButton(sign_window, text="ENTER", 
                                        font=("AMCAP Eternal", 30), command=post_sign)
    signup_Enter_button.place(x=336, y=286)

    back_button = ctk.CTkButton(sign_window, text="BACK", font=("AMCAP Eternal", 20),
                                 command=open_login_screen)
    back_button.place(x=20, y=20)

    sign_window.bind("<Escape>", lambda e: sign_window.destroy())
    sign_window.mainloop()

def enter(event=None):
    global col
    user_check = user_entry.get()
    pass_check = pass_entry.get()
    print(f"user: {user_check}    , password: {pass_check}")

    if not os.path.exists("IDs/LOGIN_INFO.txt"):
        print("Login info file not found.")
        return
    elif not user_check or not pass_check:
        print("Error!!! username or password not entered")
    else:
        with open("IDs/LOGIN_INFO.txt", "r") as f:
            total_data = f.readlines()
            found = False
            for indi_data in total_data:
                indi_list = indi_data.strip().split("~")
                if indi_list[0] == user_check and indi_list[1] == pass_check:
                    found = True
                    name = indi_list[2]
                    print(f"Welcome, {name}!")
                    subprocess.Popen(['python', 'web scraping trials_FUNCTION.py'])
                    with open("IDs/PRESENT_USER.txt", "a+") as f:
                        f.write("\n" + name)
                    break
            if not found:
                if col:
                    colour="red"
                    col=False
                else:
                    colour="blue"
                    col=True
                error_label.configure(text="Login failed: Invalid username or password",
                                      text_color=colour)
col=True
open_login_screen()











