'''
Created on Feb 11, 2016

@author: leo
'''
from contact import Contact, ContactsDb
class ContactsApp():
    print "Contacts 0.1"
    def __init__(self, prompt=":> ", quitChar='\\'):
        self.prompt = prompt
        self.quitChar = quitChar
        self.mainMenu = """   
        {}   Exit Prompt
        1   Create Contact
        2   Edit Contact
        3   Delete Contact
        4   Show Contact 
@Main{}""".format(quitChar, prompt )
        contactDb = ContactsDb('localhost', 'root', '1234', 'contacts_orm', 'contacts' )
        Contact.connect(contactDb)
        pass
    
    def run(self):
        entry = ''
        while True :
            entry = raw_input(self.mainMenu).strip()
            if  entry == '1': 
                self.createNewContactPrompt()
            elif entry == '2': 
                self.editContactPrompt()
            elif entry == '3': 
                self.deleteContactPrompt()
            elif entry == '4': 
                self.showContactPrompt()
            elif entry == self.quitChar: 
                break
            else: 
                print 'Invalid Input. Enter (1, 2, 3, 4 or \q) \n'
        pass
    
        print 'Done'
        
    def createNewContactPrompt(self):
        data = NewContactPrompt(self.prompt).run()
        contact = Contact(*data).save()
        print str(contact) + ' SAVED\n'
        
    def editContactPrompt(self):
        editor = EditContactPrompt(self.prompt)
        id = editor.readContactId()
        contact = Contact.retrieve(id)
        if contact:
            contact.name = editor.readEdittedName(contact.name)
            contact.phone = editor.readEdittedPhone(contact.phone)
            contact.gender = editor.readEdittedGender(contact.gender)
            contact.description = editor.readEdittedDescription(contact.description)
            contact.update()
            print '{} UPDATED\n'.format(contact)
        else:
            print 'Contact #{} does not exist'.format(id)
            self.editContactPrompt()
        
    def deleteContactPrompt(self):
        deleter = DeleteContactPrompt(self.prompt)
        id = deleter.readContactIdForDeletion()
        contact = Contact.retrieve(id)
        if contact:
            if contact.delete() :
                print '{} DELETED'.format(contact) 
        else:
            print 'Contact #{} does not exist'.format(id)
            self.deleteContactPrompt()
            
    def showContactPrompt(self):
        shower = ShowContactPrompt(self.prompt)
        id = shower.readContactIdToShow()
        if id == -1:
            contacts = Contact.retrieveAll()
            shower.showAll(contacts)
            return 
        
        contact = Contact.retrieve(id)
        if contact:
            shower.show(contact)
        else:
            print 'Contact #{} does not exist'.format(id)
            shower.readContactIdToShow()
        

class EditContactPrompt():
    def __init__(self, prompt):
        self.prompt = prompt
        self.editEntryTpl = "@Edit:{}[{}] or Enter to skip"+self.prompt
        
    def readContactId(self):
        enterContactId = "@Edit:"+'#id of contact to edit?'+self.prompt
        id_ = raw_input(enterContactId).strip()
        try:
            return int(id_)
        except ValueError:
            print id_+' is an invalid Id'
            self.readContactId()        
    
    def readEdittedName(self, oldName):
        editName = self.editEntryTpl.format('name', oldName)
        return raw_input(editName) or oldName
    
    def readEdittedPhone(self, oldPhone):
        editPhone = self.editEntryTpl.format('phone', oldPhone)
        return raw_input(editPhone) or oldPhone
    
    def readEdittedDescription(self, oldDescription):
        editDescription = self.editEntryTpl.format('description', oldDescription)
        return raw_input(editDescription) or oldDescription
    
    def readEdittedGender(self, oldGender):
        editGender = self.editEntryTpl.format('gender', oldGender)
        gender_ = raw_input(editGender)
        if gender_:
            genderUppercase_ = gender_.upper()
            if genderUppercase_ in ['M', 'F']:
                return genderUppercase_
            else:
                print gender_+' is invalid. Enter M or F'
                return self.readEdittedGender(oldGender)
        else:
            return oldGender
        
class DeleteContactPrompt():
    def __init__(self, prompt):
        self.prompt = prompt
        pass
    
    def readContactIdForDeletion(self):
        id_ = raw_input("@Delete:#id of contact to delete?")
        try:
            return int(id_)
        except ValueError:
            print id_+' is an invalid Id'
            self.readContactIdForDeletion()
        
class ShowContactPrompt():
    def __init__(self, prompt):
        self.prompt = prompt
        pass
    
    def readContactIdToShow(self):
        id_ = raw_input("@Show:#id of contact or -1 to view all?")
        try:
            return int(id_)
        except ValueError:
            print id_+' is an invalid Id'
            self.readContactIdToShow()
            
    def showAll(self, contacts):
        for contact in contacts:
            self.show(contact)
    
    def show(self, contact):
        contactTpl = '''
        id             :{}
        name           :{}
        gender         :{}
        phone          :{}
        description    :{}
        '''
        print contactTpl.format(contact.id, contact.name,  
                                contact.gender, contact.phone,
                                contact.description)
        
            
class NewContactPrompt():
    def __init__(self, prompt):
        self.prompt = prompt
        pass
    
    def run(self):
        while True :
            name = self.readName()
            phone = self.readPhone()
            gender = self.readGender()
            description = self.readDescription()
            return name, gender, phone, description 
            
    def readName(self):
        enterContactName = "@Create:"+'name?'+self.prompt
        name = raw_input(enterContactName).strip()
        if name :
            return name
        else:
            print 'name is required'
            self.readName()
        
    def readPhone(self):
        enterContactPhone = "@Create:"+'phone number?'+self.prompt
        phone = raw_input(enterContactPhone).strip()
        if phone:
            return phone
        else:
            print 'phone number is required'
            self.readPhone()
            
    def readGender(self):
        enterContactGender = "@Create:gender(M or F)?" 
        gender_ = raw_input(enterContactGender).strip() 
        gender = gender_.upper()   
        if gender in ['M', 'F'] :
            return gender 
        else:
            print gender_+' is invalid. Enter M or F'
            self.readGender()
            
    def readDescription(self):
        enterContactDescription = "@Create:description?"  
        description = raw_input(enterContactDescription).strip()   
        return description            
    
    
if '__main__' == __name__:
    app = ContactsApp()
    app.run()
