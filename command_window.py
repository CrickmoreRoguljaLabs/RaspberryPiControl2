# a way to keep all the buttons in one place for a window corresponding to a Pi
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
	import tkinter as tk
import time
import stopwatch
from receive_image import VideoStream
import threading

class Command_Window(object):
	def __init__(self, window,ListOfProtocols,colors=["Red"],port=8000):
		self.window = window
		self.ListOfProtocols = ListOfProtocols
		self.protFrame = tk.Frame(self.window)
		self.commandFrame = tk.Frame(self.window)
		self.historyFrame = tk.Frame(self.commandFrame)
		self.timerFrame = tk.Frame(self.commandFrame)
		self.videoFrame = tk.Frame(self.window)
		self.videoFrame.pack(side=tk.RIGHT)
		self.button_dict = {}
		self.command_entries = []
		self.command_labels = []
		self.command_history = []
		self.stream = None
		self.panel = None
		self.stop_vid = threading.Event()
		self.colors = colors

	def set_title(self, title):
		self.window.title(title)

	def demo_play_video(self, port=8000):
		# for testing when ssh is off
		pass 

	def play_video(self,vid_shell,port=8000):
		stream=VideoStream(port=port,vid_shell=vid_shell)
		time.sleep(1)
		threading.Thread(target=stream.play_video).start()
		print self.stop_vid.is_set()
		while not self.stop_vid.is_set():
			frame = stream.read()
			print frame
			if self.panel is None:
				self.panel = tk.Label(self.videoFrame,image=frame)
				self.panel.image = frame
				self.panel.pack(side=tk.TOP, padx=10, pady=10)
		
				# otherwise, simply update the panel
			else:
				self.panel.configure(image=frame)
				self.panel.image = frame

	def stop_video(self):
		self.stop_vid.set()

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
			self.command_labels[-1].pack(anchor=tk.N)
			self.command_entries.append(tk.Entry(commandFrame))
			self.command_entries[-1].pack(anchor=tk.N)
			# if there are multiple colors, make multiple color command frames
			colorFrame = tk.Frame(commandFrame)
			colorFrame.pack(side=tk.TOP)
			color_frame_dict = {}
			for color in self.colors:
				frame = tk.Frame(colorFrame)
				frame.pack(side=tk.RIGHT)
				tk.Label(frame,text=color).pack(side=tk.TOP)
				# To revert, replace "frame" with "commandFrame"
				self.command_labels.append(tk.Label(frame,text='Wait (min)'))
				self.command_labels[-1].pack(anchor=tk.NW)
				self.command_entries.append(tk.Entry(frame))
				self.command_entries[-1].pack(anchor=tk.NW)

				self.command_labels.append(tk.Label(frame,text='First pulse (ms)'))
				self.command_labels[-1].pack(anchor=tk.NW)
				self.command_entries.append(tk.Entry(frame))
				self.command_entries[-1].pack(anchor=tk.NW)
				
				self.command_labels.append(tk.Label(frame,text='Rest duration (s)'))
				self.command_labels[-1].pack(anchor=tk.NW)
				self.command_entries.append(tk.Entry(frame))
				self.command_entries[-1].pack(anchor=tk.NW)

				self.command_labels.append(tk.Label(frame,text='Second pulse (ms)'))
				self.command_labels[-1].pack(anchor=tk.NW)
				self.command_entries.append(tk.Entry(frame))
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
		butt = tk.Button(self.indTimersFrame,text="New timer",command=self.make_new_timer)
		butt.pack(side=tk.BOTTOM,anchor=tk.N)
		self.make_new_timer()

	def make_new_timer(self):
		new_timer = tk.Frame(self.indTimersFrame)
		new_timer.pack(side=tk.TOP,anchor=tk.N)
		timer = tk.Entry(new_timer,width=5)
		timer.insert(tk.END, 'Well #')
		timer.pack(side=tk.LEFT)
		sw = stopwatch.StopWatch(parent=new_timer)
		sw.pack(side=tk.LEFT)
		start_button = tk.Button(new_timer,text="Start",command=sw.Start)
		start_button.pack(side=tk.LEFT)
		stop_button = tk.Button(new_timer,text="Stop",command=sw.Stop)
		stop_button.pack(side=tk.LEFT)
		reset_button = tk.Button(new_timer,text="Reset",command=sw.Reset)
		reset_button.pack(side=tk.LEFT)
		destroy_button = tk.Button(new_timer,text="Destroy",command= lambda: self.destroy_timer(timer,sw,start_button,stop_button,reset_button,destroy_button))
		destroy_button.pack(side=tk.LEFT)

	def destroy_timer(self, *args):
		for arg in args:
			arg.destroy()

	def remove_button(self,name_of_button):
		self.button_dict[name_of_button].pack_forget()

	def destroy(self):
		self.window.destroy()