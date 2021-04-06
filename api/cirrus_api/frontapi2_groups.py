class Groups(object):
    def __init__(self, api_access):
        self._api_access = api_access

    def get_all(self):
        """
        Current team's groups
        covers: GET /front/api/v1t/groups
        """

        return self._api_access.http_get("groups").json()

    def create(self, name):
        """
        Create new Group
        covers: POST /front/api/v1t/groups
        """

        body = {"name": name}
        return self._api_access.http_post_data("groups", body).json()

    def get(self, group_id):
        """
        Get Team
        covers: GET /front/api/v1t/groups/{group_id}
        Params:
          group_id: Group ID
        """

        params = {"group_id": group_id}
        return self._api_access.http_get("groups/%(group_id)s" % params).json()

    def rename(self, group_id, name):
        """
        Save Team
        covers: PUT /front/api/v1t/groups/{group_id}
        Params:
          group_id: Group to group_rename
          name: New name
        """

        params = {"group_id": group_id}
        return self._api_access.http_put_data("groups/%(group_id)s" % params, {"name": name}).json()

    def delete(self, group_id):
        """
        Delete team
        covers: DELETE /front/api/v1t/groups/{group_id}
        Params:
          group_id: Group ID
        """

        params = {"group_id": group_id}
        return self._api_access.http_delete("groups/%(group_id)s" % params).json()

    def get_group_devices(self, group_id):
        """
        Get group's devices
        covers: GET /front/api/v1t/groups/{group_id}/devices
        Params:
          group_id: Group ID
        """

        params = {"group_id": group_id}
        return self._api_access.http_get("groups/%(group_id)s/devices" % params).json()

    def add_device_to_group(self, group_id, device_id):
        """
        Add device to group
        covers: POST /front/api/v1t/groups/{group_id}/{device_id}
        Params:
          group_id: Group ID
          device_id: Device ID
        """

        params = {"group_id": group_id, "device_id": device_id}
        return self._api_access.http_post_data("groups/%(group_id)s/%(device_id)s" % params, {}).json()

    def remove_device_from_group(self, group_id, device_id):
        """
        Delete device from group
        covers: DELETE /front/api/v1t/groups/{group_id}/{device_id}
        Params:
          group_id: Group ID
          device_id: Device ID
        """

        params = {"group_id": group_id, "device_id": device_id}
        return self._api_access.http_delete("groups/%(group_id)s/%(device_id)s" % params).json()
