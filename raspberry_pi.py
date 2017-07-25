import paramiko
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
	import tkinter as tk
import time
import threading
from command_window import Command_Window

use_ssh = True
test_video = True

class Raspberry_Pi(object):
	# Defines the raspberry pi class with address IP_ADDRESS, controls shell interactions with the Pi using paramiko
	
	def __init__(self,ID,master,colors=["Red"]):
		self.IP_ADDRESS = ID[0]
		ListOfProtocols = ["Paired pulse", "Flashing Lights", "Blocks"]
		self.window = Command_Window(tk.Toplevel(master),ListOfProtocols,colors=colors)
		self.window.set_title(ID[1])

		self.window.protocol_button(self)
		self.window.quit_button(lambda: self.close_pi())

		if use_ssh:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(ID[0],username='pi',password='raspberry')
			self.ssh = ssh
			#vid_shell = paramiko.SSHClient()
			#vid_shell.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			#vid_shell.connect(ID[0],username='pi',password='raspberry')
			#self.vid_shell = vid_shell
			#self.build_video_frame(self.vid_shell)
		if (not use_ssh) or test_video:
			self.demo_video_frame()
	
	def demo_video_frame(self):
		# for testing before ssh is implemented
		self.window.make_video_frame()

	def build_video_frame(self, vid_shell):
		start_vid_button = tk.Button(self.window.videoFrame,text="Start video",command = lambda: self.start_video(start_vid_button, vid_shell))
		start_vid_button.pack()

	def start_video(self,start_vid_button,vid_shell):
		start_vid_button.destroy()
		threading.Thread(target=self.window.play_video(vid_shell)).start()
		stop_vid_button = tk.Button(self.window.videoFrame,text="Stop video",command = lambda: self.stop_video(stop_vid_button))
		stop_vid_button.pack(side=tk.BOTTOM)

	def stop_video(self,stop_vid_button):
		self.window.stop_video()
		stop_vid_button.destroy()
		self.build_video_frame(self.vid_shell)

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
		#if not self.window.stream is None:
		#	self.window.stream.stop()
		self.window.destroy()