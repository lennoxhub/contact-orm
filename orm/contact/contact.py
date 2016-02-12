'''
Created on Feb 11, 2016

@author: leo
'''
import MySQLdb as mdb
UNDEFINED_ID = None
class ContactsDb(object):
    MALE = 'male'
    FEMALE = 'female'
    def __init__(self, host, username, password, dbName, tableName):
        self.dbUsername = username
        self.dbPassword = password
        self.dbHost = host
        self.dbName = dbName
        self.tableName = tableName
        pass
    
    def connect(self):
        self.conn = mdb.connect(self.dbHost, self.dbUsername, self.dbPassword, self.dbName)
        return True
    
    def save(self, contact):
        return self._insert(contact)
    
    def retrieve(self, contactId):
        cursor = self.conn.cursor()
        try:
            sql = """SELECT name, gender, phone, description, id FROM {}
                     WHERE id = '{}'""".format(self.tableName, contactId)
            
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                return Contact(row[0], row[1], row[2], row[3], id = row[4])
            else:
                return None
        except Exception, e:
            self.conn.rollback()
            raise e

    
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
            return contact
        except Exception, e:
            self.conn.rollback()
            raise e

    def clear(self):
        cursor = self.conn.cursor()
        try:
            sql = "TRUNCATE TABLE {}".format(self.tableName)
            cursor.execute(sql)
            self.conn.commit()
        except Exception, e:
            self.conn.rollback()
            raise e 
        
    def update(self, contact):
        cursor = self.conn.cursor()
        try:
            sql = """UPDATE {} SET name='{}', gender='{}', phone='{}', description='{}' 
                    WHERE id='{}'""".format(self.tableName, 
                                            contact.name, 
                                            contact.gender, 
                                            contact.phone, 
                                            contact.description, 
                                            contact.id)
            cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception, e:
            self.conn.rollback()
            raise e 
        
    def delete(self, id):
        cursor = self.conn.cursor()
        try:
            sql = """DELETE FROM {} WHERE id='{}'""".format(self.tableName, id)
            cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception, e:
            self.conn.rollback()
            raise e 
        
            
        
class Contact():
    @classmethod
    def connect(cls, contactDb):
        cls.contactDb = contactDb
        cls.contactDb.connect()
       
    @classmethod 
    def clear(cls):
        cls.contactDb.clear()
        
    @classmethod
    def retrieve(cls, id):
        return cls.contactDb.retrieve(id)
        
    def __init__(self, name, gender, phone, description, id=UNDEFINED_ID):
        self.name = name
        self.gender = gender
        self.phone = phone
        self.description = description
        self.id = id
        
    def save(self):
        return Contact.contactDb.save(self)
    
    def delete(self):
        if self.id:
            return Contact.contactDb.delete(self.id)
        return False
    
    def update(self):
        if self.id:
            return Contact.contactDb.update(self)
        return False
    
    def __repr__(self):
        return '#{} {} ({}) {} phone:{}'.format(self.id, self.name, self.gender,
                                                self.description, self.phone)
    
    def __str__(self):
        return self.__repr__()
        
        
    def saved(self):
        return self.id != UNDEFINED_ID  
    
    