import tkinter as tk
import timeit
import threading
import tkinter.messagebox as msg
import requests
import sys
import os


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def smash():
    threading.Thread(target=smashThread).start()
    smashButton["state"] = tk.DISABLED


def smashThread():
    try:
        global count
        link = linkEntry.get()
        if link == "":
            msg.showwarning(title="Attention", message="please enter a link")
            smashButton["state"] = tk.NORMAL
            return
        try:
            num = int(numEntry.get())
            if num < 0 or num > 1000:
                msg.showwarning(title="Attention", message="please enter number between 1-1000")
                smashButton["state"] = tk.NORMAL
                return
        except:
            msg.showwarning(title="Attention", message="please enter a valid number")
            smashButton["state"] = tk.NORMAL
            return

        count = 1

        def spam():
            for i in range(10):
                res = requests.post(link, data=payload)
                global count
                if res.status_code == 200:
                    count += 1
                if count > num + 1:
                    return

        link = link.replace("/d/e/", "/u/0/d/e/")
        link = link.replace("/viewform", "/formResponse")
        payload = {}
        # getting the entries:
        for i in range(len(entries)):
            if entries[i].get() != "" and values[i].get():
                payload[entries[i].get()] = values[i].get()

        start = timeit.default_timer()
        for _ in range(num // 10):
            threading.Thread(target=spam).start()

        for _ in range(num % 10):
            res = requests.post(link, data=payload)
            if res.status_code == 200:
                count += 1
        while count < num + 1:
            pass
        msg.showinfo(title="finished",
                     message=f"form spammed {count - 1} times in {timeit.default_timer() - start} seconds")
        smashButton["state"] = tk.NORMAL
    except:
        msg.showerror(title="Error", message="Error, Please Try Again.")
        return


def addEntry():
    global counter
    if counter < 21:
        entry = tk.Entry(entriesFrame, width=40, borderwidth=2)
        entry.grid(row=counter, column=0)
        val = tk.Entry(entriesFrame, width=40, borderwidth=2)
        val.grid(row=counter, column=1)
        values.append(val)
        entries.append(entry)
        counter += 1
    else:
        msg.showwarning(title="Attention", message="20 entries is the max")


def removeEntry():
    global entries, values
    global counter
    if len(entries) > 1:
        entries[len(entries) - 1].destroy()
        entries.pop()
        values[len(values) - 1].destroy()
        values.pop()
        counter -= 1


counter = 1
root = tk.Tk()
root.title("Google Forms Flooder")
root.iconbitmap(resource_path("icon.ico"))
root.geometry("500x670")
root.resizable(width=False, height=False)

entriesFrame = tk.LabelFrame(root, text="entries : values")
entriesFrame.pack(side=tk.TOP)

entries = []
e = tk.Entry(entriesFrame, width=40, borderwidth=2)
e.grid(row=0, column=0)
entries.append(e)

values = []
val = tk.Entry(entriesFrame, width=40, borderwidth=2)
val.grid(row=0, column=1)
values.append(val)

numFrame = tk.LabelFrame(root, width=20, text="number")
numFrame.place(x=150, y=470)

linkFrame = tk.LabelFrame(root, width=100, text="link")
linkFrame.place(x=75, y=520)

text = tk.Label(linkFrame, text="Form's Link:")
text.grid(row=0, column=0)

linkEntry = tk.Entry(linkFrame, width=50, borderwidth=2)
linkEntry.grid(row=0, column=1)

numEntry = tk.Entry(numFrame, width=10, borderwidth=2)
numEntry.grid(row=0, column=1)

text = tk.Label(numFrame, text="Number Of Answers:")
text.grid(row=0, column=0)

add = tk.Button(root, text="add entry", width=20, height=2, command=addEntry)
add.place(x=70, y=570)

remove = tk.Button(root, text="remove entry", width=20, height=2, command=removeEntry)
remove.place(x=300, y=570)

smashButton = tk.Button(root, text="smash", width=40, height=2, command=smash)
smashButton.place(x=100, y=620)

root.mainloop()
