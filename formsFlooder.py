import tkinter as tk
import timeit
from threading import Thread
import tkinter.messagebox as msg
import requests
import sys
import os


def resource_path(relative_path):
    # If compiled
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def smash():
    # First thing is to disable the button
    smashButton["state"] = tk.DISABLED
    # Run the smasher in another thread
    Thread(target=smashThread).start()


def smashThread():
    try:
        # Get the link
        link: str = linkEntry.get()
        # If no link entered
        if link == "":
            msg.showwarning(title="Attention", message="please enter a link")
            smashButton["state"] = tk.NORMAL
            return

        # Get the form spam #
        try:
            num: int = int(numEntry.get())
            if num < 0 or num > 1000:
                msg.showwarning(title="Attention", message="please enter number between 1-1000")
                smashButton["state"] = tk.NORMAL
                return
        except:
            msg.showwarning(title="Attention", message="please enter a valid number")
            smashButton["state"] = tk.NORMAL
            return

        # Start the timer
        start = timeit.default_timer()

        # Create a thread pool (don't exceed 50 threads, to respect Google servers)
        with ThreadPoolExecutor(max_workers=min(50, num)) as e:
            # Send this many forms
            for i in range(num):
                # Execute the forms API
                e.submit(send_form(link))

        # Stop the timer and show the info message
        msg.showinfo(title="finished",
                     message=f"form spammed {count - 1} times in {timeit.default_timer() - start} seconds")
        smashButton["state"] = tk.NORMAL
    except:
        msg.showerror(title="Error", message="Error, Please Try Again.")
        return


# Init GUI
root = tk.Tk()
root.title("Google Forms Flooder")
root.iconbitmap(resource_path("icon.ico"))
root.geometry("500x200")
root.resizable(width=False, height=False)

# Num of answers
numFrame = tk.LabelFrame(root, text="Number")
numFrame.place(x=20, y=10)
text = tk.Label(numFrame, text="# Of Answers:")
text.grid(row=0, column=0)
numEntry = tk.Entry(numFrame, width=10, borderwidth=2)
numEntry.grid(row=0, column=1)

# Link
linkFrame = tk.LabelFrame(root, text="Link")
linkFrame.place(x=20, y=60)
text = tk.Label(linkFrame, text="G-Forms Link:")
text.grid(row=0, column=0)
linkEntry = tk.Entry(linkFrame, width=50, borderwidth=2)
linkEntry.grid(row=0, column=1)

# Button
smashButton = tk.Button(root, text="Smash!", width=40, height=2, command=smash, borderwidth=3)
smashButton.place(x=100, y=130)

# Start GUI event loop
root.mainloop()
