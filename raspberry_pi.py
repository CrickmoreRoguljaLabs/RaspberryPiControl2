# Painful references and exchange of info back and forth between here and command_window 
import paramiko
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
	import tkinter as tk
import time
import json
import StimConstructor
import threading
import socket
from command_window import Command_Window
import logging
import datetime
import os

use_ssh = True
test_video = True

class Raspberry_Pi(object):
	# Defines the raspberry pi class with address IP_ADDRESS, controls shell interactions with the Pi using paramiko
	
	def __init__(self,ID,master,colors=["Red"]):
		self.IP_ADDRESS = ID[0]
		self.master = master
		ListOfProtocols = ["Paired pulse", "Flashing Lights", "Blocks"]
		self.window = Command_Window(tk.Toplevel(master),ListOfProtocols,pi=self,colors=colors)
		self.window.set_title(ID[1])
		self.on = True
		self.connected = False
		self.window.protocol_button(self)
		self.window.quit_button(lambda: self.close_pi())

		if use_ssh:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(ID[0],username='pi',password='raspberry')
			self.ssh = ssh
			self.sftp_client = self.ssh.open_sftp()
			self.client_socket = socket.socket()
			self.ard_client_socket = socket.socket()
			self.logging_video = False
		if (not use_ssh) or test_video:
			# for testing
			self.window.make_video_frame()
	
	def retrieve_stim_dict(self,protocol):
 	# return a dict mapping file name to a collection of blocks
		list_of_stimuli_files = [file for file in self.sftp_client.listdir('./stimuli/%s' %protocol) if file.endswith('.pi')]
		stim_dict = {}
		for file in list_of_stimuli_files:
			remote_file = self.sftp_client.open('./stimuli/%s/%s'%(protocol,file),mode='r')
			try:
	 			data = json.load(remote_file)
		 		block_list = []
		 		for block_attributes in data:
		 			block_list.append(StimConstructor.load_block(block_attributes))
		 		remote_file.close()
		 		stim_dict[file] = block_list
			except:
		 		# Live dangerously
		 		pass
		return stim_dict

	def create_video_stream(self, receiver):
		# create a stream targeted to "receiver"
		pass

	def run_prot(self,protocol_listed):
		# runs the protocol listed by sending a command to the Pi, which commands the Arduino
		#self.client_socket.close()
		self.stdin, self.stdout, self.stderr = self.ssh.exec_command("python connect.py")
		time.sleep(0.5)
		try:
			self.client_socket.connect((self.IP_ADDRESS,8400))
		except Exception as e:
			error_window = tk.Toplevel(self.master)
			tk.Label(error_window,text="This Raspberry Pi is already being used!\nIf you're sure it's free, restart the Pi\nError: %s" %e).pack()
			tk.Button(error_window,text="OK",command=error_window.destroy).pack()
			self.close_pi()
		time.sleep(0.5)
		# set up the protocol
		try:
			self.prot_client_socket = socket.socket()
			self.prot_client_socket.connect((self.IP_ADDRESS,8600))
			self.prot_client_socket.sendall(protocol_listed)
			self.prot_client_socket.close()
		except Exception as e:
			error_window = tk.Toplevel(self.master)
			tk.Label(error_window,text="This Raspberry Pi is already being used!\nIf you're sure it's free, restart the Pi\nError: %s" %e).pack()
			tk.Button(error_window,text="OK",command=error_window.destroy).pack()
			self.close_pi()
		time.sleep(0.5)
		# set up the arduino protocol
		#self.ard_client_socket.close()
		try:
			self.ard_client_socket.connect((self.IP_ADDRESS,8900))
			self.connected = True
		except Exception as e:
			error_window = tk.Toplevel(self.master)
			tk.Label(error_window,text="Arduino is busy\nIf you're sure it's free, restart the Pi\nError: %s" %e).pack()
			tk.Button(error_window,text="OK",command=error_window.destroy).pack()
			self.close_pi()
		self.window.prot_specs(protocol_listed,self)
		self.window.open_timers()
		self.stim_dict = self.retrieve_stim_dict(protocol_listed)
		self.window.button_dict['Run protocol'].destroy()
		self.window.button_dict['Run protocol'].pack_forget()

	def update_intensity(self, new_intensity):
		# Updates the green light intensity
		if use_ssh:
			self.ard_client_socket.sendall("i,%s\n" %new_intensity)
			print ("i,%s" %new_intensity)

	def send_command(self, command_entries = []):
		# For when stimulus constructor is not supported
		if command_entries == []:
			command_entries = self.window.command_entries
			command_params = [entry.get() for entry in command_entries]
			command = ",".join(command_params)
		else:
			pass
		# Sends the command from the command window to the raspberry pi
		self.update_history(command)
		if use_ssh:
			self.ard_client_socket.sendall(command+'\n')
			if self.logging_video:
				self.write_command_to_log(command)

	def command_verbatim(self,command):
		# This just explicitly sends exactly the command we want to use without messing with joining stuff
		if use_ssh:
			self.ard_client_socket.sendall(command+'\n')
			# update if logging video
			if self.logging_video:
				self.write_command_to_log(command)

	def lights_out(self):
		if use_ssh:
			pass

	def open_video_log(self,name_of_video):
		self.logging_video = True
		self.name_of_video = name_of_video
		ssh_log = paramiko.SSHClient()
		ssh_log.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh_log.connect(self.IP_ADDRESS,username='pi',password='raspberry')
		self.ssh_log = ssh_log
		self.stdin_log, self.stdout_log, self.stderr_log = self.ssh_log.exec_command("python logExperiment.py %s" %name_of_video)
		self.ssh_log.close()

	def write_command_to_log(self,command):
		pass

	def update_history(self,command):
		# Updates the command history
		self.window.command_history.append(command)
		col_size,row_size= self.window.historyValFrame.grid_size()
		tk.Label(self.window.historyValFrame,text= time.strftime('%H:%M:%S')).grid(column=0,row=row_size)
		tk.Label(self.window.historyValFrame,text= command).grid(column=2,row=row_size)

	def disconnect(self):
		self.client_socket.sendall("Off")
		self.client_socket.close()
		self.ard_client_socket.close()

	def close_pi(self):
		# End the ssh session and close the window
		if self.connected:
			self.disconnect()	
		self.ssh.close()
		self.on=False
		#if not self.window.stream is None:
		#	self.window.stream.stop()
		self.window.destroy()