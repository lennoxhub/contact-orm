'''
Created on Feb 11, 2016

@author: leo
'''
import unittest
from contact import ContactsApp
from _mysql_exceptions import OperationalError
USERNAME = 'root'
PASSWORD = 'leonardo'
DBNAME = 'contacts_orm'

class TestDb(unittest.TestCase):
    def testDbConnect(self):
        self.assertTrue(ContactsApp(USERNAME, PASSWORD, dbName=DBNAME).connect())
        pass

    def testWrongPasswordForConnect(self):
        self.assertRaises(OperationalError, ContactsApp(USERNAME, 'wrongpassword', dbName=DBNAME).connect)
        

class Test(unittest.TestCase):
    def setUp(self):
        self.contactsApp = ContactsApp(USERNAME, PASSWORD, dbName=DBNAME)
        self.contactsApp.connect()

    def tearDown(self):
        self.contactsApp.clear()
        pass

    def testSaveNewContact(self):
        name = 'Lennox'
        gender = ContactsApp.MALE
        phone = '02099888999'
        description = 'Black, short'
        contact = self.contactsApp.save(name, gender, phone, description)
        self.failUnless(contact.saved())
        self.assertEquals(contact.id, 1)

    
    
        
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