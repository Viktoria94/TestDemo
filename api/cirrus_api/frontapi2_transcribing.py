class Transcribing(object):
    def __init__(self, api_access):
        self._api_access = api_access

    def session_id(self):
        pass

    def start(self, device_id):
        """
        covers: front/api/v1t/team/{team_id}/devices/{device_id}/transcribe/start
        """
        r = self._api_access.http_post("devices/%s/transcribe/start" % device_id)
        return r.json()

    def set_short_url(self, device_id, short_url):
        """
        covers: front/api/v1t/team/{team_id}/devices/{device_id}/transcribe/id
        """
        data = {
            "id": short_url
        }
        r = self._api_access.http_post_data("devices/%s/transcribe/id" % device_id, data)
        return r.json()

    def get_billing_info(self, begin_ts, interval, end_ts):
        """
        begin_ts=1582934400
        interval=1d
        end_ts=1585440000
        covers: front/api/v1t/team/{team_id}/teams/{team_id}/billing?from={begin_ts}&interval={1d}&to={end_ts}
        """
        team_id = self._api_access.current_team
        r = self._api_access.http_get(
            "teams/%s/billing?from=%s&interval=%s&to=%s" % (team_id, begin_ts, interval, end_ts))
        return r.json()

    def get_billing_plan(self):
        """
        covers: front/api/v1t/team/{team_id}/teams/{team_id}/billing/plan
        """
        team_id = self._api_access.current_team
        r = self._api_access.http_get("teams/%s/billing/plan" % team_id)
        return r.json()

    def stop(self, device_id):
        """
        covers: front/api/v1t/team/{team_id}/devices/{device_id}/transcribe/stop
        """
        self._api_access.http_post("devices/%s/transcribe/stop" % device_id)

    def pause(self, device_id):
        """
        covers: front/api/v1t/team/{team_id}/devices/{device_id}/transcribe/pause
        """
        self._api_access.http_post("devices/%s/transcribe/stop" % device_id)

    def delete_session(self, device_id, session_id):
        """
        covers: front/api/v1t/team/{team_id}/transcribing/{device_id}/sessions/{session_id}
        """
        r = self._api_access.http_delete("transcribing/%s/sessions/%s" % (device_id, session_id))
        return r.json()

    def get_sessions(self, device_id):
        """
        front/api/v1t/team/{team_id}/transcribing/{device_id}/sessions
        """
        r = self._api_access.http_get("transcribing/%s/sessions" % device_id)
        return r.json()

    def download_srt(self, device_id, session_id):
        """
        front/api/v1t/team/{team_id}/transcribing/{device_id}/sessions/{session_id}/srt
        """
        return self._api_access.http_get("transcribing/%s/sessions/%s/srt" % (device_id, session_id))

    def download_txt(self, device_id, session_id):
        """
        front/api/v1t/team/{team_id}/transcribing/{device_id}/sessions/{session_id}/txt
        """
        return self._api_access.http_get("transcribing/%s/sessions/%s/txt" % (device_id, session_id))

    def get_results(self, device_id):
        """
        front/api/v1t/team/{team_id}/transcribing/{device_id}/result
        """
        r = self._api_access.http_get("transcribing/%s/result" % device_id)
        return r.json()

    def get_config(self, device_id):
        """
        covers: GET front/api/v1t/team/{team_id}/devices/{device_id}
        """
        r = self._api_access.http_get("devices/%s" % device_id)
        return r.json()

    def get_transcribe_config(self, device_id):
        """
        covers: GET {FRONTAPI_URL}/front/api/v1t/team/{team_id}/devices/{device_id}/transcribe/configuration
        """
        r = self._api_access.http_get(f"devices/{device_id}/transcribe/configuration")
        return r.json()

    def set_transcribe_config(self, device_id, data):
        """
        covers: PUT {FRONTAPI_URL}/front/api/v1t/team/{team_id}/devices/{device_id}/transcribe/configuration
        """
        r = self._api_access.http_put_data(f"devices/{device_id}/transcribe/configuration", data)
        return r.json()
