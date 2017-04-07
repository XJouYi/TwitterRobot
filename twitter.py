#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import os
import socks
import json
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
        # print(resp.content)
        
    def sendImage(self,text,media_id):
        # media_id = self.uploadImage('/Users/jinyi/Downloads/IMG_0728.PNG')
        # media_id = '850180885173415936'
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
        # print(resp.content)
        
if __name__ == '__main__':
    tw = Twitter(Config())
    tw.login()
    tw.sendImage('33667aabb','850235756178161664,850235764663136256,850235774863761409,850235785630539779')