#!/usr/bin/env python
#
# Adapted from https://github.com/plivo/plivo-python


import base64
import hmac
from hashlib import sha1

from google.appengine.api import urlfetch
from google.appengine._internal.django.utils import simplejson as json


PLIVO_VERSION = "v1"


class PlivoError(Exception):
    pass


def validate_signature(uri, post_params, signature, auth_token):
    for k, v in sorted(post_params.items()):
        uri += k + v
    return base64.encodestring(hmac.new(auth_token, uri, sha1).digest()).strip() == signature


class RestAPI(object):
    def __init__(self, auth_id, auth_token, url='https://api.plivo.com', version=PLIVO_VERSION):
        self.version = version
        self.url = url.rstrip('/') + '/' + self.version
        self.auth_id = auth_id
        self.auth_token = auth_token
        self._api = self.url + '/Account/%s' % self.auth_id
        self.headers = {'User-Agent':'PythonPlivo'}
        self.Message = Message(self)

    def _request(self, method, path, data={}):

        path = path.rstrip('/') + '/'

        if method == 'POST':

            authorization = 'Basic ' + base64.b64encode(self.auth_id+':'+self.auth_token)
            
            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json'
            }
            headers.update(self.headers)
            
            url = self._api + path

            payload = json.dumps(data)
            
            res = urlfetch.fetch(
                url,
                payload=payload,
                headers=headers,
                method=urlfetch.POST
            )

        # elif method == 'GET':
        #     r = requests.get(self._api + path, headers=self.headers,
        #                      auth=(self.auth_id, self.auth_token),
        #                      params=data)
        # elif method == 'DELETE':
        #     r = requests.delete(self._api + path, headers=self.headers,
        #                         auth=(self.auth_id, self.auth_token),
        #                         params=data)
        # elif method == 'PUT':
        #     headers = {'content-type': 'application/json'}
        #     headers.update(self.headers)
        #     r = requests.put(self._api + path, headers=headers,
        #                      auth=(self.auth_id, self.auth_token),
        #                      data=json.dumps(data))

        content = res.content
        if content:
            try:
                response = json.loads(content)
            except ValueError:
                response = content
        else:
            response = content
        return (res.status_code, response)

    @staticmethod
    def get_param(params, key):
        try:
            return params[key]
        except KeyError:
            raise PlivoError("missing mandatory parameter %s" % key)

    def send_message(self, params=None):
        if not params: params = {}
        return self._request('POST', '/Message/', data=params)


class PlivoResponse(object):
    def __init__(self, rest_api=None, response=None):
        "Create a response class from json and httpresponse"
        if response:
            self.status_code = response[0]
            self.json_data = response[1]
        if rest_api:
            self.rest_api = rest_api

    @classmethod
    def get_objects_from_response(cls, rest_api=None, response=None):
        objects = response[1]['objects']
        return_objects = []
        for obj in objects:
           response_tuple = (response[0], obj)
           return_objects.append(cls(response=response_tuple, rest_api=rest_api))
        return return_objects

    def __getattr__(self, k):
        if k in self.json_data:
            return self.json_data[k]
        else:
            raise AttributeError(k)

    def __repr__(self):
        return "Status: %s \nData: %s"%(self.status_code, self.json_data)


class Message(PlivoResponse):

    def send(self, src, dst, text, url, message_type="sms", method="POST", **optional_params):
        optional_params.update({
            'src': src,
            'dst': dst,
            'text': text,
            'type': message_type,
            'url': url,
            'method': method,
        })
        return Message(
            response=self.rest_api.send_message(optional_params),
            rest_api=self.rest_api
        )
