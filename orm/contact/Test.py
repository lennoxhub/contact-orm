'''
Created on Feb 11, 2016

@author: leo
'''
import unittest
from contact import ContactsApp, Contact
from _mysql_exceptions import OperationalError
USERNAME = 'root'
PASSWORD = 'leonardo'
DBNAME = 'contacts_orm'
testContact = Contact('Lennox', ContactsApp.MALE, '02099888999', 'black, short')
class TestDb(unittest.TestCase):
    def testDbConnect(self):
        self.assertTrue(ContactsApp(USERNAME, PASSWORD, dbName=DBNAME).connect())
        pass

    def testWrongPasswordForConnect(self):
        self.assertRaises(OperationalError, ContactsApp(USERNAME, 'wrongpassword', dbName=DBNAME).connect)
        

class ContactSaveTest(unittest.TestCase):
    def setUp(self):
        self.contactsApp = ContactsApp(USERNAME, PASSWORD, dbName=DBNAME)
        self.contactsApp.connect()

    def tearDown(self):
        self.contactsApp.clear()
        pass

    def testSaveNewContact(self):
        contact = self.contactsApp.save(testContact)
        self.failUnless(contact.saved())
        self.assertEquals(contact.id, 1)
        
class ContactEditTest(unittest.TestCase):
    def setUp(self):
        self.contactsApp = ContactsApp(USERNAME, PASSWORD, dbName=DBNAME)
        self.contactsApp.connect()
        self.contactsApp.save(testContact)

    def tearDown(self):
        self.contactsApp.clear()
        pass
        
    def testEditContact(self):
        contactId = 1
        oldName = 'Lennox'
        newName = 'Leonard'
        #check confirm contact's old name
        contact = self.contactsApp.retrieve(contactId)
        self.assertEquals(contact.name, oldName)
        self.assertNotEquals(contact.name, newName)
        
        #update contact's name
        contact.name = newName
        successful = self.contactsApp.update(contact)
        self.failUnless(successful)
        
        #confirm contact's new name after update
        contact = self.contactsApp.retrieve(contactId)
        self.assertEquals(contact.name, newName)
        #successful = self.contactsApp.editContactName(contactId, newName)


        
#     def testSaveNewContactFail(self):
#         name = 'Lennox'
#         gender = ContactsApp.MALE
#         phone = '02099888999'
#         description = 'black, short'
#         contact = self.contactsApp.save(name, gender, phone, description)
#         self.failIf(contact)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()