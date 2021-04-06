def capability(name):
    """
    Decorator for checking device capability

    Usage:
    @capability("presets")
    def do_something(self):
        pass
    """

    def inner_fn(fn):
        the_fn = fn

        def wrapper(self, *args, **kwargs):
            if not self.is_capability_supported(name):
                raise NotImplementedError(f'device {self._device_id} does not support {name}')
            return the_fn(self, *args, **kwargs)

        return wrapper

    return inner_fn


def resets_json(fn):
    """
    Decorator that resets cached device info json
    Usage:
    @resets_json
    def modify_device(self):
        pass
    """
    the_fn = fn

    def wrapper(self, *args, **kwargs):
        try:
            r = the_fn(self, *args, **kwargs)
        except:
            raise
        finally:
            self._json = None

        return r

    return wrapper


class Device(object):
    """
    Device class represents a device and provides methods for device api.
    """

    def __init__(self, device_id, api_access):
        self._api_access = api_access
        self._device_id = device_id
        self._json = None

    @property
    def id(self) -> str:
        return self._device_id

    @property
    def json(self) -> dict:
        if self._json is None:
            self.fetch()

        return self._json or {}

    def fetch(self):
        """
        Retrieves device info.
        """
        self._api_access.logger().info("Getting device %s", self._device_id)
        self._json = self._api_access.http_get("devices/" + self._device_id).json()

    @property
    def children(self):
        return [
            Device(ch["DeviceID"], self._api_access)
            for ch in self.json.get("Child", [])
        ]

    @resets_json
    def delete(self):
        self._api_access.logger().info("Deleting device %s", self._device_id)
        self._api_access.http_delete("devices/" + self._device_id)

    @resets_json
    def run_command(self, cmd, **kwargs):
        cmd_desc = dict(kwargs.items())
        cmd_desc["cmd"] = cmd
        self._api_access.logger().info("Running command \"%s\" on device %s", cmd, self._device_id)
        return self._api_access.http_post_data("devices/%s/task" % self._device_id, cmd_desc)

    @property
    def name(self):
        return self.json.get("Name")

    @name.setter
    @resets_json
    def name(self, name):
        self._api_access.logger().info("Renaming device %s to \"%s\"", self._device_id, name)
        self._api_access.http_post_data(
            f'devices/{self._device_id}/rename',
            {"Name": name})

    @resets_json
    def unpair(self):
        self._api_access.logger().info("Unpairing device %s", self._device_id)
        self._api_access.http_post(f'devices/{self._device_id}/unpair')

    def download_state_image(self, local_filename):
        return self._api_access.http_download_file(f'devices/{self._device_id}/state.jpg', local_filename)

    @resets_json
    def set_prop(self, prop_name, prop_value):
        """
        Convenience method for setting device settings via setprop
        """

        if isinstance(prop_value, bool):
            prop_value = "true" if prop_value else "false"

        self.run_command("setprop:{name}={value}".format( \
            name=prop_name,
            value=prop_value))

        self._json = None

    def get_prop(self, prop_name):
        """
        Convenience method for getting device settings
        """

        # api v2 returns settings as a dictionary.
        settings = self.telemetry.get("settings", {})
        value = self.walk_through_cfg_params(settings, prop_name)
        return value

    def walk_through_cfg_params(self, params, prop_name):
        for p in params:
            if "items" in p:
                return self.walk_through_cfg_params(p["items"], prop_name)
            elif p["id"] == prop_name:
                return p["value"]
        return None

    def is_capability_supported(self, cap_name) -> bool:
        """
        Returns true if capability supported by device, false otherwise
        """
        return cap_name in self.telemetry["info"]["caps"]

    @property
    def online(self) -> bool:
        self.fetch()
        return self.json.get("Status", None) == "Online"

    @property
    def telemetry(self) -> dict:
        if self._json is None:
            self.fetch()

        telemetry = self._json.get('Telemetry')
        if not telemetry:
            self._api_access.logger().warning("No telemetry available for device: %s" % self._device_id)

        return telemetry

    @property
    def state(self) -> dict:
        return self.telemetry.get('state', {})

    def state_by_name(self, name) -> dict:
        return self.telemetry.get('state', {}).get(name)

    @property
    def desired_state(self) -> dict:
        desired_state = self.telemetry.get('DesiredState', {})
        if desired_state == {}:
            self._api_access.logger().warning("No DesiredState available for device: %s" % self._device_id)

        return desired_state

    @capability("presets")
    @resets_json
    def get_local_presets(self) -> list:
        return self.telemetry.get('presets', {}).get('local', [])

    @capability("presets")
    def apply_cloud_preset(self, preset_id, sections):
        """
        Applies cloud preset to a device
        covers: PUT /front/api/v1t/devices/DEVICEID/presets/cloud
        Params:
          preset_id: id of the preset
        """
        r = self._api_access.http_put_data(
            f'devices/{self._device_id}/presets/cloud',
            {
                "id": preset_id,
                "name": preset_id,
                "sections": sections
            })
        return r.json()

    @capability("presets")
    @resets_json
    def apply_local_preset(self, preset_name, sections):
        """
        Applies device's preset
        covers: PUT /front/api/v1t/devices/DEVICEID/presets/local
        Params:
          preset_name: name of the preset
        """
        r = self._api_access.http_put_data(
            f'devices/{self._device_id}/presets/local',
            {
                "name": preset_name,
                "sections": sections
            })
        return r.json()

    @capability("presets")
    @resets_json
    def create_local_preset(self, preset_name, sections):
        """
        Creates preset on device with given sections
        Params:
          preset_name: name of preset to create
          sections: sections that need to be included in the preset
        """

        self.run_command(
            "preset.create",
            params={
                "name": preset_name,
                "sections": sections,
            })

        self._json = None

    @capability("presets")
    def push_local_preset(self, preset_name):
        """
        Pushes preset from device to cloud
        Params:
          preset_name: name of the preset to be pushed
        """

        self.run_command(
            "preset.push",
            params={
                "name": preset_name,
            })

        self._json = None

    @capability("presets")
    @resets_json
    def delete_local_preset(self, preset_name):
        """
        Pushes preset from device to cloud
        Params:
          preset_name: name of the preset to be pushed
        """

        self.run_command(
            "preset.delete",
            params={
                "name": preset_name,
            })

        self._json = None
