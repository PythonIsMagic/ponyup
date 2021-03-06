#!/usr/bin/env python3
"""
  " Module for running the poker game in a tkinter GUI
  " Might have to do: sudo apt-get install tk-dev python-tk"
  """

import Tkinter
import tkMessageBox
from Tkconstants import *
from Tkinter import Frame, Button, Label, Menu

mb = tkMessageBox

errmsg = 'POKER HAS NOT YET BEEN IMPLEMENTED!\nBILL GATES PWNS U!!!!!!'


class QuitButton(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        widget = Button(self, text='Quit', command=self.quit)
        widget.pack(side=LEFT, expand=YES, fill=BOTH)

    def quit(self):
        if mb.askyesno('verify', 'do you really want to quit?'):
            quit()
        else:
            mb.showinfo('No', 'Quit has been cancelled')


class SplashScreen(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        labelfont = ('times', 20, 'bold')
        title = Label(self, text='PonyUp Poker')
        title.config(bg='black', fg='yellow')
        title.config(font=labelfont)
        title.config(height=2, width=30)
        title.pack(side=TOP)

        # Settings for the smaller text
        smconf = {
            'bg': 'black',
            'fg': 'yellow',
            'font': ('times', 12, 'bold'),
            'width': 30,
        }

        title2 = Label(self, text='Card Room')
        title2.config(smconf)
        title2.pack(side=TOP)

        company = Label(self, text='AoristTwilist Productions(2016)')
        company.config(smconf)
        company.pack(side=TOP)

        author = Label(self, text='Author: Erik Lunna')
        author.config(smconf)
        author.pack(side=TOP)


class MainMenu(Frame):
    """ Main menu screen and lobby """
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        menu = Menu()
        parent.config(menu=menu)

        gameMenu = Menu(menu)
        menu.add_cascade(label="File", menu=gameMenu)
        gameMenu.add_command(label="New Player", command=self.dont)
        gameMenu.add_command(label="Open Player", command=self.dont)
        gameMenu.add_command(label="Save Player", command=self.dont)
        gameMenu.add_command(label="Delete Player", command=self.dont)
        gameMenu.add_separator()
        gameMenu.add_command(label="Exit", command=self.dont)

        helpMenu = Menu(menu)

        menu.add_cascade(label="Edit", menu=helpMenu)
        helpMenu.add_command(label="Help", command=self.dont)
        helpMenu.add_command(label="Credits", command=self.dont)
        gameMenu.add_separator()
        helpMenu.add_command(label="About", command=self.dont)

    def dont(self):
        print('Octavia cellos')


class Lobby(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()


def main():
    """ Main entry point """
    # root = tk.Tk()
    root = Tkinter.Tk()
    SplashScreen(root).pack()
    QuitButton(root).pack()
    MainMenu(root).pack()

    Button(text='Poker', command=(lambda: mb.showerror('Pokerz', errmsg))).pack(fill=X)

    root.mainloop()


if __name__ == "__main__":
    main()
