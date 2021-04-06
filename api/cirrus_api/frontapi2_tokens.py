from requests import HTTPError


class Tokens(object):

    def __init__(self, api_access):
        self._api_access = api_access

    @property
    def endpoint(self):
        return "teams/%s/tokens" % self._api_access.current_team

    @property
    def _am_robot(self):
        return self._api_access.login_type == 'robot'

    def create(self, token_name):
        """
        covers: POST front/api/v1t/tokens
        """
        data = {"Name": token_name}
        response = self._api_access.http_post_data(self.endpoint, data, noteam=self._am_robot)
        return response.json()

    def get_list(self):
        """
        covers: GET front/api/v1t/tokens
        """
        response = self._api_access.http_get(self.endpoint, noteam=self._am_robot)
        return response.json()

    def rename(self, token_id, new_name):
        """
        covers: PUT fornt/api/v1t/tokens/...
        """
        data = {"name": new_name}
        response = self._api_access.http_put_data("%s/%s" % (self.endpoint, token_id), data, noteam=self._am_robot)
        return response.json()

    def delete(self, token_id):
        """
        covers: DELETE front/api/v1t/tokens/...
        """
        response = self._api_access.http_delete("%s/%s" % (self.endpoint, token_id), noteam=self._am_robot)
        return response.json()
