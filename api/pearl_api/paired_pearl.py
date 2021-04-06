from . import Device as Pearl, Error as PearlApiError, Api as PearlApi
from requests_toolbelt.utils import dump
from requests.exceptions import HTTPError
import time

import logging
import requests
import mmh3

logger = logging.getLogger()

# Duplicated from utility module to remove dependency.
def sleep_with_log(duration, message=None):
    logger = logging.getLogger()
    if message is None:
        logger.info("Sleeping for {} sec".format(duration))
    else:
        logger.info("Sleeping for {} sec: {}".format(duration, message))

    time.sleep(duration)

class PairedPearl:
    def __init__(self, api, pearl, report):
        self._pearl = pearl
        self._api = api
        self._report = report
        self._pearl_device_id = pearl.avstudio.master_id
        self._device = None

    def __enter__(self):
        if not self._pearl.avstudio.enabled:
            self._pearl.avstudio.enabled = True
            sleep_with_log(5, "Enabling AVStudio on device")

        self._report.ASSERT_FALSE(self._pearl.avstudio.paired, "paired")
        self._report.ASSERT_NOT_NONE(self._pearl_device_id, "device id")
        self._report.ASSERT_NE(self._pearl_device_id, "", "device id")
        self._api.Devices.pair(self._pearl_device_id, "testpearl")

        sleep_with_log(5, "Sleeping after pairing")
        self._report.ASSERT_TRUE(self._pearl.avstudio.paired, "paired")
        self._report.ASSERT_TRUE(self._pearl.avstudio.online, "online status")
        self._device = self._api.Devices.get(self._pearl_device_id)
        self._report.ASSERT_TRUE(self._device.online, "device is online")
        self._report(len(self._device.children)) \
            .named("number of child devices") \
            .EXPECT_EQ(len(self._pearl.channels))

        return self._device

    def __exit__(self, type, value, traceback):
        self._device.delete()

        max_unpair_attempts = 20
        for i in range(max_unpair_attempts):
            if not self._pearl.avstudio.paired:
                break

            sleep_with_log(1, f'Waiting for unpairing {i+1}/{max_unpair_attempts}')

        self._report(i) \
            .named("time until pearl knows it's unpaired") \
            .EXPECT_LT(5)

        for _ in range(20):
            if self._pearl.avstudio.online:
                self._report.EXPECT_FALSE(self._pearl.avstudio.paired, "paired")
                return

            sleep_with_log(1, "Waiting for avstudio online status")

        self._report.FAIL("Unpaired pearl never became online")
