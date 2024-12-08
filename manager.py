import mysql.connector
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkinter.simpledialog as sd

# Connecting to Database
connector = mysql.connector.connect(
    host="localhost",
    user="root",
    port=330,
    password="Hacker@85",  # Replace with your MySQL password
    database="manag"
)
cursor = connector.cursor()

# Create table if not exists
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS Library (
        BK_NAME VARCHAR(255),
        BK_ID VARCHAR(255) PRIMARY KEY NOT NULL,
        AUTHOR_NAME VARCHAR(255),
        BK_STATUS VARCHAR(50),
        CARD_ID VARCHAR(255)
    )
    '''
)

# Functions
def issuer_card():
    Cid = sd.askstring('Issuer Card ID', 'What is the Issuer\'s Card ID?')
    if not Cid:
        mb.showerror('Issuer ID Error', 'Issuer ID cannot be empty!')
    else:
        return Cid

def display_records():
    tree.delete(*tree.get_children())
    cursor.execute('SELECT * FROM Library')
    data = cursor.fetchall()
    for record in data:
        tree.insert('', END, values=record)


def clear_fields():
    bk_status.set('Available')
    for field in ['bk_id', 'bk_name', 'author_name', 'card_id']:
        exec(f"{field}.set('')")
    bk_id_entry.config(state='normal')
    try:
        tree.selection_remove(tree.selection()[0])
    except:
        pass

def clear_and_display():
    clear_fields()
    display_records()

def add_record():
    if bk_status.get() == 'Issued':
        card_id.set(issuer_card())
    else:
        card_id.set('N/A')

    surety = mb.askyesno('Confirm Entry',
                         'Are you sure you want to add this record? Book ID cannot be changed later.')
    if surety:
        try:
            cursor.execute(
                'INSERT INTO Library (BK_NAME, BK_ID, AUTHOR_NAME, BK_STATUS, CARD_ID) VALUES (%s, %s, %s, %s, %s)',
                (bk_name.get(), bk_id.get(), author_name.get(), bk_status.get(), card_id.get())
            )
            connector.commit()
            clear_and_display()
            mb.showinfo('Success', 'Record added successfully!')
        except mysql.connector.Error as e:
            mb.showerror('Error', f'Error adding record: {e}')


def view_record():
    if not tree.focus():
        mb.showerror('Error', 'Please select a record from the table.')
        return

    current_item = tree.focus()
    values = tree.item(current_item)['values']
    bk_name.set(values[0])
    bk_id.set(values[1])
    author_name.set(values[2])
    bk_status.set(values[3])
    card_id.set(values[4])

def update_record():
    def update():
        if bk_status.get() == 'Issued':
            card_id.set(issuer_card())
        else:
            card_id.set('N/A')

        cursor.execute(
            'UPDATE Library SET BK_NAME=%s, BK_STATUS=%s, AUTHOR_NAME=%s, CARD_ID=%s WHERE BK_ID=%s',
            (bk_name.get(), bk_status.get(), author_name.get(), card_id.get(), bk_id.get())
        )
        connector.commit()
        clear_and_display()
        edit.destroy()
        bk_id_entry.config(state='normal')
        clear.config(state='normal')

    view_record()
    bk_id_entry.config(state='disabled')
    clear.config(state='disabled')
    edit = Button(left_frame, text='Update Record', font=btn_font, bg=btn_hlb_bg, width=20, command=update)
    edit.place(x=50, y=375)

def remove_record():
    if not tree.selection():
        mb.showerror('Error', 'Please select a record to delete.')
        return

    current_item = tree.focus()
    bk_id = tree.item(current_item)['values'][1]
    cursor.execute('DELETE FROM Library WHERE BK_ID=%s', (bk_id,))
    connector.commit()
    tree.delete(current_item)
    mb.showinfo('Success', 'Record deleted successfully!')
    clear_and_display()

def delete_inventory():
    if mb.askyesno('Confirm', 'Are you sure you want to delete the entire inventory? This cannot be undone.'):
        cursor.execute('DELETE FROM Library')
        connector.commit()
        clear_and_display()
        mb.showinfo('Success', 'All records deleted successfully!')

def change_availability():
    if not tree.selection():
        mb.showerror('Error', 'Please select a book from the table.')
        return

    current_item = tree.focus()
    values = tree.item(current_item)['values']
    bk_id = values[1]
    bk_status = values[3]

    if bk_status == 'Issued':
        if mb.askyesno('Confirm Return', 'Has the book been returned?'):
            cursor.execute('UPDATE Library SET BK_STATUS=%s, CARD_ID=%s WHERE BK_ID=%s', ('Available', 'N/A', bk_id))
            connector.commit()
    else:
        cursor.execute('UPDATE Library SET BK_STATUS=%s, CARD_ID=%s WHERE BK_ID=%s', ('Issued', issuer_card(), bk_id))
        connector.commit()

    clear_and_display()

# GUI setup
root = Tk()
root.title('Library Management System')
root.geometry('1010x530')
root.resizable(0, 0)

lbl_font = ('Georgia', 13)
entry_font = ('Times New Roman', 12)
btn_font = ('Gill Sans MT', 13)
lf_bg = 'LightSkyBlue'
btn_hlb_bg = 'SteelBlue'

bk_status = StringVar(value='Available')
bk_name = StringVar()
bk_id = StringVar()
author_name = StringVar()
card_id = StringVar()

Label(root, text='LIBRARY MANAGEMENT SYSTEM', font=("Noto Sans CJK TC", 15, 'bold'), bg=btn_hlb_bg, fg='White').pack(side=TOP, fill=X)

left_frame = Frame(root, bg=lf_bg)
left_frame.place(x=0, y=30, relwidth=0.3, relheight=0.96)

RT_frame = Frame(root, bg='DeepSkyBlue')
RT_frame.place(relx=0.3, y=30, relheight=0.2, relwidth=0.7)

RB_frame = Frame(root)
RB_frame.place(relx=0.3, rely=0.24, relheight=0.785, relwidth=0.7)

Label(left_frame, text='Book Name', bg=lf_bg, font=lbl_font).place(x=98, y=25)
Entry(left_frame, width=25, font=entry_font, text=bk_name).place(x=45, y=55)

Label(left_frame, text='Book ID', bg=lf_bg, font=lbl_font).place(x=110, y=105)
bk_id_entry = Entry(left_frame, width=25, font=entry_font, text=bk_id)
bk_id_entry.place(x=45, y=135)

Label(left_frame, text='Author Name', bg=lf_bg, font=lbl_font).place(x=90, y=185)
Entry(left_frame, width=25, font=entry_font, text=author_name).place(x=45, y=215)

Label(left_frame, text='Status of the Book', bg=lf_bg, font=lbl_font).place(x=75, y=265)
OptionMenu(left_frame, bk_status, *['Available', 'Issued']).place(x=75, y=300)

Button(left_frame, text='Add new record', font=btn_font, bg=btn_hlb_bg, width=20, command=add_record).place(x=50, y=375)
clear = Button(left_frame, text='Clear fields', font=btn_font, bg=btn_hlb_bg, width=20, command=clear_fields)
clear.place(x=50, y=435)

Button(RT_frame, text='Delete book record', font=btn_font, bg=btn_hlb_bg, width=17, command=remove_record).place(x=8, y=30)
Button(RT_frame, text='Delete full inventory', font=btn_font, bg=btn_hlb_bg, width=17, command=delete_inventory).place(x=178, y=30)
Button(RT_frame, text='Update book details', font=btn_font, bg=btn_hlb_bg, width=17, command=update_record).place(x=348, y=30)
Button(RT_frame, text='Change Book Availability', font=btn_font, bg=btn_hlb_bg, width=19, command=change_availability).place(x=518, y=30)

Label(RB_frame, text='BOOK INVENTORY', font=("Noto Sans CJK TC", 15, 'bold')).pack(side=TOP, fill=X)

tree = ttk.Treeview(RB_frame, selectmode=BROWSE, columns=('Book Name', 'Book ID', 'Author', 'Status', 'Issuer Card ID'))
tree.heading('Book Name', text='Book Name', anchor=CENTER)
tree.heading('Book ID', text='Book ID', anchor=CENTER)
tree.heading('Author', text='Author', anchor=CENTER)
tree.heading('Status', text='Status', anchor=CENTER)
tree.heading('Issuer Card ID', text='Card ID', anchor=CENTER)

tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=225, stretch=NO)
tree.column('#2', width=70, stretch=NO)
tree.column('#3', width=155, stretch=NO)
tree.column('#4', width=135, stretch=NO)
tree.column('#5', width=165, stretch=NO)

XScrollbar = Scrollbar(RB_frame, orient=HORIZONTAL, command=tree.xview)
YScrollbar = Scrollbar(RB_frame, orient=VERTICAL, command=tree.yview)
XScrollbar.pack(side=BOTTOM, fill=X)
YScrollbar.pack(side=RIGHT, fill=Y)
tree.config(xscrollcommand=XScrollbar.set, yscrollcommand=YScrollbar.set)
tree.pack(expand=1, fill=BOTH)

display_records()
root.mainloop()
