from gameboard import BoardClass
import socket
import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter import messagebox

from tkinter import ttk

fields = 'Please enter your IP', 'Please enter your Port number'


def connection(entries):
    
    yn = "y"
    conn = ""

    try:
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            HOST = entries[0][1].get()
            PORT = int(entries[1][1].get())
        

            s.bind((HOST, PORT))
            s.listen()

            conn, addr = s.accept()
        
            # try:
            # HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
            # PORT = 5100  # Port to listen on (non-privileged ports are > 1023)

    except ValueError:
        yn = askstring("Port number is supposed to be an INTEGER", "If you want to continue press y/Y or else N/n: ")
        if yn == "n" or yn == "N":
            root.destroy()
    except:
        yn = askstring("Connection Problem...", "If you want to continue type y/Y or else N/n: ")
        if yn == "n" or yn == "N":
            root.destroy()
    
    if yn == "y":
        with conn:
            username1 = conn.recv(1024).decode()
            username2 = askstring('Input', 'Please enter your username, player2: ')
            while not username2.isalnum():
                username2 = askstring('Input', 'Error: No special characters can be used. Please enter a valid username with no special characters: ')

            root.destroy()
            conn.sendall(username2.encode())
            gameBoard2 = BoardClass(userName=username2, lastUserName="Farahnaz", other=username1,
                                        numWins=0, numLosses=0, numTies=0, numGames=0, conn=conn, symbol="O")

            # this is where the program will get stuck
            # until someone connects

            
                

def makeform(root, fields):
    entries = []
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=15, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
    return entries

    """
    [
        ('Host', <tkinter.Entry object .!frame.!entry>), 
        ('Port', <tkinter.Entry object .!frame2.!entry>), 
        ('Username', <tkinter.Entry object .!frame3.!entry>)]
    """


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Player 2')
    ents = makeform(root, fields)

    root.bind('<Return>', (lambda event, e=ents: connection(e)))

    b1 = tk.Button(root, text='Connect',
                   command=(lambda e=ents: connection(e)))

    b1.pack(side=tk.LEFT, padx=5, pady=5)

    b2 = tk.Button(root, text='Quit', command=root.quit)

    b2.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()
