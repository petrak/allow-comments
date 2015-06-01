
from google.appengine.api import users
from google.appengine.ext import ndb

import os

import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)
# --------------------- database   -----------------

DEFAULT_WALL = 'Public'

# We set a parent key on the 'Post' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.

def wall_key(wall_name=DEFAULT_WALL):
  	# """Constructs a Datastore key for a Wall entity.

  	# We use wall_name as the key.
  	# """
  	return ndb.Key('Wall', wall_name)

class Author(ndb.Model):
  	# """Sub model for representing an author."""
  	identity = ndb.StringProperty(indexed=True)
  	name = ndb.StringProperty(indexed=False)
 	email = ndb.StringProperty(indexed=False)

class Post(ndb.Model):
  	# """A main model for representing an individual post entry."""
 	 #author = ndb.StructuredProperty(Author)
  	komentar = ndb.TextProperty(indexed=False)
  	date = ndb.DateTimeProperty(auto_now_add=True)

  # --------------------- database   -----------------
class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def get(self):

		items = ["Network   Network is a group of entities that can communicate, though they are not directly connected. It is important to define: way to encode and interpret messages, way to route messages and rules for deciding who gets to use resources. Network measuring units are latency (= time it takes to get from source to destination) and bandwidth (=amount of information that can be transmitted per unit time). HTTP (= Hypertext Transfer Protocol) is protocol that defines the rules how entites communcate with each other on internet. Communication entities are Clients (web Browser) and Servers.", 
				 "Servers   The purpose of servers is to respond to HTTP requests (clients (=browsers) send http requests for documents) and servers respond to those requests. The responses can be static ( e.g. prewritten file that the server returns: image,...) or dynamic (= the response is built on the fly, by the programms called web applications that are running on servers). The requsts are referenced by address: http (=protocol)& host (=domain name (or IP address) of the server that has the document we want to access)&path (= path to document we want to fetch)", 
				 "Forms      Forms are what users will use to enter data: text, select from dropdown menus, check checkboxes, radiobuttons, ... When client submitt a form, web applications  get input from users. It is also important that the data that are received by the server are secure and correct. Then the response is posted back to client by the server (http requese, http response, GET method, POST method).",
				  "GET : POSTGET: parameters in URL, used for fetching documents, maximum URL length, OK to cache, sholuldn't change the server. POST: parametrs in body, used for updating data, no max lengt, not ok to cache, ok to change the server", 
				  "ValidationInput validation is used to prevent to deal with junk data and to prevent the web applications from being hacked. It means verifying on the server side that what we received is what we expected to receive. Before saving data to data bases all data have to be validated: all entered dates have to be valid, checking data according to same lists (dictionaries). On error the application returnes error message. Very good way to do this is redirection. Entered data have to be secure. For this purpose Python string substitution is very useful (e.g. substitution of HTML special signs). It can be used to prevent  our applications to be hacked.", 
				  "Templates  Template library is library to build complicated strings. Most of the time web applications are refering to HTML strings. We have used the library jinja2 (more info on page jinja.pocoo.org) which is built in Google App Engine. There are many templating libraries and they are all very similar. Important concepts of technology called Templates are: Variable Substitution using {{name}}, Statement Syntax {% Statement %} and {% end statement %}, for loop syntax {% for statement %} and {% endfor  %}, jinja autoescape function prevents input to make damage (prevent to input HTML), Template inheritance let us define a base template which we can later plug new  HTML into (e.g. it is useful to have consistent header and footer across a application) ... The technology makes code structured, it eliminates repetition, makes it easier to implement changes and find errors. It is possible to escape variables automaticaly (= more secure websites), to minimize code in templates (= HTML is easier to modify),  minimize html in the code (= separate different types of code) and  make more readable code."]

		 # --------------------- database   -----------------
		wall_name = self.request.get('wall_name',DEFAULT_WALL)

	    	if wall_name == DEFAULT_WALL.lower():
	    		wall_name = DEFAULT_WALL

			    # Ancestor Queries, as shown here, are strongly consistent
			    # with the High Replication Datastore. Queries that span
			    # entity groups are eventually consistent. If we omitted the
			    # ancestor from this query there would be a slight chance that
			    # Greeting that had just been written would not show up in a
			    # query.
			    # [START query]ancestor
		posts_query = Post.query(ancestor = wall_key(wall_name)).order(-Post.date)

			    # The function fetch_page() returns three things:
			    # a list of post objects,
			    # a cursor to indicate where we are currently in the
			    # database and a boolean to indicate whether there are more posts that we
			    # can further get.
			    # We pass in 10 to get 10 posts from the database
		posts, cursor, more = posts_query.fetch_page(10)
			    # [END query]

	     # --------------------- database parent  -----------------
		post = Post(parent=wall_key(wall_name))

		comments = self.request.get_all("naloga") 

		ind = "0"
		if   comments:
        		post.komentar = self.request.get("naloga")
    			post.put()
    			ind = "1"
    			# if comments ==' ':
    			# 	self.redirect('/napaka')
    			self.render("concepts.html", items = items, comments = comments)
    	# else:
    	# 		comments = posts
    			
  		
		if ind == "0":
					self.render("concepts.html", items = items, comments = posts)

# class PostError(webapp2.RequestHandler):
# 	def get(self):
# 		self.response.out.write("Empty comment is not allowed"


app = webapp2.WSGIApplication([
  ('/', MainPage),
  # ('/napaka', PostError),
], debug=True)