"""Generate UUIDs using a Simple GUI"""
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import logging
import re
import os
from unique import Unique
from unique import is_reasonable_quantity
from unique import is_uuid_ns_name
from ulid import Ulid

class Settings:
    """Settings for UUID Generation Class"""
    def __init__(self):
        """Initialise Application Settings Class"""
        logging.debug("Initialise Application Settings Class")
        self.quantity = 1
        self.urn_flag = False
        self.upper_flag = False
        self.short_flag = False
        self.namespace = ""
        self.name = ""
        self.quant_colour = "pale green"
        self.name_colour = ""
        self.filename = ""
        self.title = ""

    def short_fn(self):
        """Return just the short name (instead of whole path) of the current_settings.filename"""
        try:
            shortfilename = re.search(r"[a-zA-Z0-9#! ._\-+\(\)]+?$", self.filename).group()
            #logging.debug("\tRegEx Match: %s", shortfilename)
        except AttributeError:
            shortfilename = ""
        return str(shortfilename)

    def window_title(self):
        """Create or Update the window title using current file name (if applicable)"""
        if self.short_fn() != "":
            title = "Unique: UUID & ULID Generator - " + self.short_fn()
        else:
            title = "Unique: UUID & ULID Generator"

        window.title(title)

    def toggle_uppercase(self):
        """turn on uppercase"""
        if menu_var_upper.get():
            self.upper_flag = 1
            self.short_flag = 0
            self.urn_flag = 0
        else:
            self.upper_flag = 0
        self.__update_toggles()

    def toggle_base64(self):
        """turn on base64"""
        if menu_var_base64.get():
            self.short_flag = 1
            self.upper_flag = 0
            self.urn_flag = 0
        else:
            self.short_flag = 0
        self.__update_toggles()

    def toggle_urn_prefix(self):
        """turn on base64"""
        if menu_var_prefix.get():
            self.urn_flag = 1
            self.short_flag = 0
            self.upper_flag = 0
        else:
            self.urn_flag = 0
        self.__update_toggles()

    def __update_toggles(self):
        menu_var_upper.set(current_settings.upper_flag)
        menu_var_base64.set(current_settings.short_flag)
        menu_var_prefix.set(current_settings.urn_flag)

def about():
    """Display About Message"""
    about_me = ["Unique: The UUID and ULID Generation Tool",
                "MIT Licence",
                "Adam Bonner, 2023",
                "https://github.com/adambonneruk/unique"]
    messagebox.showinfo("About", "\n".join(about_me))

def empty_pta():
    """Empty the plain text area and reset the current filename"""
    plain_text_area.delete('1.0', "end")
    current_settings.filename = ""
    current_settings.window_title()

def file_load():
    """Open file dialog to select a file, then loads file into plain text area"""
    persisted_file = filedialog.askopenfile(defaultextension='.txt',
                                            mode='r',
                                            title='Select your file',
                                            filetypes=[("All Files", ".*"),
                                                       ("UUID Plain Text", ".uuid"),
                                                       ("Text Documents", ".txt")])

    if persisted_file is not None:
        empty_pta()
        text_blob = persisted_file.read()
        plain_text_area.insert('1.0', text_blob)
        persisted_file.close()

        # Saved File Settings
        current_settings.filename = str(persisted_file.name)
        logging.debug("\tFilename: %s", current_settings.filename)

        # Refresh Window Title
        current_settings.window_title()

def file_save_as():
    """Prompt for Save As File Location and Write to the File"""
    logging.debug("----------------")
    logging.debug("File: Save As...")
    logging.debug("\tOpening Save As FileDialog")
    persisted_file = filedialog.asksaveasfile(initialdir="~",
                                              defaultextension='.txt',
                                              mode='w',
                                              title="Save As",
                                              filetypes=[("Text Documents", ".txt"),
                                                         ("UUID Plain Text", ".uuid"),
                                                         ("All Files", ".*")])

    if persisted_file is not None:
        logging.debug("\tSaving...")
        text_blob = plain_text_area.get('1.0', "end"+'-1c')
        persisted_file.write(text_blob)
        persisted_file.close()
        logging.debug("\tSaved")

        # Saved File Settings
        current_settings.filename = str(persisted_file.name)
        logging.debug("\tFilename: %s", current_settings.filename)

        # Refresh Window Title
        current_settings.window_title()

    else:
        logging.debug("\tCancelled")

def file_save():
    """Save to existing file, or Prompt for Save As if no existning file"""
    logging.debug("----------")
    logging.debug("File: Save")

    if current_settings.filename == "":
        logging.debug("\tNo File!, Launch Save As...")
        file_save_as()
    else:
        logging.debug("\tWe have a file: %s", current_settings.filename)

        # Compare text_blob to file contents
        logging.debug("\tCompare text_blob to file contents")
        text_blob = plain_text_area.get('1.0', "end"+'-1c')
        persisted_file = open(current_settings.filename, "r")
        if text_blob == persisted_file.read():
            logging.debug("\tPlain Text Area and File Contents are the Same, No Save")
        else:
            logging.debug("\tPlain Text Area and File Contents are Different, Saving...")
            persisted_file = open(current_settings.filename, "w")
            persisted_file.write(text_blob)
            persisted_file.close()
            logging.debug("\t...Saved")

def file_new():
    """Display are you sure message before emptying window"""
    logging.debug("---------\nFile: New")
    if current_settings.filename != "":
        logging.debug("\twe have an existing savefile")
        text_blob = plain_text_area.get('1.0', "end"+'-1c')
        persisted_file = open(current_settings.filename, "r")
        if text_blob != persisted_file.read():
            logging.debug("\tthere are changes")

            message = "Save changes to " + current_settings.short_fn() + "?"
            quit_ask = messagebox.askyesnocancel(current_settings.short_fn(), message)

            if quit_ask: #Yes
                logging.debug("\tOption: Save & New")
                empty_pta()

            elif quit_ask is None: #Cancel
                logging.debug("\tOption: Cancel")
            else: #No
                logging.debug("\tOption: New")
                empty_pta()

        else: #theres no changes
            logging.debug("\tthere are no changes")
            empty_pta()

    else:
        logging.debug("\twe don't have an existing savefile")
        text_blob = plain_text_area.get('1.0', "end"+'-1c')
        if text_blob != "": #plain text is not empty
            quit_ask = messagebox.askyesnocancel("Untitled", "Save changes to \"Untitled\"?")
            if quit_ask: #Yes
                logging.debug("\tOption: Save & New")
                file_save()
                empty_pta()
            elif quit_ask is None: #Cancel
                logging.debug("\tOption: Cancel")
            else: #No
                logging.debug("\tOption: New")
                empty_pta()
        else: #no file, and no text area contents
            logging.debug("\tNo content in the \"Plain Text Area\" detected, Do Nothing")

def file_open(): #ctrl o
    """Display are you sure message before opening file, then load the new file in"""
    logging.debug("----------\nFile: Open")
    if current_settings.filename != "":
        logging.debug("\twe have an existing savefile")
        text_blob = plain_text_area.get('1.0', "end"+'-1c')
        persisted_file = open(current_settings.filename, "r")
        if text_blob != persisted_file.read():
            logging.debug("\tthere are changes")

            message = "Save changes to " + current_settings.short_fn() + "?"
            quit_ask = messagebox.askyesnocancel(current_settings.short_fn(), message)

            if quit_ask: #Yes
                logging.debug("\tOption: Save & Open")
                file_save()
                file_load()

            elif quit_ask is None: #Cancel
                logging.debug("\tOption: Cancel")
            else: #No
                logging.debug("\tOption: Just Open")
                file_load()

        else: #theres no changes
            logging.debug("\tthere are no changes")
            file_load()

    else:
        logging.debug("\twe don't have an existing savefile")
        text_blob = plain_text_area.get('1.0', "end"+'-1c')
        if text_blob != "": #plain text is not empty
            quit_ask = messagebox.askyesnocancel("Untitled", "Save changes to \"Untitled\"?")
            if quit_ask: #Yes
                logging.debug("\tOption: Save & Open")
                file_save()
                file_load()
            elif quit_ask is None: #Cancel
                logging.debug("\tOption: Cancel")
            else: #No
                logging.debug("\tOption: Just Open")
                file_load()
        else: #no file, and no text area contents
            logging.debug("\tNo content in the \"Plain Text Area\" detected, Just Open")
            file_load()

    return "break" #fix for default ctrl + o binding

def add_uuids_to_pta(version):
    """Append a new UUID(s) to the Plain Text Area"""
    logging.debug("---------------------------------------------")
    logging.debug("Append a new UUID(s) to the \"Plain Text Area\"")

    #Settings
    logging.debug("Version: %s", str(version))
    if version == 3 or version == 5:
        logging.debug("\tNamespace:%s", str(current_settings.namespace).upper())
        logging.debug("\tName: %s", str(current_settings.name))
        if not is_uuid_ns_name(current_settings.namespace, current_settings.name):
            options_popup()
            return
    logging.debug("Quantity: %s", str(current_settings.quantity))
    logging.debug("URN Prefix?: %s", str(current_settings.urn_flag))
    logging.debug("Uppercase?: %s", str(current_settings.upper_flag))
    logging.debug("Base64?: %s", str(current_settings.short_flag))

    for _ in range(0, current_settings.quantity):
        # Generate a UUID
        logging.debug("Generate a UUID:")
        myuuid = Unique(version,
                        current_settings.namespace,
                        current_settings.name)

        if current_settings.upper_flag:
            generated_uuid = myuuid.upper()
        elif current_settings.urn_flag:
            generated_uuid = myuuid.prefix()
        elif current_settings.short_flag:
            generated_uuid = myuuid.encode()
        else:
            generated_uuid = myuuid

        logging.debug(generated_uuid)

        # Get contents of "Plain Text Area" as text_blob
        logging.debug("Get contents of \"Plain Text Area\" as text_blob")
        text_blob = plain_text_area.get('1.0', "end"+'-1c')

        #If the "Plain Text Area" isn't Empty, Newline Required
        if text_blob != "":
            logging.debug("\"Plain Text Area\" isn't Empty, Newline Required")
            plain_text_area.insert("end", "\n")

        # Insert text_blob into Plain Text Area with new UUID
        logging.debug("Insert UUID at \"end\" of plain_text_area")
        plain_text_area.insert("end", generated_uuid)

def add_ulids_to_pta():
    """Append a new ULID(s) to the Plain Text Area"""
    logging.debug("---------------------------------------------")
    logging.debug("Append a new ULID(s) to the \"Plain Text Area\"")

    for _ in range(0, current_settings.quantity):
        # Generate a ULID
        logging.debug("Generate a ULID:")
        my_ulid = Ulid()

        logging.debug(my_ulid)

        # Get contents of "Plain Text Area" as text_blob
        logging.debug("Get contents of \"Plain Text Area\" as text_blob")
        text_blob = plain_text_area.get('1.0', "end"+'-1c')

        # If the "Plain Text Area" isn't Empty, Newline Required
        if text_blob != "":
            logging.debug("\"Plain Text Area\" isn't Empty, Newline Required")
            plain_text_area.insert("end", "\n")

        # Insert text_blob into Plain Text Area with new ULID
        logging.debug("Insert ULID at \"end\" of plain_text_area")
        plain_text_area.insert("end", my_ulid)

def exit_are_you_sure():
    """Display exit message before destorying window"""
    logging.debug("----\nExit")
    if current_settings.filename != "":
        logging.debug("\twe have an existing savefile")
        text_blob = plain_text_area.get('1.0', "end"+'-1c')
        persisted_file = open(current_settings.filename, "r")
        if text_blob != persisted_file.read():
            logging.debug("\tthere are changes")

            message = "Save changes to " + current_settings.short_fn() + "?"
            quit_ask = messagebox.askyesnocancel(current_settings.short_fn(), message)

            if quit_ask: #Yes
                logging.debug("\tOption: Save & Quit")
                file_save()
                window.destroy()
            elif quit_ask is None: #Cancel
                logging.debug("\tOption: Cancel")
            else: #No
                logging.debug("\tOption: Quit")
                window.destroy()

        else: #theres no changes
            logging.debug("\tthere are no changes")
            window.destroy()

    else:
        logging.debug("\twe don't have an existing savefile")
        text_blob = plain_text_area.get('1.0', "end"+'-1c')
        if text_blob != "": #plain text is not empty
            quit_ask = messagebox.askyesnocancel("Quit", "Save changes to \"Untitled\"?")
            if quit_ask: #Yes
                logging.debug("\tOption: Save & Quit")
                file_save()
                window.destroy()
            elif quit_ask is None: #Cancel
                logging.debug("\tOption: Cancel")
            else: #No
                logging.debug("\tOption: Quit")
                window.destroy()
        else: #no file, and no text area contents
            window.destroy()

def options_popup():
    """Create a Small Popup Window to Set Application Options"""
    logging.debug("------------------------------------------------------")
    logging.debug("Create a Small Popup Window to Set Application Options")
    popup = tk.Toplevel(window)
    popup.transient(window)
    popup.title("Options")
    popup.geometry("204x153+150+150")
    popup.iconbitmap(os.path.join(basedir, "icon/unique.ico"))

    logging.debug("Create Quantity Entry Box")
    quant_var = tk.StringVar()

    # Log current_settings.quantity
    logging.debug("Original Quantity: %s", str(current_settings.quantity))
    quant_var.set(str(current_settings.quantity))
    current_settings.quant_colour = "pale green"

    #Create Entry Box with current colour
    quant = tk.Entry(popup, width=20, textvariable=quant_var, bg=current_settings.quant_colour)
    tk.Label(popup, text="Quantity").grid(sticky="w", pady=5, padx=2, row=0, column=0)
    quant.grid(row=0, column=1, pady=12, columnspan=2)

    name_var = tk.StringVar()

    # Log current_settings.name
    logging.debug("Original Name: %s", str(current_settings.name))
    name_var.set(str(current_settings.name))
    current_settings.name_colour = "white"

    #Create Entry Box with current colour
    name = tk.Entry(popup, width=20, textvariable=name_var, bg=current_settings.name_colour)
    tk.Label(popup, text="Name").grid(sticky="w", pady=5, padx=2, row=2, column=0)
    name.grid(row=2, column=1, pady=12, columnspan=2)

    namespaces_var = tk.StringVar()
    namespaces = {"dns", "url", "oid", "x500"}

    # Set and Log current_settings.namespace
    logging.debug("Current NS: %s", str(current_settings.namespace))
    namespaces_var.set(str(current_settings.namespace))

    # Create Option Box
    tk.Label(popup, text="Namespace").grid(sticky="w", padx=2, row=1, column=0)
    namespaces_popup = tk.OptionMenu(popup, namespaces_var, *namespaces)
    namespaces_popup.grid(row=1, column=1, padx=2, sticky="w")

    def change_namespaces(*args):
        """Changing the namespaces"""
        logging.debug("Event: Changing the Namespace: %s",
                      str(args))

        current_namespace = namespaces_var.get()
        logging.debug("\tNew Selection is: %s", current_namespace)

        #Update current_settings Class
        logging.debug("\tSaving new URN namespaces Flag choice in current_settings")

        current_settings.namespace = current_namespace

        return True

    def set_quantity():
        """Quanitiy Set Button Pressed"""
        logging.debug("Event: Quanitiy Set Button Pressed")
        new_quant = quant_var.get()
        is_destroyable = False
        try:
            int(new_quant)
            logging.debug("\tValue is an Integer")
            if is_reasonable_quantity(int(new_quant)):
                logging.debug("\t...and of a reasonable quanitity")
                logging.debug("\tSaving new quanitity is current_settings")
                current_settings.quantity = int(new_quant)
                current_settings.quant_colour = "pale green"
                quant.config(bg=current_settings.quant_colour) #refresh
                is_destroyable = True

            else:
                logging.debug("\t...but too low or high")
                current_settings.quant_colour = "light goldenrod"
                quant.config(bg=current_settings.quant_colour) #refresh
                messagebox.showwarning("Quantity", "Value too large (1 - 65536)")
        except ValueError:
            logging.debug("\tValue is not an Integer")
            current_settings.quant_colour = "light coral"
            quant.config(bg=current_settings.quant_colour) #refresh
            messagebox.showerror("Quantity", "Value not an integer")
        return is_destroyable

    def set_name():
        """name Set Button Pressed"""
        logging.debug("Event: name Set Button Pressed")
        new_name = name_var.get()
        logging.debug(new_name)
        is_destroyable = False
        if is_uuid_ns_name(current_settings.namespace, new_name):
            current_settings.name = new_name
            current_settings.name_colour = "pale green"
            name.config(bg=current_settings.name_colour) #refresh
            is_destroyable = True
        else:
            logging.debug("\t..fail check")
            current_settings.name_colour = "light coral"
            name.config(bg=current_settings.name_colour) #refresh
            messagebox.showwarning("not a good", "name for the namespace")
        return is_destroyable

    def press_button_ok():
        if set_quantity() and change_namespaces() and current_settings.namespace == "":
            popup.destroy()

        elif set_quantity() and change_namespaces() and current_settings.namespace != "" and set_name():
            popup.destroy()

    def press_button_apply():
        set_quantity()
        change_namespaces()
        if current_settings.namespace != "":
            set_name()

    button_ok = tk.Button(popup, text="OK", command=press_button_ok, width=5)
    button_apply = tk.Button(popup, text="Apply", command=press_button_apply, width=5)
    button_close = tk.Button(popup, text="Close", command=popup.destroy, width=5)
    button_ok.grid(row=4, column=0, padx=5, pady=5)
    button_apply.grid(row=4, column=1, padx=5, pady=5)
    button_close.grid(row=4, column=2, padx=5, pady=5)

logging.basicConfig(format='%(message)s', level=logging.WARN)
logging.debug("-----------------\nDEBUG MODE ACTIVE\n-----------------")

current_settings = Settings()
basedir = os.path.dirname(__file__)

'''
https://www.pythonguis.com/tutorials/packaging-tkinter-applications-windows-pyinstaller/
When you run your application, Windows looks at the executable and tries to guess what "application group"
it belongs to. By default, any Python scripts (including your application) are grouped under the same
"Python" group, and so will show the Python icon. To stop this happening, we need to provide Windows with
a different application identifier.'''

try:
    from ctypes import windll  # Only exists on Windows.

    myappid = "uk.bonner.unique.5-beta"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

# Create the Window
logging.info("Create the Window")
window = tk.Tk()
#window.title(current_settings.title)
current_settings.window_title()
window.iconbitmap(os.path.join(basedir, "icon/unique.ico"))
window.geometry("385x275+100+100")
#window.wm_attributes("-topmost", 1) #always on top
window.protocol("WM_DELETE_WINDOW", exit_are_you_sure) #Close Buttom Prompt

# Create the Menu Bar
logging.debug("Create the Menu Bar")
menu_bar = tk.Menu(window)

# Load Icons
new_icon = tk.PhotoImage(file=os.path.join(basedir, 'icon/vswin2019/NewFile_16x.png'))
open_icon = tk.PhotoImage(file=os.path.join(basedir, 'icon/vswin2019/OpenFile_16x.png'))
save_icon = tk.PhotoImage(file=os.path.join(basedir, 'icon/vswin2019/Save_16x.png'))
saveas_icon = tk.PhotoImage(file=os.path.join(basedir, 'icon/vswin2019/SaveAs_16x.png'))
exit_icon = tk.PhotoImage(file=os.path.join(basedir, 'icon/vswin2019/CloseSolution_16x.png'))
uuid0_icon = tk.PhotoImage(file=os.path.join(basedir, 'icon/vswin2019/LevelAll_16x.png'))
uuid1_icon = tk.PhotoImage(file=os.path.join(basedir, 'icon/vswin2019/LevelOne_16x.png'))
uuid3_icon = tk.PhotoImage(file=os.path.join(basedir, 'icon/vswin2019/LevelThree_16x.png'))
uuid4_icon = tk.PhotoImage(file=os.path.join(basedir, 'icon/vswin2019/LevelFour_16x.png'))
uuid5_icon = tk.PhotoImage(file=os.path.join(basedir, 'icon/vswin2019/LevelFive_16x.png'))
ulid_icon = tk.PhotoImage(file=os.path.join(basedir, 'icon/vswin2019/Sort_16x.png'))
uppercase_icon = tk.PhotoImage(file=os.path.join(basedir, 'icon/vswin2019/CaseSensitive_16x.png'))
base64_icon = tk.PhotoImage(file=os.path.join(basedir, 'icon/vswin2019/Binary_16x.png'))
urn_icon = tk.PhotoImage(file=os.path.join(basedir, 'icon/vswin2019/Link_16x.png'))
options_icon = tk.PhotoImage(file=os.path.join(basedir, 'icon/vswin2019/Settings_16x.png'))
about_icon = tk.PhotoImage(file=os.path.join(basedir, 'icon/vswin2019/InformationSymbol_16x.png'))

# Create the File Menu
logging.debug("Create the File Menu")
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", accelerator='Ctrl+N', compound=tk.LEFT,
                      image=new_icon, underline=0, command=file_new)
file_menu.add_command(label="Open", accelerator='Ctrl+O', compound=tk.LEFT,
                      image=open_icon, underline=0, command=file_open)
file_menu.add_command(label="Save", accelerator='Ctrl+S', compound=tk.LEFT,
                      image=save_icon, underline=0, command=file_save)
file_menu.add_command(label="Save As...", compound=tk.LEFT,
                      image=saveas_icon, underline=0, command=file_save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", accelerator='Alt+F4', compound=tk.LEFT,
                      image=exit_icon, underline=0, command=exit_are_you_sure)
menu_bar.add_cascade(label="File", menu=file_menu)

# Create the Generate Menu
logging.debug("Create the Generate Menu")
uuid_menu = tk.Menu(menu_bar, tearoff=0)
uuid_menu.add_command(label="Version 1 UUID", accelerator='Ctrl+1', compound=tk.LEFT,
                      image=uuid1_icon, underline=0, command=lambda: add_uuids_to_pta(1))
uuid_menu.add_command(label="Version 4 UUID", accelerator='Ctrl+4', compound=tk.LEFT,
                      image=uuid4_icon, underline=0, command=lambda: add_uuids_to_pta(4))
uuid_menu.add_separator()
uuid_menu.add_command(label="Version 3 UUID", accelerator='Ctrl+3', compound=tk.LEFT,
                      image=uuid3_icon, underline=0, command=lambda: add_uuids_to_pta(3))#,
                      #state="disabled")
uuid_menu.add_command(label="Version 5 UUID", accelerator='Ctrl+5', compound=tk.LEFT,
                      image=uuid5_icon, underline=0, command=lambda: add_uuids_to_pta(5))#,
                      #state="disabled")
uuid_menu.add_separator()
uuid_menu.add_command(label="Special Nil UUID", accelerator='Ctrl+0', compound=tk.LEFT,
                      image=uuid0_icon, underline=0, command=lambda: add_uuids_to_pta(0))
uuid_menu.add_separator()
uuid_menu.add_command(label="Sortable ULID", accelerator='Ctrl+L', compound=tk.LEFT,
                      image=ulid_icon, underline=0, command=lambda: add_ulids_to_pta())
menu_bar.add_cascade(label="Generate", menu=uuid_menu)

# Create the Tools Menu
logging.debug("Create the Tools Menu")
menu_var_upper = tk.IntVar()
menu_var_upper.set(current_settings.upper_flag)
menu_var_base64 = tk.IntVar()
menu_var_base64.set(current_settings.short_flag)
menu_var_prefix = tk.IntVar()
menu_var_prefix.set(current_settings.urn_flag)

tools_menu = tk.Menu(menu_bar, tearoff=0)
tools_menu.add_checkbutton(label=" Toggle URN Prefix", variable=menu_var_prefix, compound=tk.LEFT,
                           image=urn_icon,  command=current_settings.toggle_urn_prefix)
tools_menu.add_checkbutton(label=" Toggle Base64", variable=menu_var_base64, compound=tk.LEFT,
                           image=base64_icon, command=current_settings.toggle_base64)
tools_menu.add_checkbutton(label=" Toggle Uppercase", variable=menu_var_upper, compound=tk.LEFT,
                           image=uppercase_icon, command=current_settings.toggle_uppercase)
tools_menu.add_separator()
tools_menu.add_command(label="Options...", accelerator='F9', compound=tk.LEFT,
                       image=options_icon, underline=0, command=options_popup)
menu_bar.add_cascade(label="Tools", menu=tools_menu)

# Create the Help Menu
logging.debug("Create the Help Menu")
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About Unique...", accelerator='F1', compound=tk.LEFT,
                      image=about_icon, underline=0, command=about)
menu_bar.add_cascade(label="Help", menu=help_menu)

window.config(menu=menu_bar)

# Create Plain Text Area
logging.debug("Create Plain Text Area")
plain_text_area = tk.Text(window)
scroll_bar = tk.Scrollbar(window, command=plain_text_area.yview)
plain_text_area.configure(yscrollcommand=scroll_bar.set, font=("Lucida Console", 10))
scroll_bar.pack(side='right', fill="both")
plain_text_area.pack(fill="both", expand="yes")

# Bind Keyboard Shortcuts to the Plain Text Area
window.bind_all('<Control-Key-N>', lambda event: file_new())
window.bind_all('<Control-Key-n>', lambda event: file_new())
window.bind_all('<Control-Key-S>', lambda event: file_save())
window.bind_all('<Control-Key-s>', lambda event: file_save())
window.bind_all('<Control-Key-0>', lambda event: add_uuids_to_pta(0))
window.bind_all('<Control-Key-1>', lambda event: add_uuids_to_pta(1))
window.bind_all('<Control-Key-3>', lambda event: add_uuids_to_pta(3))
window.bind_all('<Control-Key-4>', lambda event: add_uuids_to_pta(4))
window.bind_all('<Control-Key-5>', lambda event: add_uuids_to_pta(5))
window.bind_all('<Control-Key-L>', lambda event: add_uuids_to_pta(4))
window.bind_all('<Control-Key-l>', lambda event: add_ulids_to_pta())
window.bind('<F9>', lambda event: options_popup())
window.bind('<F1>', lambda event: about())

# Fix for Default Ctrl+O Binding
window.bind('<Control-Key-O>', lambda event: file_open())
window.bind('<Control-Key-o>', lambda event: file_open())
plain_text_area.bind('<Control-Key-o>', lambda event: file_open())
plain_text_area.bind('<Control-Key-o>', lambda event: file_open())

# Start the Window Main Loop
logging.debug("------------------------------\nStart Tkinter Window Main Loop")
window.mainloop()
logging.debug("=============================\nStop Tkinter Window Main Loop")
