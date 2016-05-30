#!/usr/bin/env python
from models import PhoneBookEntry
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class ListHandler(BaseHandler):
    def get(self):
        entries = PhoneBookEntry.query().fetch()
        params = {"entries": entries}
        return self.render_template("phonebook.html", params=params)

    def post(self):
        name = self.request.get("name")
        phone = self.request.get("phone")
        entry = PhoneBookEntry(name=name, phone=phone)
        entry.put()

        entries = PhoneBookEntry.query().fetch()

        '''
        The just added entry is not yet visible in the DB.
        I'll therefore add it manually to the list of entries
        before displaying them.
        '''
        entries.insert(0, entry)
        params = {"entries": entries}

        return self.render_template("phonebook.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', ListHandler),
], debug=True)
