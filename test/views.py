import os

from google.appengine.dist import use_library
use_library('django', '1.2')
os.environ['DJANGO_SETTINGS_MODULE'] = '__init__'
import webapp2 as webapp
from webapp2_extras import sessions
from google.appengine.ext.webapp import template
from lib import plivo
sessions.default_config['secret_key'] = '-- secret key --'
import yaml

with open('secrets.yml', 'r') as f:
    conf = yaml.load(f)


class SMSView(webapp.RequestHandler):

    def dispatch(self):

        self.session_store = sessions.get_store(
            request=self.request
        )
        try:
            webapp.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp.cached_property
    def session(self):
        return self.session_store.get_session()

    def get(self):

        template_values = {
        }

        path = os.path.join(
                os.path.dirname(__file__), 'template.html'
            )
        self.response.out.write(template.render(path, template_values))

    def post(self):

        plivo_number = conf['PLIVO_NUMBER']

        destination_number = self.request.get('number')

        text = self.request.get('msg')

        message_params = {
          'src': plivo_number,
          'dst': destination_number,
          'text': text,
        }

        p = plivo.RestAPI(conf['PLIVO_AUTH_ID'], conf['PLIVO_AUTH_TOKEN'])

        template_values = {
            'response': p.send_message(message_params),
            'number': destination_number,
            'msg': text
        }

        path = os.path.join(
            os.path.dirname(__file__), 'template.html'
        )
        self.response.out.write(template.render(path, template_values))


urls = [
    ('/', SMSView),
]

app = webapp.WSGIApplication(urls, debug=True)
