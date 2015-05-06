__author__ = 'roman'

import pickle
from contact import Contact

class ContactsSerializer:
    def serializeContacts(self, contacts):
        with open('book.pickle', 'wb') as f:
	        pickle.dump(contacts, f)

    def deserializeContacts(self):
        with open('book.pickle', 'rb') as f:
	        return pickle.load(f)

    def addContact(self, contact):
        contacts = self.deserializeContacts()
        contacts.append(contact)
        self.serializeContacts(contacts)

    def deleteContacts(self, contactsToDelete):
        contacts = self.deserializeContacts()
        for contactToDelete in contactsToDelete:
            for contact in contacts:
                if unicode(contact.Name) == str(contactToDelete.Name) and unicode(contact.Phone) == str(contactToDelete.Phone):
                    contacts.remove(contact)
        self.serializeContacts(contacts)

    def getInitialData(self):
        serializer = ContactsSerializer()
        contacts = []
        contacts.append(Contact("Roman", "1234567", "Roman Adress here"))
        contacts.append(Contact("Grisha", "9873451", "Grisha Adress here"))
        contacts.append(Contact("Andru", "7352531", "Andru Adress here"))
        serializer.serializeContacts(contacts)
        return contacts

