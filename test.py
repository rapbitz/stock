import tkinter as tk
 
root = tk.Tk()
root.title("Tk dropdown example")
 
# Add a grid
mainframe = tk.Frame(root)
mainframe.grid(column=0,row=0, sticky=(tk.N,tk.W,tk.E,tk.S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 100, padx = 100)
 
# Create a Tkinter variable
tkvar = tk.StringVar(root)
 
# Dictionary with options
choices = { 'Pizza','Lasagne','Fries','Fish','Potatoe'}
tkvar.set('Pizza') # set the default option
 
popupMenu = tk.OptionMenu(mainframe, tkvar, *choices)
tk.Label(mainframe, text="Choose a dish").grid(row = 1, column = 1)
popupMenu.grid(row = 2, column =1)
 
# on change dropdown value
def change_dropdown(*args):
    print( tkvar.get() )
 
# link function to change dropdown
tkvar.trace('w', change_dropdown)
 
root.mainloop()