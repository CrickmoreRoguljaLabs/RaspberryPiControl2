# a way to keep all the buttons in one place for a window corresponding to a Pi
import paramiko
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
	import tkinter as tk
import time
import stopwatch

class Command_Window(object):
	def __init__(self, window,ListOfProtocols):
		self.window = window
		self.ListOfProtocols = ListOfProtocols
		self.protFrame = tk.Frame(self.window)
		self.commandFrame = tk.Frame(self.window)
		self.historyFrame = tk.Frame(self.commandFrame)
		self.timerFrame = tk.Frame(self.commandFrame)
		self.videoFrame = tk.Frame(self.window)
		self.button_dict = {}
		self.command_entries = []
		self.command_labels = []
		self.command_history = []

	def set_title(self, title):
		self.window.title(title)

	def protocol_button(self,this_pi):
		protFrame = self.protFrame
		protFrame.pack(side=tk.TOP, anchor=tk.W)
		protocols = tk.StringVar(protFrame)
		protocols.set(self.ListOfProtocols[0])
		protlist = tk.OptionMenu(protFrame,protocols, *self.ListOfProtocols)
		protlist.pack(side=tk.LEFT, anchor=tk.W)
		protbut = tk.Button(protFrame, text='Run protocol',command=lambda: this_pi.run_prot(protocols.get()))
		protbut.pack(side=tk.LEFT, anchor=tk.W)
		self.button_dict['Run protocol']=protbut
		self.protFrame = protFrame

	def quit_button(self,command):
		botFrame = tk.Frame(self.window)
		botFrame.pack(side=tk.BOTTOM, anchor=tk.SW)
		button = tk.Button(botFrame, text="Quit", command=command)
		button.pack(anchor=tk.W)
		self.button_dict["Quit"] = button

	def get_button(self,name_of_button):
		return self.button_dict[name_of_button]

	def prot_specs(self,protocol_listed,pi):
		# Establish a frame with the option to send commands
		map(lambda entry: entry.destroy(), self.command_entries)
		map(lambda label: label.destroy(), self.command_labels)
		if "Send command" in self.button_dict:
			self.button_dict["Send command"].destroy()
		self.command_entries = []
		self.command_labels = []
		self.command_history = []
		self.commandFrame.destroy()
		commandFrame = tk.Frame(self.window)
		commandFrame.pack(anchor=tk.NW)
		self.historyFrame.destroy()
		callFrame = tk.Frame(commandFrame)
		callFrame.pack(side=tk.LEFT,anchor=tk.NW)
		historyFrame = tk.Frame(commandFrame)
		historyFrame.pack(side=tk.LEFT,padx=15,anchor=tk.NW)
		self.set_up_protocol(callFrame,protocol_listed)
		historyLabelFrame = tk.Frame(historyFrame)
		historyLabelFrame.pack(side=tk.TOP,anchor=tk.NW)
		tk.Label(historyLabelFrame,text="Command History").grid(row= 0, column=1)
		tk.Label(historyLabelFrame,text="Time").grid(row=1,column=0)
		tk.Label(historyLabelFrame,text="Command").grid(row=1,column=2)
		historyValFrame = tk.Frame(historyFrame)
		historyValFrame.pack(side=tk.BOTTOM)

		send_command = tk.Button(callFrame,text="Send command",command=pi.send_command)
		send_command.pack(anchor=tk.S)
		self.button_dict["Send command"] = send_command
		self.commandFrame = commandFrame
		self.historyFrame = historyFrame
		self.historyValFrame = historyValFrame

	def set_up_protocol(self, commandFrame, protocol_listed):
		## Sets up all the fields entered for each protocol
		if protocol_listed == "Paired pulse":

			self.command_labels.append(tk.Label(commandFrame,text='Well Number'))
			self.command_labels[-1].pack(anchor=tk.NW)
			self.command_entries.append(tk.Entry(commandFrame))
			self.command_entries[-1].pack(anchor=tk.NW)

			self.command_labels.append(tk.Label(commandFrame,text='Wait (min)'))
			self.command_labels[-1].pack(anchor=tk.NW)
			self.command_entries.append(tk.Entry(commandFrame))
			self.command_entries[-1].pack(anchor=tk.NW)

			self.command_labels.append(tk.Label(commandFrame,text='First pulse (ms)'))
			self.command_labels[-1].pack(anchor=tk.NW)
			self.command_entries.append(tk.Entry(commandFrame))
			self.command_entries[-1].pack(anchor=tk.NW)
			
			self.command_labels.append(tk.Label(commandFrame,text='Rest duration (s)'))
			self.command_labels[-1].pack(anchor=tk.NW)
			self.command_entries.append(tk.Entry(commandFrame))
			self.command_entries[-1].pack(anchor=tk.NW)

			self.command_labels.append(tk.Label(commandFrame,text='Second pulse (ms)'))
			self.command_labels[-1].pack(anchor=tk.NW)
			self.command_entries.append(tk.Entry(commandFrame))
			self.command_entries[-1].pack(anchor=tk.NW)

		if protocol_listed == "Flashing Lights":
			self.command_labels.append(tk.Label(commandFrame,text='Well Number'))
			self.command_labels[-1].pack(anchor=tk.NW)
			self.command_entries.append(tk.Entry(commandFrame))
			self.command_entries[-1].pack(anchor=tk.NW)

			self.command_labels.append(tk.Label(commandFrame,text='Frequency (Hz)'))
			self.command_labels[-1].pack(anchor=tk.NW)
			self.command_entries.append(tk.Entry(commandFrame))
			self.command_entries[-1].pack(anchor=tk.NW)

			self.command_labels.append(tk.Label(commandFrame,text='Pulse duration (ms)'))
			self.command_labels[-1].pack(anchor=tk.NW)
			self.command_entries.append(tk.Entry(commandFrame))
			self.command_entries[-1].pack(anchor=tk.NW)
		if protocol_listed == "Blocks":
			pass

	def open_timers(self):
		self.timerFrame.destroy()
		self.timerFrame = tk.Frame(self.commandFrame)
		self.timerFrame.pack(side=tk.LEFT,anchor=tk.NW,padx=40)
		tk.Label(self.timerFrame,text='Well Timers').pack(side=tk.TOP)
		self.indTimersFrame = tk.Frame(self.timerFrame)
		self.indTimersFrame.pack(side=tk.BOTTOM)
		self.num_Timers = 0
		butt = tk.Button(self.timerFrame,text="New timer",command=self.make_new_timer)
		butt.pack(side=tk.TOP)
		self.make_new_timer()

	def make_new_timer(self):
		new_timer = tk.Frame(self.indTimersFrame)
		new_timer.pack(side=tk.TOP)
		row_val = self.num_Timers
		timer = tk.Entry(new_timer,width=5)
		timer.insert(tk.END, 'Well #')
		timer.grid(row=row_val,column=0)
		sw = stopwatch.StopWatch(parent=new_timer)
		sw.grid(row=row_val,column=1)
		start_button = tk.Button(new_timer,text="Start",command=sw.Start)
		start_button.grid(row=row_val,column=2)
		stop_button = tk.Button(new_timer,text="Stop",command=sw.Stop)
		stop_button.grid(row=row_val,column=3)
		reset_button = tk.Button(new_timer,text="Reset",command=sw.Reset)
		reset_button.grid(row=row_val,column=4)
		self.num_Timers = self.num_Timers +1


	def remove_button(self,name_of_button):
		self.button_dict[name_of_button].pack_forget()

	def destroy(self):
		self.window.destroy()