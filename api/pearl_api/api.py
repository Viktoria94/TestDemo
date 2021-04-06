"""
Multimedia Devices REST api library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests_toolbelt.utils import dump
from PIL import Image
from io import BytesIO
import json
import logging

"""
api Errors
~~~~~~~~~~~
"""

class Error(Exception):
    """ Base error for all api command """
    def __init__(self, url, message, code=0):
        self.url = url
        self.message = message
        self.code = code

class NotFound(Error):
    """ Resource is not found """
    def __init__(self, url, message='Not found'):
        super(NotFound, self).__init__(url, message, 404)

class Forbidden(Error):
    """ Access is denied """
    def __init__(self, url, message='Forbidden'):
        super(Forbidden, self).__init__(url, message, 403)


class ServerError(Error):
    """ Server error """
    def __init__(self, url, message='Server error', code=500):
        super(ServerError, self).__init__(url, message, code)


"""
Device REST api
"""

class Api(object):
    class Role(object):
        """ Access role: Administrator, Operator, Viewer """
        Admin       = 'admin'
        Operator    = 'operator'
        Viewer      = 'viewer'

        def __init__(self, user, password = ''):
            self.user = user
            self.password = password


        def auth(self):
            from requests.auth import HTTPBasicAuth
            """ Return authentication credentials for specified role """
            return HTTPBasicAuth(self.user, self.password)

    def __init__(self, address, role=Role(Role.Admin, ''), protocol='http'):
        self.baseurl = protocol+'://'+address+'/api/'
        self.auth = role.auth()
        self.logger = logging.getLogger()

        # workaround to handle cases
        # when server refuses http connection with error aka
        # "Failed to establish a new connection: [Errno 111] Connection refused"
        self._session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        self._session.mount('http://', adapter)
        self._session.mount('https://', adapter)

    def _logger(self):
        return self.logger

    def _dump_request(self, r):
        request_dump = dump.dump_all(r)
        dump_str = str(request_dump, 'ascii')
        if r.status_code in range(200,400):
            self._logger().debug(dump_str)
        else:
            self._logger().error(dump_str)

    def __call(self, method, name, params=None, **kwargs):
        """ Call REST api and parse results """

        url = self.baseurl + name
        if method == 'get':
            r = self._session.get(url,
                      params=params,
                      verify=False,
                      auth=self.auth)
        elif method == 'delete':
            r = self._session.delete(url,
                         verify=False,
                         auth=self.auth)
        elif method in ['post', 'put', 'patch']:
            r = self._session.request(method,
                          url,
                          data=params,
                          json=kwargs.get('json', None),
                          files=kwargs.get('files', None),
                          verify=False,
                          auth=self.auth)
        else:
            raise Exception('Unsupported HTTP method')

        self._dump_request(r)

        content_type = r.headers.get('content-type', None)
        if content_type == 'application/json':
            return self.__parse_json(r)

        # Generic error handling for non-json responses
        if r.status_code == 404:
            raise NotFound(r.request.url)
        elif r.status_code == 403:
            raise Forbidden(r.request.url)
        elif r.status_code >= 500:
            raise ServerError(r.request.url, 'Server Error', r.status_code)
        elif r.status_code != requests.codes.ok:
            raise Error(r.request.url, 'Error', r.status_code)

        # Generic images
        if content_type.startswith('image/'):
            return Image.open(BytesIO(r.content))

        # Generic text
        if content_type.startswith('text/'):
            return r.content

        # All other data
        return r.content

    def __parse_json(self, response):
        """ Parse response as json """
        json = response.json()
        if 'status' not in json:
            raise Error(response.request.url, 'Unsupported response', response.status_code)
        status = json['status']
        if status == 'ok':
            result = json.get('result', None)
            return result
        elif status == 'notfound':
            raise NotFound(response.request.url)
        elif status == 'forbidden':
            raise Forbidden(response.request.url)
        elif status == 'error':
            raise Error(response.request.url, json.get('error', 'Error'), response.status_code)
        else:
            raise Error(response.request.url, 'Unsupported status', response.status_code)

    """
    REST api calls
    ~~~~~~~~~~~~~~
    For succeeded call returns a result or None.
    In case of error a corresponding exception is risen
    """

    def get(self, name, params=None, **kwargs):
        return self.__call('get', name, params=params, **kwargs)

    def post(self, name, data=None, **kwargs):
        return self.__call('post', name, params=data, **kwargs)

    def put(self, name, data=None, **kwargs):
        return self.__call('put', name, params=data, **kwargs)

    def patch(self, name, data=None, **kwargs):
        return self.__call('patch', name, params=data, **kwargs)

    def delete(self, name, **kwargs):
        return self.__call('delete', name, **kwargs)

