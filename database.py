#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymysql
from config import Config

class DataBase(object):
    def __init__(self,config):
        self.config = config
        
    def _getConnection(self):
        config = self.config
        connection = pymysql.connect(
            host=config.DB_HOST, 
            port=config.DB_PORT, 
            user=config.DB_USER, 
            passwd=config.DB_PASSWORD, 
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            db=config.DB_NAME)
        return connection
    

    def searchOne(self,sql,args=None):
        connection = self._getConnection()
        with connection.cursor() as cursor:
            cursor.execute(sql,args)
            result = cursor.fetchone()
        connection.close()
        return result
        
    def insertData(self,sql,args=None):
        connection = self._getConnection()
        with connection.cursor() as cursor:
            cursor.execute(sql,args)
        connection.commit()
        connection.close()
    

    def search(self,sql,args=None):
        connection = self._getConnection()
        with connection.cursor() as cursor:
            cursor.execute(sql,args)
            result = cursor.fetchall()
        connection.close()
        return result
if __name__ == '__main__':
    db = DataBase(Config())
    result = db.search("select * from wb_message")
    print(result)