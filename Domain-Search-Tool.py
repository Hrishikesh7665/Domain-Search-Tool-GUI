from tkinter import *
from tkinter import ttk, font, messagebox
from bs4 import BeautifulSoup
import dns.resolver
import requests
import re
import threading
import os, sys,signal
from sys import path_hooks, platform
import time
import subprocess
import lxml

path =""

if platform == "darwin":
    print("Not For Mac")
    sys.exit()
elif platform == "win32" or platform == "linux" or platform == "linux2":
    def resource_path():
        CurrentPath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        spriteFolderPath = os.path.join(CurrentPath, 'Assets')
        path = os.path.join(spriteFolderPath)
        newPath = path.replace(os.sep, '/')
        return newPath+"/"
    path = resource_path()
    def resource_path2():
        CurrentPath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        spriteFolderPath = os.path.join(CurrentPath,"Logs")
        path = os.path.join(spriteFolderPath)
        newPath = path.replace(os.sep, '/')
        return newPath+"/"
    path2 = resource_path2()


found = []

background_col = "#fff1d0"

mainwindow = Tk()
mainwindow.config(bg=background_col)

def center_window(w,h):
    ws = mainwindow.winfo_screenwidth()
    hs = mainwindow.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    mainwindow.geometry('%dx%d+%d+%d' % (w, h, x, y))

center_window(812,450)

TOPFRAME = Frame(bg=background_col)

deli = 220           # milliseconds of delay per character
svar = StringVar()
webadd = StringVar()
webadd.set("Example: google.com")
limitvar = StringVar()
limitvar.set("No Limit")
logvar = StringVar()
logvar.set("No")

labl = Label(TOPFRAME, textvariable=svar,bg="#4c4c4c",fg="white")

def shif():
    shif.msg = shif.msg[1:] + shif.msg[0]
    svar.set(shif.msg)
    TOPFRAME.after(deli, shif)

shif.msg = '                        Tool For Sub-Domain Search With IP Address Python 3.9 With Tkinter Gui For Linux And Windows                                                                Tool For Sub-Domain Search With IP Address Python 3.9 With Tkinter Gui For Linux And Windows                                        '
shif()
labl.pack(side=TOP,fill=BOTH)



homeLabel = Label(mainwindow, text="HR", font=("Eras Demi ITC", 10),bg="lavender blush", fg="gray17")
homeLabel.place(x=752,y=0)

def tic():
    homeLabel['text'] = time.strftime('%I:%M:%S')

tic()

def tac():
    tic()
    homeLabel.after(1000, tac)

tac()

Label(TOPFRAME,text=" ",font=("arial",3),bg=background_col).pack()

webLabel = Label(TOPFRAME,text="  Enter Website  ",font=("Arial Rounded MT Bold",12),bg=background_col)
webLabel.pack(side=LEFT)

websiteEntry = Entry(TOPFRAME,textvariable=webadd,bg="azure",fg = 'grey',font=("Segoe Print",10),width=19)
websiteEntry.pack(side=LEFT)

Label(TOPFRAME,text="        ",bg=background_col).pack(side=LEFT)

scanlimit_lbl = Label(TOPFRAME,text="Enter Scan Limit  ",font=("Arial Rounded MT Bold",12),bg=background_col)
scanlimit_lbl.pack(side=LEFT)

scanlimitEntry = Entry(TOPFRAME,textvariable=limitvar,bg="azure",fg = 'grey',font=("Segoe Print",10),width=7)
scanlimitEntry.pack(side=LEFT)

Label(TOPFRAME,text="        ",bg=background_col).pack(side=LEFT)

log_lbl = Label(TOPFRAME,text="Create Log File  ",font=("Arial Rounded MT Bold",12),bg=background_col)
log_lbl.pack(side=LEFT)

option = ttk.Combobox(TOPFRAME,width=4,textvariable = logvar,state="readonly",values= ('Yes',' No'),font=("ArialBlack",11))
option.current()
option.pack(side=LEFT)


TOPFRAME.pack(side=TOP,fill=BOTH)


tabel_frame = Frame(mainwindow,bg=background_col)
tabel_frame.pack(fill=BOTH,expand=1)

scrollbar_x = Scrollbar(tabel_frame,orient=HORIZONTAL)
scrollbar_y = Scrollbar(tabel_frame,orient=VERTICAL)



def fixed_map(option):
    return [elm for elm in style.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]

style = ttk.Style(mainwindow)
style.theme_use("clam")
style.configure("Treeview.Heading",font=("arial",12, "bold"))
style.configure("Treeview",font=("arial",12),rowheight=25)
style.map('Treeview', foreground=fixed_map('foreground'),background=fixed_map('background'))

tabel = ttk.Treeview(tabel_frame,style = "Treeview",
            columns =("No","Domain","IP","Status"),xscrollcommand=scrollbar_x.set,
            yscrollcommand=scrollbar_y.set)

tabel.heading("No",text="Num.")
tabel.heading("Domain",text="Sub-Domain")
tabel.heading("IP",text="IP Address")
tabel.heading("Status",text="Domain Status")
tabel["displaycolumns"]=("No", "Domain", "IP", "Status")
tabel["show"] = "headings"
tabel.column("No",anchor='center',width=2)
tabel.column("Domain",anchor='center')
tabel.column("IP",anchor='center')
tabel.column("Status",anchor='center',width=40)

scrollbar_x.pack(side=BOTTOM,fill=X)
scrollbar_y.pack(side=RIGHT,fill=Y)

scrollbar_x.configure(command=tabel.xview)
scrollbar_y.configure(command=tabel.yview)

tabel.pack(fill=BOTH,expand=1)

tabel.tag_configure("ok",background='#00b300',foreground="white")
tabel.tag_configure('fail', background='#ff6a33',foreground="white")

stop = False

Search_icon = PhotoImage(file = path+'Se.png')
Reset_icon = PhotoImage(file = path+'Reset.png')
Stop_icon = PhotoImage(file = path+'Stop.png')


def main_function():
    global stop, found
    if b1['text'] == "Start Scan":
        if webadd.get() !="Example: google.com" and webadd.get() != "":
            website=(webadd.get().lower())
            if limitvar.get () == 'No Limit' or limitvar.get () == "":
                limit = 0
            else:
                limit = int(limitvar.get ())
            stop = False
            websiteEntry.config(state=DISABLED)
            scanlimitEntry.config(state=DISABLED)
            option.config(state=DISABLED)
            x = threading.Thread(target=lambda:certscanner(website,limit,logvar.get()))
            x.start()
            b1.config(text="Stop Scan",image=Stop_icon,compound=LEFT)
        else:
            messagebox.showerror("Wrong Value","Please Enter Website\n(e.g. google.com)")
    elif b1['text'] == "Stop Scan":
        b1.config(text="Reset",image=Reset_icon,compound=LEFT)
        stop = True
        try:
            frame.destroy()
        except:
            pass
        try:
            frame_2.destroy()
        except:
            pass
    elif b1['text'] == "Reset":
        b1.config(text="Start Scan",image=Search_icon,compound=LEFT)
        websiteEntry.config(state=NORMAL)
        scanlimitEntry.config(state=NORMAL)
        option.config(state=NORMAL)
        webadd.set("Example: google.com")
        limitvar.set("No Limit")
        logvar.set("No")
        found = []
        scanlimitEntry.config(fg = 'grey',font=("Segoe Print",10))
        websiteEntry.config(fg = 'grey',font=("Segoe Print",10))
        for i in tabel.get_children():
            tabel.delete(i)
        tabel_frame.focus_set()
target = ""
frame = ""
frame_2 =""
def certscanner(emailformat,limit,log):
    global target,frame,frame_2
    dnsresolver = dns.resolver.Resolver()
    dnsresolver.nameservers = ['8.8.8.8']
    domain = emailformat
    company = domain.split('.', 1)[0]
    companyname = domain.split(".")[0]
    #target = open("Output/"+companyname+"/domains.csv", 'w+')
    #target.write("Domain, IP"+"\r\n")
    frame = Frame(mainwindow,bg="white")
    if platform == "win32":
        frame.place(x=46,y=155)
    elif platform == "linux" or platform == "linux2":
        frame.place(x=20,y=155)
    Label(frame,text="Loading....\nPlease Wait.......",font=("Copperplate Gothic Bold",12),bg="white").pack()
    if platform == "win32":
        Label(frame,bg="white",text="                                                                                                                                                                                                                                          ").pack()
    elif platform == "linux" or platform == "linux2":
        Label(frame,bg="white",text="                                                                                                                                                                                           ").pack()
    label_line_progress = Label(frame, bg="#333")
    label_line_progress.pack(fill="x", expand=True, anchor="sw")

    line_progress = ttk.Progressbar(label_line_progress)
    line_progress.start(100)
    line_progress.pack(fill='x', expand=True, pady=10)
    Label(frame,text="Searching For Domain's.......",font=("Copperplate Gothic Light",10),bg="white").pack()
    html = requests.get("https://crt.sh/?q=%."+domain+"&exclude=expired").text
    soup = BeautifulSoup(html, "lxml")
    isdir = os.path.isdir(path2)
    if isdir == False and log == "Yes":
        os.mkdir(path2)
    if log == "Yes":
        timestr = time.strftime("%I_%M_%S(%d %m %Y "+str(emailformat)+")")
        target = open(path2+"/"+str(timestr)+".txt", 'w')
    for link in soup.findAll("a"):
        if stop == False:
            if "?id=" in link.get('href'):
                id = link.get('href')
                cert = requests.get("https://crt.sh/"+id).text
                myregex = r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}'
                domains = re.findall(myregex, cert)
                for i in domains:
                    if stop == False:
                        if company in i:
                            if i in found:
                                pass
                            else:
                                found.append(i)
                                try:
                                    frame.destroy()
                                except:
                                    pass
                                if frame_2 =="":
                                    frame_2 = Frame(mainwindow,bg=background_col)
                                    if platform == "win32":
                                        frame_2.place(x=692,y=389)
                                    elif platform == "linux" or platform == "linux2":
                                        frame_2.place(x=692,y=395)
                                    #Label(frame_2,bg=background_col,text="                                          ").pack()
                                    label_line_progress = Label(frame_2, bg=background_col)
                                    label_line_progress.pack(fill="x", expand=True, anchor="sw")

                                    line_progress = ttk.Progressbar(label_line_progress)
                                    line_progress.start(100)
                                    line_progress.pack(fill='x', expand=True, pady=10)
                                no = "("+str(len(found))+") "
                                if limit != 0 and stop == False:
                                    if limit >=len(found):
                                        try:
                                            public_ip = dnsresolver.query(i)[0]
                                            tabel.insert('',END,values=[len(found),i,public_ip,"Working"],tags=('ok',))
                                            tabel.yview_moveto(1)
                                            if log == "Yes":
                                                wr = str(no)+str(i)+" "+str(public_ip)+" [Working]\r"
                                                target.write(wr)
                                        except:
                                            public_ip = ""
                                            tabel.insert('',END,values=[len(found),i,"--Null--","Not Responding"],tags=('fail',))
                                            tabel.yview_moveto(1)
                                            if log == "Yes":
                                                wr = str(no)+str(i)+" --Null-- [Not Responding]\r"
                                                target.write(wr)
                                    else:
                                        if log == "Yes":
                                            target.close()
                                        main_function()
                                        return
                                else:
                                    try:
                                        public_ip = dnsresolver.query(i)[0]
                                        tabel.insert('',END,values=[len(found),i,public_ip,"Working"],tags=('ok',))
                                        tabel.yview_moveto(1)
                                        if log == "Yes":
                                            wr = str(no)+str(i)+" "+str(public_ip)+" [Working]\r"
                                            target.write(wr)
                                    except:
                                        public_ip = ""
                                        tabel.insert('',END,values=[len(found),i,"--Null--","Not Responding"],tags=('fail',))
                                        tabel.yview_moveto(1)
                                        if log == "Yes":
                                            wr = str(no)+str(i)+" --Null-- [Not Responding]\r"
                                            target.write(wr)
                    else:
                        if log == "Yes":
                            target.close()
                        return
        else:
            if log == "Yes":
                target.close()
            return

def on_scanlimitEntry_click(e):
    if limitvar.get() == 'No Limit':
        scanlimitEntry.delete(0, "end")
        scanlimitEntry.insert(0, '')
        scanlimitEntry.config(fg = 'black',font=("Comic Sans MS",12))


def on_scanlimitEntry_focusout(e):
    if limitvar.get () != 'No Limit':
        scanlimitEntry.config(fg = 'black',font=("Comic Sans MS",12))
    if limitvar.get() == '':
        limitvar.set('No Limit')
        scanlimitEntry.config(fg = 'grey',font=("Segoe Print",10))
    if limitvar.get () != 'No Limit' and limitvar.get() != '':
        try:
            int(limitvar.get ())
        except ValueError:
            messagebox.showerror("Wrong Value","Please Enter A Int Value\nOr\nLeave Blank For No Limit")
            scanlimitEntry.focus_set()

scanlimitEntry.bind('<FocusIn>', on_scanlimitEntry_click)
scanlimitEntry.bind('<FocusOut>', on_scanlimitEntry_focusout)



def on_websiteEntry_click(e):
    if webadd.get() == 'Example: google.com':
        websiteEntry.delete(0, "end")
        websiteEntry.insert(0, '')
        websiteEntry.config(fg = 'black',font=("Comic Sans MS",12))


def on_websiteEntry_focusout(e):
    if webadd.get () != 'Example: google.com':
        websiteEntry.config(fg = 'black',font=("Comic Sans MS",12))
    if webadd.get() == '':
        webadd.set('Example: google.com')
        websiteEntry.config(fg = 'grey',font=("Segoe Print",10))

websiteEntry.bind('<FocusIn>', on_websiteEntry_click)
websiteEntry.bind('<FocusOut>', on_websiteEntry_focusout)

if platform == "linux" or platform == "linux2":
    Label(mainwindow,text=" ",font=("arial",2),bg=background_col).pack()


b1 = Button(mainwindow,text="Start Scan",image=Search_icon,compound=LEFT,command=main_function,font=("Lucida Bright",11),bg="snow2")
b1.pack()

Label(mainwindow,text=" ",font=("arial",1),bg=background_col).pack()

def showAbout():
    messagebox.showinfo("About","Coding By\nHrishikesh Patra\nGitHub: Hrishi7665")


def openL():
    isdir = os.path.isdir(path2)
    if platform == "win32":
        if isdir == True:
            path =  path2.replace('/','\\')
            subprocess.Popen(f'explorer "{path}"')
        elif isdir == False:
            messagebox.showerror("Error", "Log's File Does\nNot Exits.")
    elif platform == "linux" or platform == "linux2":
        if isdir == True:
            subprocess.Popen(["xdg-open", path2])
        elif isdir == False:
            messagebox.showerror("Error", "Log's File Does\nNot Exits.")



def exit_fun ():
    ans = messagebox.askyesno("Exit", "Are You Sure,\nYou want to Exit ?")
    if ans == True:
        try:
            target.close()
        except:
            pass
        mainwindow.destroy()
        pid= os.getpid()
        os.kill(pid,signal.SIGTERM)

mainwindow.tk.call('wm', 'iconphoto', mainwindow._w, PhotoImage(file=path+'web.png'))
mainwindow.title("Domain Search Tool With GUI")
mainwindow.resizable(False,False)
mainwindow.wm_protocol ("WM_DELETE_WINDOW",exit_fun )



menubar = Menu(mainwindow)

menubar.add_command(label="Open Log File's",command=openL)
menubar.add_command(label="About", command=showAbout)
menubar.add_command(label="Exit", command=exit_fun)

mainwindow.config(menu=menubar)
mainwindow.mainloop()