'''
Created on Feb 11, 2016

@author: leo
'''
import MySQLdb as mdb
UNDEFINED_ID = None
class ContactsApp(object):
    MALE = 'male'
    FEMALE = 'female'
    def __init__(self, username, password, host="localhost", dbName=''):
        self.dbUsername = username
        self.dbPassword = password
        self.dbHost = host
        self.dbName = dbName
        pass
    
    def connect(self):
        self.conn = mdb.connect(self.dbHost, self.dbUsername, self.dbPassword, self.dbName)
        return True
    
    def save(self, name, gender, phone, description, id=UNDEFINED_ID):
        contact = Contact(name, gender, phone, description)
        return self._insert(contact)
    
    def _insert(self, contact):
        cursor = self.conn.cursor()
        try:
            sql = """INSERT INTO contacts(name, gender, phone, description) 
                     VALUES ('{}', '{}', '{}', '{}')""".format(
                                                            contact.name, 
                                                            contact.gender,
                                                            contact.phone,
                                                            contact.description
                                                        )
            
            cursor.execute(sql)
            self.conn.commit()
            id = cursor.lastrowid
            contact.id = id
            print id
            return contact
        except Exception, e:
            self.conn.rollback()
            raise e

    def clear(self):
        cursor = self.conn.cursor()
        try:
            sql = "TRUNCATE TABLE contacts"
            cursor.execute(sql)
            self.conn.commit()
        except Exception, e:
            self.conn.rollback()
            raise e 
        
class Contact():
    def __init__(self, name, gender, phone, description, id=UNDEFINED_ID):
        self.name = name
        self.gender = gender
        self.phone = phone
        self.description = description
        self.id = id
        
    def saved(self):
        return self.id != UNDEFINED_ID    