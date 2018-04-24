#!/usr/bin/env python3
from tkinter import (BooleanVar, Button, Checkbutton, Entry, Frame, Label,
                     Scrollbar, Tk, Toplevel, messagebox)
from tkinter.constants import (ACTIVE, BOTH, CENTER, DISABLED, LEFT, NORMAL,
                               RIGHT, TOP, W, E, N, S)

from controller import (add_new, delete_item, show_within, sort_show_vehicle,
                        update_checks)
from view_autocomplete import Combobox_Autocomplete
from view_multi_listbox import Multicolumn_Listbox


root = Tk()
root.title("RoadTax Renewal Tracker")
root.configure(background='lavender')
# window_width = 1080
# window_height = 700
# root.maxsize(width=window_width, height=window_height)
# root.minsize(width=window_width, height=window_height)

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
tableframe.configure(background='lavender')

editframe = Frame(root)
editframe.configure(background='lavender')


title = Label(inputframe, font=(
    "Courier", 28), text="Road-Tax Renewal Tracker", bg='lavender')
label = Label(inputframe, text="day(s)", bg='lavender')

title.grid(row=0, column=0)
label.grid(row=1, column=3)

inputframe.grid(row=0, column=0, padx=100, pady=30)
tableframe.grid(row=1, column=0, padx=30, pady=30)
editframe.grid(row=2, column=0, padx=30,  pady=30)

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
        update.config(state=NORMAL)
        pass

editframe_label = Label(editframe, text="Edit", bg='lavender')
editframe_label.grid(row=1, column=0, columnspan=6, pady=5, padx=5)

add_vehlabel = Label(editframe, text='Vehicle no.', bg='lavender')
add_vehlabel.grid(row=2, column=1, pady=5, padx=5)

sorted_list = list(sort_show_vehicle())

add_vehicle = Combobox_Autocomplete(editframe, list_of_items=sorted_list)
add_vehicle.grid(row=2, column=2, pady=5, padx=5)

add_explabel = Label(editframe, text='expiry date in (dd.mm.yyyy)', bg='lavender')
add_explabel.grid(row=2, column=3, pady=5, padx=5)

add_expiry = Entry(editframe)
add_expiry.grid(row=2, column=4, pady=5, padx=5)

def del_edit():
    delete = delete_item(add_vehicle.get())
    if delete != None:
        show_info(delete)

delete_button = Button(editframe, command=del_edit, text="delete")
delete_button.grid(row=2, column=5, pady=5, padx=5)

def quit_edit():
    add_vehicle1 = add_new(add_vehicle.get(), add_expiry.get())
    if add_vehicle1 != None:
        show_info(add_vehicle1)

add_button = Button(editframe, command=quit_edit, text="Add / Edit", bg='lavender')
add_button.grid(row=2, column=6, pady=5, padx=5)


update = Button(inputframe, padx=10, text="Update!")
inputframe.bind("<Return>", callback)
update.bind("<Button-1>", callback)

entry.grid(row=1, column=0, pady=1, padx=1)
update.grid(row=1, column=7, pady=1, padx=1)
entry.grid(row=1, column=2, pady=1, padx=1)

chkbox1.grid(row=1, column=4, pady=1, padx=1)
chkbox2.grid(row=1, column=5, pady=1, padx=1)
chkbox3.grid(row=1, column=6, pady=1, padx=1)

root.mainloop()
