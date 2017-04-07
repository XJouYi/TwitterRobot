#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import uuid
from database import DataBase
from datetime import datetime
from twitter import Twitter
from config import Config

class WeiboMessage(object):
    def __init__(self,site,moduleId,moduleName,moduleImageList):
        self.message_id = str(uuid.uuid1())
        self.message_comment = moduleName
        self.message_web_site = site
        self.message_module_id = moduleId

        self.moduleImageList = moduleImageList


class WeiboImage(object):
    def __init__(self,imageid,filepath):
        self.imageid = imageid
        self.filepath = filepath
        self.pid = ''



class TwitterTask(object):
    def __init__(self,config):
        self.config = config
        self.db = DataBase(self.config)
        self.lasttime = self.getLastTime()
        
    def getLastTime(self):
        sql = "SELECT message_time from wb_message order by message_time desc LIMIT 0,1"
        result = self.db.searchOne(sql)
        if result != None:
            return result['message_time'] 
        return None
        
    def getYeskyMessage(self):
        sql = "SELECT module_id,module_name FROM yeskysite where NOT EXISTS (SELECT message_module_id from wb_message where message_module_id = yeskysite.module_id) LIMIT 0 ,1"
        result = self.db.searchOne(sql)
        if result != None:
            moduleId = result['module_id']
            moduleName = result['module_name']
            moduleImageList = []
            sql = "SELECT image_id,filepath FROM yeskyimage WHERE module_id = '"+moduleId+"'"
            result = self.db.search(sql)
            for row in result:
                moduleImageList.append(WeiboImage(row['image_id'],row['filepath']))
            if len(moduleImageList) >0:
                return WeiboMessage('yesky',moduleId,moduleName,moduleImageList)
        return None
        
    def getMessage(self):
        return self.getYeskyMessage()

    def sendMessage(self,message):
        tw = Twitter(self.config)
        picList = []
        for image in message.moduleImageList:
            if image.filepath != None and image.filepath != '':
                pid = tw.uploadImage(image.filepath)
                print(pid)
                image.pid = pid
                picList.append(pid)
        iCount = 0    
        pids = ""
        iSend = 1;
        for i in range(len(picList)):
            pids = pids + picList[i] + ","
            iCount = iCount +1
            if iCount >= 4:
                tw.sendImage(message.message_comment + str(iSend),pids.strip())
                iSend = iSend + 1
                time.sleep(1)
                pids = ""
                iCount = 0
        if iCount > 0:
            tw.sendImage(message.message_comment + str(iSend),pids.strip())
        self.saveToDatabase(message)

    def saveToDatabase(self,message):
        sql = "Insert into wb_message values('"+message.message_id+"',now(),'"+message.message_comment+"','"+self.config.Login+"','"+message.message_web_site+"','"+message.message_module_id+"')"
        self.db.insertData(sql)
        for image in message.moduleImageList:
            sql = "Insert into wb_message_image values('"+str(uuid.uuid1())+"','"+image.imageid+"','"+image.pid+"')"
            self.db.insertData(sql)

        
    def start(self):
        while True:
            try:
                currTime = datetime.now()
                if self.lasttime == None or (currTime - self.lasttime).seconds / 60 >= 10:
                    message = self.getMessage()
                    print(message.message_comment)
                    if message != None :
                        self.sendMessage(message)
                    self.lasttime = currTime
            except Exception as e:
                print(e)
            time.sleep(120)
        
if __name__ == '__main__':
    tt = TwitterTask(Config())
    tt.start()
