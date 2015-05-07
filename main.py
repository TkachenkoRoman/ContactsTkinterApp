import Tkinter as tk
import os
import ttk
from contact import Contact
from contactsSerializer import ContactsSerializer
import tkSimpleDialog
import tkMessageBox
import re

class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.createWidgets()
        self.serializer = ContactsSerializer()

    def createWidgets(self):
        # list all button
        self.buttonListAll = tk.Button(self, text="List all", command=self.buttonListAllHandler)
        self.buttonListAll.grid(row=0, column=0, sticky='snew')
        #find button
        self.buttonFind = tk.Button(self, text="Find", command=self.buttonFindHandler)
        self.buttonFind.grid(row=0, column=1, sticky='snew')
        # mask button
        self.buttonMask = tk.Button(self, text="Mask", command=self.buttonMaskHandler)
        self.buttonMask.grid(row=0, column=2, sticky='snew')
        # add button
        self.buttonAdd = tk.Button(self, text="Add", command=self.buttonAddHandler)
        self.buttonAdd.grid(row=0, column=3, sticky='snew')
        # delete button
        self.buttonDelete = tk.Button(self, text="Delete", command=self.buttonDeleteHandler)
        self.buttonDelete.grid(row=0, column=4, sticky='snew')
        # treeView to display contacts
        self.createTreeView()

    def createTreeView(self):
        self.tree = ttk.Treeview(self)
        ysb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)

        self.tree["columns"]=("Name","Phone", "Address")
        self.tree.column("Name", width=150 )
        self.tree.column("Phone", width=150)
        self.tree.column("Address", width=200)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone number")
        self.tree.heading("Address", text="Address")
        self.tree['show'] = 'headings'

        self.tree.grid(columnspan=5, row=1, column=0)
        ysb.grid(row=1, column=6, sticky='ns')
        xsb.grid(columnspan=5, row=2, column=0, sticky='ew')
        self.grid()

    def fillTreeView(self, contacts):
        for contact in contacts:
            self.tree.insert("" , "end", values=(contact.Name, contact.Phone, contact.Address))

    def clearTreeView(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def buttonListAllHandler(self):
        self.clearTreeView()
        contacts = self.serializer.deserializeContacts()
        self.fillTreeView(contacts)

    def buttonFindHandler(self):
        d = FindDialog(self)
        found = False
        if d.result != None:
            print d.result
            for item in self.tree.get_children():
                values = self.tree.item(item)["values"]
                if d.result["mode"] == 'Name':
                    if d.result["find"] == str(values[0]):
                        self.tree.selection_add(item)
                        found = True
                if d.result["mode"] == 'Phone':
                    if d.result["find"] == str(values[1]):
                        self.tree.selection_add(item)
                        found = True
            if found == False:
                tkMessageBox.showinfo("Result", "Nothing found!")

    def buttonMaskHandler(self):
        d = MaskDialog(self)
        pattern = ''
        if d.result != None:
            if d.result["mask"] != '' and d.result["mask"] != None:
                for char in d.result["mask"]:
                    if char == '*':
                        pattern += '.*'
                    else:
                        pattern += char
            print "pattern", pattern
            for item in self.tree.get_children():
                values = self.tree.item(item)["values"]
                if re.search(pattern, str(values[0])):
                    print "found a match"
                    self.tree.selection_add(item)

    def buttonAddHandler(self):
        d = AddDialog(self)
        self.wait_window(d.top)
        self.buttonListAllHandler()

    def buttonDeleteHandler(self):
        contacts = []
        for item in self.tree.selection():
            values = self.tree.item(item)["values"]
            contact = Contact(values[0], values[1], values[2])
            print values[0], values[1], values[2]
            contacts.append(contact)
        self.serializer.deleteContacts(contacts)
        self.buttonListAllHandler()


class AddDialog:

    def __init__(self, parent):

        top = self.top = tk.Toplevel(parent)

        tk.Label(top, text="Name").grid(row = 0, column = 0)
        tk.Label(top, text="Phone").grid(row = 1, column = 0)
        tk.Label(top, text="Address").grid(row = 2, column = 0)

        self.entryName = tk.Entry(top)
        self.entryName.grid(row = 0, column = 1)

        self.entryPhone = tk.Entry(top)
        self.entryPhone.grid(row = 1, column = 1)

        self.entryAddress = tk.Entry(top)
        self.entryAddress.grid(row = 2, column = 1)

        buttonOk = tk.Button(top, text="OK", command=self.ok)
        buttonOk.grid(row = 3, column = 0, sticky='snew')
        buttonCancel = tk.Button(top, text="Cancel", command=self.cancel)
        buttonCancel.grid(row = 3, column = 1, sticky='snew')

    def ok(self):
        contact = Contact(str(self.entryName.get()), str(self.entryPhone.get()), str(self.entryAddress.get()))
        serializer = ContactsSerializer()
        if contact.Name != '' or contact.Phone != '' or contact.Address != '':
            serializer.addContact(contact)
        self.top.destroy()

    def cancel(self):
        self.top.destroy()

class FindDialog(tkSimpleDialog.Dialog):

    def body(self, master):

        tk.Label(master, text="Find:").grid(row=0)

        self.entryFind = tk.Entry(master)
        self.entryFind.grid(row=0, column=1)

        self.mode = tk.StringVar()
        self.mode.set('Name')

        tk.Radiobutton(master, text="Name", variable=self.mode, value='Name').grid(row=1)
        tk.Radiobutton(master, text="Phone", variable=self.mode, value='Phone').grid(row=2)

        return self.entryFind # initial focus

    def apply(self):
        findWord = str(self.entryFind.get())
        mode = self.mode.get()
        self.result = {"find": findWord, "mode": mode}

class MaskDialog(tkSimpleDialog.Dialog):

    def body(self, master):

        tk.Label(master, text="Name mask:").grid(row=0)

        self.entryMask = tk.Entry(master)
        self.entryMask.grid(row=0, column=1)

        return self.entryMask # initial focus

    def apply(self):
        mask = str(self.entryMask.get())
        self.result = {"mask": mask}

root = tk.Tk()
app = App(root)

app.mainloop()


