from . import Device as Pearl, Error as PearlApiError, Api as PearlApi
from requests_toolbelt.utils import dump
from requests.exceptions import HTTPError

import logging
import requests
import mmh3

logger = logging.getLogger()

class RemoteLoginTunnel(PearlApi):
    tunnel_url_prefix = 'https://%(prefix)s.%(cluster)s.pearls.avstudio.com'

    def __init__(self, api, pearl, cluster, report, role=PearlApi.Role(PearlApi.Role.Admin, '')):
        self._pearl = pearl
        self._avs_api = api
        self._cluster = cluster
        self._report = report
        self._session = None
        self._session_id = None
        self._domain = None

        self._device_id = self._pearl.avstudio.master_id
        self._device_name = self._avs_api.Devices.get(self._device_id).name
        self._session_id = self._avs_api.HTTP.session_id
        tunnel_prefix = mmh3.hash(''.join((self._session_id,self._device_id,self._device_name)), signed=False)

        self._domain = '%s.%s.pearls.avstudio.com' % (tunnel_prefix, self._cluster)
        super(RemoteLoginTunnel, self).__init__(self._domain, role, protocol='https')


    def __enter__(self):
        teamid = self._avs_api.current_team

        # Hit this url to start the vtun session between AVStudio and our Pearl
        startup_url = 'https://%s/start-md-access-session?KSESSIONID=%s&TUNTEAMID=%s&TUNDID=%s' % (self._domain, self._session_id, teamid, self._device_id)

        # Requests won't let us follow the redirect naturally,
        # So we need to do it as two steps
        try:
            # Start the connection
            logger.info('Getting startup url: %s'%startup_url)
            resp = self._session.get(startup_url, allow_redirects=False, verify=False)
            logger.debug(dump.dump_all(resp).decode('utf8'))
            self._report(resp.status_code).named("Startup request status").ASSERT_EQ(302)

            # This will fail 401
            # We need to trigger an authentication challenge
            # before the Pearl will accept an Authorization header
            resp = self._session.get('https://' + self._domain + '/')
            logger.debug(dump.dump_all(resp).decode('utf8'))
            self._report(resp.status_code).named("Auth challenge status").EXPECT_EQ(401)

            # Now we send Authorization and (hopefully) get 200
            self._session.auth = self.auth
            resp = self._session.get('https://' + self._domain + '/api/system/status')
            logger.debug(dump.dump_all(resp).decode('utf8'))
            self._report(resp.status_code).named("Tunnel probe request status").ASSERT_EQ(200)
        except (PearlApiError, HTTPError) as ex:
            logger.error("Unable to establish tunnel - {}".format(ex))
            raise ex

        return self


    def __exit__(self, type, value, traceback):
        pass
