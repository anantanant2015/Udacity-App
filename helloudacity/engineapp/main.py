#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, urllib2

import cgi

import os

from classes.rot13 import rot

from classes.ResponseWrite import jinjaWriter

from classes.helloworld import HelloWorld

from classes.usersignup import UserSignUp
from classes.usersignup import UserLogin
from classes.usersignup import UserLogout

from classes.welcome import Welcome

from classes.fizzbuzz import FizzBuzz

from classes.shoppinglist import ShoppingList

from classes.asciichan import AsciiChan

from classes.bloghandler import BlogHandler

from classes.wiki import WikiHandler

from classes.mapconfig import MapConfig

path=os.path.dirname(__file__)

jw=jinjaWriter()

links=['/','/helloworld','/rot13','/signup','/signupregister','/welcome','/cookiewelcome','/fizzbuzz',
'/shoppinglist','/asciichan','/blog','/blog/newpost','/login','/logout', '/flush', '/wiki', '/mapconfig']

class MainHandler(webapp2.RequestHandler):
    def get(self):
        global path,links
        paramdct={}
        paramdct['title']='Home'
        paramdct['links']=links
        paramdct['header']='Home'
        paramdct['footer']='Udacity'
        self.response.write(jw.WriteTemplate('home.html','website_layout.css',path,**paramdct))
        

        
y=rot()
x=MainHandler()
hw=HelloWorld()
su=UserSignUp()
li=UserLogin()
lo=UserLogout()
wl=Welcome()
fb=FizzBuzz()
sl=ShoppingList()
asc=AsciiChan()
bl=BlogHandler()
wk=WikiHandler()
mc=MapConfig()
urlMapping=[('/', x.__class__)]

def urlMappingAppend(path,objRecieved):
    global urlMapping
    tu=(path,objRecieved.__class__)
    urlMapping.append(tu)

urlMappingAppend('/rot13',y)
urlMappingAppend('/mapconfig',mc)
urlMappingAppend('/helloworld',hw)
urlMappingAppend('/signup',su)
urlMappingAppend('/signupregister',su)
urlMappingAppend('/login',li)
urlMappingAppend('/logout',lo)
urlMappingAppend('/welcome',wl)
urlMappingAppend('/cookiewelcome',wl)
urlMappingAppend('/fizzbuzz',fb)
urlMappingAppend('/shoppinglist',sl)
urlMappingAppend('/asciichan', asc)
urlMappingAppend('/blog/newpost', bl)
urlMappingAppend('/blog?(?:\.json)?',bl)
urlMappingAppend('/flush', bl)
urlMappingAppend('/wiki?(?:[a-zA-Z0-9_-]+/?)*', wk)

app = webapp2.WSGIApplication(urlMapping, debug=True)
