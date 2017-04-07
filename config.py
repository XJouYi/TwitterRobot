#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json

class Config(object):
    def __init__(self):
        path = sys.path[0] + "/config.json"
        configFile = open(path,'r')
        try:
            configJson = json.load(configFile)
            self.Login = configJson["login_code"]
            self.Password = configJson["password"]
            self.Proxy = configJson["proxy"]
            self.ProxyUrl = configJson["proxy_url"]
            
            self.DB_HOST = configJson["DB_HOST"]
            self.DB_PORT = configJson["DB_PORT"]
            self.DB_USER = configJson["DB_USER"]
            self.DB_PASSWORD = configJson["DB_PASSWORD"]
            self.DB_NAME = configJson["DB_NAME"]
        except Exception as e:
            print(e)
        finally:
           configFile.close() 

if __name__ == '__main__':
    print("hello,world")