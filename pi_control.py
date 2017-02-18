## GUI for raspis. I'm just learning paramiko, don't make fun of me =(
## SCT Feb. 2017

import paramiko
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
	import tkinter as tk
import time
from command_window import Command_Window
from raspberry_pi import Raspberry_Pi

def pi_connect(address):
	## Connect to a raspberry pi at location address.
	try:
		this_pi = Raspberry_Pi(address,master)
		ListOfPis.append(this_pi)
	except:
		connection_error()

def connection_error():
	error_window = tk.Toplevel(master)
	tk.Label(error_window,text="Error connecting to raspberry pis.\nMake sure you're on TCH network").pack()
	tk.Button(error_window,text="OK",command=error_window.destroy).pack()

def close_down():
	for pi in ListOfPis:
		pi.close_pi()
	master.destroy()

master = tk.Tk()
master.title('Raspberry Pi Manager')

ListOfPis = []

tk.Label(master, text="Pi address").grid(row=0)

# PUT THE IP ADDRESSES OF EACH PI HERE
# you can use a dictionary to make aliases and do it that way
# if you need help remembering who's who
ListOfAddresses=[ "10.32.64.132", "10.32.64.93", 
	"10.32.64.180", 
	"10.32.64.110"]
ListOfAliases=["Single Wells (1)", "Single Wells (2)", "Green / red water", "Green / red"]

alias_address_map = dict(zip(ListOfAliases,ListOfAddresses))

add = tk.StringVar(master)
add.set(ListOfAliases[0]) # default value

w = tk.OptionMenu(master, add, *ListOfAliases)
w.grid(row=0, column=1)
conn_button = tk.Button(master, text='Connect', command=lambda: pi_connect(alias_address_map[add.get()]))
conn_button.grid(row=0, column=2)
tk.Button(master, text='Quit', command=lambda: close_down()).grid(row=7, column=0, pady=4)
master.mainloop()
