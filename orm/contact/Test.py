'''
Created on Feb 11, 2016

@author: leo
'''
import unittest
from contact import ContactsDb, Contact
from _mysql_exceptions import OperationalError
HOST = 'localhost'
USERNAME = 'root'
PASSWORD = '1234'
TABLE = 'contacts'
DBNAME = 'contacts_orm_test'
testContact = Contact('Lennox', ContactsDb.MALE, '02099888999', 'self')
testContact2 = Contact('Leonard', ContactsDb.MALE, '03044556646', 'other self')

class TestDb(unittest.TestCase):
    def testDbConnect(self):
        self.assertTrue(ContactsDb(HOST, USERNAME, PASSWORD, DBNAME, TABLE).connect())
        pass

    def testWrongPasswordForConnect(self):
        self.assertRaises(OperationalError, ContactsDb(HOST, USERNAME, 'wrongpassword', DBNAME, TABLE).connect)
        
class ContactSaveTest(unittest.TestCase):
    def setUp(self):
        cdb = ContactsDb(HOST, USERNAME, PASSWORD, DBNAME, TABLE)
        Contact.connect(cdb)

    def tearDown(self):
        Contact.clear()
        pass

    def testSaveNewContact(self):
        contact = testContact.save()
        self.failUnless(contact.saved())
        self.assertEquals(contact.id, 1)
        
class ContactEditTest(unittest.TestCase):
    def setUp(self):
        cdb = ContactsDb(HOST, USERNAME, PASSWORD, DBNAME, TABLE)
        Contact.connect(cdb)
        testContact.save()

    def tearDown(self):
        Contact.clear()
        pass
        
    def testEditContactName(self):
        contactId = 1
        oldName, newName = 'Lennox', 'Leonard'
        #check confirm contact's old name
        contact = Contact.retrieve(contactId)
        self.assertEquals(contact.name, oldName)
        self.assertNotEquals(contact.name, newName)
        
        #update contact's name
        contact.name = newName
        successful = contact.update()
        self.failUnless(successful)
        
        #confirm contact's new name after update
        contact = Contact.retrieve(contactId)
        self.assertEquals(contact.name, newName)
        self.assertNotEquals(contact.name, oldName)
        
    def testEditContactPhone(self):
        contactId = 1
        oldPhone, newPhone = '02099888999', '02011222111'
        #check confirm contact's old phone
        contact = Contact.retrieve(contactId)
        self.assertEquals(contact.phone, oldPhone)
        self.assertNotEquals(contact.phone, newPhone)
        
        #update contact's phone
        contact.phone = newPhone
        successful = contact.update()
        self.failUnless(successful)
        
        #confirm contact's new name after update
        contact = Contact.retrieve(contactId)
        self.assertEquals(contact.phone, newPhone)
        self.assertNotEquals(contact.phone, oldPhone)
        
class ContactDeleteTest(unittest.TestCase):
    def setUp(self):
        cdb = ContactsDb(HOST, USERNAME, PASSWORD, DBNAME, TABLE)
        Contact.connect(cdb)
        testContact.save()

    def tearDown(self):
        Contact.clear()
    
    def testDeleteContactById(self):
        contactId = 1
        #check if contact #1 exist
        contact = Contact.retrieve(contactId)
        self.failUnless(contact)
        
        #delete contact #1 
        successful = contact.delete()
        self.failUnless(successful)
        
        #confirm contact #1 no longer exist
        contact = Contact.retrieve(contactId)
        self.failIf( contact )
        #self.assertRaises(excClass, callableObj)
        
class ContactRetrieveTest(unittest.TestCase):
    def setUp(self):
        cdb = ContactsDb(HOST, USERNAME, PASSWORD, DBNAME, TABLE)
        Contact.connect(cdb)
        testContact.save()
        testContact2.save() 

    def tearDown(self):
        Contact.clear()
    
    def testRetrieveContactById(self):
        contactId = 1
        #check if contact #1 exist
        contact = Contact.retrieve(contactId)
        self.failUnless(contact)
        self.assertEqual(contactId, contact.id)
        #self.assertRaises(excClass, callableObj)
        
    def testRetrieveAll(self):
        contacts = Contact.retrieveAll()
        self.assertEquals(len(contacts), 2)
        
        
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
