from time import time

from src.rate_limiter import RateLimiter


class SlidingWindowStore:
    def __init__(self, capacity: int, window_seconds: int):
        self.capacity = capacity
        self.window_seconds = window_seconds
        self._windows = {}

    def is_allowed(self, identifier: str):
        if identifier not in self._windows:
            window = SlidingWindow(self.capacity, self.window_seconds)
            self._windows[identifier] = window
        return self._windows[identifier].is_allowed()


class SlidingWindow(RateLimiter):
    def __init__(self, capacity: int, window_seconds: int) -> None:
        self.capacity = capacity
        self.window_seconds = window_seconds
        self.previous_requests: list[float] = []

    def is_allowed(self) -> bool:
        now = time()
        self.previous_requests = [
            t for t in self.previous_requests if now - t < self.window_seconds
        ]
        if len(self.previous_requests) < self.capacity:
            self.previous_requests.append(now)
            return True
        return False
