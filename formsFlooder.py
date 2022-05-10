import tkinter as tk
import timeit
from threading import Thread
import tkinter.messagebox as msg
import requests
import sys
import os
from FormsAPI import send_form
from concurrent.futures import ThreadPoolExecutor
from traceback import format_exc


def resource_path(relative_path):
    # If compiled
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def enableButton():
    # Revert text
    smashButton["text"] = "Smash!"
    # Revert state
    smashButton["state"] = tk.NORMAL

def disableButton():
    # Set state and text
    smashButton["text"] = "Smashing..."
    smashButton["state"] = tk.DISABLED   

def smash():
    # First thing is to disable the button
    disableButton()
    # Run the smasher in another thread
    Thread(target=smashThread).start()


success = 0
def form_callback(link: str) -> None:
    global success
    # If form was successfully sent
    if send_form(link):
        success += 1

def smashThread():
    global success
    try:
        # Get the link
        link: str = linkEntry.get()
        # If no link entered
        if link == "":
            msg.showwarning(title="Attention", message="please enter a link")
            enableButton()
            return

        # Get the form spam #
        try:
            num: int = int(numEntry.get())
            if num < 0 or num > 1000:
                msg.showwarning(title="Attention", message="please enter number between 1-1000")
                enableButton()
                return
        except:
            msg.showwarning(title="Attention", message="please enter a valid number")
            enableButton()
            return

        # Start the timer
        start = timeit.default_timer()

        # Create a thread pool (don't exceed 50 threads, to respect Google servers)
        with ThreadPoolExecutor(max_workers=min(50, num // 10 + 3)) as e:
            # Send this many forms
            for i in range(num):
                # Execute the form callback (wrapper)
                e.submit(form_callback(link))

        # Stop the timer and show the info message
        msg.showinfo(title="Finished!",
                     message=f"Form spammed {success} times in {round(timeit.default_timer() - start, 1)} seconds.")
        enableButton()
    except Exception as e:
        # Print traceback
        print(format_exc())
        msg.showerror(title="Error", message="Please check logs/console for more info.")


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
