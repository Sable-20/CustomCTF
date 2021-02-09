from tkinter import *
from testConn import testConnection
from connection import connection
from download_client import downloader
from login_client import login
from flag_client import flagCheck

import json
import time

with open("./settings.json") as f:
    data = json.load(f)
window = Tk() #Open window
window.title(data["window"]["title"])
window.geometry(data["window"]["size"])
window.resizable(width=False, height=False)
connTest = testConnection()

PORT = 0

#Changes global port
def setPort(port):
    global PORT
    PORT = port

#Gets global port
def getPort():
    return(PORT)

#Checks if port is valid
def checkPort(port):
    if(connTest.test(port)):
        return(True)
    return(False)

#Message when entering a screen with the incorrect port
def portNotFound():
    var = StringVar()
    label = Label(window, textvariable=var, font=128, padx=10, width=10)
    var.set("Port not found!")
    back = Button(window, text = "Back", font=32, padx=10, widt=10, command= lambda: hide([label, back], 'menu'))

    label.pack(pady=(100,0))
    back.pack(pady=(100,0))

#To hide screens
def hide(events, screen):
    for event in events:
        event.destroy()
    show(screen)

#Shows the given screen
def show(screen):
    print("Screen: ", screen)
    if (screen == 'home'):
        home()
    elif (screen == 'port'):
        portScreen()
    elif (screen == 'menu'):
        menu()
    elif (screen == 'download'):
        downloadScreen()
    elif (screen == 'login'):
        loginScreen()
    elif (screen == 'flag'):
        flagScreen()
    elif (screen == 'ping'):
        pingScreen()

#home screen
def home():
    var = StringVar()
    label = Label(window, textvariable=var, height=3, font=64)
    start = Button(window, text = "Start", font=32, padx = 10, command=lambda: hide([start, label], 'port'))
    #start['command'] = hide([start, label])

    var.set("Welcome to the CTF!")
    label.pack()
    start.pack(pady=100)

#Must enter port before moving to menu screen
def portScreen():
    err_msg = Label(window, font=128)
    submit = Button(window, text = "Submit", font=32, padx = 10, command=lambda: portScreenHandler(eP.get(),[lP, eP, submit, err_msg]))
    lH = Label(window, text=data["host"])
    lP = Label(window, text="Port: ")
    eP = Entry(window, bd = 2)

    lH.pack(side = TOP, pady=(20,20))
    submit.pack(side = BOTTOM, pady=(20,20))
    lP.pack(side = LEFT, padx=(75,0))
    eP.pack(side = RIGHT, padx=(0,75))
    #print("Coming Soon")

#Too many middleman functions ... but be an easier way.
def portScreenHandler(portString, entries):
    try:
        port = int(portString)
    except ValueError:
        entries[3]['text'] = "Bad Character."
        entries[3]['bg'] = 'red'
        entries[3].place(anchor=S, rely=0.7, relx=0.5)
        return
    if(type(port) == type(1) and port <= 65535 and port >= 0 and checkPort(port)):
        setPort(port)
        print(PORT)
        entries[3].place_forget()
        hide(entries,'menu')
    else:
        entries[3]['text'] = 'Invalid port.'
        entries[3]['bg'] = 'red'
        entries[3].place(anchor=S, rely=0.7, relx=0.5)

#Menu Screen
def menu():
    var = StringVar()
    label = Label(window, textvariable=var, height=3, font=64)
    var.set("Each challenge leads to the next!")
    dB = Button(window, text = "Ping", font=32, padx=10, width=10, command = lambda: hide([label, dB, lB, fB],'ping'))
    lB = Button(window, text = "Download", font=32, padx=10, width=10, command=lambda: hide([label, dB, lB, fB],'login'))
    fB = Button(window, text = "Flag", font=32, padx=10, width=10, command=lambda: hide([label, dB, lB, fB],'flag'))

    label.pack()
    dB.pack(pady=(50,10))
    lB.pack(pady=10)
    fB.pack(pady=10)

#Screen to show hints
def hint(prevScreen):
    var = StringVar()
    label = Label(window, textvariable=var, height=3, font=64)

    back = Button(window, text = "Back", font=32, padx = 10, pady = 10)
    events = [ping, label, back]
    ping['command']=lambda: pingHandler(events)
    back['command']=lambda: hide(events, 'menu')
    var.set("Ping Me!")

    if (screen == 'port'):
        var = "Placeholder"
    elif (screen == 'menu'):
        menu()
    elif (screen == 'download'):
        downloadScreen()
    elif (screen == 'login'):
        loginScreen()
    elif (screen == 'flag'):
        flagScreen()
    elif (screen == 'ping'):
        pingScreen()

    label.grid(column=0, row=0, pady=(25,0), padx=(75,0))
    back.grid(column=0, row=1, pady=(75, 0), padx=(0,50))

# def downloadScreen():
#     print(getPort())
#     if(checkPort(getPort())): #Change to isConnected
#         var = StringVar()
#         label = Label(window, textvariable=var, height=3, font=64)
#
#         download = Button(window, text = "Download", font=32, padx = 10, pady = 10)
#         back = Button(window, text = "Back", font=32, padx = 10, pady = 10)
#         events = [download, label, back]
#         download['command']=lambda: downloadHandler(events)
#         back['command']=lambda: hide(events, 'menu')
#         var.set("Click to download the pcap file")
#
#         label.grid(column=0, row=0, padx=(50,0))
#         back.grid(column=0, row=1, pady=(50, 0), padx=(0,75))
#         download.grid(column=0, row=1, pady=(50,0), padx=(125,0))
#     else:
#         portNotFound()
#
# #Downloads file then changes events on screen
# def downloadHandler(events):
#     conn = connection()
#     server = conn.connect(getPort())
#     downloader().download(server)
#     conn.disconnect(server)
#     newVar = StringVar()
#     events[1]['textvariable'] = newVar
#     events[1]['font']=128
#     newVar.set("Done.")
#     events[0].destroy()
#     events = events[1:]
#
#     events[0].grid(column=0, row=0, padx=(110,0), pady=(25,0))
#     events[1].grid(column=0, row=1, padx=(110,0), pady=(125,0))

#Actually the download, but login kept by legacy
def loginScreen():
    if(checkPort(getPort())):
        result = Label(window, font=128) #Result Text
        login = Button(window, text = "Download", font=32, padx = 10, command=lambda: loginHandler(eUser.get(), ePass.get(), result))
        back = Button(window, text = "Back", font=32, padx = 10, command=lambda: hide([lUser, eUser, lPass, ePass, login, back, result], 'menu'))

        lUser = Label(window, text="Username:")
        eUser = Entry(window, bd = 2)
        lPass = Label(window, text="Password:")
        ePass = Entry(window, bd = 2)

        lUser.grid(column=0, row=0, padx=(50,0), pady=(100,0))
        eUser.grid(column=1, row=0, pady=(100,0))

        lPass.grid(column=0, row=1, padx=(50,0))
        ePass.grid(column=1, row=1)

        login.grid(column=1, row=2)
        back.grid(column=0, row=2, padx=(50,0))
    else:
        portNotFound()

def loginHandler(user, password, result):
    log = login()
    conn = connection()
    server = conn.connect(getPort())
    response = log.check(user, password, server)

    if (not response[0]):
        result['text'] = 'Something went wrong.' #Scapegoating
    else:
        result['text'] = response[0]
    result['bg'] = '#f0f0f0'
    print(f"response: {response[1]}")
    if(int(response[1]) == 1):
        downloader().download(server)
        result['bg'] = 'lightgrey'
        result['font']=("Courier", 10)


    result.place(anchor=S, rely=0.85, relx=0.5)
    conn.disconnect(server)



def flagScreen():
    if(checkPort(getPort())): #Change to isConnected
        result = Label(window, font=128) #Result Text
        submit = Button(window, text = "Submit", font=32, padx = 10, command=lambda: flagHandler(eFlag.get(),result))
        back = Button(window, text = "Back", font=32, padx = 10, command=lambda: hide([lFlag, eFlag, submit, back, result], 'menu'))
        lFlag = Label(window, text="Flag: ")
        eFlag = Entry(window, bd = 2)

        submit.grid(column=1, row=1, padx=(0,50), pady=(20,20))
        back.grid(column=0, row=1, padx=(50,0), pady=(20,20))
        lFlag.grid(column=0, row=0, padx=(75,0), pady=(75,0))
        eFlag.grid(column=1, row=0, padx=(0,75), pady=(75,0))
    else:
        portNotFound()

#prevCall = "" #Prevent timeouts
def flagHandler(text, result):
    #global prevCall
    #if(not result['text'] == 'Server Timed out. Please try again.' and not text == "" and prevCall == text):
    #    return
    #prevCall = text
    flagger = flagCheck()
    conn = connection()
    server = conn.connect(getPort())
    response = flagger.check(text, server) #Maybe resolve timeout issue?
    if (not response[0]):
        result['text'] = 'Something went wrong.' #Scapegoating
    else:
        result['text'] = response[0]
    result['bg'] = 'red'
    print(f"response: {response[1]}")
    if(int(response[1]) == 1):
        result['bg'] = 'green2'

    result.place(anchor=S, rely=0.7, relx=0.5)
    conn.disconnect(server)

def pingScreen():
    print(getPort())
    if(checkPort(getPort())): #Change to isConnected
        var = StringVar()
        label = Label(window, textvariable=var, height=3, font=64)

        ping = Button(window, text = "ping", font=32, padx = 10, pady = 10)
        back = Button(window, text = "Back", font=32, padx = 10, pady = 10)
        events = [ping, label, back]
        ping['command']=lambda: pingHandler(events)
        back['command']=lambda: hide(events, 'menu')
        var.set("Ping Me!")

        label.grid(column=0, row=0, pady=(25,0), padx=(75,0))
        back.grid(column=0, row=1, pady=(75, 0), padx=(0,50))
        ping.grid(column=0, row=1, pady=(75,0), padx=(175,0))
    else:
        portNotFound()

#Downloads file then changes events on screen
def pingHandler(events):
    conn = connection()
    server = conn.connect(getPort())
    server.sendall("ping".encode("utf-8"))

    timeStart = time.perf_counter()
    newVar = StringVar()
    events[1]['textvariable'] = newVar
    events[1]['font']=128
    responseCode = server.recv(1234).decode().split(";%^#&$")[0]
    timeEnd = time.perf_counter()
    conn.disconnect(server)
    newVar.set(f"{responseCode}\n{int((timeEnd-timeStart)*1000)}ms")
    events[0].destroy()
    events = events[1:]

    events[0].grid(column=0, row=0, padx=(110,0), pady=(25,0))
    events[1].grid(column=0, row=1, padx=(110,0), pady=(75,0))

show('home')

#bottomframe = Frame(root)
#bottomframe.pack( side = BOTTOM )

window.mainloop()
