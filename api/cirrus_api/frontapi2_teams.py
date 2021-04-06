from requests import HTTPError
import time


class Teams(object):
    def __init__(self, api_access):
        self._api_access = api_access

    def get_all(self):
        """
        Current user teams
        covers: GET /front/api/v1t/teams
        """

        return self._api_access.http_get("teams").json()

    def current_team(self):
        """
        Get the current team

        returns: (team_id, role)
        """
        ui = self._api_access.get_user_info()
        return ui["CurrentTeam"], ui["CurrentRole"]

    def create(self):
        """
        Create new Team
        covers: POST /front/api/v1t/teams
        """

        body = {"Billing": {}}
        return self._api_access.http_post_data("teams", body).json()["ID"]

    def get(self, team_id):
        """
        Get Team
        covers: GET /front/api/v1t/teams/{team}
        Params:
          team: Team ID
        """

        params = {"team": team_id}
        return self._api_access.http_get("teams/%(team)s" % params).json()

    def switch_to(self, team_id):
        """
        Switches current team
        Params:
          team: Team ID
        """

        old_team_id = self._api_access.current_team
        self._api_access.logger().info("Switching to team %s", team_id)
        self._api_access.current_team = team_id

        try:

            self._api_access.get_user_info()
            self._api_access.logger().info("Switched to team %s" % self.current_team()[0])
        except HTTPError:
            self._api_access.logger().warning("Could not switch to team %s, reverting to %s" % (team_id, old_team_id))
            self._api_access.current_team = old_team_id
            self._api_access.get_user_info()
            raise

    def rename(self, team_id, name):
        """
        Save Team
        covers: PUT /front/api/v1t/teams/{team}
        Params:
          team: Team to team_rename
          name: New name
        """

        params = {"team": team_id}
        return self._api_access.http_put_data("teams/%(team)s" % params, {"Name": name})

    def delete(self, team_id):
        """
        Delete team
        covers: DELETE /front/api/v1t/teams/{team}
        Params:
          team_id: Team ID
        """

        params = {"team": team_id}
        return self._api_access.http_delete("teams/%(team)s" % params).json()

    def get_users(self, team_id):
        """
        Get team members
        covers: GET /front/api/v1t/teams/{team}/users
        Params:
          team_id: Team ID
        """

        params = {"team": team_id}
        return self._api_access.http_get("teams/%(team)s/users" % params).json()

    def check_role_validity(self, role):
        valid_roles = ["owner", "editor", "operator"]
        if role not in valid_roles:
            raise Exception('User role "%s" is not valid, use one of the following: %s', role, ','.join(valid_roles))

    def invite(self, team_id, email, role):
        """
        Invite new user to the team.
        covers: POST /front/api/v1t/teams/{team}/users
        Params:
          team: Team ID
          role: Role

        returns: Invite ID
        """

        self.check_role_validity(role)

        params = {"team": team_id}
        body = {"Email": email, "Role": role}
        return self._api_access.http_post_data("teams/%(team)s/users" % params, body).json()["ID"]

    def delete_user_from_team(self, team_id, user_id):
        """
        Delete user from team
        covers: DELETE /front/api/v1t/teams/{team}/users/{user}
        params:
          team_id: Team ID
          user_id: User ID
        """
        params = {"team": team_id, "user": user_id}
        return self._api_access.http_delete("teams/%(team)s/users/%(user)s" % params)

    def get_unread_device_alerts(self, user_id):
        """
        Get unread device alerts for the team
        covers: GET /front/api/v1t/teams/{team}/users/{user}/unread_device_alerts
        params:
          user_id: User ID
        """
        return self._api_access.http_get("users/%(user)s/unread_device_alerts" % {"user": user_id}).json()

    def set_device_alerts(self, user_id, settings):
        """
        Get unread device alerts for the team
        covers: POST /front/api/v1t/team/TEAMID/users/{user}/device_alerts
        params:
          user_id: User ID
        """
        return self._api_access.http_post_data("users/%(user)s/device_alerts" % {"user": user_id}, settings).json()

    def get_source_image(self, device_id, source_id, local_filename):
        """`
        Get unread device alerts for the team
        covers: GET /front/api/v1t/team/TEAMID/devices/{device}/{source}/state.jpg
        params:
          device: Device ID
          source: Source ID
        """
        time_ms = int(round(time.time() * 1000))
        relative_url = "devices/%(device)s/%(source)s/state.jpg?v=%(time)s" % {"device": device_id, "source": source_id,
                                                                               "time": time_ms}
        return self._api_access.http_download_file(relative_url, local_filename)

    def request_source_previews(self, device_id):
        """`
        Request for source_previews events from device
        covers: POST /front/api/v1t/team/TEAM_ID/devices/request/source_previews
        params:
          device: Device ID
        """
        data = {"Devices": [device_id]}
        return self._api_access.http_post_data("devices/request/source_previews", data)

    def set_user_role(self, team_id, user_id, new_role):
        """
        Update user role
        covers: PUT /front/api/v1t/teams/{team}/users/{user}
        Params:
          team: Team ID
          user: User ID
        """

        self.check_role_validity(new_role)

        params = {"team": team_id, "user": user_id}
        body = {"Role": new_role}
        return self._api_access.http_put_data("teams/%(team)s/users/%(user)s" % params, body).json()
