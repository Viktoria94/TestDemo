import logging
import requests
import time
import os
import warnings
from .request_dump import dump_all

from .frontapi2_devices import Devices
from .frontapi2_hls import HLS
from .frontapi2_teams import Teams
from .frontapi2_streaming import Streaming
from .frontapi2_tokens import Tokens
from .frontapi2_transcribing import Transcribing
from .frontapi2_groups import Groups
from .frontapi2_presets import Presets

TIMEOUT = 60


class APIAccess(object):
    _address = None
    _cookies = {}
    _username = None
    _debug = False
    _current_team = None
    _user_info = None
    _headers = None
    _use_token = False

    # Privates

    def get_full_url(self, request, noteam=False):
        if not self._use_token:
            request_params = {
                "host": self._address,
                "version": "v1t",
                "teamid": self._current_team if self._current_team else None,
                "request": request
            }
        else:
            noteam = True
            request_params = {
                "host": self._address,
                "version": "v2",
                "request": request
            }

        if request[0] == '/':
            # Absolute path
            return "%(host)s%(request)s" % request_params
        else:
            # Relative paths
            if self._current_team is None or noteam:
                return "%(host)s/front/api/%(version)s/%(request)s" % request_params
            else:
                return "%(host)s/front/api/%(version)s/team/%(teamid)s/%(request)s" % request_params

    def logger(self):
        return logging.getLogger("frontapi")

    def dump_request(self, r, request_time=None):
        if r.status_code in (200, 302) and self.logger().level != logging.DEBUG:
            return

        request_dump = dump_all(r)
        try:
            request_dump_str = request_dump.decode('utf-8')
        except UnicodeDecodeError as e:
            self.logger().debug("Unable to decode request body as text, dumping headers only - {}".format(e))
            request_dump_str = dump_all(r, headers_only=True).decode('utf-8')
            request_dump_str += "+ %d binary bytes" % (len(request_dump) - len(request_dump_str))

        if request_time is not None:
            request_dump_str += "\nRequest processed in {} seconds".format(request_time)

        if r.status_code in (200, 302):
            self.logger().debug(request_dump_str)
        else:
            self.logger().error(request_dump_str)

    def _request_generic(self, method, url, noteam=False, **kwargs):
        start_time = time.time()

        r = requests.request(
            method,
            self.get_full_url(url, noteam),
            cookies=self._cookies,
            headers=self._headers,
            timeout=TIMEOUT,
            **kwargs)

        self.dump_request(r, time.time() - start_time)
        r.raise_for_status()
        return r

    def http_get(self, url, noteam=False):
        return self._request_generic("get", url, noteam)

    def http_delete(self, url, noteam=False):
        return self._request_generic("delete", url, noteam)

    def http_post(self, url, noteam=False):
        return self._request_generic("post", url, noteam)

    def http_post_data(self, url, json, noteam=False):
        return self._request_generic("post", url, json=json, noteam=noteam)

    def http_put_data(self, url, json, noteam=False):
        return self._request_generic("put", url, json=json, noteam=noteam)

    def http_post_file(self, url, filename, mime="application/binary", data={}, noteam=False):
        files = {"file": (os.path.basename(filename), open(filename, "rb"), mime)}

        return self._request_generic(
            "post",
            url,
            data=data,
            files=files)

    def http_download_file(self, url, local_filename, noteam=False):
        self.logger().debug("Downloading \"%s\" to file \"%s\"" % (url, local_filename))

        r = self._request_generic("get", url, stream=True)

        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

        self.logger().debug("Downloaded \"%s\" to file \"%s\"" % (url, local_filename))

        return r

    def __init__(self, address):
        self._address = address

        if not (self._address.startswith("https://") or self._address.startswith("http://")):
            self._address = "https://" + self._address

    def set_auth_token(self, token):
        self._use_token = True
        self._headers = {
            "Authorization": "Bearer " + token
        }

        self.get_user_info()

    def login(self, username, password, invite_token=None):
        """
        covers: GET /front/api/v1t/oauth/base/{user_id}
        """

        if self._user_info:
            self.logger().debug("Already logged in, logout first")
            self.logout()

        self._username = username
        login_url = self.get_full_url("oauth/base/" + username)

        self.logger().info("Logging in: %s", login_url)

        params = {
            "pwd": password
        }

        if invite_token is not None:
            params["state"] = "token=" + invite_token

        r = requests.get(login_url, allow_redirects=False, params=params)
        self.dump_request(r)
        r.raise_for_status()

        # Temporary code for retrieving team id
        self._current_team = r.headers["X-Current-Team-Id"]

        self._cookies = {"KSESSIONID": r.cookies["KSESSIONID"]}
        self.get_user_info()

    def get_user_info(self):
        """
        covers: GET /front/api/v1t/users/me
        """
        self._user_info = self.http_get("users/me").json()
        return self._user_info

    def logout(self):
        """
        covers: GET /front/api/v1t/oauth/logout
        """
        self._current_team = None
        logout_url = self.get_full_url("oauth/logout")
        self.logger().info("Logging out as %s", self._username)
        r = requests.get(logout_url, allow_redirects=False, cookies=self._cookies)
        self._cookies = {}
        r.raise_for_status()
        self._user_info = None

    def test_user_create(self, username, password):
        """
        covers: GET /front/api/v1t/oauth/base/root
        covers: POST /front/api/v1t/users/system/add
        """

        root_password = os.environ.get("ROOT_PASSWORD")
        if root_password is None:
            raise Exception("Root password is not set in ROOT_PASSWORD env variable")

        root_login_url = self.get_full_url("oauth/base/root?pwd=" + root_password)
        r = requests.get(root_login_url, allow_redirects=False)
        self.dump_request(r)
        if r.status_code not in [302, 200]:
            return

        self._cookies = {"KSESSIONID": r.cookies["KSESSIONID"]}

        user_json = {
            "ID": username,
            "Name": username,
            "Pwd": password
        }

        self.http_post_data("users/system/add", user_json)
        self.logger().info("Created user: \"%s\" with password \"%s\"" % (username, password))
        self.login(username, password)

    def test_user_delete(self, username):
        """
        covers: DELETE /front/api/v1t/users/{user_id}
        """
        if self._username != username:
            raise Exception("You must be logged in as %s" % username)

        self.http_delete("users/" + username)
        self.logger().info("Deleted user: \"%s\"" % username)

    @property
    def current_user_id(self):
        return None if self._user_info is None else self._user_info["ID"]

    @property
    def current_user_name(self):
        return None if self._user_info is None else self._user_info["Name"]

    @property
    def current_team(self):
        return None if self._user_info is None else self._user_info["CurrentTeam"]

    @property
    def login_type(self):
        return None if self._user_info is None else self._user_info["LoginType"]

    @property
    def current_role(self):
        return None if self._user_info is None else self._user_info["CurrentRole"]

    @property
    def session_id(self):
        return self._cookies.get("KSESSIONID", None)

    @current_team.setter
    def current_team(self, teamid):
        self._current_team = teamid


# Our own deprecated decorator
# Got in its entiriety from
#   https://wiki.python.org/moin/PythonDecoratorLibrary#Generating_Deprecation_Warnings
def frontapi_deprecated(func):
    '''This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.'''

    def new_func(*args, **kwargs):
        warnings.warn("Deprecated FrontAPI used: function {}.".format(func.__name__), category=DeprecationWarning)
        return func(*args, **kwargs)

    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func


class FrontAPI2(object):
    def __init__(self, address):
        self.HTTP = APIAccess(address)
        self._api_access = self.HTTP  # _api_access is obsolete

        self.Devices = Devices(self._api_access)
        self.HLS = HLS(self._api_access)
        self.Teams = Teams(self._api_access)
        self.Streaming = Streaming(self._api_access)
        self.Tokens = Tokens(self._api_access)
        self.Transcribing = Transcribing(self._api_access)
        self.Groups = Groups(self._api_access)
        self.Presets = Presets(self._api_access)

    def set_auth_token(self, token):
        self._api_access.set_auth_token(token)

    def login(self, username, password, invite_token=None):
        self._api_access.login(username, password, invite_token)

    def logout(self):
        self._api_access.logout()

    def test_user_create(self, username, password):
        self._api_access.test_user_create(username, password)

    def test_user_delete(self, username):
        self._api_access.test_user_delete(username)

    @property
    def current_user_id(self):
        return self._api_access.current_user_id

    @property
    def current_user_name(self):
        return self._api_access.current_user_name

    @property
    def current_team(self):
        return self._api_access.current_team

    @property
    def current_role(self):
        return self._api_access.current_role

    @property
    def login_type(self):
        return self._api_access.login_type

    def delete_all(self):
        """
        Deletes all scenes, devices and assets
        """
        for subsys in [self.Devices]:
            subsys.delete_all()

    def get_current_agreement(self):
        agr = self.HTTP.http_get("users/agreement").json()
        return agr["AgreementID"], agr["AgreementTime"]

    def accept_agreement(self, agreement=None):
        """
        Accepts agreement

        Params:
        -------
         agreement: (agreement id, agreement time) tuple
             Agreement to accept. If None, gets the current one.
        """

        if agreement is None:
            agreement = self.get_current_agreement()

        self.HTTP.http_post_data("users/agreement", {
            "AgreementID": agreement[0],
            "AgreementTime": agreement[1]
        })

    def get_cluster_version(self):
        cloud_versions = self.HTTP.http_get("/front/api/v0.1/versions").json()
        return cloud_versions["Release"]

    def get_cluster_component_versions(self):
        cloud_versions = self.HTTP.http_get("/front/api/v0.1/versions").json()
        return dict([(d["Name"], d["Version"]) for d in cloud_versions["Components"]])

    # Obsolete methods

    @frontapi_deprecated
    def scene_batch_set(self, scene_ids, preroll=None, postroll=None):
        return self.scene_batch_set(scene_ids, preroll, postroll)

    @frontapi_deprecated
    def devices_get(self):
        return self.Devices.get_all()

    @frontapi_deprecated
    def device_get(self, device_id):
        return self.Devices.get(device_id)

    @frontapi_deprecated
    def device_delete(self, device_id):
        return self.Devices.get(device_id).delete()

    @frontapi_deprecated
    def device_cmd(self, device_id, cmd):
        return self.Devices.get(device_id).run_command(cmd)

    @frontapi_deprecated
    def device_add(self, device_id, name):
        return self.Devices.pair(device_id, name)

    @frontapi_deprecated
    def device_set_name(self, device_id, name):
        self.Devices.get(device_id).name = name

    @frontapi_deprecated
    def device_unpair(self, device_id):
        self.Devices.get(device_id).unpair()

    @frontapi_deprecated
    def device_get_state_image(self, device_id, local_filename):
        return self.Devices.get(device_id).download_state_image(local_filename)

    @frontapi_deprecated
    def create_hls_stream(self, scene, stream_id, begin_ts=None, end_ts=None, relative=False, out_of_scene=False):
        return self.HLS.create_stream(scene, stream_id, begin_ts, end_ts, relative, out_of_scene)

    @frontapi_deprecated
    def delete_hls_stream(self, scene, stream_id):
        return self.HLS.delete_stream(scene, stream_id)

    @frontapi_deprecated
    def get_live_stream_url(self, device_id):
        return self.HLS.stream_url_for_device(device_id)

    @frontapi_deprecated
    def get_my_teams(self):
        return self.Teams.get_all()

    @frontapi_deprecated
    def get_current_team(self):
        return self.Teams.current_team()

    @frontapi_deprecated
    def team_create(self):
        return self.Teams.create()

    @frontapi_deprecated
    def team_get(self, team_id):
        return self.Teams.get(team_id)

    @frontapi_deprecated
    def switch_to_team(self, team_id):
        return self.Teams.switch_to(team_id)

    @frontapi_deprecated
    def team_rename(self, team_id, name):
        return self.Teams.rename(team_id, name)

    @frontapi_deprecated
    def team_delete(self, team_id):
        return self.Teams.delete(team_id)

    @frontapi_deprecated
    def team_users(self, team_id):
        return self.Teams.get_users(team_id)

    @frontapi_deprecated
    def check_role_validity(self, role):
        return self.Teams.check_role_validity(role)

    @frontapi_deprecated
    def invite_user_to_team(self, team_id, email, role):
        return self.Teams.invite(team_id, email, role)

    @frontapi_deprecated
    def team_user_delete(self, team_id, user_id):
        return self.Teams.delete_user_from_team(team_id, user_id)

    @frontapi_deprecated
    def team_set_user_role(self, team_id, user_id, new_role):
        return self.Teams.set_user_role(team_id, user_id, new_role)

    @frontapi_deprecated
    def devices_delete_all(self):
        return self.Devices.delete_all()
