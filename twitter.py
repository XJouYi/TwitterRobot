#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import os
import socks
import json
import random
from bs4 import BeautifulSoup
from config import Config

class Twitter(object):
    def __init__(self,config):
        self.config = config
        user_agent = (
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) '
            'Chrome/20.0.1132.57 Safari/536.11'
        )
        self.session = requests.session()
        self.session.headers = {
            "User-Agent":user_agent
        }
        # 代理
        if self.config.Proxy :
            self.session.proxies = { "http": self.config.ProxyUrl, "https": self.config.ProxyUrl, } 
        
        self.getToken()
        self.login()
        self.getHotTips()

    def getToken(self):
        soup = BeautifulSoup(self.session.get('https://twitter.com').content,'lxml')
        token = soup.find_all('input',{'name':'authenticity_token'})
        self.authenticity_token = token[0].get('value')
        print('token',token[0].get('value'))


    def login(self):
        data = {
            'session[username_or_email]' :self.config.Login,
            'session[password]': self.config.Password,
            'remember_me':1,
            'return_to_ssl':'true',
            'scribe_log':'',
            'redirect_after_login':'/?lang=zh-cn',
            'authenticity_token':self.authenticity_token
        }
        resp = self.session.post('https://twitter.com/sessions',data = data)
        
        
    def getHotTips(self):
        resp = self.session.get('https://twitter.com/i/trends?pc=true&show_context=true&src=module')
        text = resp.content
        text = text.replace(r'\"',"'")
        text = text.replace(r"\n","")
        textJson = json.loads(text)
        soup = BeautifulSoup(textJson['module_html'],'lxml')
        lis = soup.find_all('li')
        self.hotTips = []
        for item in lis:
            tip = item.get('data-trend-name')
            if tip != None:
                self.hotTips.append(tip)
        
    def getRandomTips(self):      
        if self.hotTips == None or len(self.hotTips) == 0:
            return ""
        iCount = random.randint(0,len(self.hotTips)-1)
        return self.hotTips[iCount]
        
    def sendText(self,test):
        data = {
            'authenticity_token' : self.authenticity_token,
            'is_permalink_page' : 'false',
            'place_id':'',
            'status': test,
            'tagged_users':''
        }
        self.session.headers["origin"]="https://twitter.com"
        self.session.headers["referer"]="https://twitter.com/"
        self.session.headers["x-twitter-active-user"] = 'yes'
        resp = self.session.post('https://twitter.com/i/tweet/create',data = data)
        print(resp.content)
        
    def uploadImage(self,path):
        size = os.path.getsize(path)
        data = {
            'command' :'INIT',
            'total_bytes' : size,
            'media_type' : 'image/png',
            'media_category' : 'tweet_image'
        }
        self.session.headers["origin"]="https://twitter.com"
        self.session.headers["referer"]="https://twitter.com/"
        resp = self.session.post('https://upload.twitter.com/i/media/upload.json',data = data)
        resultJson = json.loads(resp.content)
        media_id = resultJson['media_id_string']
        
        self.uploadImageAppend(media_id,path)
        return media_id
        
    def uploadImageAppend(self,media_id,path):
        data = {
            'command':'APPEND',
            'media_id':media_id,
            'segment_index':0,
        }
        file = open(path,'r')
        files = {
            'media':('blob',file.read())
        }
        resp = self.session.post('https://upload.twitter.com/i/media/upload.json',data = data,files = files)
        self.session.post('https://upload.twitter.com/i/media/upload.json',data = {
            'command' : 'FINALIZE',
            'media_id': media_id
        })
        
    def sendImage(self,text,media_id):
        data = {
            'authenticity_token' : self.authenticity_token,
            'is_permalink_page' : 'false',
            'media_ids' : media_id,
            'place_id':'',
            'status': text,
            'tagged_users':''
        }
        self.session.headers["origin"]="https://twitter.com"
        self.session.headers["referer"]="https://twitter.com/"
        self.session.headers["x-twitter-active-user"] = 'yes'
        resp = self.session.post('https://twitter.com/i/tweet/create',data = data)
        
if __name__ == '__main__':
    tw = Twitter(Config())
    print(tw.getRandomTips())
    # tw.sendImage('33667aabb','850235756178161664,850235764663136256,850235774863761409,850235785630539779')