#THIS CURRENT CONFIG WORKSSSS

import cgi
import webapp2
#from jinja2 import Environment, PackageLoader
import jinja2

from google.appengine.ext import db

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
	],
	debug=True)