import modal
import tkinter as tk

class modalEntry(modal.Dialog):

	def body(self,master):
		tk.Label(master, text="First:").grid(row=0, sticky="W")
		tk.Label(master, text="Second:").grid(row=1, sticky="W")
		
		self.e1 = tk.Entry(master)
		self.e2 = tk.Entry(master)

		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)

		return self.e1

	def apply(self):
		first = int(self.e1.get())
		second = int(self.e2.get())
		print(first, second)

root = tk.Tk()
d = modalEntry(root)