from requests import HTTPError


class Streaming(object):
    def __init__(self, api_access):
        self._api_access = api_access

    def get_all(self):
        """
        Getting all streams
        covers: GET /front/api/v1t/team/TEAM/streams
        """

        return self._api_access.http_get("streams").json()

    def get(self, stream_id):
        """
        Getting stream by id
        covers: GET /front/api/v1t/team/TEAM/streams/STREAMID
        """

        return self._api_access.http_get("streams/" + stream_id).json()

    def add_rtmp_stream(self, name, url, stream_key):
        """
        Creating new rtmp stream
        covers: POST /front/api/v1t/team/TEAM/streams
        """

        payload = {
            "Name": name,
            "RTMP": {
                "DestName": name,
                "URL": url,
                "StreamingKey": stream_key,
            }
        }

        return self._api_access.http_post_data("streams", payload).json()

    def delete_by_id(self, stream_id):
        """
        Delete stream by id
        covers: DELETE /front/api/v1t/team/TEAM/streams/STREAMID
        """
        return self._api_access.http_delete("streams/" + stream_id).json()

    def attach(self, stream_id, device_id):
        """
        Attach the stream destination to the device
        covers: POST /front/api/v1t/team/TEAM/streams/STREAMID/attach
        """
        return self._api_access.http_post_data("streams/%s/attach" % stream_id,
                                               {
                                                   "DeviceID": device_id
                                               }).json()

    def start(self, stream_id, device_id):
        """
        Start stream from device to stream destination
        covers: POST /front/api/v1t/team/TEAM/streams/STREAMID/start
        """
        return self._api_access.http_post_data("streams/%s/start" % stream_id,
                                               {
                                                   "DeviceID": device_id
                                               }).json()

    def stop(self, stream_id, device_id):
        """
        Stop streaming
        covers: POST /front/api/v1t/team/TEAM/streams/STREAMID/stop
        """

        self._api_access.http_post_data("streams/%s/stop" % stream_id,
                                        {
                                            "DeviceID": device_id
                                        })
