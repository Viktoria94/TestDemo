class HLS(object):
    def __init__(self, api_access):
        self._api_access = api_access

    def create_stream(self, scene, stream_id, begin_ts=None, end_ts=None, relative=False, out_of_scene=False):
        """
        covers: GET /front/api/v1t/media/scenes/{scene}/stream/{stream}
        """

        params = {
            "scene_id": scene.id,
            "stream_id": stream_id
        }

        self._api_access.http_get("media/scenes/%(scene_id)s/stream/%(stream_id)s" % params)

    def delete_stream(self, scene, stream_id):
        """
        covers: DELETE /front/api/v1t/media/scenes/{scene}/stream/{stream}
        """

        params = {
            "scene_id": scene.id,
            "stream_id": stream_id
        }

        self._api_access.http_delete("media/scenes/%(scene_id)s/stream/%(stream_id)s" % params)

    def stream_url_for_device(self, device_id):
        """
        Gets /hlsserver/s/live_{DEVICE ID} m3u8 playlist
        """
        return "%s/hlsserver/s/live_%s" % (self._api_access._address, device_id)
