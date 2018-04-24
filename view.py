#!/usr/bin/env python3
from tkinter import (BooleanVar, Button, Checkbutton, Entry, Frame, Label,
                     Scrollbar, Tk, Toplevel, messagebox)
from tkinter.constants import (ACTIVE, BOTH, CENTER, DISABLED, LEFT, NORMAL,
                               RIGHT, TOP, W, E, N, S)

from controller import (add_new, delete_item, show_within, sort_show_vehicle,
                        update_checks)
from view_autocomplete import Combobox_Autocomplete
from view_multi_listbox import Multicolumn_Listbox


def SecWindow():
    if to_edit['state'] == 'normal':
        to_edit.config(state=DISABLED)

    edit_window = Toplevel()

    ##########################################################################################
    # ToDo:
    # Implement autocomplet on vehicle
    # instead of second window, make a pane or notbook for editing
    edit_window.add_vehlabel = Label(edit_window, text='Vehicle no.')
    edit_window.add_vehlabel.grid(row=0, column=0)
    sorted_list = sort_show_vehicle()
    edit_window.add_vehicle = Combobox_Autocomplete(edit_window, sorted_list)
    edit_window.add_vehicle.grid(row=0, column=0)
    
    edit_window.add_explabel = Label(
        edit_window, text='expiry date in (dd.mm.yyyy)')
    edit_window.add_explabel.grid(row=0, column=0)
    
    edit_window.add_expiry = Entry(edit_window)
    edit_window.add_expiry.grid(row=0, column=0)
    
    def show_info(msg):
        messagebox.showinfo("This is magical!", msg)

    def del_edit():
        delete = delete_item(edit_window.add_vehicle.get())
        if delete != None:
            show_info(delete)
        edit_window.destroy()
        to_edit.config(state=NORMAL)

    def quit_edit():
        add_vehicle = add_new(edit_window.add_vehicle.get(),
                              edit_window.add_expiry.get())
        if add_vehicle != None:
            show_info(add_vehicle)
        edit_window.destroy()
        to_edit.config(state=NORMAL)

    edit_window.delete_button = Button(
        edit_window, command=del_edit, text="delete")
    edit_window.delete_button.grid(row=0, column=0)
    
    edit_window.add_button = Button(
        edit_window, command=quit_edit, text="Add / Edit")
    edit_window.add_button.grid(row=0, column=0)
    
    edit_window.protocol("WM_DELETE_WINDOW", quit_edit)


root = Tk()
root.title("RoadTax Renewal Tracker")
root.configure(background='lavender')
window_width = 1080
window_height = 600
root.maxsize(width=window_width, height=window_height)
root.minsize(width=window_width, height=window_height)

vehicle = ""
expiry = ""
informed = BooleanVar()
inspected = BooleanVar()
renewed = BooleanVar()


def on_select(data):
    # to impliment multiple selection
    global vehicle
    global expiry

    vehicle = data[0]
    expiry = data[1]
    informed.set(data[2])
    inspected.set(data[3])
    renewed.set(data[4])

    return vehicle, informed, inspected, renewed


def show_info(msg):
    messagebox.showinfo("This is magical!", msg)


inputframe = Frame(root)
inputframe.configure(background='lavender')

tableframe = Frame(root)
inputframe.configure(background='lavender')

title = Label(inputframe, font=(
    "Courier", 24), text="Road-Tax Renewal Tracker", bg='lavender')
label = Label(inputframe, text="day(s)", bg='lavender')

title.grid(row=0, column=0, columnspan=8,padx=40)
label.grid(row=1, column=3)

inputframe.grid(row=0, column=0)
tableframe.grid(row=1, column=0, padx=30, pady=30, sticky=N+S+E+W)

# relief column defination to controller.py
mc = Multicolumn_Listbox(tableframe, ["Vehicle Number", "Expiry Date",
                                      "Informed", "Inspected", "Renewed"],
                         stripped_rows=("white", "lavender"), command=on_select,
                         cell_anchor="center", height=20)

scrollbar = Scrollbar(tableframe)
scrollbar.config(command=mc.interior.yview)

scrollbar.grid(row=0, column=1, sticky=N+S)

# mc.configure_column(width=600, minwidth=100)

mc.interior.config(yscrollcommand=scrollbar.set)
mc.interior.grid(row=0, column=0, sticky=N+S+E+W)
entry = Entry(inputframe)
entry.insert(0, "30")
entry.focus_set()

mc.table_data = show_within(entry.get())

chkbox1 = Checkbutton(inputframe, text="Informed",
                      variable=informed, bg='lavender')
chkbox2 = Checkbutton(inputframe, text="Inspected",
                      variable=inspected, bg='lavender')
chkbox3 = Checkbutton(inputframe, text="Renewed",
                      variable=renewed, bg='lavender')


def callback(event):

    try:
        update = update_checks(
            vehicle, expiry, informed.get(), inspected.get(), renewed.get())
        entry.get()
        mc.table_data = show_within(entry.get())
        if update != None:
            show_info(update)
        return entry.get()
    except ValueError:
        show_info("Invalid input, Number only la!!!")
        send.config(state=NORMAL)
        pass


send = Button(inputframe, padx=10, text="Update!")
inputframe.bind("<Return>", callback)
send.bind("<Button-1>", callback)

to_edit = Button(root, text='Edit', command=SecWindow, width=15)
to_edit.config(state=ACTIVE)

entry.grid(row=1, column=0, pady=1, padx=1)
send.grid(row=1, column=7, pady=1, padx=1)
to_edit.grid(row=2, column=0, padx=40)
entry.grid(row=1, column=2, pady=1, padx=1)
chkbox3.grid(row=1, column=4, pady=1, padx=1)
chkbox2.grid(row=1, column=5, pady=1, padx=1)
chkbox1.grid(row=1, column=6, pady=1, padx=1)


root.mainloop()
