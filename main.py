#!/usr/bin/python
# -*- coding: utf-8 -*-
from twitter import Twitter
from config import Config

if __name__ == '__main__':
    conf = Config()
    tw = Twitter(conf)
    tw.login()
    tw.sendText('99')