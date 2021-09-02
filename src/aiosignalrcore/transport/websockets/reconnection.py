import asyncio
import threading
import time
from enum import Enum


class ConnectionStateChecker(object):
    def __init__(
        self,
        ping_function,
        keep_alive_interval,
    ):
        self._keep_alive_interval = keep_alive_interval
        self._last_message = time.time()
        self._ping_function = ping_function

    async def run(self):
        while True:
            await asyncio.sleep(1)
            time_without_messages = time.time() - self._last_message
            if self._keep_alive_interval < time_without_messages:
                await self._ping_function()

    def reset(self):
        self._last_message = time.time()


class ReconnectionType(Enum):
    raw = 0  # Reconnection with max reconnections and constant sleep time
    interval = 1  # variable sleep time


class ReconnectionHandler(object):
    def __init__(self):
        self.reconnecting = False
        self.attempt_number = 0
        self.last_attempt = time.time()

    def next(self):
        raise NotImplementedError()

    def reset(self):
        self.attempt_number = 0
        self.reconnecting = False


class RawReconnectionHandler(ReconnectionHandler):
    def __init__(self, sleep_time, max_attempts):
        super(RawReconnectionHandler, self).__init__()
        self.sleep_time = sleep_time
        self.max_reconnection_attempts = max_attempts

    def next(self):
        self.reconnecting = True
        if self.max_reconnection_attempts is not None:
            if self.attempt_number <= self.max_reconnection_attempts:
                self.attempt_number += 1
                return self.sleep_time
            else:
                raise ValueError(
                    "Max attemps reached {0}".format(self.max_reconnection_attempts)
                )
        else:  # Infinite reconnect
            return self.sleep_time


class IntervalReconnectionHandler(ReconnectionHandler):
    def __init__(self, intervals):
        super(IntervalReconnectionHandler, self).__init__()
        self._intervals = intervals

    def next(self):
        self.reconnecting = True
        index = self.attempt_number
        self.attempt_number += 1
        if index >= len(self._intervals):
            raise ValueError("Max intervals reached {0}".format(self._intervals))
        return self._intervals[index]
