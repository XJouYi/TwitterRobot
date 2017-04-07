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
        except Exception as e:
            print(e)
        finally:
           configFile.close() 

if __name__ == '__main__':
    print("hello,world")