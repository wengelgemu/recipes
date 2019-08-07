import os
import json
import webapp2
import jinja2
from urllib import urlencode
from google.appengine.api import urlfetch

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#search request handler/search form handler
class SearchFormHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/form.html')
        self.response.write(template.render())


class RecipieDisplayHandler(webapp2.RequestHandler):
    def post(self):
        query = self.request.get('query')
        base_url = 'http://www.recipepuppy.com/api/?'
        params = { 'q': query }
        response = urlfetch.fetch(base_url + urlencode(params)).content
        results = json.loads(response)

        template = jinja_env.get_template('templates/recipe.html')
        self.response.write(template.render({
            'results': results
        }))

# the app configuration section
app = webapp2.WSGIApplication([
    # ('/main', MainPage),
    # ('/cece', CecePage),
    # ('/about-us', AboutPage),
    ('/', SearchFormHandler),
    ('/recipe', RecipieDisplayHandler),
], debug=True)