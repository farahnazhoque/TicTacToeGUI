# echo-client.py
from gameboard import BoardClass
import socket
import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter import messagebox


from tkinter import ttk
yn = 'y'

fields = 'Host', 'Port'


def connection(entries):

    try:
        HOST = entries[0][1].get()
        PORT = int(entries[1][1].get())
        yn = True
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            s.connect((HOST, PORT))
            userName1 = askstring("Input", "Please enter your username, player1: ")
            while not userName1.isalnum():
                userName1 = askstring('Input', 'Error: No special characters can be used. Please enter a valid username with no special characters: ')
                if userName1.isalnum():
                    break
            s.sendall(userName1.encode())
            root.destroy()
            username2 = s.recv(1024).decode()
            gameBoard1 = BoardClass(userName=userName1, lastUserName= "Ali", other = username2,
                                                        numWins = 0, numLosses = 0, numTies = 0, numGames = 0,
                                                        conn = s, symbol = "X")
        if not gameBoard1.isRunning:
            root.destroy()
        
    except ValueError:
        yn = messagebox.askyesno("Yes|No", "Port number is supposed to be an INTEGER. If you want to continue press y/Y or else N/n: ")
        if not yn:
            root.destroy()
    except:
        yn = messagebox.askyesno("Yes|No", "Connection Problem. If you want to continue press y/Y or else N/n: ")
        if not yn:
            root.destroy()

    


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

    """pyth
    [
        ('Host', <tkinter.Entry object .!frame.!entry>), 
        ('Port', <tkinter.Entry object .!frame2.!entry>), 
        ('Username', <tkinter.Entry object .!frame3.!entry>)]
    """


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Player 1')
    ents = makeform(root, fields)

    root.bind('<Return>', (lambda event, e=ents: connection(e)))

    b1 = tk.Button(root, text='Connect',
                   command=(lambda e=ents: connection(e)))

    b1.pack(side=tk.LEFT, padx=5, pady=5)

    b2 = tk.Button(root, text='Quit', command=root.quit)

    b2.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()
