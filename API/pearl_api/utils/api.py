"""
Internal utilities: API
~~~~~~~~~~~~~~~~~~~~~~~~
"""

from ..api import Api

""" 
Relative REST API 

Provides convenient way to call subsystem REST API
For example, for for specified channel it can be
  self._get('name')
instead of
  self._api.get('channels/' + self._id + '/name')
"""


class RelativeApi(object):
    def __init__(self, api, url, **kwargs):
        self._api = api
        self._baseurl = url + '/'
        # currently supports query string parameters, like:
        # ?channels=true
        strparams = kwargs.get('params', None)
        if strparams:
            self._baseurl += strparams


    """ Helpers to call API with relative URL """
    def _get(self, url, params=None, **kwargs):
        return self._api.get(self._baseurl+url, params, **kwargs)
    
    def _post(self, url, data=None, **kwargs):
        return self._api.post(self._baseurl+url, data, **kwargs)

    def _put(self, url, data=None, **kwargs):
        return self._api.put(self._baseurl+url, data, **kwargs)

    def _patch(self, url, data=None, **kwargs):
        return self._api.patch(self._baseurl+url, data, **kwargs)

    def _delete(self, url, **kwargs):
        return self._api.delete(self._baseurl+url, **kwargs)