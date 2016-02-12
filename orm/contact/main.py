'''
Created on Feb 11, 2016

@author: leo
'''
from contact import Contact, ContactsDb
class ContactsApp():
    QUIT_CHAR = '\\'  
    prompt = ":> "
    print "Contacts 0.1\n"
    quitMenu = QUIT_CHAR+"   Exit Prompt\n"
    mainMenu = quitMenu + """1   Create Contact
2   Edit Contact
3   Delete Contact
4   Show Contact
@Main"""+prompt

    def __init__(self, prompt=":> "):
        self.prompt = prompt
        contactDb = ContactsDb('localhost', 'root', 'leonardo', 'contacts_orm', 'contacts' )
        Contact.connect(contactDb)
        pass
    
    def run(self):
        entry = ''
        while True :
            self.editContactPrompt()
            entry = raw_input(ContactsApp.mainMenu).strip()
            if  entry == '1': 
                self.createNewContactPrompt()
            elif entry == '2': 
                self.editContactPrompt()
            elif entry == '3': 
                self.deleteContactPrompt()
            elif entry == '4': 
                self.showContactPrompt()
            elif entry == ContactsApp.QUIT_CHAR: 
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
        contact.name = editor.readEdittedName(contact.name)
        contact.phone = editor.readEdittedPhone(contact.phone)
        contact.gender = editor.readEdittedGender(contact.gender)
        contact.description = editor.readEdittedDescription(contact.description)
        print contact
        

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
