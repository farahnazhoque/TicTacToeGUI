import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter import messagebox

class BoardClass:
    
    """A simple class to note the updates and moves occurring within the game

    Attributes:
        userName (str): The usernames for players.
        otherUserName (str): This displays the username of the player against whom
        each player is playing.
        lastUserName (str): The username of the last player's turn.
        numWins (int): Number of times a player wins.
        numLosses (int): Number of times a player loses.
        numTies (int): Number of times neither players wins or loses.
        numGames (int): Number of games being started.
        conn (int): The connection between player1(client) and player2(server), defined.
        symbol (str): The move made by either player.

        """


    def __init__(self, userName = "", other = "", lastUserName = "", numWins = 0,
                 numLosses = 0, numTies = 0, numGames = 0, conn = 0,
                 symbol = "X"):
        """Make a BoardClass.

        Args:
            userName: The usernames for the players.
            otherUserName: This displays the username of the player against whom
            each player is playing.
            lastUserName: The username of the last player's turn.
            numWins: Number of times a player wins.
            numLosses: Number of times a player loses.
            numTies: Number of times neither player wins or loses.
            numGames: Number of games being started.
            conn: The connection between player1(client) and player2(server), defined.
            symbol: The move made by either player.

        """
        self._userName = userName
        self._otherUserName = other 
        self._lastUserName = lastUserName
        self._numWins = numWins
        self._numLosses = numLosses
        self._numTies = numTies
        self._numGames = numGames
        
        self._conn = conn
        self._symbol = symbol
        self.isRunning = True
        #if symbol == "X".upper():
        #    self.askUser()

        '''This is occurring simultaneously in two terminal.'''
        self.createGUI()
        if symbol == "O".upper():
            print("Got there!")
            self.root.after(500, self.receiveData)
        self.root.mainloop()

    def click(self, r, c):
        """This function creates a clean slate for the buttons using the createGUI() function
        anf then calls the updateGameBoard() function to update the symbol of the respective
        players.
        """
        if type(r)==int and type(c) == int:
            if self.buttons[r][c].cget('text') =="":
                #self.buttons[r][c].config(text=self._symbol)
                self.updateGameBoard(r,c, self._symbol)
                
                
                #send the data to other user
                data = str(r) + ',' + str(c)

                self._conn.sendall(data.encode())

                if self.isWinner() or self.boardIsFull():
                    return self.restart()
                if self.isRunning:
                    self.root.after(500, self.receiveData)
        else:
            print('Error')
            
                
        




    def createGUI(self):
        """This is the function that originally creates the graphical user interface
        for each of the players and arranges the buttons on the respective windows.
        """
        
        self.root =tk.Tk()
        

        self.root.title(self._userName)
        self.root.geometry('275x200')
        self.root.resizable(0,0)
        
        self.b1 = tk.Button(self.root, command= lambda: self.click(int(0), int(0)))
        self.b2 = tk.Button(self.root, command= lambda: self.click(int(0), int(1)))
        self.b3 = tk.Button(self.root, command= lambda: self.click(int(0), int(2)))
        self.b4 = tk.Button(self.root, command= lambda: self.click(int(1), int(0)))
        self.b5 = tk.Button(self.root, command= lambda: self.click(int(1), int(1)))
        self.b6 = tk.Button(self.root, command= lambda: self.click(int(1), int(2)))
        self.b7 = tk.Button(self.root, command= lambda: self.click(int(2), int(0)))
        self.b8 = tk.Button(self.root, command= lambda: self.click(int(2), int(1)))
        self.b9 = tk.Button(self.root, command= lambda: self.click(int(2), int(2)))

        self.b1.grid(row=10, column=2, padx = 20, pady = 10)
        self.b2.grid(row=10, column=4, padx = 20, pady = 10)
        self.b3.grid(row=10, column=6, padx = 20, pady = 10)
        self.b4.grid(row=20, column=2, padx = 20, pady = 10)
        self.b5.grid(row=20, column=4, padx = 20, pady = 10)
        self.b6.grid(row=20, column=6, padx = 20, pady = 10)
        self.b7.grid(row=30, column=2, padx = 20, pady = 10)
        self.b8.grid(row=30, column=4, padx = 20, pady = 10)
        self.b9.grid(row=30, column=6, padx = 20, pady = 10)
        self.buttons = [[self.b1, self.b2, self.b3], [self.b4, self.b5, self.b6], [self.b7, self.b8, self.b9]]
        self.label1 = tk.Label(self.root, text=f"{self._userName}'s turn!").grid(row=50, column=4)

        
    def disableButtons(self):
        """This function is first called when GUI for player2 is created but it is disabled
        as the first move should always be player1's. And when player1 gives their move, their GUI
        buttons are all disabled, and player2's buttons are enabled.
        """
        for ButtonRow in self.buttons:
            for button in ButtonRow:
                button.config(state='disabled')
        self.root.update()
        self.label1 = tk.Label(self.root, text=f"{self._otherUserName}'s turn!").grid(row=50, column=4)

    def enableButtons(self):
        """This function is called everytime each of the players have to enable the buttons of the player
        whose turn it is currently.
        """
        self.label1 = tk.Label(self.root, text="").grid(row=50, column=4)
        for ButtonRow in self.buttons:
            for button in ButtonRow:
                button.config(state='active')
        self.root.update()
        self.label1 = tk.Label(self.root, text=f"{self._userName}'s turn!").grid(row=50, column=4)

    def updateGamesPlayed(self):
        """This will be incremented every time a new game starts
        and this function is called.
        """
        self._numGames += 1


    def resetGameBoard(self):
        """This function clears the game board by replacing the
        old one with a new, clear game board every time this function
        is called.
        """

        for r in range(0, len(self.buttons)):
            for c in range(0, len(self.buttons[r])):
                self.buttons[r][c].config(text="")


    def restart(self):
        """The purpose of this function is to get input from player1
        whether or not they want to restart the game or not, and start the entire
        process if yes, or terminate the program if no.
        """
        self.updateGamesPlayed()

    
        if self._symbol == 'X':
            try:
                playAgain = askstring('Please enter Y/y and N/n ONLY', 'Do you want to play again, Y/y or N/n: ')
                assert playAgain == 'Y' or playAgain == 'y' or playAgain == 'n' or playAgain == 'N'
                if playAgain == 'y' or playAgain == 'Y':
                    self._conn.sendall('Play Again'.encode())
            
                    self.resetGameBoard()
                        
                elif playAgain == 'n' or playAgain == "N":
                    self._conn.sendall('Fun Times'.encode())
                    self.root.destroy()
                    
                    self.computeStats()
                    #self.isRunning = False
            except AssertionError:
                self.restart()
            except:
                self.restart()
                 
        else:
            playAgain = self._conn.recv(1024)
            playAgain=playAgain.decode()
    
            self.message = tk.Tk()
            self.message.title(f'Message:')
            self.message.geometry('200x50')
            self.message.config(background='black')
            self.message.resizable(0,0)
            if playAgain == 'Play Again':
                tk.Label(self.message, text=f'{self._otherUserName} wants to Play Again.').pack()
                tk.Button(self.message, text='OK', command=self.message.destroy).pack()
                self.resetGameBoard()
                return self.receiveData()
            else:
                tk.Label(self.message, text=f'{self._otherUserName} says Fun Times').pack()
                tk.Button(self.message, text='OK', command=self.message.destroy).pack()
                self.root.destroy()
                self.computeStats()

            
            #self.message.mainloop()


                 #closed it but still not closing
            return




    def receiveData(self):
        """This is called when the client player makes a move and is done when the
        server player also receives data from the client player. Here, we also
        check if a game has won or tied, in order to restart the game accordingly.
        """
        try:
            self.disableButtons()
            self.root.update()

            data = self._conn.recv(1024)
            data = data.decode()
            #converting it back to string
            data = data.split(",")
            r, c = int(data[0]), int(data[1])
            if self._symbol == "X".upper():
                self.updateGameBoard(r,c, "O".upper())
            elif self._symbol == "O".upper():
                self.updateGameBoard(r,c, "X".upper())

            self.enableButtons()
            self.root.update()

            if self.isWinner() or self.boardIsFull():
                return self.restart()

        except ValueError:
            messagebox.showerror('Error', 'We are restarting the game')
            self.resetGameBoard()
            

            
            

    def printBoard(self):
        """This function will print out the board everytime it has been updated
        by the updateGameBoard() function.
        """
        print()
        for row in self._board:
            for cell in row:
                if cell=='':
                    print("*", end='')
                else:
                    print(cell, end='')
            print()
    def updateGameBoard(self, r, c, symbol):
        """This function is called every time a player updates a move, and this
        updates it to the actual gameboard. Not only that, it also updates and
        checks the number of times a player has won or lost.
        It also checks which player made the last move, and updates the statistical
        data accordiningly.
        """


        self.buttons[r][c].config(text=symbol)
        self.root.update()


        if self.isWinner():
            if symbol == self._symbol:
                self._lastUserName = self._userName
                self._numWins += 1

            else:
                self._numLosses += 1
                self._lastUserName = self._otherUserName
        elif self.boardIsFull():
            self._numTies += 1
            if symbol == self._symbol:
                self._lastUserName = self._userName
            else:
                self._lastUserName = self._otherUserName

                
            

        

    def isWinner(self):
        """This function checks if there is a win(or loss for the other player)
        and is called when it is time to update how many times each player
        has won or lost.
        """
        board = self.buttons
        for i in range(3):
            if board[i][0].cget('text')==board[i][1].cget('text')==board[i][2].cget('text') and board[i][0].cget('text')!='':
                return True
            if board[0][i].cget('text')==board[1][i].cget('text')==board[2][i].cget('text') and board[0][i].cget('text')!='':
                return True
        if board[0][0].cget('text')==board[1][1].cget('text')==board[2][2].cget('text') and board[1][1].cget('text')!='':
            return True
        if board[0][2].cget('text')==board[1][1].cget('text')==board[2][0].cget('text') and board[1][1].cget('text')!='':
            return True
        return False

    def computeStats(self):
        """The purpose of this function is to print out the stats
        to both the players after a game is won/lost/tied.
        Prints the players user name
        Prints the user name of the last person to make a move
        prints the number of games
        Prints the number of wins
        Prints the number of losses
        Prints the number of ties

        """
        #if symbol == 'O'.upper():
        #    messagebox.showinfo('Message:', 'Fun Times!')
        self.compute = tk.Tk()
        self.compute.geometry('300x200')
        self.compute.config(background='black')
        self.compute.resizable(0,0)
        self.compute.title(f'Game Stats for: {self._userName}')
        tk.Label(self.compute, text=f'Username: {self._userName}').pack()
        tk.Label(self.compute, text=f'Number of games played: {self._numGames}').pack()
        tk.Label(self.compute, text=f'Number of wins: {self._numWins}').pack()
        tk.Label(self.compute, text=f'Number of losses: {self._numLosses}').pack()
        tk.Label(self.compute, text=f'Number of ties: {self._numTies}').pack()
        tk.Button(self.compute, text='Done', command=self.compute.destroy).pack()

        self.compute.mainloop()


    def boardIsFull(self):
        """This function checks if the gameboard is full or not, and returns
        true if it is and is called when it is time to update the number of
        ties.
        """
        board = self.buttons
        ties = False        
        count = 0
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j].cget('text') != '':
                    count += 1
            
        if count == 9:
            ties = True

        return ties
        
