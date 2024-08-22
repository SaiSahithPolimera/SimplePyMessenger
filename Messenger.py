# Program to enable chatting from GUI using sockets.

import tkinter as tk
from PIL import Image, ImageTk
import threading
import socket

def start_chatting():
	global client
	client = socket.socket()
	client.connect(('localhost', 3690))

	def client_receive():
		client.send(bytes(name.get(), 'utf-8'))
		while True:
			try:
				message = client.recv(1024).decode('utf-8')
				chat_box.config(state = tk.NORMAL)
				chat_box.insert(tk.END, message + '\n')
				chat_box.config(state = tk.DISABLED)
			except:
				chat_box.config(state = tk.NORMAL)
				chat_box.insert(tk.END, 'Error!\n')
				chat_box.config(state = tk.DISABLED)
				client.close()
				break

	def client_send(event = None):
		message = f'{input_box.get()}'
		input_box.delete(0, tk.END)
		client.send(bytes(message, 'utf-8'))

	receive_thread = threading.Thread(target = client_receive)
	receive_thread.start()

	send_button.config(command = client_send)
	root.bind('<Return>', client_send)

def clear_chat():
	chat_box.config(state = tk.NORMAL)
	chat_box.delete(1.0, tk.END)
	chat_box.config(state = tk.DISABLED)

def submit_name():
	name_entry_frame.pack_forget()
	start_chatting()

root = tk.Tk()
root.title("Chat Box")
root.config(bg = '#7F7FFF')

chat_box = tk.Text(root, state = tk.DISABLED, bg = '#2B2B2B', fg = 'white')
chat_box.pack(padx = 10, pady = 10)

input_frame = tk.Frame(root, bg = '#C1C1CD')
input_frame.pack(padx = 10, pady = 10)

name_entry_frame = tk.Frame(root)
name_entry_frame.pack(padx = 10, pady = 10)

name_label = tk.Label(name_entry_frame, text = "Enter your name:")
name_label.pack(side = tk.LEFT)

name = tk.StringVar()
name_entry = tk.Entry(name_entry_frame, width = 30, textvariable = name)
name_entry.pack(side = tk.LEFT)

submit_button = tk.Button(name_entry_frame, text = "Submit", command = submit_name)
submit_button.pack(side = tk.LEFT, padx = 5)

input_box = tk.Entry(input_frame, width = 86)
input_box.pack(side = tk.LEFT, padx = 5)

image = Image.open('icon.png')
img = image.resize((25,25))
send_icon = ImageTk.PhotoImage(img)
send_button = tk.Button(input_frame,image = send_icon, text = "Send")
send_button.pack(side = tk.LEFT, padx = 5)

clear_button = tk.Button(input_frame, text = "Clear Chat", command = clear_chat)
clear_button.pack(side = tk.LEFT, padx = 5)

name_entry_frame.pack()
name_entry.focus()

root.mainloop()