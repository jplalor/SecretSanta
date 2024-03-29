#THIS CURRENT CONFIG WORKSSSS

import cgi
import webapp2
#from jinja2 import Environment, PackageLoader
import jinja2
import random

from google.appengine.ext import db
from google.appengine.api import mail

env = jinja2.Environment(autoescape=True,
	loader=jinja2.FileSystemLoader('templates'))
	
class Person (db.Model):
	name = db.StringProperty()
	email=db.StringProperty()
	date=db.DateTimeProperty(auto_now_add=True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	def render_str(self, template, **params):
		t = env.get_template(template)
		return t.render(**params)
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):
        template = env.get_template('front.html')
        self.render(template)
		
class Admin(Handler):
	def get(self):
		people = db.GqlQuery("SELECT * "
							 "FROM Person "
							 "ORDER BY date DESC")
		emails=[]
		names=[]
		people2=[]
		canSend = False
		
		for person in people:
			names.append(person.name)
			people2.append(person.name)
			
		random.shuffle(names)
		
		while canSend == False:
			for person in people2:
				if person == names[people2.index(person)]:
					random.shuffle(names)
					canSend=False
					break
				else:
					canSend = True
		
		template=env.get_template('admin.html')
		self.response.out.write(template.render({'people': people, 'names':names}))	
			
		
class ThankYou(Handler):
	def post(self):
	
		fullname = self.request.get('fullname')
		emailaddress=self.request.get('emailaddress')
		p = Person(name=fullname, email=emailaddress)
		p.put()
		people = db.GqlQuery("SELECT * "
							 "FROM Person "
							 "ORDER BY date DESC")
		template=env.get_template('thanks.html')
		self.response.out.write(template.render({'people': people}))
		
#class SendMail(Handler):
#	def get(self):
#		people = db.GqlQuery("SELECT * "
#							 "FROM Person "
#							 "ORDER BY date DESC")
#		emails=[]
#		names=[]
#		people2=[]
#		i=0
#		text_output=""
#		canSend = False
#		
#		for person in people:
#			names.append(person.name)
#			emails.append(person.email)
#			people2.append(person.name)
#			
#		random.shuffle(names)
#		
#		while canSend == False:
#			for person in people2:
#				if person == names[people2.index(person)]:
#					random.shuffle(names)
#					canSend=False
#					break
#				else:
#					canSend = True
#					
#		
#		for email in emails:
#			email_text = "Hello! this is Hugey the Elf.  This year, for Secret Santa, you will be buying a gift for: %s \n\nMerry Christmas!!" % names[i]
#			mail.send_mail(sender="Hugey the Elf <hugeytheelf@gmail.com>",
#			              to=email,
#						  subject="Merry Christmas! Here is your Secret Santa Information!",
#						  body=email_text)
#			
#			i +=1
#			
#			text_output = text_output+ "Email sent to "+email + " with text: "+email_text+"\r\n\r\n"
#		
		#dont need a template in this instance
#		template=env.get_template('sendemail.html')
#		self.response.out.write(template.render({'text_output': text_output}))	
	
		


#class Handler(webapp2.RequestHandler):
#	def write(self, *a, **kw):
#		self.response.out.write(*a, **kw)
#	def render_str(self, template, **params):
#		t = jinja_environment.get_template(template)
#		return t.render(**params)
#	def render(self, template, **kw):
#		self.write(self.render_str(template, **kw))

#class MainPage(Handler):
#class MainPage(webapp2.RequestHandler):
    #def get(self):
        #template = jinja_environment.get_template('front.html')
        #posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
        #self.response.out.write(template.render(posts))
        #self.response.out.write(template)

app = webapp2.WSGIApplication([('/', MainPage),
								('/thanks.html', ThankYou),
								('/admin.html', Admin),
#								('/sendmail.html', SendMail),
	],
	debug=True)