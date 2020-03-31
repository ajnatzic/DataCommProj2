# Some starter code from: https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
# Created by AJ Natzic

import socket
import sys
import threading
import tkinter as tk
import webbrowser

# Used to listen for peer (acts as host)
def listen(portd, si) :
    si = socket.socket()
    si.bind(('', portd))
    print ("socket binded to " + str(portd))

    # put the socket into listening mode
    si.listen(5)
    print ("socket is listening")
    c, addr = si.accept()
    print("Got a connection from ", addr)
    return c

# Used to connect to peer (acts as client)
def connect(port, s, host) :
    s.connect((host, port))
    return s

# Function used to recieve messages up to 4096 characters
def receive(s):
    while True:
        data = (s.recv(4096)).decode()  # decode message from sender
        if not data: sys.exit(0)
        messageList.insert(tk.END, data)

# Used to send message with nametag
def send(s, toSend):
        sendString = toSend.get()   # Get message from textbox
        toSend.set("")  # Clear textbox for next message
        sent = name + ": " + sendString # Append nametag and send to reciever
        messageList.insert(tk.END, sent)
        s.sendall(sent.encode())

# Function that will open a browser to the emoji webpage users can copy and paste emojis from
def emoji(event=None):
    webbrowser.open('https://getemoji.com/', new=2)

# Function to close the connection (used with quit button)
def close(s):
    s.close()
    exit(0)


s = socket.socket()

# Prompt user for input for GUI
host = input("Enter host address (can be localhost): ")
port = int(input("Enter port: "))
name = input("Finally, enter the name you want to use: ")

# If peer cannot connect to host server, it will automatically become the new host
try:
    connect(port, s, host)
    c = s
except:
    print("%s, you are now the host at address %s:%s" % (name, host, port))
    c = listen(port, s)

# Instantiate GUI elements
master = tk.Tk()
master.title('P2P Python Chat')
messageFrame = tk.Frame(master)
scroll = tk.Scrollbar(messageFrame)
messageList = tk.Listbox(messageFrame, height = 20, width = 50, yscrollcommand = scroll.set, font= 36)
scroll.pack(side = tk.RIGHT, fill = tk.Y)
messageList.pack(side = tk.LEFT, fill = tk.BOTH)
messageList.pack()
messageFrame.pack()
messageList.insert(tk.END, "Welcome to Quarantine chat, %s!" % (name))
messageList.insert(tk.END, "To use emojis, click the emoji button and copy/paste.")


# Creates text field input
toSend = tk.StringVar()
toSend.set("")
messageField = tk.Entry(master, textvariable = toSend)

# Creates send button
sendButton = tk.Button(master, text = "Send", bg='#42f54b', fg='#000000', command = lambda: send(c, toSend) )

# Creates emoji button
emoji_button = tk.Button(master, text="Emoji 😀", bg='#0052cc', fg='#ffffff', command = emoji)

# Button used to close the connection
closeButton = tk.Button(master, text = "Quit", bg='#ff0000', fg='#ffffff', command = lambda: close(c))

# Pack all elements into the GUI
messageField.pack()
sendButton.pack()
emoji_button.pack()
closeButton.pack()

threading.Thread(target = receive, args=(c,)).start()
# Build the GUI
master.mainloop()
