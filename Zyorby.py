import os
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import shutil
import webbrowser

# Global variables to store directories
fivem_directory = ""
gta_directory = ""

def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

def show_error_page(error_message):
    error_window = tk.Tk()
    error_window.title("Error")
    error_window.geometry("400x200")

    # Dark mode colors
    background_color = "#121212"
    text_color = "#FFFFFF"

    # Configure the main window background
    error_window.configure(bg=background_color)

    label = tk.Label(error_window, text=error_message, font=("Impact", 12), fg=text_color, bg=background_color)
    label.pack(pady=20)

    button = tk.Button(error_window, text="Exit", command=error_window.destroy, fg=text_color, bg=background_color)
    button.pack(pady=10)

    error_window.mainloop()

def check_directories():
    # Look for the FiveM directory
    user_dir = os.environ['USERPROFILE']
    fivem_dir = os.path.join("AppData", "Local", "FiveM", "FiveM.app")
    fivem_directory = os.path.join(user_dir, fivem_dir)

    # Initialize Tkinter window for messages
    message_window = tk.Tk()
    message_window.title("Checking Directories")
    message_window.geometry("400x200")

    # Dark mode colors
    background_color = "#121212"
    text_color = "#FFFFFF"

    # Configure the main window
    message_window.configure(bg=background_color)

    # Text widget to display messages
    message_text = tk.Text(message_window, wrap="word", height=10, width=40, fg=text_color, bg=background_color)
    message_text.pack(pady=20)

    def display_message(message):
        message_text.insert(tk.END, message + "\n")
        message_text.yview(tk.END)

    def ask_directory():
        directory = filedialog.askdirectory()
        if not directory:
            display_message("User canceled. Shutting down the program.")
            message_window.destroy()
            sys.exit()
        display_message(f"Directory has been found: {directory}")
        return directory

    # Check and display messages for FiveM directory
    if os.path.exists(fivem_directory):
        display_message("FiveM folder has been found!")
    else:
        display_message("FiveM folder not found")
        display_message("You will be prompted to find your FiveM directory")
        fivem_directory = ask_directory()
            
    # Look for the GTA directory
    gta_dir = os.path.join("C:", "Program Files (x86)", "Steam", "steamapps", "common", "Grand Theft Auto V")

    # Check and display messages for GTA directory
    if os.path.exists(gta_dir):
        display_message("GTA 5 folder found!")
    else:
        display_message("GTA 5 folder not found :( ")
        display_message("Please locate your GTA 5 directory!")
        gta_dir = ask_directory()

    # Close the Tkinter window
    message_window.destroy()

    return fivem_directory, gta_dir

def uac_check():
    if isAdmin():
        return True
    else:
        show_error_page("Please exit and run the program as administrator.")
        sys.exit()

def setup_directories():
    global fivem_directory, gta_directory
    fivem_directory, gta_directory = check_directories()

def cache_cleaner(fivem_directory):
    decision = messagebox.askquestion("Clear Cache", "Are you sure you want to clear your cache?")
    decision = decision.upper()
    if decision == "YES":
        cache_path = os.path.join(fivem_directory, "data")
        if os.path.exists(cache_path):
            shutil.rmtree(cache_path)
            messagebox.showinfo("Cache Cleaned", "Cache cleaned successfully!")
        else:
            messagebox.showerror("Error", "Could not find the FiveM data folder.\nCurrent directory: " + str(fivem_directory))
    elif decision == "NO":
        pass
    else:
         messagebox.showerror("Error", f"{decision} is not a valid option. Please try again.")


def citizen_cleaner(fivem_directory):
    decision = messagebox.askquestion("Clear Citizen Folder", "Are you sure you want to clear the Citizen folder?")
    decision = decision.upper()
    if decision == "YES":
        citizen_path = os.path.join(fivem_directory, "citizen")
        if os.path.exists(citizen_path):
            shutil.rmtree(citizen_path)
            messagebox.showinfo("Citizen Folder Cleared", "Citizen folder cleared successfully!")
        else:
            messagebox.showerror("Error", "Could not find the Citizen folder.\nCurrent directory: " + str(fivem_directory))
    elif decision == "NO":
        pass
    else:
        messagebox.showerror("Error", f"{decision} is not a valid option. Please try again.")

def enb_cleaner(gta_directory):
    # List of ENB-related files and folders to be removed
    enb_items = [
        "enbseries",
        "readme_en.txt",
        "license_en.txt",
        "enblightsprite.fx",
        "enblens.fx",
        "enbeffectprepass.fx",
        "enbeffectpostpass.fx",
        "enbeffect.fx",
        "enbbloom.fx",
        "enbseries.ini",
        "enblocal.ini",
        "d3dcompiler_46e.dll",
        "d3d11.dll"
    ]

    decision = messagebox.askquestion("Clear ENB Files", "Are you sure you want to remove ENB files?")
    decision = decision.upper()

    if decision == "YES":
        for item in enb_items:
            item_path = os.path.join(gta_directory, item)

            if os.path.exists(item_path):
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                elif os.path.isfile(item_path):
                    os.remove(item_path)
                messagebox.showinfo("ENB Files Removed", "ENB files removed successfully!")
            else:
                messagebox.showwarning("File Not Found", f"{item} not found in the GTA V directory.")

        
    elif decision == "NO":
        pass
    else:
        messagebox.showerror("Error", f"{decision} is not a valid option. Please try again.")

def reshade_cleaner(gta_directory):
    decision = messagebox.askquestion("Clear Reshade", "Are you sure you want to clean Reshade files?")
    decision = decision.upper()

    if decision == "YES":
        files_to_clean = [
            "D3D8.DLL", "D3D9.DLL", "D3D10.DLL", "D3D11.DLL", "OPENGL.DLL",
            "DXGI.DLL", "D3D9.INI", "D3D10.INI", "D3D11.INI", "OPENGL.INI",
            "DXGI.INI", "reshade-shaders"
        ]

        try:
            for file_or_folder in files_to_clean:
                path = os.path.join(gta_directory, file_or_folder)

                if os.path.exists(path):
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                    messagebox.showinfo("Cleaned Successfully", f"{file_or_folder} has been cleaned successfully!")
                else:
                    messagebox.showwarning("File Not Found", f"{file_or_folder} not found in the GTA V directory.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    elif decision == "NO":
        pass
    else:
        messagebox.showerror("Error", f"{decision} is not a valid option. Please try again.")

def fivem_uninstall(fivem_directory):
    # First confirmation
    confirm = messagebox.askyesno("Confirm Uninstall", "Are you sure you want to uninstall FiveM?")

    if confirm:
        # Second confirmation
        really_confirm = messagebox.askyesno("Really Confirm", "Are you really, really sure? This action is irreversible.")

        if really_confirm:
            # Uninstall
                # Check if the path ends with 'FiveM.app' and modify accordingly
                if fivem_directory.endswith('FiveM.app'):
                    parent_directory = os.path.dirname(fivem_directory)
                else:
                    parent_directory = fivem_directory

                shutil.rmtree(parent_directory)
                messagebox.showinfo("Uninstall Successful", "FiveM has been successfully uninstalled.")
        else:
            messagebox.showinfo("Uninstall Canceled", "FiveM uninstallation has been canceled.")
    else:
        messagebox.showinfo("Uninstall Canceled", "FiveM uninstallation has been canceled.")

def fivem_page():
    fivem_window = tk.Tk()
    fivem_window.title("Zyorby Cleaner // FiveM Page")
    fivem_window.geometry("400x400+100+50")
    fivem_window.configure(bg="#121212")

    text_color = "#FFFFFF"

    title_label = tk.Label(fivem_window, text="Zyorby Cleaner V3", font=("Impact", 16), fg=text_color, bg="#121212")
    title_label.grid(row=0, column=0, columnspan=3, pady=20, sticky="n")

    button_cache = tk.Button(fivem_window, text="Cache Cleaner", command=lambda: cache_cleaner(fivem_directory), fg=text_color, bg="#363636", height=1)
    button_cache.grid(row=1, column=0, padx=20, pady=50, sticky="nsew")

    button_citizen = tk.Button(fivem_window, text="Citizen Cleaner", command=lambda: citizen_cleaner(fivem_directory), fg=text_color, bg="#363636",height=1)
    button_citizen.grid(row=1, column=1, padx=20, pady=50, sticky="nsew")

    button_enb = tk.Button(fivem_window, text="ENB Cleaner", command=lambda: enb_cleaner(gta_directory), fg=text_color, bg="#363636", height=1)
    button_enb.grid(row=1, column=2, padx=20, pady=50, sticky="nsew")

    button_reshade = tk.Button(fivem_window, text="Reshade Cleaner", command=lambda: reshade_cleaner(gta_directory), fg=text_color, bg="#363636", height=1)
    button_reshade.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

    button_uninstall = tk.Button(fivem_window, text="FiveM Uninstall", command=lambda: fivem_uninstall(fivem_directory), fg=text_color, bg="#363636", height=1)
    button_uninstall.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")

    button_home = tk.Button(fivem_window, text="Home", command=fivem_window.destroy, fg=text_color, bg="#363636", height=1)
    button_home.grid(row=2, column=2, padx=20, pady=20, sticky="nsew")

    fivem_window.grid_rowconfigure(0, weight=1)
    fivem_window.grid_rowconfigure(1, weight=1)
    fivem_window.grid_rowconfigure(2, weight=1)
    fivem_window.grid_columnconfigure(0, weight=1)
    fivem_window.grid_columnconfigure(1, weight=1)
    fivem_window.grid_columnconfigure(2, weight=1)

    fivem_window.mainloop()

def clean_temp_folders():
    try:
        temp_folder = os.path.join(os.environ['TEMP'])
        shutil.rmtree(temp_folder, ignore_errors=True)
        messagebox.showinfo("Cleanup Successful", "Temporary folders cleaned successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def clean_recycle_bin():
    try:
        # SHFileOperation requires absolute paths
        recycle_bin = ctypes.windll.shell32.SHBrowseForFolderW(0, 0, 0, 0)
        ctypes.windll.shell32.SHEmptyRecycleBinW(recycle_bin, 0, 0)
        messagebox.showinfo("Cleanup Successful", "Recycle bin cleaned successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def windows_page():
    windows_window = tk.Tk()
    windows_window.title("Zyorby Cleaner // Windows Page")
    windows_window.geometry("400x400+1400+50")
    windows_window.configure(bg="#121212")

    label = tk.Label(windows_window, text="Zyorby Cleaner V3", font=("Impact", 14), fg="#FFFFFF", bg="#121212")
    label.pack(pady=20)

    button_clean_temp = tk.Button(windows_window, text="Clean Temporary Folders", command=clean_temp_folders, fg="#FFFFFF", bg="#363636")
    button_clean_temp.pack(pady=10)

    button_clean_recycle_bin = tk.Button(windows_window, text="Clean Recycle Bin", command=clean_recycle_bin, fg="#FFFFFF", bg="#363636")
    button_clean_recycle_bin.pack(pady=10)

    button_back = tk.Button(windows_window, text="Back to Home", command=windows_window.destroy, fg="#FFFFFF", bg="#363636")
    button_back.pack(pady=10)

    windows_window.mainloop()


def apps_page():
    apps_window = tk.Tk()
    apps_window.title("Zyorby Cleaner // install apps page")
    apps_window.geometry("400x400+100+500")
    apps_window.configure(bg="#121212")

    label = tk.Label(apps_window, text="This is the Install Apps Page", font=("Impact", 14), fg="#FFFFFF", bg="#121212")
    label.pack(pady=20)

    button_back = tk.Button(apps_window, text="Back to Home", command=apps_window.destroy, fg="#FFFFFF", bg="#363636")
    button_back.pack(pady=10)

    apps_window.mainloop()

def open_youtube():
    webbrowser.open("https://www.youtube.com/Zyorby")

def open_discord():
    webbrowser.open("https://discord.gg/Zyorby")

def credits_page():
    credits_window = tk.Tk()
    credits_window.title("Zyorby Cleaner // Credits Page")
    credits_window.geometry("400x400+1400+500")
    credits_window.configure(bg="#121212")

    label = tk.Label(credits_window, text="Zyorby Cleaner V3", font=("Impact", 14), fg="#FFFFFF", bg="#121212")
    label.pack(pady=20)

    button_youtube = tk.Button(credits_window, text="YouTube", command=open_youtube, fg="#FFFFFF", bg="#363636")
    button_youtube.pack(pady=10)

    button_discord = tk.Button(credits_window, text="Discord", command=open_discord, fg="#FFFFFF", bg="#363636")
    button_discord.pack(pady=10)

    button_back = tk.Button(credits_window, text="Back to Home", command=credits_window.destroy, fg="#FFFFFF", bg="#363636")
    button_back.pack(pady=10)

    credits_window.mainloop()


def home_page():

    home_window = tk.Tk()
    home_window.title("Zyorby Cleaner // Home Page")
    home_window.geometry("500x500+720+260")

    # Dark mode colors
    background_color = "#121212"
    text_color = "#FFFFFF"

    # Configure the main window background color
    home_window.configure(bg=background_color)

    title_label = tk.Label(home_window, text="Zyorby Cleaner V3", font=("Impact", 20), fg=text_color, bg=background_color)
    title_label.grid(row=0, column=1, columnspan=2, pady=20, sticky="n")  # Use columnspan to span across both columns

    button_fivem = tk.Button(home_window, text="Fivem", command=fivem_page, fg=text_color, bg="#363636")
    button_fivem.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    button_gta = tk.Button(home_window, text="Windows", command=windows_page, fg=text_color, bg="#363636")
    button_gta.grid(row=1, column=2, padx=20, pady=20, sticky="nsew")

    button_apps = tk.Button(home_window, text="Install Apps", command=apps_page, fg=text_color, bg="#363636")
    button_apps.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")

    button_credits = tk.Button(home_window, text="Credits", command=credits_page, fg=text_color, bg="#363636")
    button_credits.grid(row=2, column=2, padx=20, pady=20, sticky="nsew")

    button_exit = tk.Button(home_window, text="Exit", command=home_window.destroy, fg="red", bg="#363636")
    button_exit.grid(row=3, column=1, pady=20, padx=20, sticky="nsew")

    # Center the grid
    home_window.grid_rowconfigure(0, weight=1)
    home_window.grid_columnconfigure(1, weight=1)
    home_window.grid_columnconfigure(2, weight=1)

    home_window.mainloop()

# UAC check
uac_check()

setup_directories()

# Proceed to the home page if UAC check passes
home_page()
