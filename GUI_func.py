from tkinter import *
from tkinter import messagebox
import sqlite3

class modal:
    def __init__(self):
        self.__n_records = 0
        self.__records = None
        self.__currRec = 0

    def setNRecords(self,n):
        self.__n_records = n
    def setRecords(self,r):
        self.__records = r
    def setCurrRecord(self,c):
        self.__currRec = c
    def getNRecords(self):
        return self.__n_records
    def getRecords(self):
        return self.__records
    def getCurrRecord(self):
        return self.__currRec

def connect_db(data):
    mydb = sqlite3.connect('DB2.db')
    cursor = mydb.cursor()
    try:
        tblcmd = 'create table Account_directory (id integer primary key autoincrement, name char(32), phone int(10), username char(32), password char(32), DOB char(32))'
        cursor.execute(tblcmd)
    except:
        update(data)
        if data.getNRecords() > 0:
            firstRec(data)
    mydb.commit()
    mydb.close()



    


def firstRec(data):
    if data.getNRecords()==0:
        messagebox.showerror("SQL ERROR", "No Records...")
        return
    data.setCurrRecord(0)
    print(data.getRecords())
    name.set(data.getRecords()[data.getCurrRecord()][1])
    phone.set(str(data.getRecords()[data.getCurrRecord()][2]))
    username.set(data.getRecords()[data.getCurrRecord()][3])
    password.set(data.getRecords()[data.getCurrRecord()][4])
    DOB.set(data.getRecords()[data.getCurrRecord()][5])
    

def addRec(data):
    nameVar = name.get()
    phoneVar = phone.get()
    usernameVar= username.get()
    passwordVar=password.get()
    DOBVar=DOB.get()
    if (not nameVar) or (not phoneVar) or (not phoneVar.isnumeric()) or (not usernameVar) or (not passwordVar) or (not DOBVar):
        messagebox.showerror("Error","Please provide correct data!")
    else:
        conn = sqlite3.connect('DB2.db')
        curs = conn.cursor()
        curs.execute('select * from Account_directory where phone=? LIMIT 1', (phoneVar,))
        res = curs.fetchone()
        if res:
            # Pending here
            messagebox.showinfo("Data updated!","Name changed from %s to %s for username %s" % (res[1], nameVar, usernameVar))
            curs.execute('update Account_directory set name = ?, phone = ?, password = ?, dob =? where username= ? ', (nameVar,phoneVar,passwordVar,DOBVar,phoneVar))
        else:
            curs.execute('insert into Account_directory (name, phone,username,password,DOB) values(?, ?, ?, ?,?)', (nameVar, phoneVar,usernameVar,passwordVar,DOBVar))
            messagebox.showinfo("Saved to Database!","Added %s having username %s to directory!" % (nameVar, usernameVar))
        conn.commit()
        conn.close()
        update(data)

def prevRec(data):
    if(data.getCurrRecord()==0):
        messagebox.showerror("ERROR", "You are seeing first record!")
        return
    data.setCurrRecord(data.getCurrRecord()-1)
    name.set(data.getRecords()[data.getCurrRecord()][1])
    phone.set(str(data.getRecords()[data.getCurrRecord()][2]))
    username.set(data.getRecords()[data.getCurrRecord()][3])
    password.set(data.getRecords()[data.getCurrRecord()][4])
    DOB.set(data.getRecords()[data.getCurrRecord()][5])

def update(data):
    mydb = sqlite3.connect('DB2.db')
    cursor = mydb.cursor()
    select_record = cursor.execute('select * from Account_directory')
    rec = cursor.fetchall()
    data.setNRecords(len(rec))
    data.setRecords(rec)
    mydb.commit()
    mydb.close()

def deleteRec(data):
    nameVar = name.get()
    phoneVar = phone.get()
    usernameVar= username.get()
    passwordVar=password.get()
    DOBVar=DOB.get()
    mydb = sqlite3.connect('DB2.db')
    cursor = mydb.cursor()
    cursor.execute('Delete from Account_directory where username = ?', (usernameVar,))
    name.set("")
    phone.set("")
    username.set("")
    password.set("")
    DOB.set("")
    messagebox.showinfo("Error","RECORD DELETED")   
    update(data)

def nextRec(data):
    if(data.getCurrRecord()==data.getNRecords()-1):
        messagebox.showerror("ERROR", "You are seeing last record!")
        return
    data.setCurrRecord(data.getCurrRecord()+1)
    name.set(data.getRecords()[data.getCurrRecord()][1])
    phone.set(str(data.getRecords()[data.getCurrRecord()][2]))
    username.set(data.getRecords()[data.getCurrRecord()][3])
    password.set(data.getRecords()[data.getCurrRecord()][4])
    DOB.set(data.getRecords()[data.getCurrRecord()][5])

def searchRec(data):
    # SEARCH PENDING
    nameVar = name.get()
    phoneVar = phone.get()
    usernameVar= username.get()
    passwordVar=password.get()
    DOBVar=DOB.get()
    filtered = []
    for value in data.getRecords():
        if re.search(usernameVar, value[3], re.IGNORECASE) and usernameVar:
            filtered.append(f"{value[1]}, {value[2]}, {value[3]}, {value[4]}, {value[5]}")
            continue
        if re.search(str(phoneVar), str(value[3]), re.IGNORECASE) and phoneVar:
            filtered.append(f"{value[1]}, {value[2]}, {value[3]}, {value[4]}, {value[5]}")
    if filtered:
        title = f"Found {len(filtered)} record(s):\n"
    else:
        title = "No record found!"
    messagebox.showinfo("SEARCH RESULT", title + '\n'.join(filtered))

win = Tk()

win.title("Account Directory")
# width = win.winfo_screenwidth()
# height = win.winfo_screenheight()
res = "%dx%d" % (370,370)
win.geometry(res)

nameLabel = Label(win, text="Name:", font=("Roboto",14), anchor="w",width="8")
nameLabel.grid(row=1,column=1,padx=2,pady=5)
name = StringVar()
nameInput = Entry(win,textvariable = name,font=("Roboto",14))
nameInput.grid(row=1,column=2,columnspan=3,padx=2,pady=5)


phoneLabel = Label(win, text="Phone:", font=("Roboto",14), anchor="w", width="8")
phoneLabel.grid(row=2,column=1,padx=2,pady=5)
phone = StringVar()
phoneInput = Entry(win,textvariable = phone,font=("Roboto",14))
phoneInput.grid(row=2,column=2,columnspan=3,padx=2,pady=5)


usernameLabel= Label(win, text="Username:", font=("Roboto",14), anchor="w", width="8")
usernameLabel.grid(row=3,column=1,padx=2,pady=5)
username=StringVar()
usernameInput=Entry(win,textvariable=username,font=("Roboto",14))
usernameInput.grid(row=3,column=2,columnspan=3,padx=2,pady=5)


passwordLabel= Label(win, text="Password:", font=("Roboto",14), anchor="w", width="8")
passwordLabel.grid(row=4,column=1,padx=2,pady=5)
password=StringVar()
passwordInput=Entry(win,textvariable=password,show='*',font=("Roboto",14))
passwordInput.grid(row=4,column=2,columnspan=3,padx=2,pady=5)


DOBLabel= Label(win, text="DOB:", font=("Roboto",14), anchor="w", width="8")
DOBLabel.grid(row=5,column=1,padx=2,pady=5)
DOB=StringVar()
DOBInput=Entry(win,textvariable=DOB,font=("Roboto",14))
DOBInput.grid(row=5,column=2,columnspan=3,padx=2,pady=5)





previousButton = Button(win, width=8, bg="blue" , fg="white" , command=lambda : prevRec(data), text="<<", font=("Roboto",12,"bold"))
previousButton.grid(row=6, column=2,padx=2,pady=5)

nextButton = Button(win, width=8, text=">>",bg="blue" , fg="white", command=lambda : nextRec(data), font=("Roboto",12,"bold"))
nextButton.grid(row=6, column=3,padx=2,pady=5)

addButton = Button(win, width=8,bg="green" , fg="white", command=lambda : addRec(data), text="Add", font=("Roboto",12,"bold"))
addButton.grid(row=7, column=2,padx=2,pady=5)

searchButton = Button(win, width=8,bg="yellow" , fg="white", text="Search", command=lambda : searchRec(data), font=("Roboto",12,"bold"))
searchButton.grid(row=7, column=3,padx=2,pady=5)

deleteButton = Button(win, width=8,bg="red" , fg="white", command=lambda : deleteRec(data), text="Delete", font=("Roboto",12,"bold"))
deleteButton.grid(row=8, column=2,padx=2,pady=5,columnspan=2)

data = modal()
connect_db(data)

win.mainloop()