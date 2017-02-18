import paramiko
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
	import tkinter as tk
import time
from command_window import Command_Window

use_ssh = True

class Raspberry_Pi(object):
	# Defines the raspberry pi class with address IP_ADDRESS
	
	def __init__(self,IP_ADDRESS,master):
		self.IP_ADDRESS = IP_ADDRESS
		ListOfProtocols = ["Paired pulse", "Flashing Lights", "Blocks"]
		self.window = Command_Window(tk.Toplevel(master),ListOfProtocols)
		self.window.set_title("Raspberry Pi at: "+self.IP_ADDRESS)
		
		self.window.protocol_button(self)
		self.window.quit_button(lambda: self.close_pi())
		if use_ssh:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(IP_ADDRESS,username='pi',password='raspberry')
			self.ssh = ssh

	def run_prot(self,protocol_listed):
		# runs the protocol listed by sending a command to the Pi, which commands the Arduino
		command_dict = {"Paired pulse":"PairedPulseStim.py","Flashing Lights":"WellStim.py","Blocks":"blockStim.py"}
		if use_ssh:
			self.stdin, self.stdout, self.stderr = self.ssh.exec_command("python "+command_dict[protocol_listed])
		self.window.prot_specs(protocol_listed,self)
		self.window.open_timers()

	def send_command(self):
		# Sends the command from the command window to the raspberry pi
		command_params = [entry.get() for entry in self.window.command_entries]
		command = ",".join(command_params)
		self.update_history(command)
		if use_ssh:
			self.stdin.write(command+'\n')
			self.stdin.flush()

	def update_history(self,command):
		# Updates the command history
		self.window.command_history.append(command)
		col_size,row_size= self.window.historyValFrame.grid_size()
		tk.Label(self.window.historyValFrame,text= time.strftime('%H:%M:%S')).grid(column=0,row=row_size)
		tk.Label(self.window.historyValFrame,text= command).grid(column=2,row=row_size)


	def close_pi(self):
		# End the ssh session and close the window
		if use_ssh:
			self.ssh.close()
		self.window.destroy()