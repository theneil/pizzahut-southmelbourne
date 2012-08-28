import webapp2
import cgi
import re
from google.appengine.ext import db


from BaseHandler import BaseHandler
from Handler import Signin,CreateRoster,MainPage

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/createroster',CreateRoster),
                               ('/signin', Signin)]
			      ,debug=True)
