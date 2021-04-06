from requests import HTTPError


class Presets(object):
    def __init__(self, api_access):
        self._api_access = api_access

    def get_all(self):
        """
        Team's presets
        covers: GET /front/api/v1t/presets
        """

        return self._api_access.http_get("presets").json()

    def download(self, preset_id, filename):
        """
        Get a specific preset
        covers: GET /front/api/v1t/presets/PRESETID
        Params:
          preset_id: id of the preset
        """
        r = self._api_access.http_get(f'presets/{preset_id}')
        with open(filename, 'wb') as f:
            f.write(r.content)

    def upload(self, filename, name, description):
        """
        Uploads a preset
        covers: POST /front/api/v1t/presets
        Params:
          name: display name of the preset
          description: preset description
          filename: source filename
        """
        r = self._api_access.http_post_file(f'presets', filename, {
            "name": name,
            "description": description
        })
        return r.json()

    def rename(self, preset_id, name, description):
        """
        Modifies preset name and description
        covers: POST /front/api/v1t/presets
        Params:
          preset_id: id of the preset
          name: display name of the preset
          description: preset description
        """
        self._api_access.http_put_data(f'presets/{preset_id}', {
            "name": name,
            "description": description
        })

    def delete(self, preset_id):
        """
        Deletes a specific preset
        covers: DELETE /front/api/v1t/presets/PRESETID
        Params:
          preset_id: id of the preset
        """
        return self._api_access.http_delete(f'presets/{preset_id}').json()
