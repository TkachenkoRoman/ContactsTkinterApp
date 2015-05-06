__author__ = 'roman'


class Contact:
    Name = ''
    Phone = ''
    Address = ''

    def __init__(self, name, phone, address):
        self.Name = name
        self.Phone = phone
        self.Address = address

    def getDataInArray(self):
        data = []
        data.append(self.Name)
        data.append(self.Phone)
        data.append(self.Address)
        data.append(False)
        print(data)
        return data
