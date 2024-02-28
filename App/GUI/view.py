#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from App.GUI.Colors import Colors
from App.GUI.view_autocomplete import Combobox_Autocomplete
from App.GUI.view_multi_listbox import Multicolumn_Listbox
from controller import (add_new, delete_item, show_within, sort_show_vehicle,
                        update_checks)
import ctypes

bg_colour = Colors.get_background_color()
btn_colour = Colors.get_button_color()
bg_alt = Colors.get_alternative_backgroud_color()


def run():
    pass

root = tk.Tk()
root.title("RoadTax Renewal Tracker")
root.configure(background=bg_colour)
# To make the application non-resizable and to grey out the maximize button
root.resizable(False, False)

# Makes the application have a cleaner look, less blurriness with scaling.
ctypes.windll.shcore.SetProcessDpiAwareness(1)

vehicle = ""
expiry = ""
informed = tk.BooleanVar()
inspected = tk.BooleanVar()
renewed = tk.BooleanVar()


def on_select(data):
    # to impliment multiple selection
    global vehicle
    global expiry
    global new_vehicle_license
    global new_vehicle_expiry
    new_vehicle_expiry.delete(0, tk.END)
    new_vehicle_expiry.insert(tk.END, data[1])
    new_vehicle_license.set_value(data[0])
    vehicle = data[0]
    expiry = data[1]
    informed.set(data[2])
    inspected.set(data[3])
    renewed.set(data[4])

    return vehicle, informed, inspected, renewed


titleframe = tk.Frame(root)
titleframe.configure(background=bg_colour)
titleframe.grid(row=0, column=0)

editframeTitle = tk.Label(root, text="Manage Entries",
                       background=bg_colour, pady=5)

editframe = tk.LabelFrame(root, text="Manage Entries", borderwidth=1,
                       labelanchor='n', labelwidget=editframeTitle, font=("Myriad Pro Bold", 10))
editframe.configure(background=bg_colour)
editframe.grid(row=2, column=0, padx=40,  pady=25)


roadtax_tab = ttk.Notebook(root)

bodyframe = tk.Frame(roadtax_tab)
bodyframe.configure(background=bg_colour)
bodyframe.grid()

roadtax_tab.add(bodyframe, text="Roadtax")
roadtax_tab.enable_traversal()
roadtax_tab.grid(row=1, column=0, sticky=tk.S)

title = tk.Label(titleframe, font=("Courier", 28),
              text="Road-Tax Renewal Tracker", bg=bg_colour)

label = tk.Label(bodyframe, text="day(s)", bg=bg_colour)

column_header = ["Vehicle Number", "Expiry Date",
                 "Informed", "Inspected", "Renewed"]

mc = Multicolumn_Listbox(bodyframe,
                         column_header,
                         command=on_select,
                         stripped_rows=("white", bg_colour),
                         select_mode="extended",  # browse
                         cell_anchor="center", height=20)

scrollbar = tk.Scrollbar(bodyframe)
scrollbar.config(command=mc.interior.yview, activebackground=btn_colour)
scrollbar.grid(row=1, column=7, sticky=tk.N+tk.S)

mc.interior.config(yscrollcommand=scrollbar.set)
mc.interior.grid(row=1, column=0, columnspan=6, sticky=tk.N+tk.S+tk.E+tk.W)

entry = tk.Entry(bodyframe)
entry.insert(0, "30")
entry.focus_set()

mc.table_data = show_within(entry.get())

chkbox1 = tk.Checkbutton(bodyframe,
                      text="Informed",
                      variable=informed,
                      bg=bg_colour)
chkbox2 = tk.Checkbutton(bodyframe,
                      text="Inspected",
                      variable=inspected,
                      bg=bg_colour)
chkbox3 = tk.Checkbutton(bodyframe,
                      text="Renewed",
                      variable=renewed,
                      bg=bg_colour)


def callback():
    """
    update database with boolean values.
    currently partially managed by model.py
    """
    try:
        updated_vehicle = []
        for val in mc.selected_rows:
            update = update_checks(val[0], val[1], val[2], val[3], val[4])
            updated_vehicle.append(update)

        if update is not None:
            messagebox.showinfo(
                "Update", "Some informations have been updated : {}".format(updated_vehicle))
            mc.table_data = show_within(entry.get())
    except ValueError:
        messagebox.showerror(
            "Invalid input", "The value you entered in incorrect. It must be a number")
        update.config(state=tk.NORMAL)
        pass


def refresh(event):
    """
    Dynamically update table as user type in the query
        :param event:
            KeyRelease event binded to Entry widget
    """
    mc.table_data = show_within(entry.get())


add_vehlabel = tk.Label(editframe, text='Vehicle'+'\n' + 'number', bg=bg_colour)
sorted_list = list(sort_show_vehicle())
new_vehicle_license = Combobox_Autocomplete(
    editframe, list_of_items=sorted_list)
add_explabel = tk.Label(editframe, text='Expiry Date' +
                     '\n'+'(dd/mm/yyyy)', bg=bg_colour)
new_vehicle_expiry = tk.Entry(editframe)


def delete_button_func():
    """
    delete item from database
    """
    delete_vehicle = []
    for val in mc.selected_rows:
        result = delete_item(val[0])
        delete_vehicle.append(result)

    if result is not None:
        tk.messagebox.showinfo(
            "Deleted item", "An item has been succesfully deleted : {}".format(delete_vehicle))
        mc.table_data = show_within(entry.get())


delete_button = tk.Button(editframe,
                       command=delete_button_func,
                       text="Delete",
                       background=btn_colour,
                       disabledforeground="DeepSkyBlue4", borderwidth=0, highlightbackground=bg_alt)
# make sure to add "/" not "\"
delete_img = tk.PhotoImage(file="../../assets/buttons/button_delete.gif")
delete_button.config(image=delete_img)


def quit_edit():
    new_vehicle_license1 = add_new(
        new_vehicle_license.get(), new_vehicle_expiry.get())
    if new_vehicle_license1 is not None:
        tk.messagebox.showinfo("Adding new vehicle", new_vehicle_license1)
        #mc.table_data = show_within(entry.get())


add_button = tk.Button(editframe,
                    command=quit_edit,
                    text="Add / Edit",
                    background=btn_colour,
                    disabledforeground="DeepSkyBlue4", borderwidth=0, highlightbackground=bg_alt)
add_img = tk.PhotoImage(file="../../assets/buttons/button_add-edit.gif")
add_button.config(image=add_img)

update = tk.Button(bodyframe,
                text="Update!",
                background=btn_colour,
                command=callback, disabledforeground="DeepSkyBlue4", borderwidth=0, highlightbackground=bg_colour)
update_img = tk.PhotoImage(file="../../assets/buttons/button_update.gif")
update.config(image=update_img)


entry.bind("<KeyRelease>", refresh)

title.grid(row=0, column=0, columnspan=6, padx=20, pady=20)

entry.grid(row=0, column=0, pady=10, padx=10, sticky=tk.E)
label.grid(row=0, column=1, pady=10, padx=10, sticky=tk.W)
chkbox1.grid(row=0, column=2, pady=10, padx=10, sticky=tk.W+tk.E)
chkbox2.grid(row=0, column=3, pady=10, padx=10, sticky=tk.W+tk.E)
chkbox3.grid(row=0, column=4, pady=10, padx=10, sticky=tk.W+tk.E)
update.grid(row=0, column=5, pady=10, padx=10)


add_vehlabel.grid(row=2, column=1, pady=5, padx=3)
new_vehicle_license.grid(row=2, column=2, pady=5, padx=5)
add_explabel.grid(row=2, column=3, pady=5, padx=3)
new_vehicle_expiry.grid(row=2, column=4, pady=5, padx=5)
delete_button.grid(row=3, column=5, pady=0, padx=5)
add_button.grid(row=2, column=5, pady=0, padx=5, sticky=tk.E)

"""Configure window to launch in the middle of the screen"""
root.update_idletasks()
h = root.winfo_reqheight()  # width for the Tk root
w = root.winfo_reqwidth()  # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight()  # height of the screen

print(w, h, ws, hs)

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
def get_root():
    return root

#if __name__=="__main__":
#    debug_root = root
#    root.mainloop()
