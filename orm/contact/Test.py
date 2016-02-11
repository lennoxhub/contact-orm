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
        
    def testEditContactName(self):
        contactId = 1
        oldName, newName = 'Lennox', 'Leonard'
        oldPhone, newPhone = '02099888999', '02011222111'
        #check confirm contact's old name
        contact = self.contactsApp.retrieve(contactId)
        self.assertEquals(contact.name, oldName)
        self.assertNotEquals(contact.name, newName)
        
        #update contact's name
        contact.name = newName
        contact.phone = newPhone
        successful = self.contactsApp.update(contact)
        self.failUnless(successful)
        
        #confirm contact's new name after update
        contact = self.contactsApp.retrieve(contactId)
        self.assertEquals(contact.name, newName)
        self.assertNotEquals(contact.name, oldName)
        
    def testEditContactPhone(self):
        contactId = 1
        oldPhone, newPhone = '02099888999', '02011222111'
        #check confirm contact's old phone
        contact = self.contactsApp.retrieve(contactId)
        self.assertEquals(contact.phone, oldPhone)
        self.assertNotEquals(contact.phone, newPhone)
        
        #update contact's phone
        contact.phone = newPhone
        successful = self.contactsApp.update(contact)
        self.failUnless(successful)
        
        #confirm contact's new name after update
        contact = self.contactsApp.retrieve(contactId)
        self.assertEquals(contact.phone, newPhone)
        self.assertNotEquals(contact.phone, oldPhone)
        
class ContactDeleteTest(unittest.TestCase):
    def setUp(self):
        self.contactsApp = ContactsApp(USERNAME, PASSWORD, dbName=DBNAME)
        self.contactsApp.connect()
        self.contactsApp.save(testContact)

    def tearDown(self):
        self.contactsApp.clear()
    
    def testDeleteContactById(self):
        contactId = 1
        #check if contact #1 exist
        contact = self.contactsApp.retrieve(contactId)
        self.failUnless(contact)
        
        #delete contact #1 
        successful = self.contactsApp.delete(contactId)
        self.failUnless(successful)
        
        #confirm contact #1 no longer exist
        contact = self.contactsApp.retrieve(contactId)
        self.failIf( contact )
        #self.assertRaises(excClass, callableObj)
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()